"""The cast as reusable drawings: call pig(...) and wolf(...) in any panel so every character
looks the same everywhere. Coordinates are local: (0, 0) is the point between the feet.
Draft 1 of the character sheet; poses come next.
"""
import math
from mono import Pen, circle, polygon, capsule, ellipse, rotate, lerp, pt, chevron, leaf


def _group(pen, x, y, k, flip, body):
    sx = -k if flip else k
    return f'<g transform="translate({x} {y}) scale({sx} {k})">{body}</g>'


# ------------------------------------------------------------------ pigs
PIG_SIZE = {"straw": 0.94, "sticks": 1.0, "bricks": 1.06}


def belly_icon(p, kind):
    """The pig's mark: a wheat ear for straw, a twig for sticks, a little wall for bricks."""
    cx, cy = 0, -84
    if kind == "straw":
        s = p.thin(f"M{cx} {cy + 24} V{cy - 18}")
        for i, gy in enumerate((cy - 14, cy - 4, cy + 6)):
            s += p.thin(ellipse(cx - 7, gy, 7, 3.4, rot=-35)) + p.thin(ellipse(cx + 7, gy, 7, 3.4, rot=35))
        return s + p.thin(ellipse(cx, cy - 25, 3.4, 7))
    if kind == "sticks":
        s = p.thin(f"M{cx - 18} {cy + 20} L{cx + 16} {cy - 22} M{cx + 1} {cy} L{cx + 18} {cy + 4} M{cx - 8} {cy + 8} L{cx - 18} {cy - 2}")
        return s + p.thin(ellipse(cx + 24, cy + 2, 7, 3.6, rot=-20))
    # bricks
    return p.thin(f"M{cx - 22} {cy - 14} H{cx + 22} V{cy + 14} H{cx - 22} Z M{cx - 22} {cy} H{cx + 22} "
                  f"M{cx} {cy - 14} V{cy} M{cx - 11} {cy} V{cy + 14} M{cx + 11} {cy} V{cy + 14}")


def pig_face(p, expr):
    """Eyes, brows, snout and mouth. Head centre is (0, -190)."""
    s = p.thin(ellipse(0, -176, 20, 14))
    s += p.dots((-7, -176, 3.6), (7, -176, 3.6))
    if expr == "scared":
        s += p.thin(circle(-22, -204, 9)) + p.thin(circle(22, -204, 9)) + p.dots((-21, -203, 3.6), (21, -203, 3.6))
        s += p.thin("M-34 -220 L-14 -227 M34 -220 L14 -227")
        s += p.thin(ellipse(0, -151, 6, 7.5))
        s += p.thin("M60 -228 Q52 -214 60 -210 Q68 -214 60 -228 Z")
    elif expr == "teasing":
        s += p.thin("M-31 -203 Q-22 -211 -13 -203") + p.dots((22, -204, 5.5)) + p.dots() + f'<circle cx="24" cy="-206.5" r="1.8" fill="{p.paper}"/>'
        s += p.thin("M-32 -219 L-14 -217 M32 -222 L14 -217")
        s += p.thin("M-16 -156 Q0 -150 16 -156 M-7 -153 V-145 A7 7 0 0 0 7 -145 V-153 M0 -152 V-146")
    elif expr == "determined":
        s += p.dots((-22, -203, 5.5), (22, -203, 5.5)) + f'<circle cx="-20" cy="-205.5" r="1.8" fill="{p.paper}"/><circle cx="24" cy="-205.5" r="1.8" fill="{p.paper}"/>'
        s += p.thin("M-35 -221 L-12 -213 M35 -221 L12 -213")
        s += p.thin("M-10 -154 H10")
    else:  # happy
        s += p.dots((-22, -204, 5.5), (22, -204, 5.5)) + f'<circle cx="-20" cy="-206.5" r="1.8" fill="{p.paper}"/><circle cx="24" cy="-206.5" r="1.8" fill="{p.paper}"/>'
        s += p.thin("M-31 -219 Q-22 -224 -13 -219 M31 -219 Q22 -224 13 -219")
        s += p.thin("M-15 -157 Q0 -146 15 -157")
    return s


