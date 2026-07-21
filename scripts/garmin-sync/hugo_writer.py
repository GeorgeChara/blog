"""Generate Hugo content files from Garmin activity data."""

import json
import math
import os
import random
import re
from datetime import datetime
from pathlib import Path

import gpxpy

try:
    from og_card import make_og_card
except Exception:  # matplotlib missing -> skip OG cards, don't break the sync
    make_og_card = None

# Repo root is two levels up from this script
REPO_ROOT = Path(__file__).resolve().parent.parent.parent

CONTENT_DIR = REPO_ROOT / "content" / "cycling" / "rides"
DATA_DIR = REPO_ROOT / "data" / "cycling"
ACTIVITIES_DIR = DATA_DIR / "activities"
GPX_DIR = REPO_ROOT / "static" / "cycling" / "gpx"
OG_DIR = REPO_ROOT / "static" / "cycling" / "og"


def _load_home():
    """Home privacy zone: from HOME_JSON env (CI secret) or scripts/home.json (local)."""
    raw = os.environ.get("HOME_JSON")
    try:
        d = json.loads(raw) if raw else json.loads((REPO_ROOT / "scripts" / "home.json").read_text())
    except Exception:
        return None
    if not d.get("lat") or not d.get("lon"):
        return None
    d.setdefault("radius_m", 2500)
    return d


