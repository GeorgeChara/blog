#!/usr/bin/env python3
"""Build the cycling routes list from GPX files. Manually triggered.

Workflow:
  1. Plan/pick a route (Komoot, RideWithGPS, cycle.travel...) and export GPX.
  2. Drop the .gpx into static/cycling/routes/
  3. Run:  python scripts/routes/build_routes.py

For each GPX it computes distance / climbing / difficulty and writes a Hugo
page. Brand-new routes are tagged  new: true  until the next pipeline run,
which clears them. Your manual tags (scenic, coffee, bakery, cake, ...) and
source links are preserved across runs.
"""
import glob
import math
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from privacy import load_home, trim_coords, write_gpx

ROOT = Path(__file__).resolve().parents[2]
GPX_DIR = ROOT / "static" / "cycling" / "routes"
CONTENT_DIR = ROOT / "content" / "fitness" / "cycling" / "routes"


def haversine(a, b):
    R = 6371000.0
    lat1, lon1, lat2, lon2 = map(math.radians, [a[0], a[1], b[0], b[1]])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def parse_gpx(path):
    root = ET.parse(path).getroot()
    coords = []
    for p in root.findall(".//{*}trkpt") or root.findall(".//{*}rtept"):
        ele_el = p.find("{*}ele")
        ele = float(ele_el.text) if ele_el is not None and ele_el.text else None
        coords.append((float(p.get("lat")), float(p.get("lon")), ele))
    name_el = root.find(".//{*}trk/{*}name")
    if name_el is None:
        name_el = root.find(".//{*}rte/{*}name")
    if name_el is None:
        name_el = root.find(".//{*}metadata/{*}name")
    name = name_el.text.strip() if name_el is not None and name_el.text else None
    return coords, name


def compute(coords):
    dist = sum(haversine(coords[i - 1], coords[i]) for i in range(1, len(coords)))
    climb, last = 0.0, None
    for (_, _, ele) in coords:
        if ele is None:
            continue
        if last is not None and ele - last > 1.0:  # 1m threshold to cut GPS noise
            climb += ele - last
        last = ele
    return dist / 1000.0, climb


def difficulty(dist_km, climb_m):
    score = dist_km + climb_m / 30.0  # 30 m climbed ~ 1 km flat
    label = "Easy" if score < 35 else "Moderate" if score < 70 else "Hard" if score < 110 else "Severe"
    return label, round(score)


def read_existing(md_path):
    if not md_path.exists():
        return None
    m = re.search(r"^---\n(.*?)\n---", md_path.read_text(), re.S)
    fm = m.group(1) if m else ""

    def val(key):
        mm = re.search(rf"^{key}:\s*(.*)$", fm, re.M)
        return mm.group(1).strip() if mm else None

    return {
        "title": val("title"), "tags": val("tags") or "[]", "source": val("source") or '""',
        "distance_km": val("distance_km"), "climb_m": val("climb_m"),
        "difficulty": val("difficulty"), "difficulty_score": val("difficulty_score"),
    }


def main():
    home = load_home()
    if home:
        print(f"Privacy: trimming {home['radius_m']} m around home from route starts/ends.")
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    gpx_files = sorted(glob.glob(str(GPX_DIR / "*.gpx")))
    if not gpx_files:
        print(f"No GPX files in {GPX_DIR.relative_to(ROOT)}. Drop route GPX there and re-run.")
        return

    known = {p.stem for p in CONTENT_DIR.glob("*.md") if p.stem != "_index"}
    seen, new_count = set(), 0

    for gpx in gpx_files:
        slug = Path(gpx).stem
        seen.add(slug)
        coords, gpx_name = parse_gpx(gpx)
        if len(coords) < 2:
            print(f"  skip {slug}: no track points")
            continue
        md_path = CONTENT_DIR / f"{slug}.md"
        existing = read_existing(md_path)
        is_new = slug not in known
        new_count += is_new

        if existing and existing["distance_km"]:
            # preserve stats from first ingest (GPX may have been privacy-trimmed since)
            dist_str, climb_str = existing["distance_km"], existing["climb_m"]
            diff = (existing["difficulty"] or "Moderate").strip().strip('"')
            score = existing["difficulty_score"] or "0"
        else:
            dist_km, climb_m = compute(coords)
            diff, score = difficulty(dist_km, climb_m)
            dist_str, climb_str, score = f"{dist_km:.1f}", str(round(climb_m)), str(score)

        if existing:
            title = (existing["title"] or gpx_name or slug.replace("-", " ").title()).strip().strip('"')
            tags, source = existing["tags"], existing["source"]
        else:
            title = (gpx_name or slug.replace("-", " ").title()).strip().strip('"')
            tags, source = "[]", '""'

        # privacy: strip the home vicinity from the served GPX (if home configured)
        if home:
            kept = trim_coords(coords, home, seed=slug)
            if kept and len(kept) < len(coords):
                write_gpx(Path(gpx), kept, title)

        md_path.write_text("\n".join([
            "---",
            f'title: "{title}"',
            "type: cycling",
            "layout: route",
            f"gpx: /cycling/routes/{slug}.gpx",
            f"distance_km: {dist_str}",
            f"climb_m: {climb_str}",
            f'difficulty: "{diff}"',
            f"difficulty_score: {score}",
            f"tags: {tags}",
            f"source: {source}",
            f"new: {'true' if is_new else 'false'}",
            "---",
            "",
        ]))
        print(f"  {slug}: {dist_str} km, {climb_str} m, {diff}{' [NEW]' if is_new else ''}")

    idx = CONTENT_DIR / "_index.md"
    if not idx.exists():
        idx.write_text('---\ntitle: "Routes"\ntype: cycling\nlayout: routes\n---\n')

    for orphan in known - seen:
        print(f"  note: {orphan}.md has no matching GPX (left in place)")
    print(f"Done. {len(seen)} routes, {new_count} new.")


if __name__ == "__main__":
    main()