def pig_head(p, expr):
    ears, veins = [], ""
    for sx in (-1, 1):
        cx, cy, ang = sx * 40, -246, (-122 if sx < 0 else -58)
        ears.append(leaf(cx, cy, 52, 30, ang))
        a = math.radians(ang)
        veins += p.thin(f"M{cx - math.cos(a) * 6:.1f} {cy - math.sin(a) * 6:.1f} L{cx + math.cos(a) * 14:.1f} {cy + math.sin(a) * 14:.1f}")
    return p.shape([circle(0, -190, 56)] + ears, veins + pig_face(p, expr))


def _chain(points, radii):
    """A limb as rounded bars joined end to end: shoulder, elbow, wrist... (or hip, knee, ankle, toe)."""
    return [capsule(points[i], points[i + 1], radii[min(i, len(radii) - 1)]) for i in range(len(points) - 1)]


def _tip_line(p, a, b, inside=7, outside=1):
    """The small cleft line at the end of a pig's arm or leg, along the limb's direction."""
    L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1; ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
    return f"M{b[0] - ux * inside:.1f} {b[1] - uy * inside:.1f} L{b[0] + ux * (12 + outside):.1f} {b[1] + uy * (12 + outside):.1f}"


# Pig poses, facing right (flip=True to face left). Points are local: (0, 0) between the feet.
# arms: shoulder -> (elbow ->) hand; legs: hip -> foot. tilt leans the whole pig (degrees, + = forward),
# lift raises it off the ground (jumping, running), head tilts the head.
PIG_POSES = {
    "stand": dict(arms=[[(-56, -112), (-78, -74)], [(56, -112), (78, -74)]],
                  legs=[[(-26, -40), (-26, -10)], [(26, -40), (26, -10)]]),
    "run":   dict(tilt=12, lift=12, head=-6,
                  arms=[[(-56, -112), (-90, -96)], [(56, -112), (84, -140)]],
                  legs=[[(-26, -40), (-56, -20)], [(26, -40), (52, -32)]], fx="speed"),
    "build": dict(arms=[[(-56, -112), (-40, -46)], [(56, -112), (40, -46)]],
                  legs=[[(-26, -40), (-30, -10)], [(26, -40), (30, -10)]], prop=True),
    "tease": dict(tilt=-4, head=-10,
                  arms=[[(-56, -112), (-88, -96), (-62, -66)], [(56, -112), (88, -96), (62, -66)]],
                  legs=[[(-26, -40), (-26, -10)], [(26, -40), (56, -26)]]),
    "cheer": dict(lift=20, head=4,
                  arms=[[(-56, -112), (-86, -178)], [(56, -112), (86, -178)]],
                  legs=[[(-26, -40), (-42, -12)], [(26, -40), (42, -12)]], fx="jump"),
}


def pig_prop(p, kind):
    """What each pig builds with, carried in front at the waist (drawn over the hands)."""
    if kind == "straw":
        s = p.shape([polygon((-30, -64), (30, -64), (20, -18), (-20, -18))],
                    p.thin("M-16 -60 L-11 -22 M0 -60 V-22 M16 -60 L11 -22 M-26 -44 H26 M-25 -38 H25"))
        return s + p.thin("M-24 -64 L-36 -76 M-8 -64 L-12 -80 M8 -64 L12 -80 M24 -64 L36 -76")
    if kind == "sticks":
        s = ""
        for dy in (16, 0, -16):
            s += p.shape([capsule((-54, -30 + dy), (54, -58 + dy), 6)])
        return s + p.thin("M-8 -66 L0 -18 M2 -68 L10 -20", halo=True)
    return p.shape([polygon((-44, -64), (-32, -76), (48, -76), (48, -40), (36, -28), (-44, -28))],
                   p.thin("M-44 -64 H36 V-28 M36 -64 L48 -76 M-8 -50 H12"))


