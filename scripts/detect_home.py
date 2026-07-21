#!/usr/bin/env python3
"""Detect your home from ride data and write scripts/home.json (gitignored).

Your loops start and end at home, so home is the densest cluster of ride
start/end points. This reads your ride GPX, finds that cluster, and writes the
coordinate to scripts/home.json. It never prints the coordinate.

Run once (before trimming), or re-run any time:
  python scripts/detect_home.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from privacy import parse_gpx, haversine

ROOT = Path(__file__).resolve().parent.parent
GPX_DIR = ROOT / "static" / "cycling" / "gpx"
OUT = Path(__file__).resolve().parent / "home.json"
CLUSTER_M = 400
RADIUS_M = 500


def main():
    pts = []
    for gpx in sorted(GPX_DIR.glob("*.gpx")):
        coords, _ = parse_gpx(gpx)
        if len(coords) >= 2:
            pts.append((coords[0][0], coords[0][1]))
            pts.append((coords[-1][0], coords[-1][1]))
    if not pts:
        print(f"No ride GPX in {GPX_DIR.relative_to(ROOT)}.")
        return

    best_i, best_n = 0, -1
    for i, p in enumerate(pts):
        n = sum(1 for q in pts if haversine(p, q) <= CLUSTER_M)
        if n > best_n:
            best_n, best_i = n, i
    center = pts[best_i]
    near = [q for q in pts if haversine(center, q) <= CLUSTER_M]
    lat = sum(x[0] for x in near) / len(near)
    lon = sum(x[1] for x in near) / len(near)

    OUT.write_text(json.dumps({"lat": round(lat, 6), "lon": round(lon, 6), "radius_m": RADIUS_M}, indent=2) + "\n")
    pct = len(near) * 100 // len(pts)
    print(f"Detected home cluster: {len(near)} of {len(pts)} ride start/end points ({pct}%).")
    print(f"Radius {RADIUS_M} m. Written to scripts/home.json (gitignored).")
    print("Coordinate intentionally not shown.")
    if pct < 40:
        print("NOTE: low cluster share - check the result on a map (trim one ride) before scrubbing.")


if __name__ == "__main__":
    main()
