"""Draws the poses sheet. Usage: python3 poses_sheet.py OUTPUT.svg"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mono import Pen
from cast import pig, wolf

pen = Pen(weight=6, detail=3.5)           # the 3 / 1.75 pair, doubled for a 1460-wide sheet
W, H = 1460, 1460
L = lambda x, y, t, size=20: (f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Helvetica Neue, Arial, sans-serif" '
                              f'font-size="{size}" fill="#141b26" letter-spacing="1">{t}</text>')
s = [L(730, 64, "THE THREE LITTLE PIGS — POSES", 30)]
row = [("stand", "straw", "happy"), ("run", "straw", "scared"), ("build", "straw", "happy"), ("tease", "sticks", "teasing"),
       ("cheer", "sticks", "happy"), ("build", "sticks", "happy"), ("build", "bricks", "determined")]
for i, (pose, kind, expr) in enumerate(row):
    x = 120 + i * 200
    s += [pig(pen, x, 400, kind, expr, 0.8, pose=pose), L(x, 440, f"{kind.upper()} · {pose.upper()}")]
s.append('<path d="M60 490 H1400" stroke="#141b26" stroke-width="1.5" opacity="0.25"/>')
for i, (pose, expr) in enumerate([("stand", "snarl"), ("sneak", "grin"), ("huff", "huff"), ("knock", "grin")]):
    x = 230 + i * 340
    s += [wolf(pen, x, 920, expr, 0.85, pose=pose), L(x, 965, pose.upper())]
s += [wolf(pen, 700, 1380, "roar", 0.85, pose="pounce"), L(700, 1425, "POUNCE")]
open(sys.argv[1] if len(sys.argv) > 1 else "poses-sheet.svg", "w").write(pen.svg("".join(s), W, H))