def pig(pen, x, y, kind="straw", expr="happy", scale=1.0, flip=False, pose="stand"):
    k = scale * PIG_SIZE[kind]; p = pen.scaled(k)
    P = PIG_POSES[pose]
    legs = [cap for leg in P["legs"] for cap in _chain(leg, [13])]
    hooves = "".join(p.thin(_tip_line(p, leg[-2], leg[-1])) for leg in P["legs"])
    s = p.shape([ellipse(0, -84, 64, 62)] + legs, hooves + belly_icon(p, kind))
    for arm in P["arms"]:
        s += p.shape(_chain(arm, [12]), p.thin(_tip_line(p, arm[-2], arm[-1])))
    if P.get("prop"):
        s += pig_prop(p, kind)
    s += f'<g transform="rotate({P.get("head", 0)} 0 -140)">{pig_head(p, expr)}</g>'
    s = f'<g transform="translate(0 {-P.get("lift", 0)}) rotate({P.get("tilt", 0)} 0 -40)">{s}</g>'
    fx = P.get("fx")
    if fx == "speed":
        s = p.thin("M-104 -130 h-44 M-116 -96 h-60 M-100 -62 h-38") + p.thin(circle(-74, -6, 6) + circle(-92, -12, 4)) + s
    if fx == "jump":
        s = p.thin("M-30 10 q10 -8 20 0 M10 10 q10 -8 20 0") + p.thin("M-108 -170 l-14 -8 M108 -170 l14 -8 M-112 -146 h-16 M112 -146 h16") + s
    return _group(pen, x, y, k, flip, s)


def pig_portrait(pen, x, y, kind="straw", expr="happy", scale=1.0):
    """Head only, for expression studies and close-ups: (x, y) is the centre of the head."""
    k = scale * PIG_SIZE[kind]; p = pen.scaled(k)
    return f'<g transform="translate({x} {y}) scale({k}) translate(0 190)">{pig_head(p, expr)}</g>'