def _haversine(la1, lo1, la2, lo2):
    R = 6371000.0
    a1, o1, a2, o2 = map(math.radians, [la1, lo1, la2, lo2])
    h = math.sin((a2 - a1) / 2) ** 2 + math.cos(a1) * math.cos(a2) * math.sin((o2 - o1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def trim_home(gpx_xml, seed=""):
    """Strip points near home from the start and end of each segment. Moderate base
    radius + seeded asymmetric jitter so the ends don't point straight at home."""
    home = _load_home()
    if not home:
        return gpx_xml
    hlat, hlon = home["lat"], home["lon"]
    jit = home.get("jitter_m", 0)
    if jit:
        rnd = random.Random(str(seed))
        r_start = home["radius_m"] + rnd.random() * jit
        r_end = home["radius_m"] + rnd.random() * jit
    else:
        r_start = r_end = home["radius_m"]
    gpx = gpxpy.parse(gpx_xml)
    for track in gpx.tracks:
        for seg in track.segments:
            pts = seg.points
            s = 0
            while s < len(pts) and _haversine(pts[s].latitude, pts[s].longitude, hlat, hlon) <= r_start:
                s += 1
            e = len(pts) - 1
            while e >= 0 and _haversine(pts[e].latitude, pts[e].longitude, hlat, hlon) <= r_end:
                e -= 1
            seg.points = pts[s:e + 1] if s <= e else []
    return gpx.to_xml()


def ensure_dirs():
    """Create output directories if they don't exist."""
    for d in [CONTENT_DIR, ACTIVITIES_DIR, GPX_DIR, OG_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def ride_type_label(normalized_power, avg_power):
    """Same buckets the ride page uses, so the share card matches the badge."""
    np = normalized_power or avg_power
    if not np:
        return "Ride"
    r = np / FTP
    if r < 0.65:
        return "Recovery ride"
    if r < 0.80:
        return "Endurance ride"
    if r < 0.90:
        return "Tempo ride"
    if r < 1.0:
        return "Threshold ride"
    return "Intervals"


def gpx_coords(gpx_xml):
    """(lat, lon) points from a GPX string, for drawing the route outline."""
    try:
        g = gpxpy.parse(gpx_xml)
        return [(p.latitude, p.longitude) for t in g.tracks for s in t.segments for p in s.points]
    except Exception:
        return []


def slugify(text):
    """Convert text to a URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text


def simplify_gpx(gpx_xml, max_points=500):
    """Simplify a GPX track to reduce file size.

    Uses the Ramer-Douglas-Peucker algorithm via gpxpy.
    """
    gpx = gpxpy.parse(gpx_xml)
    gpx.simplify(max_distance=10)  # metres tolerance

    # If still too many points, increase tolerance
    total_points = sum(
        len(seg.points)
        for track in gpx.tracks
        for seg in track.segments
    )
    if total_points > max_points:
        gpx_retry = gpxpy.parse(gpx_xml)
        gpx_retry.simplify(max_distance=25)
        return gpx_retry.to_xml()

    return gpx.to_xml()


def extract_profiles(gpx_xml):
    """Extract elevation, speed, HR profiles from GPX data.

    Returns:
        Dict with profile arrays and distance array
    """
    gpx = gpxpy.parse(gpx_xml)

    elevation = []
    distance = []
    hr = []
    cumulative_dist = 0.0

    for track in gpx.tracks:
        for segment in track.segments:
            prev_point = None
            for point in segment.points:
                if prev_point:
                    d = point.distance_2d(prev_point)
                    if d is not None:
                        cumulative_dist += d / 1000  # km

                distance.append(round(cumulative_dist, 2))

                if point.elevation is not None:
                    elevation.append(round(point.elevation, 1))

                # Extract HR from extensions if available
                if point.extensions:
                    for ext in point.extensions:
                        hr_elem = ext.find(
                            "{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}hr"
                        )
                        if hr_elem is not None and hr_elem.text:
                            hr.append(int(hr_elem.text))

                prev_point = point

    return {
        "elevation_profile": elevation,
        "distance_profile": distance,
        "hr_profile": hr if hr else None,
    }


def format_duration(seconds):
    """Format seconds into a human-readable duration string."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    if hours > 0:
        return f"{hours}h {minutes:02d}m"
    return f"{minutes}m"


def write_activity(activity, gpx_xml, streams=None):
    """Write all Hugo files for a single activity.

    Args:
        activity: Garmin activity dict from the API
        gpx_xml: Raw GPX XML string
        streams: optional per-second streams dict (power, speed, hr, ...)

    Returns:
        Activity ID string
    """
    ensure_dirs()

    activity_id = str(activity["activityId"])
    name = activity.get("activityName") or "Ride"
    date_str = activity.get("startTimeLocal", "")
    dt = datetime.fromisoformat(date_str) if date_str else datetime.now()

    distance_km = round(activity.get("distance", 0) / 1000, 1)
    elevation_m = round(activity.get("elevationGain", 0))
    duration_sec = activity.get("duration", 0)
    moving_sec = activity.get("movingDuration", duration_sec)
    avg_speed = round(activity.get("averageSpeed", 0) * 3.6, 1)  # m/s to km/h
    max_speed = round(activity.get("maxSpeed", 0) * 3.6, 1)
    avg_hr = activity.get("averageHR")
    max_hr = activity.get("maxHR")
    avg_power = activity.get("avgPower")
    max_power = activity.get("maxPower")
    normalized_power = activity.get("normPower")
    avg_cadence = activity.get("averageBikingCadenceInRevPerMinute")
    calories = activity.get("calories")

    slug = f"{dt.strftime('%Y-%m-%d')}-{slugify(name)}"

    # 1. Home-trim the GPX and get the kept ride-distance window
    trimmed_gpx, start_m, end_m = trim_range(gpx_xml, str(activity_id))
    simplified_gpx = simplify_gpx(trimmed_gpx)
    gpx_path = GPX_DIR / f"{activity_id}.gpx"
    gpx_path.write_text(simplified_gpx)

    # 2. Build profiles from the SAME trimmed window so the chart aligns with the map
    if streams and streams.get("distance"):
        power_zones = compute_power_zones(streams.get("power", []), moving_sec)  # whole ride, before trimming
        streams = trim_streams(streams, start_m, end_m)
        profiles = build_profiles(streams)
        profiles["power_zones"] = power_zones
    else:
        profiles = extract_profiles(trimmed_gpx)
    activity_json = {
        "id": activity_id,
        "name": name,
        "date": dt.isoformat(),
        "type": activity.get("activityType", {}).get("typeKey", "cycling"),
        "distance_km": distance_km,
        "elevation_gain_m": elevation_m,
        "duration_seconds": round(duration_sec),
        "moving_time_seconds": round(moving_sec),
        "avg_speed_kmh": avg_speed,
        "max_speed_kmh": max_speed,
        "avg_hr": avg_hr,
        "max_hr": max_hr,
        "avg_power": avg_power,
        "max_power": max_power,
        "normalized_power": normalized_power,
        "avg_cadence": avg_cadence,
        "calories": calories,
    }
    activity_json.update(profiles)

    json_path = ACTIVITIES_DIR / f"{activity_id}.json"
    json_path.write_text(json.dumps(activity_json, indent=2))

    # 3. Write Hugo markdown
    duration_fmt = format_duration(duration_sec)
    frontmatter_lines = [
        "---",
        f'title: "{name}"',
        f"date: {dt.isoformat()}",
        "type: cycling",
        f'garmin_id: "{activity_id}"',
        f"distance_km: {distance_km}",
        f"elevation_m: {elevation_m}",
        f'duration: "{duration_fmt}"',
        f"avg_speed_kmh: {avg_speed}",
    ]
    if avg_hr:
        frontmatter_lines.append(f"avg_hr: {avg_hr}")
    if max_hr:
        frontmatter_lines.append(f"max_hr: {max_hr}")
    if avg_power:
        frontmatter_lines.append(f"avg_power: {avg_power}")
    if normalized_power:
        frontmatter_lines.append(f"normalized_power: {normalized_power}")
    if avg_cadence:
        frontmatter_lines.append(f"avg_cadence: {avg_cadence}")
    if calories:
        frontmatter_lines.append(f"calories: {calories}")
    frontmatter_lines += [
        f'gpx_file: "/cycling/gpx/{activity_id}.gpx"',
        "toc: false",
        "showreadingtime: false",
        "---",
    ]

    md_path = CONTENT_DIR / f"{slug}.md"
    md_path.write_text("\n".join(frontmatter_lines) + "\n")

    # 4. Open Graph preview card for rich link unfurls
    if make_og_card:
        try:
            make_og_card(
                str(OG_DIR / f"{activity_id}.png"),
                ride_type_label(normalized_power, avg_power),
                name, distance_km, elevation_m, duration_fmt,
                gpx_coords(simplified_gpx), profiles.get("power_profile") or [],
            )
        except Exception as e:
            print(f"  OG card failed for {activity_id}: {e}")

    return {
        "id": activity_id,
        "name": name,
        "date": dt.strftime("%Y-%m-%d"),
        "distance_km": distance_km,
        "elevation_gain_m": elevation_m,
        "duration": duration_fmt,
        "avg_speed_kmh": avg_speed,
        "slug": slug,
    }


def update_summary(all_ride_summaries):
    """Update the aggregate summary and recent rides JSON files."""
    ensure_dirs()

    # Sort by date descending
    sorted_rides = sorted(all_ride_summaries, key=lambda r: r["date"], reverse=True)

    # Recent rides (last 10)
    recent_path = DATA_DIR / "recent.json"
    recent_path.write_text(json.dumps(sorted_rides[:10], indent=2))

    # Aggregate summary
    total_distance = sum(r["distance_km"] for r in sorted_rides)
    total_elevation = sum(r["elevation_gain_m"] for r in sorted_rides)
    total_rides = len(sorted_rides)

    # Monthly breakdown for current year
    current_year = datetime.now().year
    monthly = {f"{m:02d}": 0.0 for m in range(1, 13)}
    for ride in sorted_rides:
        try:
            ride_dt = datetime.fromisoformat(ride["date"])
            if ride_dt.year == current_year:
                month_key = f"{ride_dt.month:02d}"
                monthly[month_key] += ride["distance_km"]
        except (ValueError, KeyError):
            pass

    # Round monthly values
    monthly = {k: round(v, 1) for k, v in monthly.items()}

    avg_speed_values = [r["avg_speed_kmh"] for r in sorted_rides if r["avg_speed_kmh"] > 0]

    summary = {
        "total_rides": total_rides,
        "total_distance_km": round(total_distance, 1),
        "total_elevation_m": round(total_elevation),
        "avg_speed_kmh": round(sum(avg_speed_values) / len(avg_speed_values), 1) if avg_speed_values else 0,
        "longest_ride_km": max((r["distance_km"] for r in sorted_rides), default=0),
        "year": current_year,
        "monthly_distance": monthly,
    }

    summary_path = DATA_DIR / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2))


# --- Strava-native writer -------------------------------------------------

def _downsample(arr, n=60):
    """Reduce a stream to ~n points for chart rendering."""
    if not arr:
        return []
    if len(arr) <= n:
        return [round(x, 1) if isinstance(x, (int, float)) else x for x in arr]
    step = len(arr) / n
    return [round(arr[int(i * step)], 1) for i in range(n)]


def streams_to_gpx(streams, name):
    """Build GPX XML from Strava latlng + altitude streams."""
    latlng = (streams.get("latlng") or {}).get("data")
    if not latlng:
        return None
    alt = (streams.get("altitude") or {}).get("data") or []
    gpx = gpxpy.gpx.GPX()
    trk = gpxpy.gpx.GPXTrack(name=name)
    gpx.tracks.append(trk)
    seg = gpxpy.gpx.GPXTrackSegment()
    trk.segments.append(seg)
    for i, pt in enumerate(latlng):
        elev = alt[i] if i < len(alt) else None
        seg.points.append(gpxpy.gpx.GPXTrackPoint(pt[0], pt[1], elevation=elev))
    return gpx.to_xml()


def streams_to_profiles(streams):
    """Downsample Strava streams into chart profile arrays."""
    def data(key):
        return (streams.get(key) or {}).get("data") or []

    dist_km = [round(x / 1000, 2) for x in data("distance")]
    speed_kmh = [round(x * 3.6, 1) for x in data("velocity_smooth")]
    return {
        "distance_profile": _downsample(dist_km),
        "elevation_profile": _downsample(data("altitude")),
        "hr_profile": _downsample(data("heartrate")) or None,
        "power_profile": _downsample(data("watts")) or None,
        "speed_profile": _downsample(speed_kmh) or None,
    }


def write_strava_activity(detail, streams):
    """Write all Hugo files for a single Strava activity."""
    ensure_dirs()
    activity_id = str(detail["id"])
    name = detail.get("name") or "Ride"
    title = name.replace('"', "'")
    date_str = detail.get("start_date_local") or detail.get("start_date")
    dt = (datetime.fromisoformat(date_str.replace("Z", "+00:00"))
          if date_str else datetime.now())

    def r0(key):
        v = detail.get(key)
        return round(v) if v is not None else None

    distance_km = round(detail.get("distance", 0) / 1000, 1)
    elevation_m = round(detail.get("total_elevation_gain", 0))
    duration_sec = detail.get("elapsed_time", 0)
    moving_sec = detail.get("moving_time", duration_sec)
    avg_speed = round(detail.get("average_speed", 0) * 3.6, 1)
    max_speed = round(detail.get("max_speed", 0) * 3.6, 1)
    avg_hr = r0("average_heartrate")
    max_hr = r0("max_heartrate")
    avg_power = r0("average_watts")
    max_power = r0("max_watts")
    normalized_power = detail.get("weighted_average_watts")
    avg_cadence = r0("average_cadence")
    calories = r0("calories")

    slug = f"{dt.strftime('%Y-%m-%d')}-{slugify(name)}"

    gpx_xml = streams_to_gpx(streams, name)
    if gpx_xml:
        (GPX_DIR / f"{activity_id}.gpx").write_text(simplify_gpx(gpx_xml))

    activity_json = {
        "id": activity_id,
        "name": name,
        "date": dt.isoformat(),
        "type": detail.get("type", "Ride"),
        "distance_km": distance_km,
        "elevation_gain_m": elevation_m,
        "duration_seconds": round(duration_sec),
        "moving_time_seconds": round(moving_sec),
        "avg_speed_kmh": avg_speed,
        "max_speed_kmh": max_speed,
        "avg_hr": avg_hr,
        "max_hr": max_hr,
        "avg_power": avg_power,
        "max_power": max_power,
        "normalized_power": normalized_power,
        "avg_cadence": avg_cadence,
        "calories": calories,
    }
    activity_json.update(streams_to_profiles(streams))
    (ACTIVITIES_DIR / f"{activity_id}.json").write_text(json.dumps(activity_json, indent=2))

    duration_fmt = format_duration(duration_sec)
    fm = [
        "---",
        f'title: "{title}"',
        f"date: {dt.isoformat()}",
        "type: cycling",
        f'garmin_id: "{activity_id}"',
        f"distance_km: {distance_km}",
        f"elevation_m: {elevation_m}",
        f'duration: "{duration_fmt}"',
        f"avg_speed_kmh: {avg_speed}",
    ]
    if avg_hr:
        fm.append(f"avg_hr: {avg_hr}")
    if max_hr:
        fm.append(f"max_hr: {max_hr}")
    if avg_power:
        fm.append(f"avg_power: {avg_power}")
    if normalized_power:
        fm.append(f"normalized_power: {normalized_power}")
    if avg_cadence:
        fm.append(f"avg_cadence: {avg_cadence}")
    if calories:
        fm.append(f"calories: {calories}")
    fm += [
        f'gpx_file: "/cycling/gpx/{activity_id}.gpx"',
        "toc: false",
        "showreadingtime: false",
        "---",
    ]
    (CONTENT_DIR / f"{slug}.md").write_text("\n".join(fm) + "\n")

    return {
        "id": activity_id,
        "name": name,
        "date": dt.strftime("%Y-%m-%d"),
        "distance_km": distance_km,
        "elevation_gain_m": elevation_m,
        "duration": duration_fmt,
        "avg_speed_kmh": avg_speed,
        "slug": slug,
    }


# --- Rich stream profiles + power zones -----------------------------------

FTP = 220  # Functional Threshold Power. Change this and re-sync to fix zones.


def _downsample_stream(arr, n=80):
    if not arr:
        return []
    if len(arr) <= n:
        return [round(x, 1) if isinstance(x, (int, float)) else None for x in arr]
    step = len(arr) / n
    out = []
    for i in range(n):
        x = arr[int(i * step)]
        out.append(round(x, 1) if isinstance(x, (int, float)) else None)
    return out


def trim_range(gpx_xml, seed=""):
    """Trim near-home points from start/end; return (trimmed_xml, start_m, end_m)
    where start_m/end_m are the ride-distance bounds of the kept portion. Used to
    trim the profile streams to the SAME extent so the chart aligns with the map."""
    home = _load_home()
    if not home:
        return gpx_xml, None, None
    hlat, hlon = home["lat"], home["lon"]
    jit = home.get("jitter_m", 0)
    if jit:
        rnd = random.Random(str(seed))
        r_start = home["radius_m"] + rnd.random() * jit
        r_end = home["radius_m"] + rnd.random() * jit
    else:
        r_start = r_end = home["radius_m"]
    gpx = gpxpy.parse(gpx_xml)
    start_m = end_m = None
    for track in gpx.tracks:
        for seg in track.segments:
            pts = seg.points
            if not pts:
                continue
            cum = [0.0]
            for i in range(1, len(pts)):
                cum.append(cum[-1] + (pts[i].distance_2d(pts[i - 1]) or 0.0))
            s = 0
            while s < len(pts) and _haversine(pts[s].latitude, pts[s].longitude, hlat, hlon) <= r_start:
                s += 1
            e = len(pts) - 1
            while e >= 0 and _haversine(pts[e].latitude, pts[e].longitude, hlat, hlon) <= r_end:
                e -= 1
            if s <= e:
                if start_m is None:
                    start_m, end_m = cum[s], cum[e]
                seg.points = pts[s:e + 1]
            else:
                seg.points = []
    return gpx.to_xml(), start_m, end_m


def trim_streams(streams, start_m, end_m):
    """Slice per-second streams to the [start_m, end_m] ride-distance window."""
    if start_m is None or not streams or not streams.get("distance"):
        return streams
    d = streams["distance"]
    keep = [i for i, x in enumerate(d) if x is not None and start_m <= x <= end_m]
    if not keep:
        return streams
    lo, hi = keep[0], keep[-1] + 1
    return {k: (v[lo:hi] if isinstance(v, list) else v) for k, v in streams.items()}


def build_profiles(streams):
    raw = streams.get("distance", [])
    base = next((x for x in raw if x is not None), 0) or 0
    dist_km = [round(((x or 0) - base) / 1000, 2) for x in raw]
    speed_kmh = [round((x or 0) * 3.6, 1) for x in streams.get("speed", [])]
    return {
        "distance_profile": _downsample_stream(dist_km),
        "elevation_profile": _downsample_stream(streams.get("elevation", [])),
        "power_profile": _downsample_stream(streams.get("power", [])) or None,
        "hr_profile": _downsample_stream(streams.get("hr", [])) or None,
        "speed_profile": _downsample_stream(speed_kmh) or None,
        "cadence_profile": _downsample_stream(streams.get("cadence", [])) or None,
    }


def compute_power_zones(power_stream, moving_seconds=None, ftp=FTP):
    """Seconds in each of 5 power zones.

    The stream is downsampled (~2000 pts max), so a sample is NOT one second.
    We tally samples per zone, then distribute the ride's real moving time
    across the zones by proportion, so the parts sum to the whole ride.
    """
    if not power_stream:
        return None
    bounds = [0.55, 0.75, 0.90, 1.05]  # fractions of FTP splitting Z1..Z5
    zones = [0, 0, 0, 0, 0]
    total = 0
    for p in power_stream:
        if p is None:
            continue
        total += 1
        frac = p / ftp
        if frac < bounds[0]:
            zones[0] += 1
        elif frac < bounds[1]:
            zones[1] += 1
        elif frac < bounds[2]:
            zones[2] += 1
        elif frac < bounds[3]:
            zones[3] += 1
        else:
            zones[4] += 1
    if not total:
        return None
    if moving_seconds:
        return [round(z / total * moving_seconds) for z in zones]
    return zones
