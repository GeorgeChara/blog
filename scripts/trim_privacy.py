#!/usr/bin/env python3
"""Strip your home vicinity from every published GPX (rides + routes).

Setup once:
  cp scripts/home.json.example scripts/home.json
  # edit scripts/home.json with your home lat/lon and a radius (metres)

Then run any time:
  python scripts/trim_privacy.py

It rewrites every GPX under static/cycling/gpx/ and static/cycling/routes/ with
the start and end near home removed. Safe to re-run (already-trimmed files are
left unchanged). scripts/home.json is gitignored, so your address is never
committed or published.
"""
from pathlib import Path

from privacy import load_home, parse_gpx, trim_coords, write_gpx

ROOT = Path(__file__).resolve().parent.parent
DIRS = [ROOT / "static" / "cycling" / "gpx", ROOT / "static" / "cycling" / "routes"]


def main():
    home = load_home()
    if not home:
        print("No scripts/home.json (or lat/lon blank). Copy scripts/home.json.example,")
        print("fill in your home lat/lon + radius_m, then re-run.")
        return
    print(f"Home privacy zone loaded (radius {home['radius_m']} m). Coordinate not shown.")
    total = trimmed = 0
    for d in DIRS:
        for gpx in sorted(d.glob("*.gpx")):
            total += 1
            coords, name = parse_gpx(gpx)
            kept = trim_coords(coords, home)
            if len(kept) == len(coords):
                continue  # nothing near home / already trimmed
            if not kept:
                print(f"  WARNING {gpx.name}: whole track within radius, skipped")
                continue
            write_gpx(gpx, kept, name)
            trimmed += 1
            print(f"  {gpx.name}: {len(coords)} -> {len(kept)} points")
    print(f"Done. {trimmed} of {total} GPX trimmed.")


if __name__ == "__main__":
    main()
