"""Shared privacy helpers: strip the home vicinity from GPX tracks.

Your home location lives in scripts/home.json (gitignored). Any track point
within radius_m of home is removed from the START and END of a track, so the
published route never reveals where you live.
"""
import json
import math
from pathlib import Path
from xml.etree import ElementTree as ET

HERE = Path(__file__).resolve().parent


def load_home():
    p = HERE / "home.json"
    if not p.exists():
        return None
    d = json.loads(p.read_text())
    if not d.get("lat") or not d.get("lon"):
        return None
    d.setdefault("radius_m", 500)
    return d


def haversine(a, b):
    R = 6371000.0
    la1, lo1, la2, lo2 = map(math.radians, [a[0], a[1], b[0], b[1]])
    dla, dlo = la2 - la1, lo2 - lo1
    h = math.sin(dla / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin(dlo / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def parse_gpx(path):
    root = ET.parse(path).getroot()
    coords = []
    for p in root.findall(".//{*}trkpt"):
        ele_el = p.find("{*}ele")
        ele = float(ele_el.text) if ele_el is not None and ele_el.text else None
        coords.append((float(p.get("lat")), float(p.get("lon")), ele))
    name_el = root.find(".//{*}trk/{*}name")
    name = name_el.text.strip() if name_el is not None and name_el.text else "Route"
    return coords, name


def trim_coords(coords, home):
    if not home or not coords:
        return coords
    hp = (home["lat"], home["lon"])
    r = home["radius_m"]
    n = len(coords)
    s = 0
    while s < n and haversine(coords[s], hp) <= r:
        s += 1
    e = n - 1
    while e >= 0 and haversine(coords[e], hp) <= r:
        e -= 1
    return coords[s:e + 1] if s <= e else []


def write_gpx(path, coords, name="Route"):
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gpx version="1.1" creator="charalambous.uk" xmlns="http://www.topografix.com/GPX/1/1">',
        f"<trk><name>{name}</name><trkseg>",
    ]
    for (lat, lon, ele) in coords:
        if ele is None:
            lines.append(f'<trkpt lat="{lat:.6f}" lon="{lon:.6f}"></trkpt>')
        else:
            lines.append(f'<trkpt lat="{lat:.6f}" lon="{lon:.6f}"><ele>{ele:.1f}</ele></trkpt>')
    lines += ["</trkseg></trk>", "</gpx>"]
    Path(path).write_text("\n".join(lines))