# ------------------------------------------------------------------ the Wolf
def wolf_head(p, expr="snarl"):
    """Head in 3/4 view facing left, centre (0, 0). The lower jaw swings open around a hinge."""
    open_by = {"grin": 0, "toothy": 0, "snarl": 26, "roar": 40, "huff": 0}[expr]
    hinge = (-20, 16)
    ears = [polygon((-30, -30), (-22, -80), (4, -40)), polygon((12, -42), (38, -80), (40, -24))]
    upper = [polygon((-16, -26), (-100, -12), (-100, 12), (-30, 12)), circle(-100, 0, 12)]
    lower_pts = rotate([(-26, 14), (-92, 16), (-92, 30), (-18, 34)], -open_by, hinge)
    tip = rotate([(-92, 23)], -open_by, hinge)[0]
    lower = [polygon(*lower_pts), circle(tip[0], tip[1], 7)]
    parts = [circle(0, 0, 44)] + ears + upper + lower
    if open_by == 0:
        parts.append(polygon((-100, 6), (-24, 6), (-24, 22), (-100, 22)))   # closed mouth: no slit between the jaws
    if expr == "huff":
        parts.append(circle(-36, 20, 24))                                  # puffed cheek
    d = p.thin("M-14 -46 L-19 -64 M24 -42 L32 -64")                      # ear veins
    tooth = lambda base, ang, h, w: (f"M{base[0] + w * math.cos(ang + math.pi / 2):.1f} {base[1] + w * math.sin(ang + math.pi / 2):.1f} "
                                     f"L{base[0] + h * math.cos(ang):.1f} {base[1] + h * math.sin(ang):.1f} "
                                     f"L{base[0] - w * math.cos(ang + math.pi / 2):.1f} {base[1] - w * math.sin(ang + math.pi / 2):.1f}")
    if open_by:
        a, b = lower_pts[1], lower_pts[0]                                   # lower jaw's top edge, tip to hinge
        def lower_y(x):
            t = (x - a[0]) / (b[0] - a[0]); return a[1] + (b[1] - a[1]) * t
        teeth = ""
        for x0, h in [(-82, 18), (-68, 8), (-56, 8), (-42, 15)]:          # upper row, fangs at the ends
            gap = lower_y(x0) - 12
            if gap < 11: continue
            teeth += tooth((x0, 12), math.pi / 2, min(h, gap * 0.55), 5 if h > 10 else 3.5) + " "
        up = math.atan2(b[1] - a[1], b[0] - a[0]) - math.pi / 2
        for t, h in [(0.24, 14), (0.42, 7), (0.58, 7)]:                    # lower row
            q = lerp(a, b, t); gap = q[1] - 12
            if gap < 8: continue
            teeth += tooth(q, up, min(h, gap * 0.45), 5 if h > 10 else 3.5) + " "
        d += f'<path d="{teeth}" fill="none" stroke="{p.ink}" stroke-width="{p.d}" stroke-linejoin="round"/>'
    if expr == "grin":
        d += p.thin("M-100 14 Q-66 24 -26 14") + f'<path d="{tooth((-52, 18), math.pi / 2, 12, 4.5)}" fill="{p.paper}" stroke="{p.ink}" stroke-width="{p.d}" stroke-linejoin="round"/>'
    if expr == "toothy":                                                  # a wide, closed, toothy smile
        A, Q, Bp = (-102, 10), (-60, 26), (-22, 4)
        curve = lambda t, off: ((1 - t) ** 2 * A[0] + 2 * (1 - t) * t * Q[0] + t * t * Bp[0],
                                (1 - t) ** 2 * A[1] + 2 * (1 - t) * t * Q[1] + t * t * Bp[1] + off * (1 - abs(2 * t - 1) * 0.5))
        top = [curve(i / 14, -7) for i in range(15)]; bot = [curve(i / 14, 7) for i in range(15)]
        lips = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in top) + f" Q{Bp[0] + 6} {Bp[1] - 2} {Bp[0] + 8} {Bp[1] - 12} M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in bot)
        zig = "M" + " L".join(f"{(top if i % 2 else bot)[i][0]:.1f} {(top if i % 2 else bot)[i][1]:.1f}" for i in range(1, 14))
        fangs = ""
        for t in (0.16, 0.74):
            (x0, y0) = curve(t, -7)
            fangs += f"M{x0 - 4.5:.1f} {y0:.1f} L{x0:.1f} {y0 + 19:.1f} L{x0 + 4.5:.1f} {y0:.1f} "
        d += f'<path d="{lips}" fill="none" stroke="{p.ink}" stroke-width="{p.d}" stroke-linecap="round" stroke-linejoin="round"/>'
        d += f'<path d="{zig}" fill="none" stroke="{p.ink}" stroke-width="{p.d}" stroke-linejoin="round"/>'
        d += f'<path d="{fangs}" fill="{p.paper}" stroke="{p.ink}" stroke-width="{p.d}" stroke-linejoin="round"/>'
    if expr == "huff":
        d += p.thin("M-101 15 Q-92 22 -84 15") + p.thin(circle(-108, 22, 4))
        d += p.thin("M-20 -14 Q-10 -8 0 -14") + p.thin("M-24 -26 L2 -22")
        for yy, ln in [(4, 46), (22, 62), (40, 42)]:
            d += p.thin(f"M-124 {yy} q-{ln/4:.0f} -6 -{ln/2:.0f} 0 t-{ln/2:.0f} 0")
    else:
        d += p.thin("M-22 -12 Q-11 -21 0 -12 Q-11 -6 -22 -12 Z") + p.dots((-11, -12.5, 3.2))
        brow = {"grin": "M-26 -30 Q-12 -36 2 -28", "toothy": "M-28 -26 L4 -30", "snarl": "M-26 -32 L4 -22", "roar": "M-28 -34 L6 -20"}[expr]
        d += p.thin(brow)
    if expr in ("snarl", "roar"):
        d += p.thin("M-74 -16 q4 -5 8 0 M-62 -19 q4 -5 8 0")              # nose wrinkles
    return p.shape(parts, d + p.dots((-110, -4, 7)))


