"""Generate a per-ride Open Graph preview card (1200x630 PNG).

Used for rich link unfurls: when a ride URL is shared, apps show this card.
Left column = ride type / name / stats, right = the route outline, a faint
elevation strip runs along the bottom. Matplotlib (bundles DejaVu fonts, so it
renders the same on macOS and the Linux CI runner).
"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.font_manager as fm  # noqa: E402

BG = "#f7f5ef"
INK = "#141414"
BLUE = "#2b7fd9"
ACCENT = "#4169E1"
MUT = "#7a7468"
MONO = fm.FontProperties(family="DejaVu Sans Mono")
MONOB = fm.FontProperties(family="DejaVu Sans Mono", weight="bold")


def make_og_card(out_path, ride_type, name, dist_km, climb_m, duration, coords, elev):
    """coords: list of (lat, lon).  elev: list of elevation values (may hold None)."""
    W, H, DPI = 1200, 630, 100
    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI)
    fig.patch.set_facecolor(BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_facecolor(BG)

    # --- faint elevation strip along the bottom (the "graph" hint) ---
    ev = [e for e in (elev or []) if e is not None]
    if len(ev) > 3:
        n = len(elev)
        lo, hi = min(ev), max(ev)
        span = (hi - lo) or 1.0
        last = ev[0]
        xs, ys = [], []
        for i, e in enumerate(elev):
            if e is None:
                e = last
            last = e
            xs.append(i / (n - 1))
            ys.append(0.02 + ((e - lo) / span) * 0.11)
        ax.fill_between(xs, 0, ys, color="#ccc4b2", alpha=0.5, lw=0, zorder=1)
        ax.plot(xs, ys, color="#b7ac95", lw=1.0, alpha=0.6, zorder=1)

    # --- route outline on the right ---
    if coords and len(coords) > 1:
        latm = sum(c[0] for c in coords) / len(coords)
        k = math.cos(math.radians(latm)) or 1.0
        rx = [c[1] * k for c in coords]
        ry = [c[0] for c in coords]
        minx, maxx = min(rx), max(rx)
        miny, maxy = min(ry), max(ry)
        rw = (maxx - minx) or 1e-9
        rh = (maxy - miny) or 1e-9
        bx0, bx1, by0, by1 = 0.47, 0.96, 0.16, 0.9  # target box (figure coords)
        scale = min((bx1 - bx0) / rw, (by1 - by0) / rh)
        cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
        fx, fy = (bx0 + bx1) / 2, (by0 + by1) / 2
        px = [fx + (x - cx) * scale for x in rx]
        py = [fy + (y - cy) * scale for y in ry]
        ax.plot(px, py, color=BLUE, lw=4.5, solid_capstyle="round",
                solid_joinstyle="round", zorder=3)

    # --- text column on the left ---
    fig.text(0.055, 0.78, ride_type.upper(), fontproperties=MONOB, fontsize=21,
             color=ACCENT, va="top")
    fig.text(0.055, 0.70, name, fontproperties=MONOB, fontsize=33, color=INK, va="top")
    lines = []
    if dist_km is not None:
        lines.append(f"{dist_km} km")
    if climb_m is not None:
        lines.append(f"{climb_m} m up")
    if duration:
        lines.append(str(duration))
    fig.text(0.055, 0.60, "   ".join(lines), fontproperties=MONO, fontsize=23,
             color=MUT, va="top")
    fig.text(0.055, 0.08, "charalambous.uk/cycling", fontproperties=MONO,
             fontsize=15, color="#a49c8c", va="bottom")

    fig.savefig(out_path, facecolor=BG, dpi=DPI)
    plt.close(fig)
