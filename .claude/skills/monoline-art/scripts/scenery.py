"""Scenery for comic panels: the three houses, trees, bushes, clouds and a beanstalk.
Each function returns SVG; outlines at the pen's main weight, inside details thin.
"""
import math
from mono import circle, polygon, vesica, lerp, toward, pt, leaf, capsule


def _door(pen, cx, base, w, h):
    d = f"M{cx - w / 2:.1f} {base} V{base - h + w / 2:.1f} A{w / 2:.1f} {w / 2:.1f} 0 0 1 {cx + w / 2:.1f} {base - h + w / 2:.1f} V{base}"
    return f'<path d="{d} Z" fill="{pen.paper}" stroke="{pen.ink}" stroke-width="{pen.d}" stroke-linejoin="round"/>'


def haystack(pen, x, base, w):
    """The Straw Pig's house: a big hay heap with a little door and a round window."""
    h = w * 0.78
    dome = f"M{x} {base} C{x} {base - h * 1.3:.1f} {x + w} {base - h * 1.3:.1f} {x + w} {base} Z"
    cx = x + w / 2
    d = ""
    for k, f in enumerate((0.35, 0.6, 0.82)):                      # straw bands following the dome
        y = base - h * f
        half = w / 2 * math.sqrt(max(0.05, 1 - (f ** 1.6))) * 0.92
        d += f"M{cx - half:.1f} {y + 6:.1f} Q{cx:.1f} {y - 8:.1f} {cx + half:.1f} {y + 6:.1f} "
    for dx in (-0.32, -0.2, 0.2, 0.32):                             # loose straws
        d += f"M{cx + w * dx:.1f} {base - h * 0.18:.1f} l{w * 0.02:.1f} {-w * 0.08:.1f} "
    top = (cx, base - h * 0.98)
    tuft = pen.line(f"M{top[0]:.1f} {top[1]:.1f} l-10 -14 M{top[0]:.1f} {top[1]:.1f} l2 -17 M{top[0]:.1f} {top[1]:.1f} l12 -12", halo=True)
    s = pen.shape([dome], pen.thin(d) + _door(pen, cx, base, w * 0.2, w * 0.3) + pen.thin(circle(cx + w * 0.24, base - h * 0.5, w * 0.06)))
    return s + tuft


def box_house(pen, kind, x, base, w, vp, t=0.28):
    """The Sticks or Bricks house: a front face looking at us, its side and roof running to the vanishing point."""
    hw = w * 0.86
    FL, FR, TR, TL = (x, base), (x + w, base), (x + w, base - hw), (x, base - hw)
    APEX = (x + w / 2, base - hw - w * 0.48)
    right = vp[0] > x + w / 2
    B, T = (FR, TR) if right else (FL, TL)
    SB, ST, RIDGE = toward(B, vp, t), toward(T, vp, t), toward(APEX, vp, t)
    front = polygon(FL, FR, TR, APEX, TL)
    side = polygon(B, SB, ST, T)
    roof = polygon(T, APEX, RIDGE, ST)
    cx = x + w / 2
    det = pen.thin(f"M{pt(T)} L{pt(B)} M{pt(T)} L{pt(ST)} M{pt(TL)} L{pt(TR)}")
    if kind == "sticks":
        tex = "".join(f"M{x + w * f:.1f} {base - 4:.1f} V{base - hw + 6:.1f} " for f in (0.12, 0.24, 0.76, 0.88))
        tex += f"M{x + 4:.1f} {base - hw * 0.62:.1f} H{x + w - 4:.1f} "                   # the string
        for k in (0.3, 0.55, 0.8):
            r0, e0 = lerp(APEX, RIDGE, k), lerp(T, ST, k)
            tex += f"M{pt(lerp(r0, e0, 0.2))} L{pt(lerp(r0, e0, 0.75))} "
        det += pen.thin(tex)
    else:
        tex, rows = "", 7
        for r in range(1, rows):
            y = base - hw * r / rows
            tex += f"M{x + 3:.1f} {y:.1f} H{x + w - 3:.1f} "
        for r in range(rows):
            y0, y1 = base - hw * r / rows, base - hw * (r + 1) / rows
            off = 0.5 if r % 2 else 0
            for c in range(4):
                xx = x + w * (c + off) / 4
                if x + 4 < xx < x + w - 4:
                    tex += f"M{xx:.1f} {y0:.1f} V{y1:.1f} "
        det += pen.thin(tex)
    det += _door(pen, cx, base, w * 0.26, w * 0.44)
    if kind == "sticks":
        det += f'<path d="{polygon((x + w * 0.62, base - hw * 0.8), (x + w * 0.84, base - hw * 0.8), (x + w * 0.84, base - hw * 0.58), (x + w * 0.62, base - hw * 0.58))}" fill="{pen.paper}" stroke="{pen.ink}" stroke-width="{pen.d}"/>'
    else:
        det += pen.thin(circle(cx, base - hw - w * 0.2, w * 0.07))
    s = pen.shape([front, side, roof], det)
    if kind == "bricks":                                          # chimney on the roof
        c0 = lerp(lerp(APEX, RIDGE, 0.55), lerp(T, ST, 0.55), 0.35)
        s += pen.shape([polygon((c0[0] - 9, c0[1] + 4), (c0[0] - 9, c0[1] - 26), (c0[0] + 9, c0[1] - 26), (c0[0] + 9, c0[1] + 10))])
    return s


