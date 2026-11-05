"""Comic page tools: a widescreen (16:9) page cut into panels, speech bubbles, captions, sound
effects, and the self-contained HTML that publishes the page.

Panels are made row by row. Dividers between panels can slant: two slanted dividers side by side
make a parallelogram, one makes a trapezoid, none makes a rectangle or square. The gap (gutter)
between panels is the same everywhere.
"""
import html as _html
import random as _random
from mono import Pen, polygon, pt

PAGE_W, PAGE_H = 1920, 1080            # the whole story fits one widescreen page
FONT = "'Chalkboard SE', 'Comic Neue', 'Comic Sans MS', 'Marker Felt', sans-serif"


class Panel:
    def __init__(self, pid, corners, row=0):
        self.id = pid
        self.row = row
        self.corners = corners                       # top-left, top-right, bottom-right, bottom-left
        xs = [c[0] for c in corners]; ys = [c[1] for c in corners]
        self.x, self.y = min(xs), min(ys)
        self.w, self.h = max(xs) - self.x, max(ys) - self.y

    def path(self):
        return polygon(*self.corners)

    def left_at(self, v):
        """x of the panel's left edge at local height v (0 = top), in local coordinates."""
        (tlx, tly), (blx, bly) = self.corners[0], self.corners[3]
        return tlx + (blx - tlx) * v / self.h - self.x

    def right_at(self, v):
        (trx, try_), (brx, bry) = self.corners[1], self.corners[2]
        return trx + (brx - trx) * v / self.h - self.x


def layout(rows, top=110, margin=36, gutter=24, W=PAGE_W, H=PAGE_H):
    """rows: list of (height_share, widths, slants). widths are relative shares within the row;
    slants has one value per divider: how far its top leans right of its bottom (0 = upright)."""
    panels, n, rows_done = [], 0, 0
    total_h = H - top - margin - gutter * (len(rows) - 1)
    share_sum = sum(r[0] for r in rows)
    y = top
    for share, widths, slants in rows:
        h = total_h * share / share_sum
        inner = W - 2 * margin - gutter * (len(widths) - 1)
        xs = [margin]
        for wdt in widths:
            xs.append(xs[-1] + inner * wdt / sum(widths) + gutter)
        divs = [(xs[i + 1] - gutter / 2, slants[i]) for i in range(len(widths) - 1)]
        for i in range(len(widths)):
            if i == 0: ltop = lbot = margin
            else:
                c, s = divs[i - 1]; ltop, lbot = c + s / 2 + gutter / 2, c - s / 2 + gutter / 2
            if i == len(widths) - 1: rtop = rbot = W - margin
            else:
                c, s = divs[i]; rtop, rbot = c + s / 2 - gutter / 2, c - s / 2 - gutter / 2
            n += 1
            panels.append(Panel(n, [(ltop, y), (rtop, y), (rbot, y + h), (lbot, y + h)], row=rows_done))
        y += h + gutter
        rows_done += 1
    return panels


def check_reading(panels, min_offset=150):
    """Checks that a person would read the panels in story order: top to bottom, then left to right.

    Returns a list of problems (empty means the page reads well):
    - the order a reader would follow (rows by height, then left to right) must match the panel numbers;
    - between two rows, no gap between panels may line up with a gap in the row above, or the eye
      reads down the page as if it were in columns."""
    problems = []
    rows = sorted({p.row for p in panels})
    seen = sorted(panels, key=lambda p: (round(p.y), (p.corners[0][0] + p.corners[3][0]) / 2))
    if [p.id for p in seen] != sorted(p.id for p in panels):
        problems.append(f"reading order {[p.id for p in seen]} does not match the story order")
    for r in rows[:-1]:
        upper = [p for p in panels if p.row == r]; lower = [p for p in panels if p.row == r + 1]
        ups = [(a.corners[2][0] + b.corners[3][0]) / 2 for a, b in zip(upper, upper[1:])]      # gaps at the bottom of the upper row
        lows = [(a.corners[1][0] + b.corners[0][0]) / 2 for a, b in zip(lower, lower[1:])]      # gaps at the top of the lower row
        for u in ups:
            for l in lows:
                if abs(u - l) < min_offset:
                    problems.append(f"gap at x={u:.0f} in row {r + 1} lines up with gap at x={l:.0f} in row {r + 2} "
                                    f"({abs(u - l):.0f}px apart, need {min_offset}): it reads as a column")
    return problems


