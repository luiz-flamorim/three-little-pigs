"""Monoline drawing kit for the Three Little Pigs comic.

One ink, two weights, no fills or shading: outlines (the silhouette of each object) use the
main weight, and details inside a shape (faces, belly icons, fur, veins, windows) use the
thinner detail weight. Every shape gets a thin white halo so lines stop cleanly where something
passes in front, and the parts of one object merge into a single outline. Change the weights in
one place (Pen(weight=..., detail=...)) and every shape follows.
"""
import math

INK = "#141b26"     # dark navy, the only colour
PAPER = "#ffffff"


class Pen:
    def __init__(self, weight=3.0, detail=None, gap=4.0, ink=INK, paper=PAPER):
        self.w = weight        # outline weight: the silhouette of every object
        self.d = detail if detail is not None else weight * 0.58   # inner details: about 1.75 when weight is 3
        self.gap = gap         # the white gap left where a line passes behind something
        self.ink = ink
        self.paper = paper

    @property
    def halo(self):
        return self.w + 2 * self.gap

    def shape(self, parts, details=""):
        """A solid object drawn as one merged outline.

        parts: list of SVG path strings that together make the object (e.g. head, snout, ears).
        details: SVG drawn on top, inside the object (eyes, veins, inner edges).
        Layers: white halo, then a double-width ink stroke, then a white fill that eats the inner
        half of the stroke, so only the outer edge of the union stays visible."""
        p = "".join(f'<path d="{d}"/>' for d in parts)
        return (f'<g fill="{self.paper}" stroke="{self.paper}" stroke-width="{self.halo}" stroke-linejoin="round">{p}</g>'
                f'<g fill="none" stroke="{self.ink}" stroke-width="{self.w * 2 + 1.5}" stroke-linejoin="round" stroke-linecap="round">{p}</g>'
                f'<g fill="{self.paper}" stroke="{self.paper}" stroke-width="1.5" stroke-linejoin="round">{p}</g>'
                + details)

    def line(self, d, halo=False):
        """Open lines (horizon, road, limbs, details). halo=True when the line passes in front of others."""
        s = f'<path d="{d}" fill="none" stroke="{self.paper}" stroke-width="{self.halo}" stroke-linecap="round"/>' if halo else ""
        return s + f'<path d="{d}" fill="none" stroke="{self.ink}" stroke-width="{self.w}" stroke-linecap="round" stroke-linejoin="round"/>'

    def thin(self, d, halo=False):
        """Details inside a shape: faces, belly icons, fur, veins, windows, teeth."""
        s = f'<path d="{d}" fill="none" stroke="{self.paper}" stroke-width="{self.d + 2 * self.gap}" stroke-linecap="round"/>' if halo else ""
        return s + f'<path d="{d}" fill="none" stroke="{self.ink}" stroke-width="{self.d}" stroke-linecap="round" stroke-linejoin="round"/>'

    def scaled(self, k):
        """The same pen for a group drawn with transform scale(k): lines keep their on-page weight."""
        return Pen(self.w / k, self.d / k, self.gap / k, self.ink, self.paper)

    def dots(self, *circles):
        """Small solid dots (eyes, nostrils, a nose): (x, y, r) tuples. The only filled ink allowed."""
        return "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{self.ink}"/>' for x, y, r in circles)

    def svg(self, body, width=600, height=420):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">'
                f'<rect width="{width}" height="{height}" fill="{self.paper}"/>{body}</svg>')


# ---------- geometry: build everything from circles, arcs and straight lines ----------

def pt(p):
    return f"{p[0]:.1f} {p[1]:.1f}"


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def toward(p, vp, t):
    """Move point p a fraction t of the way to the vanishing point: use it for every receding edge."""
    return lerp(p, vp, t)


def polygon(*points):
    return "M" + " L".join(pt(p) for p in points) + " Z"


def circle(cx, cy, r):
    return f"M{cx - r} {cy} a{r} {r} 0 1 0 {2 * r} 0 a{r} {r} 0 1 0 {-2 * r} 0 Z"


def vesica(x, top, bottom, r):
    """Pointed leaf shape (two arcs), standing upright: tree canopies, ears, flames."""
    return f"M{x} {top} A{r} {r} 0 0 1 {x} {bottom} A{r} {r} 0 0 1 {x} {top} Z"


def on_arc(cx, cy, r, degrees):
    """A point on a circle, angle counter-clockwise from the right: for placing things evenly on a curve."""
    a = math.radians(degrees)
    return (cx + r * math.cos(a), cy - r * math.sin(a))


def chevron(x, y, w=16, h=7):
    """A small '^' mark centred on (x, y): fur, grass, birds."""
    return f"M{x - w / 2:.1f} {y + h / 2:.1f} L{x:.1f} {y - h / 2:.1f} L{x + w / 2:.1f} {y + h / 2:.1f}"


def capsule(a, b, r, n=10):
    """A rounded bar from a to b with radius r: limbs, jaws, fingers."""
    ang = math.atan2(b[1] - a[1], b[0] - a[0]); pts = []
    for k in range(n + 1):
        t = ang - math.pi / 2 + math.pi * k / n
        pts.append((b[0] + r * math.cos(t), b[1] + r * math.sin(t)))
    for k in range(n + 1):
        t = ang + math.pi / 2 + math.pi * k / n
        pts.append((a[0] + r * math.cos(t), a[1] + r * math.sin(t)))
    return polygon(*pts)


def ellipse(cx, cy, rx, ry, rot=0, n=24):
    """An ellipse as a path, optionally rotated (degrees): snouts, grains, leaves, mouths."""
    a = math.radians(rot); pts = []
    for k in range(n):
        t = 2 * math.pi * k / n
        x, y = rx * math.cos(t), ry * math.sin(t)
        pts.append((cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)))
    return polygon(*pts)


def rotate(points, degrees, center):
    """Rotate points around a centre (screen coordinates, y down): opening a jaw, swinging an arm."""
    a = math.radians(degrees); cx, cy = center
    return [(cx + (x - cx) * math.cos(a) - (y - cy) * math.sin(a), cy + (x - cx) * math.sin(a) + (y - cy) * math.cos(a)) for x, y in points]


def leaf(cx, cy, length, width, angle, n=16):
    """A soft pointed leaf (lens) centred on (cx, cy), its long axis at `angle` degrees: pig ears, leaves, grains."""
    a = math.radians(angle); ux, uy = math.cos(a), math.sin(a); nx, ny = -uy, ux
    side1, side2 = [], []
    for i in range(n + 1):
        t = i / n; along = (t - 0.5) * length; half = width / 2 * math.sin(math.pi * t)
        side1.append((cx + ux * along + nx * half, cy + uy * along + ny * half))
        side2.append((cx + ux * along - nx * half, cy + uy * along - ny * half))
    return polygon(*(side1 + side2[::-1][1:-1]))