def tree(pen, x, base, height, width_ratio=0.75):
    """A leaf tree: trunk and a pointed canopy with one vein."""
    top = base - height; bot = base - height * 0.38
    r = (bot - top) * width_ratio
    vein = f"M{x - 3} {bot - (bot - top) * 0.18:.1f} Q{x - 6} {(top + bot) / 2:.1f} {x - 3} {top + (bot - top) * 0.3:.1f}"
    return pen.line(f"M{x} {bot} V{base}", halo=True) + pen.shape([vesica(x, top, bot, r)], pen.thin(vein))


def bush(pen, x, base, w):
    """A low bush made of merged circles with a flat base."""
    r = w / 4.2
    parts = [circle(x + r, base - r * 0.8, r), circle(x + w / 2, base - r * 1.3, r * 1.25), circle(x + w - r, base - r * 0.8, r),
             polygon((x + r * 0.2, base), (x + w - r * 0.2, base), (x + w - r * 0.2, base - r), (x + r * 0.2, base - r))]
    return pen.shape(parts, pen.thin(f"M{x + w * 0.3:.1f} {base - r * 1.2:.1f} q8 -8 16 0 M{x + w * 0.6:.1f} {base - r * 1.6:.1f} q8 -8 16 0"))


def cloud(pen, x, y, w):
    r = w / 6
    s = pen.shape([circle(x + r * 1.5, y, r), circle(x + w / 2, y - r * 0.6, r * 1.4), circle(x + w - r * 1.5, y, r)])
    return s + f'<rect x="{x - 4}" y="{y + 1.5 + pen.w / 2:.1f}" width="{w + 8}" height="{r * 1.2:.1f}" fill="{pen.paper}"/>' + pen.line(f"M{x + r * 0.55:.1f} {y + 1:.1f} H{x + w - r * 0.55:.1f}")


def beanstalk(pen, points, leaf_size=34, width=9):
    """Jack's beanstalk: a thick wavy stalk with leaves on alternate sides and a curl at the top."""
    stalk = [capsule(points[i], points[i + 1], width) for i in range(len(points) - 1)]
    leaves, veins = [], ""
    for i in range(1, len(points) - 1):
        (x0, y0), (x1, y1) = points[i - 1], points[i + 1]
        ang = math.degrees(math.atan2(y1 - y0, x1 - x0))
        side = 1 if i % 2 else -1
        a = ang + side * 70
        cx = points[i][0] + math.cos(math.radians(a)) * leaf_size * 0.62
        cy = points[i][1] + math.sin(math.radians(a)) * leaf_size * 0.62
        leaves.append(leaf(cx, cy, leaf_size * 1.15, leaf_size * 0.55, a))
        veins += f"M{points[i][0] + math.cos(math.radians(a)) * leaf_size * 0.3:.1f} {points[i][1] + math.sin(math.radians(a)) * leaf_size * 0.3:.1f} L{cx + math.cos(math.radians(a)) * leaf_size * 0.3:.1f} {cy + math.sin(math.radians(a)) * leaf_size * 0.3:.1f} "
    tip = points[-1]
    curl = pen.line(f"M{tip[0]:.1f} {tip[1]:.1f} c14 -10 30 0 24 14 c-4 9 -16 6 -14 -2", halo=True)
    return pen.shape(stalk + leaves, pen.thin(veins)) + curl


def bean(pen, x, y, size=14, angle=-20, sparkle=True):
    """Jack's magic bean: a small kidney shape, with sparkle lines if it is magic."""
    from mono import ellipse
    out = pen.shape([ellipse(x, y, size, size * 0.62, angle)], pen.thin(f"M{x - size * 0.4:.1f} {y - size * 0.05:.1f} q{size * 0.4:.1f} {size * 0.3:.1f} {size * 0.8:.1f} 0"))
    if sparkle:
        r0, r1 = size * 1.35, size * 1.9
        out += pen.thin("".join(f"M{x + r0 * math.cos(math.radians(a)):.1f} {y + r0 * math.sin(math.radians(a)):.1f} L{x + r1 * math.cos(math.radians(a)):.1f} {y + r1 * math.sin(math.radians(a)):.1f} " for a in (-150, -90, -30, 30)))
    return out


def brick_wall(pen, x, base, w, rows=3, row_h=14):
    """A low brick wall still being built: a few rows of bricks."""
    h = rows * row_h
    tex = ""
    for r in range(1, rows):
        tex += f"M{x + 2} {base - r * row_h} H{x + w - 2} "
    for r in range(rows):
        off = 0.5 if r % 2 else 0
        n = max(2, int(w / 34))
        for c in range(n + 1):
            xx = x + w * (c + off) / n
            if x + 3 < xx < x + w - 3:
                tex += f"M{xx:.1f} {base - r * row_h} V{base - (r + 1) * row_h} "
    return pen.shape([polygon((x, base), (x + w, base), (x + w, base - h), (x, base - h))], pen.thin(tex))


def speed_lines(pen, x, y, length=40, gap=14, n=3, angle=0):
    a = math.radians(angle); ux, uy = math.cos(a), math.sin(a); nx, ny = -uy, ux
    return pen.thin("".join(f"M{x + nx * gap * i:.1f} {y + ny * gap * i:.1f} l{ux * length * (1 - 0.2 * (i % 2)):.1f} {uy * length * (1 - 0.2 * (i % 2)):.1f} " for i in range(n)))