SIZE_WIDTH = {"big": 620, "wide": 600, "square": 330, "tall": 280, "small": 250}


def plan_layout(size_rows, slants=None, tries=60000, min_width=210, seed=1, **kw):
    """Find panel widths that match the screenwriter's sizes AND read well.

    size_rows: one list of sizes per row, e.g. [["big", "square", "wide", "small"], ...].
    slants: one list per row with a slant per divider (0 = upright); default mixes upright and slanted.
    Tries many random width sets and keeps the one closest to the wanted sizes that passes
    check_reading. Returns (panels, rows_spec) or raises ValueError if nothing reads well."""
    if slants is None:
        slants = [[(50 if (r + i) % 3 == 1 else 0) for i in range(len(row) - 1)] for r, row in enumerate(size_rows)]
    rnd, best = _random.Random(seed), None
    flat = [s for row in size_rows for s in row]
    for _ in range(tries):
        ws = [[max(min_width, SIZE_WIDTH[s] * rnd.uniform(0.7, 1.4)) for s in row] for row in size_rows]
        spec = [(1, w, sl) for w, sl in zip(ws, slants)]
        panels = layout(spec, **kw)
        if min(p.w for p in panels) < min_width or check_reading(panels):
            continue
        score = sum(abs(p.w - SIZE_WIDTH[s]) for p, s in zip(panels, flat))
        if best is None or score < best[0]:
            best = (score, panels, spec)
    if best is None:
        raise ValueError("no layout reads well with these rows; move a panel to another row and try again")
    return best[1], best[2]


def wrap(text, width, size):
    """Split text into lines that fit `width` pixels at font `size` (an estimate; leaves a little slack)."""
    per_line = max(8, int(width / (size * 0.52)))
    lines, cur = [], ""
    for word in text.split():
        if len(cur) + len(word) + (1 if cur else 0) > per_line:
            lines.append(cur); cur = word
        else:
            cur = f"{cur} {word}" if cur else word
    return lines + ([cur] if cur else [])


def _text(lines, x, y, size, anchor="middle", lh=1.22):
    out = f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" fill="#141b26" text-anchor="{anchor}">'
    for i, ln in enumerate(lines):
        out += f'<tspan x="{x:.1f}" dy="{0 if i == 0 else size * lh:.1f}">{_html.escape(ln)}</tspan>'
    return out + "</text>"


def bubble(pen, text, x, y, width, tail, size=21):
    """A speech bubble: rounded box with its top-left at (x, y) and a tail pointing at `tail` (a point)."""
    lines = wrap(text, width - 36, size)
    h = len(lines) * size * 1.22 + 30
    r = 22
    box = (f"M{x + r} {y} H{x + width - r} A{r} {r} 0 0 1 {x + width} {y + r} V{y + h - r} A{r} {r} 0 0 1 {x + width - r} {y + h} "
           f"H{x + r} A{r} {r} 0 0 1 {x} {y + h - r} V{y + r} A{r} {r} 0 0 1 {x + r} {y} Z")
    cx = min(max(tail[0], x + 40), x + width - 40)
    base_y = y + h - 2 if tail[1] > y + h else y + 2
    t = polygon((cx - 13, base_y), (cx + 13, base_y), tail)
    s = pen.shape([box, t])
    return s + _text(lines, x + width / 2, y + 15 + size * 0.85, size), h


