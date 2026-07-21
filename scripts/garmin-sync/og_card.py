"""Generate a per-ride Open Graph preview card (1200x630 PNG).

Rich link unfurls: when a ride URL is shared, apps show this card. It mirrors
the ride widget — real map tiles + the route (loop closed), the zone-coloured
power graph along the bottom, and a stats panel. staticmap fetches/stitches the
tiles and projects the route; Pillow draws the overlays.
"""
import math

from PIL import Image, ImageDraw, ImageFont
from staticmap import StaticMap, Line

import matplotlib.font_manager as fm

W, H = 1200, 630
FTP = 220
# Voyager (not light_all): its roads are clearly visible, so the route reads as
# following real roads rather than floating over the near-white light basemap.
TILE_URL = "https://a.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png"
BLUE = "#2b7fd9"
# zone fill (Zwift-style, translucent) and the power line
ZBOUNDS = [0.55, 0.75, 0.90, 1.05]
ZFILL = [(148, 163, 184), (96, 165, 250), (52, 211, 153), (251, 191, 36), (248, 113, 113)]
ZALPHA = 92
POWER_LINE = (192, 57, 43, 235)


def _font(bold=False, size=24):
    path = fm.findfont(fm.FontProperties(family="DejaVu Sans Mono", weight="bold" if bold else "normal"))
    return ImageFont.truetype(path, size)


def _smooth(a, w=5):
    half = w // 2
    out = []
    for i in range(len(a)):
        s, c = 0, 0
        for j in range(i - half, i + half + 1):
            if 0 <= j < len(a) and a[j] is not None:
                s += a[j]
                c += 1
        out.append(s / c if c else None)
    return out


def _zidx(w):
    f = w / FTP
    for i, b in enumerate(ZBOUNDS):
        if f < b:
            return i
    return 4


def _draw_power(base, power):
    """Zone-coloured power graph footer (translucent, so the map reads through)."""
    if not power or len([p for p in power if p is not None]) < 4:
        return base
    power = _smooth(power, 7)  # trend, not spikes (matches the ride page)
    vals = [p for p in power if p is not None]
    n = len(power)
    x0, x1 = 14, W - 14
    y_bot = H - 14
    y_top = H * 0.60  # peak reaches up to here
    pmax = max(vals)
    ymax = max(50, math.ceil((pmax or 150) / 50) * 50)

    def px(i):
        return x0 + (i / (n - 1)) * (x1 - x0)

    def py(v):
        return y_bot - min((v or 0) / ymax, 1.0) * (y_bot - y_top)

    ov = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for i in range(1, n):
        a, b = power[i - 1], power[i]
        if a is None or b is None:
            continue
        r, g, bl = ZFILL[_zidx(b)]
        d.polygon([(px(i - 1), y_bot), (px(i - 1), py(a)), (px(i), py(b)), (px(i), y_bot)],
                  fill=(r, g, bl, ZALPHA))
    line = [(px(i), py(power[i])) for i in range(n) if power[i] is not None]
    if len(line) > 1:
        d.line(line, fill=POWER_LINE, width=3, joint="curve")
    return Image.alpha_composite(base, ov)


def _draw_panel(base, ride_type, name, dist_km, climb_m, duration):
    d = ImageDraw.Draw(base)
    f_type, f_name, f_stat = _font(True, 22), _font(True, 34), _font(False, 24)
    stats = "   ".join([s for s in [
        (f"{dist_km} km" if dist_km is not None else None),
        (f"{climb_m} m up" if climb_m is not None else None),
        (str(duration) if duration else None),
    ] if s])
    pad = 22
    widths = [d.textlength(name, font=f_name), d.textlength(ride_type.upper(), font=f_type), d.textlength(stats, font=f_stat)]
    pw = int(max(widths)) + pad * 2
    ph = 150
    d.rounded_rectangle([16, 16, 16 + pw, 16 + ph], radius=8, fill=(255, 255, 255, 224), outline=(229, 222, 207, 255), width=1)
    d.text((16 + pad, 30), ride_type.upper(), font=f_type, fill=(65, 105, 225, 255))
    d.text((16 + pad, 62), name, font=f_name, fill=(20, 20, 20, 255))
    d.text((16 + pad, 114), stats, font=f_stat, fill=(90, 90, 90, 255))
    d.text((W - 18, H - 16), "charalambous.uk/cycling", font=_font(False, 16), fill=(120, 113, 98, 255), anchor="rs")
    return base


def make_og_card(out_path, ride_type, name, dist_km, climb_m, duration, coords, power):
    """coords: (lat, lon) points.  power: power_profile list (may hold None)."""
    m = StaticMap(W, H, url_template=TILE_URL, padding_x=70, padding_y=80)
    if coords and len(coords) > 1:
        lonlat = [(c[1], c[0]) for c in coords]
        # close the loop when the ride starts and finishes near the same place
        if abs(lonlat[0][0] - lonlat[-1][0]) < 0.05 and abs(lonlat[0][1] - lonlat[-1][1]) < 0.05:
            lonlat = lonlat + [lonlat[0]]
        m.add_line(Line(lonlat, "#ffffff", 8))   # white halo so the route reads on any tile
        m.add_line(Line(lonlat, BLUE, 5))
    img = m.render().convert("RGBA")
    img = _draw_power(img, power)
    img = _draw_panel(img, ride_type, name, dist_km, climb_m, duration)
    img.convert("RGB").save(out_path)
