"""Generate a per-ride Open Graph preview card (1200x630 PNG).

Rich link unfurls: when a ride URL is shared, apps show this card. It mirrors
the ride widget — real map tiles + the route (loop closed), the zone-coloured
power graph along the bottom, and a stats panel. staticmap fetches/stitches the
tiles and projects the route; Pillow draws the overlays.
"""
import math

from PIL import Image, ImageDraw, ImageFont, ImageFilter
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


def _draw_panel(base, name, dist_km, climb_m, duration, calories):
    """Frosted-glass stats panel: name + DIST/CLMB/TIME/KCAL rows, with the map
    blurred and lightened behind it so the blue route still shows through."""
    d0 = ImageDraw.Draw(base)
    f_name = _font(True, 40)
    f_lab = _font(False, 25)
    f_val = _font(True, 31)

    rows = []
    if dist_km is not None:
        rows.append(("DIST", f"{dist_km} km"))
    if climb_m is not None:
        rows.append(("CLMB", f"{climb_m} m"))
    if duration:
        rows.append(("TIME", str(duration)))
    if calories:
        rows.append(("KCAL", str(int(round(float(calories))))))

    pad, row_h, name_h, col_gap = 26, 42, 56, 22
    label_w = int(max((d0.textlength(l, font=f_lab) for l, _ in rows), default=0))
    val_w = int(max((d0.textlength(v, font=f_val) for _, v in rows), default=0))
    content_w = max(int(d0.textlength(name, font=f_name)), label_w + col_gap + val_w)
    x0, y0 = 22, 22
    x1 = x0 + content_w + pad * 2
    y1 = y0 + pad + name_h + len(rows) * row_h + pad - row_h + 30

    # frosted glass: blur + lighten the map region under the panel
    crop = base.crop((x0, y0, x1, y1)).filter(ImageFilter.GaussianBlur(7)).convert("RGBA")
    crop = Image.blend(crop, Image.new("RGBA", crop.size, (255, 255, 255, 255)), 0.55)
    mask = Image.new("L", crop.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, crop.size[0] - 1, crop.size[1] - 1], radius=12, fill=255)
    base.paste(crop, (x0, y0), mask)

    d = ImageDraw.Draw(base)
    d.rounded_rectangle([x0, y0, x1, y1], radius=12, outline=(205, 198, 182, 255), width=1)
    tx = x0 + pad
    d.text((tx, y0 + pad - 4), name, font=f_name, fill=(18, 18, 18, 255))
    ty = y0 + pad + name_h
    for lab, val in rows:
        cy = ty + row_h / 2
        d.text((tx, cy), lab, font=f_lab, fill=(140, 135, 124, 255), anchor="lm")
        d.text((tx + label_w + col_gap, cy), val, font=f_val, fill=(18, 18, 18, 255), anchor="lm")
        ty += row_h
    d.text((W - 18, H - 16), "charalambous.uk/cycling", font=_font(False, 16), fill=(120, 113, 98, 255), anchor="rs")
    return base


def make_og_card(out_path, name, dist_km, climb_m, duration, calories, coords, power):
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
    img = _draw_panel(img, name, dist_km, climb_m, duration, calories)
    img.convert("RGB").save(out_path)
