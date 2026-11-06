"""Exports every character in every expression, and in every pose, as its own SVG into assets/characters/ (poses in assets/characters/poses/).

Usage: python3 export_characters.py [OUTPUT_FOLDER]
Run it again after changing a design in cast.py, so the folder always matches the code.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mono import Pen
from cast import pig, wolf, PIG_SIZE, PIG_POSES, WOLF_POSES

out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "assets", "characters")
os.makedirs(out, exist_ok=True)
pen = Pen(weight=3)          # the panel weights: 3 for outlines, 1.75 for details
M = 12                        # margin around each character

for kind in ("straw", "sticks", "bricks"):
    k = PIG_SIZE[kind]
    w, h = 190 * k + 2 * M, 290 * k + 2 * M
    for expr in ("happy", "scared", "teasing", "determined"):
        body = pig(pen, w / 2, h - M - 4 * k, kind, expr)
        open(os.path.join(out, f"{kind}-pig-{expr}.svg"), "w").write(pen.svg(body, round(w), round(h)))

for expr in ("grin", "toothy", "snarl", "roar", "huff"):
    left = 180 if expr == "huff" else 140      # the breath lines need room in front of the mouth
    w, h = left + 140 + 2 * M, 410 + 2 * M
    body = wolf(pen, M + left, h - M - 4, expr)
    open(os.path.join(out, f"wolf-{expr}.svg"), "w").write(pen.svg(body, round(w), round(h)))

# poses, each with the expression that suits it; framed generously because limbs reach out
poses_dir = os.path.join(out, "poses"); os.makedirs(poses_dir, exist_ok=True)
PIG_EXPR = {"stand": "happy", "run": "scared", "build": "happy", "tease": "teasing", "cheer": "happy"}
for kind in ("straw", "sticks", "bricks"):
    k = PIG_SIZE[kind]
    for pose in PIG_POSES:
        expr = "determined" if (kind == "bricks" and pose == "build") else PIG_EXPR[pose]
        w, h = 330 * k, 380 * k
        body = pig(pen, w / 2 + (20 * k if pose == "run" else 0), h - 36 * k, kind, expr, pose=pose)
        open(os.path.join(poses_dir, f"{kind}-pig-{pose}.svg"), "w").write(pen.svg(body, round(w), round(h)))
WOLF_EXPR = {"stand": "snarl", "sneak": "grin", "huff": "huff", "pounce": "roar", "knock": "grin", "climb": "grin", "hold": "grin"}
for pose in WOLF_POSES:
    if pose == "pounce":
        w, h, x0 = 620, 500, 290
    else:
        w, h, x0 = 470, 450, 240
    body = wolf(pen, x0, h - 16, WOLF_EXPR.get(pose, "grin"), pose=pose)
    open(os.path.join(poses_dir, f"wolf-{pose}.svg"), "w").write(pen.svg(body, w, h))

print(out)
