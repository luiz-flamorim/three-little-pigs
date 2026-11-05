"""Draws the character sheet. Usage: python3 character_sheet.py OUTPUT.svg"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mono import Pen
from cast import pig, pig_portrait, wolf, wolf_portrait
pen = Pen(weight=6, detail=3.5)           # the 3 / 1.75 pair, doubled for a 1400-wide sheet
W, H = 1400, 1420
def label(x, y, t, size=24):
    return f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Helvetica Neue, Arial, sans-serif" font-size="{size}" fill="#141b26" letter-spacing="1">{t}</text>'
s = [label(700, 64, "THE THREE LITTLE PIGS — CHARACTER SHEET", 30)]
s += [pig(pen, 170, 560, "straw", "happy"), pig(pen, 430, 560, "sticks", "happy"), pig(pen, 690, 560, "bricks", "determined")]
s += [label(170, 610, "STRAW PIG"), label(430, 610, "STICKS PIG"), label(690, 610, "BRICKS PIG")]
s += [wolf(pen, 1110, 560, "snarl"), label(1110, 610, "THE WOLF")]
s.append(f'<path d="M60 680 H1340" stroke="#141b26" stroke-width="1.5" opacity="0.25"/>')
for i, (e, kind) in enumerate([("happy", "straw"), ("scared", "straw"), ("teasing", "sticks"), ("determined", "bricks")]):
    x = 200 + i * 330
    s += [pig_portrait(pen, x, 830, kind, e), label(x, 940, e.upper(), 20)]
s.append(f'<path d="M60 990 H1340" stroke="#141b26" stroke-width="1.5" opacity="0.25"/>')
for i, e in enumerate(["grin", "snarl", "roar", "huff"]):
    x = 270 + i * 330
    s += [wolf_portrait(pen, x, 1180, e, 1.15), label(x - 40, 1340, {"grin": "SLY GRIN", "snarl": "SNARL", "roar": "ROAR", "huff": "HUFF AND PUFF"}[e], 20)]
open(sys.argv[1] if len(sys.argv) > 1 else "character-sheet.svg", "w").write(pen.svg("".join(s), W, H))