# Wolf poses, facing left (flip=True to face right). tilt leans the body around the hips
# (degrees, - = forward), lift raises him (leaping), head turns the head on top of the tilt.
# Arms are offsets from the shoulder: elbow, then wrist. The front arm (screen left) is drawn in front
# of the body; the back arm behind it. Legs are hip -> knee -> ankle -> toe, in local points.
WOLF_POSES = {
    "stand":  dict(front=[(-18, 58), (-14, 114)], back=[(18, 58), (14, 114)],
                   legs=[[(-34, -84), (-28, -16), (-54, -4)], [(34, -84), (28, -16), (54, -4)]]),
    "sneak":  dict(tilt=-16, head=8, front=[(-46, -10), (-62, 26)], back=[(-60, -26), (-116, -6)],
                   legs=[[(-70, -112), (-88, -52), (-106, -40)], [(40, -90), (30, -22), (8, -4)]]),
    "huff":   dict(tilt=10, head=-8, front=[(-46, 44), (-8, 92)], back=[(46, 44), (8, 92)],
                   legs=[[(-64, -92), (-78, -18), (-104, -6)], [(60, -90), (70, -18), (96, -6)]]),
    "pounce": dict(tilt=-50, lift=70, head=30, front=[(-58, 8), (-114, 0)], back=[(-56, 16), (-108, 14)],
                   legs=[[(62, -152), (122, -140), (148, -150)], [(66, -120), (126, -102), (152, -108)]], fx="leap"),
    "climb":  dict(tilt=-6, head=-4, front=[(-30, -52), (-22, -110)], back=[(30, -50), (14, -106)],
                   legs=[[(-56, -126), (-50, -66), (-72, -58)], [(40, -92), (36, -24), (58, -12)]]),
    "knock":  dict(tilt=-4, front=[(-50, 4), (-90, -20)], back=[(14, 52), (-14, 90)],
                   legs=[[(-36, -84), (-30, -16), (-56, -4)], [(32, -84), (30, -16), (56, -4)]], fx="knock"),
    "hold":   dict(head=-6, front=[(-44, 20), (-104, -24)], back=[(-36, 40), (-112, 6)],
                   legs=[[(-34, -84), (-28, -16), (-54, -4)], [(34, -84), (28, -16), (54, -4)]]),
}


def _rot(pt_, deg, c=(0, -150)):
    return rotate([pt_], deg, c)[0]


def _hand(p, wrist, elbow, front=True):
    """A round hand at the end of the forearm with three claws pointing onward."""
    L = math.hypot(wrist[0] - elbow[0], wrist[1] - elbow[1]) or 1
    ux, uy = (wrist[0] - elbow[0]) / L, (wrist[1] - elbow[1]) / L
    hc = (wrist[0] + ux * 8, wrist[1] + uy * 8)
    claws = ""
    for spread in (-28, 0, 28):
        a = math.atan2(uy, ux) + math.radians(spread)
        sx, sy = hc[0] + 10 * math.cos(a), hc[1] + 10 * math.sin(a)
        claws += f"M{sx:.1f} {sy:.1f} L{sx + 13 * math.cos(a):.1f} {sy + 13 * math.sin(a):.1f} "
    return circle(hc[0], hc[1], 12), claws