def caption(pen, text, x, y, width, size=20):
    """The Storyteller's caption: a plain box with square corners."""
    lines = wrap(text, width - 32, size)
    h = len(lines) * size * 1.22 + 26
    s = pen.shape([polygon((x, y), (x + width, y), (x + width, y + h), (x, y + h))])
    return s + _text(lines, x + 16, y + 13 + size * 0.85, size, anchor="start"), h


def sfx(word, x, y, size=64, rotate=-8, pen=None):
    """A sound effect in hollow outlined letters, like WHOOSH!"""
    w = pen.w if pen else 3
    return (f'<text x="{x}" y="{y}" transform="rotate({rotate} {x} {y})" font-family="{FONT}" font-size="{size}" font-weight="bold" '
            f'fill="#ffffff" stroke="#141b26" stroke-width="{w}" stroke-linejoin="round" paint-order="stroke" text-anchor="middle" '
            f'letter-spacing="2">{_html.escape(word)}</text>')


def _panel(pen, p, scene):
    art, words = scene(p) if scene else ("", "")
    clip = f'<clipPath id="panel{p.id}"><path d="{p.path()}"/></clipPath>'
    body = (f'<g clip-path="url(#panel{p.id})"><g transform="translate({p.x:.1f} {p.y:.1f})">{art}</g></g>'
            f'<path d="{p.path()}" fill="none" stroke="#141b26" stroke-width="{pen.w * 1.3:.1f}" stroke-linejoin="round"/>'
            f'<g transform="translate({p.x:.1f} {p.y:.1f})">{words}</g>')
    return clip, body


def export_panels(pen, panels, scenes, folder):
    """Save each panel as its own SVG (panels/panel-01.svg ...), framed tightly: used as thumbnails
    on the production page, and handy for sharing a single moment."""
    import os
    os.makedirs(folder, exist_ok=True)
    paths = []
    for p in panels:
        clip, body = _panel(pen, p, scenes.get(p.id))
        m = pen.w * 2
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{p.x - m:.1f} {p.y - m:.1f} {p.w + 2 * m:.1f} {p.h + 2 * m:.1f}" '
               f'width="{p.w + 2 * m:.0f}" height="{p.h + 2 * m:.0f}"><rect x="{p.x - m:.1f}" y="{p.y - m:.1f}" width="{p.w + 2 * m:.1f}" '
               f'height="{p.h + 2 * m:.1f}" fill="{pen.paper}"/><defs>{clip}</defs>{body}</svg>')
        path = os.path.join(folder, f"panel-{p.id:02d}.svg")
        open(path, "w").write(svg)
        paths.append(path)
    return paths


def page(pen, panels, scenes, title):
    """Assemble the page: title, then each panel's scene clipped to its shape, then its border.
    scenes: {panel id: function(panel) -> (art_svg, text_svg)}; art is in panel-local coordinates."""
    s = [f'<text x="{PAGE_W / 2}" y="74" font-family="{FONT}" font-size="44" fill="#141b26" text-anchor="middle">{_html.escape(title)}</text>']
    parts = [_panel(pen, p, scenes.get(p.id)) for p in panels]
    s.append("<defs>" + "".join(c for c, _ in parts) + "</defs>")
    s += [b for _, b in parts]
    return pen.svg("".join(s), PAGE_W, PAGE_H)


def publish(svg, title, summary, out_path):
    """Write the page as one self-contained HTML file: no external files, opens in any browser."""
    doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_html.escape(title)}</title><meta name="description" content="{_html.escape(summary)}">
<style>html,body{{margin:0;height:100%;background:#ffffff}}body{{display:flex;align-items:center;justify-content:center}}
svg{{width:100vw;height:auto;max-height:100vh;max-width:calc(100vh * 16 / 9)}}</style></head>
<body>{svg}</body></html>
"""
    open(out_path, "w").write(doc)
    return out_path
