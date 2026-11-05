"""The approved reference panel: the Wolf over-the-shoulder, the Straw Pig on the road, the straw house.

Usage: python3 example_scene.py OUTPUT.svg [--weight 3] [--detail 1.75]
Read it as a worked example of the rules in SKILL.md, not as something to copy panel by panel.
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mono import Pen, circle, vesica, lerp, toward, polygon, on_arc, chevron, pt

out = sys.argv[1] if len(sys.argv) > 1 else "scene.svg"
weight = float(sys.argv[sys.argv.index("--weight") + 1]) if "--weight" in sys.argv else 3.0
detail = float(sys.argv[sys.argv.index("--detail") + 1]) if "--detail" in sys.argv else None
pen = Pen(weight=weight, detail=detail)
VP = (354, 204)          # one vanishing point, on the horizon, just right of centre
s = []

# 1. sky (furthest back): sun, cloud as merged circles with a flat base, birds
s.append(pen.line(circle(96, 84, 18)))
s.append(pen.line(" ".join(f"M{pt(on_arc(96, 84, 26, a))} L{pt(on_arc(96, 84, 34, a))}" for a in range(0, 360, 45))))
s.append(pen.shape([circle(240, 96, 12), circle(262, 88, 16), circle(284, 96, 12)])
         + f'<rect x="220" y="101.5" width="90" height="20" fill="{pen.paper}"/>' + pen.line("M228.7 100 H295.3"))
s.append(pen.line("M384 96 a6 6 0 0 1 12 0 a6 6 0 0 1 12 0 M420 114 a4 4 0 0 1 8 0 a4 4 0 0 1 8 0"))

# 2. far: horizon, hill, the other two houses (tiny = far away)
s.append(pen.line("M24 204 H348 M360 204 H378 M570 204 H582"))
s.append(pen.line("M378 204 A120 120 0 0 1 570 204"))
s.append(pen.shape(["M412 170 V154 H428 V170 Z", "M408 156 L420 144 L432 156 Z"]))
s.append(pen.shape(["M546 186 V176 H558 V186 Z", "M543 177 L552 169 L561 177 Z", "M555 172 V164 H559 V176 Z"]))

# 3. road: both edges run to the vanishing point; dashes shrink with distance and hide behind the pig
s.append(pen.line("M240 420 L348 204 M468 420 L360 204"))
s.append(pen.line("M354 414 V400 M354 290 V282 M354 272 V266 M354 259 V255 M354 249 V246"))

# 4. middle: leaf trees (vesica + one floating vein), grass
for x, top, bot, r, trunk in [(60, 222, 306, 63, 354), (102, 240, 282, 31.5, 306)]:
    s.append(pen.line(f"M{x} {bot} V{trunk}", halo=True))
    vein = f"M{x - 3} {bot - (bot - top) * 0.18:.0f} Q{x - 6} {(top + bot) / 2:.0f} {x - 3} {top + (bot - top) * 0.3:.0f}"
    s.append(pen.shape([vesica(x, top, bot, r)], pen.thin(vein)))
s.append(pen.line("M78 372 l4 -8 l4 8 l4 -8 l4 8 M196 396 l4 -8 l4 8 l4 -8 l4 8"))

# 5. the straw house: front is a true rectangle facing us; side, roof ridge and thatch go to the VP
t = 0.3
FL, FR, TR, APEX, TL = (132, 360), (216, 360), (216, 276), (174, 234), (132, 276)
SB, ST, RIDGE = toward(FR, VP, t), toward(TR, VP, t), toward(APEX, VP, t)
front, side, roof = polygon(FL, FR, TR, APEX, TL), polygon(FR, SB, ST, TR), polygon(TR, APEX, RIDGE, ST)
thatch = ""
for k in (0.3, 0.55, 0.8):
    r0, e0 = lerp(APEX, RIDGE, k), lerp(TR, ST, k)
    thatch += f"M{pt(lerp(r0, e0, 0.22))} L{pt(lerp(r0, e0, 0.72))} "
det = pen.thin(f"M{pt(TR)} V360 M{pt(TR)} L{pt(ST)} M132 276 H216 M143 276 L174 245 L205 276")
det += pen.thin(thatch) + pen.thin(circle(174, 264, 7) + " M174 257 V271 M167 264 H181")
det += pen.thin("M162 360 V338 A12 12 0 0 1 186 338 V360 M147 300 V320 M201 300 V320")
s.append(pen.shape([front, side, roof], det))
s.append(pen.line("M102 360 H124"))

# 6. the Straw Pig: circles; limbs and tail behind the body; hat in front of the head
s.append(pen.line("M306 364 a5 5 0 1 1 -2 -8 M316 370 V386 M332 370 V386 M312 350 L296 334 M336 350 L352 334"))
s.append(pen.shape([circle(324, 358, 18)]))
s.append(pen.shape([circle(324, 326, 17)]))
s.append(pen.shape(["M318.5 333 a5.5 4 0 1 0 11 0 a5.5 4 0 1 0 -11 0 Z"]) + pen.dots((321.5, 333, 1.2), (326.5, 333, 1.2)))
s.append(pen.dots((317.5, 326, 1.9), (330.5, 326, 1.9)) + pen.thin("M312 321 L318 318 M336 321 L330 318"))
s.append(pen.shape(["M313 312 A11 11 0 0 1 335 312 Z"], pen.line("M303 312 H345", halo=True)))

# 7. the Wolf (closest): body + arm merged; head + snout + ears merged
body = "M432 426 V384 A96 96 0 0 1 624 384 V426 Z"
arm = "M452 328 L398 322 A11 11 0 0 0 398 344 L456 352 Z"
fur = "".join(chevron(*on_arc(528, 384, 60, a)) + " " for a in (125, 90, 55))
s.append(pen.shape([body, arm], pen.thin(fur) + pen.line("M389 327 L377 321 M386 333 L373 333 M389 340 L377 346", halo=True)))
head, snout = circle(510, 258, 34), "M492 236 L432 250 A11 11 0 0 0 434 272 L494 274 Z"
ears = ["M486 234 L488 196 L508 226 Z", "M514 226 L536 196 L536 234 Z"]
wd = pen.thin("M440 264 L486 266 M449 264.5 L452.5 270 L456 265") + pen.thin("M496 226 L492 210 M527 226 L532 210")
wd += pen.thin("M491 245 Q498 239 505 245 Q498 249 491 245 Z") + pen.dots((498, 244.6, 1.8), (428, 256, 5))
s.append(pen.shape([head, snout] + ears, wd))

open(out, "w").write(pen.svg("".join(s)))
print(out)