def wolf(pen, x, y, expr="snarl", scale=1.0, flip=False, pose="stand"):
    k = scale; p = pen.scaled(k)
    P = WOLF_POSES[pose]; t = P.get("tilt", 0)
    s = ""
    tail = "M30 -150 C80 -164 132 -132 130 -80 C129 -60 116 -50 106 -56 C112 -90 82 -120 34 -128 Z"
    s += f'<g transform="rotate({t * 0.6:.1f} 30 -150)">' + p.shape([tail], p.thin(chevron(108, -112, 12, 6) + chevron(116, -88, 12, 6))) + "</g>"
    claws_line = ""
    for sx, leg in zip((-1, 1), P["legs"]):                                # legs, behind the body
        hip = _rot((sx * 26, -152), t)
        pts = [hip] + leg
        s += p.shape(_chain(pts, [15, 11, 8]))
        toe, ank = pts[-1], pts[-2]
        L = math.hypot(toe[0] - ank[0], toe[1] - ank[1]) or 1
        claws_line += f"M{toe[0] + (toe[0] - ank[0]) / L * 4:.1f} {toe[1] + (toe[1] - ank[1]) / L * 4:.1f} l{(toe[0] - ank[0]) / L * 8:.1f} {(toe[1] - ank[1]) / L * 8 + 2:.1f} "
    def arm(sx, offs):
        sh = _rot((sx * 52, -254), t)
        el = (sh[0] + offs[0][0], sh[1] + offs[0][1]); wr = (sh[0] + offs[1][0], sh[1] + offs[1][1])
        hand, claws = _hand(p, wr, el)
        return p.shape(_chain([sh, el, wr], [12, 10]) + [hand]) + p.line(claws, halo=True)
    s += arm(1, P["back"])                                                  # back arm, behind the body
    torso = "M-50 -268 C-66 -230 -60 -190 -42 -160 C-36 -150 -30 -146 -24 -144 L24 -144 C30 -146 36 -150 42 -160 C60 -190 66 -230 50 -268 C36 -284 -36 -284 -50 -268 Z"
    det = p.thin("M-26 -250 C-36 -212 -28 -178 0 -162 C28 -178 36 -212 26 -250") + p.thin(chevron(-30, -200, 12, 6) + chevron(34, -214, 12, 6))
    s += f'<g transform="rotate({t} 0 -150)">' + p.shape([torso], det) + "</g>"
    s += p.line(claws_line)
    hc = _rot((8, -318), t)
    s += f'<g transform="translate({hc[0]:.1f} {hc[1]:.1f}) rotate({t + P.get("head", 0)})">{wolf_head(p, expr)}</g>'
    s += arm(-1, P["front"])                                                # front arm, in front of everything
    s = f'<g transform="translate(0 {-P.get("lift", 0)})">{s}</g>'
    fx = P.get("fx")
    if fx == "leap":
        s = p.thin("M178 -236 h50 M188 -206 h64 M178 -176 h40") + p.thin(ellipse(10, 2, 90, 7)) + s
    if fx == "knock":
        s += p.thin("M-176 -300 q-10 16 0 32 M-190 -308 q-14 24 0 48")
    return _group(pen, x, y, k, flip, s)


def wolf_portrait(pen, x, y, expr="snarl", scale=1.0):
    p = pen.scaled(scale)
    return f'<g transform="translate({x} {y}) scale({scale})">{wolf_head(p, expr)}</g>'


def wolf_back(pen, x, y, scale=1.0, expr="grin", arm=False):
    """The Wolf seen from behind, for over-the-shoulder shots (as in the reference panel).
    (x, y) is the centre of his shoulders' arc; he looks left. The body runs off below."""
    k = scale; p = pen.scaled(k)
    body = "M-96 60 V0 A96 96 0 0 1 96 0 V60 Z"
    parts = [body]
    if arm:
        parts.append("M-76 -56 L-130 -62 A11 11 0 0 0 -130 -40 L-72 -32 Z")
    fur = "".join(chevron(*(lambda a: (60 * math.cos(math.radians(a)), -60 * math.sin(math.radians(a))))(a), 16, 7) + " " for a in (125, 90, 55))
    s = p.shape(parts, p.thin(fur) + (p.line("M-139 -57 L-151 -63 M-142 -51 L-155 -51 M-139 -44 L-151 -38", halo=True) if arm else ""))
    head, snout = circle(-18, -126, 34), "M-36 -148 L-96 -134 A11 11 0 0 0 -94 -112 L-34 -110 Z"
    ears = [polygon((-42, -150), (-40, -188), (-20, -158)), polygon((-14, -158), (8, -188), (8, -150))]
    d = p.thin("M-88 -120 L-42 -118 M-79 -119.5 L-75.5 -114 L-72 -119") + p.thin("M-32 -158 L-36 -174 M-1 -158 L4 -174")
    d += p.thin("M-37 -139 Q-30 -145 -23 -139 Q-30 -135 -37 -139 Z") + p.dots((-30, -139.4, 1.8), (-100, -128, 5))
    s += p.shape([head, snout] + ears, d)
    return f'<g transform="translate({x} {y}) scale({k})">{s}</g>'
