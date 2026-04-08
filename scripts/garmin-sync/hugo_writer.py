"""Generate Hugo content files from Garmin activity data."""

import json
import re
from datetime import datetime
from pathlib import Path

import gpxpy

# Repo root is two levels up from this script
REPO_ROOT = Path(__file__).resolve().parent.parent.parent

CONTENT_DIR = REPO_ROOT / "content" / "cycling" / "rides"
DATA_DIR = REPO_ROOT / "data" / "cycling"
ACTIVITIES_DIR = DATA_DIR / "activities"
GPX_DIR = REPO_ROOT / "static" / "cycling" / "gpx"


def ensure_dirs():
    """Create output directories if they don't exist."""
    for d in [CONTENT_DIR, ACTIVITIES_DIR, GPX_DIR]:
        d.mkdir(parents=True, exist_ok=True)


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


def write_activity(activity, gpx_xml):
    """Write all Hugo files for a single activity.

    Args:
        activity: Garmin activity dict from the API
        gpx_xml: Raw GPX XML string

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
    avg_cadence = activity.get("averageBikingCadenceInRevPerMinute")
    calories = activity.get("calories")

    slug = f"{dt.strftime('%Y-%m-%d')}-{slugify(name)}"

    # 1. Write simplified GPX
    simplified_gpx = simplify_gpx(gpx_xml)
    gpx_path = GPX_DIR / f"{activity_id}.gpx"
    gpx_path.write_text(simplified_gpx)

    # 2. Extract profiles and write JSON
    profiles = extract_profiles(gpx_xml)
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
