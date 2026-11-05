"""Draws the comic for this production from its screenplay (../screenplay.md) with the monoline-art skill.
Writes ../comic.html and ../panels/. Run it from anywhere: python3 <production>/build/comic.py
"""
import math, os, sys
PRODUCTION = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(PRODUCTION))
sys.path.insert(0, os.path.join(ROOT, ".claude", "skills", "monoline-art", "scripts"))
from mono import Pen, circle, leaf, capsule, ellipse
from cast import pig, pig_portrait, wolf, wolf_back, wolf_portrait
from scenery import haystack, box_house, tree, cloud, beanstalk, bean, brick_wall, speed_lines
from comic import plan_layout, bubble, caption, sfx, page, publish, export_panels

pen = Pen(weight=3.4, detail=2)
TITLE = "The Three Pigs and the Magic Bean"
SUMMARY = ("Three pigs built houses of hay, sticks and bricks. Straw Pig threw a magic bean at the wolf, and a giant beanstalk grew. "
           "The wolf climbed it, Straw ran to the brick house, and now the wolf sees Sticks Pig all alone.")
panels, _ = plan_layout([["big", "square", "wide", "small"], ["wide", "square", "small", "tall"], ["tall", "wide", "square", "big"]],
                        slants=[[0, 0, 0], [0, 50, 50], [50, 50, 0]], top=96, margin=30, gutter=20, seed=3)
B = lambda text, x, y, w, tail: bubble(pen, text, x, y, w, tail, size=17)
C = lambda text, x, y, w: caption(pen, text, x, y, w, size=16)
ground = lambda w, y: pen.line(f"M0 {y} H{w}")
rot = lambda svg, a, cx, cy: f'<g transform="rotate({a} {cx} {cy})">{svg}</g>'


def p1(p):   # the three pigs set off; eyes in the trees
    w, h = p.w, p.h
    a = pen.line(f"M0 150 H{w}") + pen.line(f"M150 {h} L282 150 M330 {h} L294 150")
    a += tree(pen, 48, 250, 170) + tree(pen, 108, 210, 104)
    a += f'<ellipse cx="48" cy="150" rx="17" ry="10" fill="{pen.paper}"/>' + pen.thin("M34 150 Q40 145 46 150 Q40 153 34 150 Z M50 150 Q56 145 62 150 Q56 153 50 150 Z") + pen.dots((40, 149.5, 1.6), (56, 149.5, 1.6))
    a += pig(pen, 280, 205, "bricks", "happy", 0.17) + pig(pen, 258, 242, "sticks", "happy", 0.22) + pig(pen, 236, 290, "straw", "happy", 0.28)
    t, _ = C("Once upon a time, three little pigs left home with big dreams...", 16, 16, w - 32)
    return a, t


def p2(p):   # Straw flops on his hay heap
    w, h = p.w, p.h
    a = ground(w, 290) + haystack(pen, 110, 290, 210)
    a += rot(pig(pen, 214, 150, "straw", "happy", 0.27, pose="cheer"), -82, 214, 128)
    a += pen.thin("M150 112 l-10 -12 M170 100 l-2 -14 M262 106 l10 -12 M282 118 l14 -6")
    b, _ = B("Done! Best house ever, and it took five minutes!", 14, 14, 196, (150, 128))
    return a, b + sfx("FLOMP!", 320, 70, 40, -10, pen)


def p3(p):   # Sticks ties his sticks; Bricks lays bricks
    w, h = p.w, p.h
    a = ground(w, 288) + tree(pen, 40, 288, 150)
    a += pig(pen, 200, 270, "sticks", "scared", 0.3, pose="build")
    a += brick_wall(pen, 560, 288, 120, rows=3, row_h=15) + pig(pen, 480, 300, "bricks", "determined", 0.36, pose="build")
    b1, _ = B("Good enough! A wolf can't blow through string… right?", 70, 14, 230, (200, 170))
    b2, _ = B("Slow and steady, brothers. A wolf can blow on hay, but not on bricks!", 360, 14, 300, (478, 186))
    return a, b1 + b2 + sfx("CLINK!", 640, 200, 32, -8, pen)


def p4(p):   # close-up: the Wolf's eyes in the leaves
    w, h = p.w, p.h
    a = ""
    for (x, y, L, ang) in [(30, 150, 90, -60), (190, 160, 100, -120), (60, 280, 110, -30), (170, 285, 100, -150),
                           (110, 120, 80, -90), (20, 220, 80, 20), (205, 230, 80, 160), (110, 300, 70, -90)]:
        a += pen.shape([leaf(x, y, L, L * 0.42, ang)], pen.thin(f"M{x - math.cos(math.radians(ang)) * L * 0.3:.1f} {y - math.sin(math.radians(ang)) * L * 0.3:.1f} L{x + math.cos(math.radians(ang)) * L * 0.3:.1f} {y + math.sin(math.radians(ang)) * L * 0.3:.1f}"))
    a += f'<ellipse cx="108" cy="208" rx="62" ry="30" fill="{pen.paper}"/>'
    a += pen.thin("M70 208 Q84 196 98 208 Q84 214 70 208 Z M118 208 Q132 196 146 208 Q132 214 118 208 Z M68 194 L96 202 M148 194 L120 202")
    a += pen.dots((85, 207, 3.4), (131, 207, 3.4))
    t, _ = C("In the trees, a pair of yellow eyes watched the hay house...", 12, 12, w - 24)
    return a, t + sfx("GRRRUMBLE...", 108, 280, 22, 0, pen)


def p5(p):   # the Wolf creeps up to the shut door
    w, h = p.w, p.h
    a = ground(w, 285) + haystack(pen, 470, 285, 210) + tree(pen, 60, 285, 140)
    a += wolf(pen, 300, 300, "grin", 0.36, flip=True, pose="sneak")
    a += pen.thin("M402 170 q8 -6 16 0 t16 0 M404 184 q8 -6 16 0 t16 0")
    b, _ = B("Little pig, little pig, your house smells like lunch! Let me in!", 40, 14, 300, (310, 152))
    return a, b + sfx("SNIFF SNIFF", 560, 70, 26, -6, pen)


def p6(p):   # Straw leans out of the window and flings the bean over the Wolf's head
    w, h = p.w, p.h
    a = haystack(pen, -90, 470, 520)
    a += pen.shape([circle(165, 200, 62)])
    a += pig_portrait(pen, 165, 212, "straw", "teasing", 0.68)
    a += pen.shape([capsule((206, 232), (238, 186), 10)], pen.thin("M242 180 l5 -6"))
    a += bean(pen, 282, 120, 16, -30) + pen.thin("M250 172 q10 -24 22 -34") + speed_lines(pen, 252, 150, 22, 9, 2, -55)
    a += wolf_back(pen, 360, 372, 0.9)
    b, _ = B("Not by the hair of my chinny-chin-chin! Go climb that, Wolfy!", 14, 14, 200, (150, 170))
    return a, b + sfx("FLICK!", 300, 62, 32, -14, pen)


def p7(p):   # close-up: the bean lands
    w, h = p.w, p.h
    a = haystack(pen, -330, 230, 420) + ground(w, 230)
    a += pen.thin("M120 250 l4 -8 l4 8 M250 262 l4 -8 l4 8 M300 246 l4 -8 l4 8 M90 266 h4 M180 258 h4 M230 272 h4")
    a += bean(pen, 200, 214, 18, -15, sparkle=False)
    a += pen.thin(circle(160, 222, 7) + circle(244, 220, 6) + circle(176, 206, 4))
    a += pen.thin("M200 186 V170 M176 192 L166 180 M224 192 L234 180 M160 206 L146 202 M240 206 L254 202")
    t, _ = C("The bean hit the ground and...", 64, 14, 240)
    return a, t + sfx("THUNK!", 230, 140, 40, -10, pen)


def p8(p):   # the beanstalk shoots up; the Wolf stares
    w, h = p.w, p.h
    a = ground(w, 288) + haystack(pen, 20, 288, 150) + cloud(pen, 270, 110, 120)
    a += beanstalk(pen, [(210, 300), (196, 230), (222, 160), (200, 90), (224, 20), (210, -40)], 34, 8)
    a += speed_lines(pen, 254, 230, 40, 12, 3, -90) + speed_lines(pen, 166, 250, 40, 12, 3, -90)
    a += wolf(pen, 360, 296, "roar", 0.26, pose="stand")
    t, _ = C("...a giant green beanstalk shot up, all the way to the clouds!", 60, 14, w - 76)
    return a, t + sfx("WHOOSH!", 300, 215, 34, -70, pen)


def p9(p):   # the Wolf climbs
    w, h = p.w, p.h
    a = haystack(pen, -20, 340, 140) + cloud(pen, 160, 160, 100)
    a += beanstalk(pen, [(80, 340), (110, 270), (150, 200), (190, 130), (230, 60), (270, -20)], 34, 8)
    a += wolf(pen, 150, 300, "grin", 0.4, pose="climb")
    b, _ = B("Thanks, piggy! Now I can jump down right on top of your hay roof!", 12, 12, 240, (120, 150))
    return a, b + sfx("SCRITCH SCRATCH", 196, 236, 16, -58, pen)


def p10(p):  # Straw bolts for the brick house while the Wolf is still climbing
    w, h = p.w, p.h
    a = ground(w, 286) + haystack(pen, 60, 286, 150)
    a += beanstalk(pen, [(230, 296), (214, 220), (240, 150), (220, 80), (244, 10), (230, -40)], 30, 7)
    a += wolf(pen, 236, 150, "grin", 0.2, pose="climb")
    a += box_house(pen, "bricks", 520, 286, 100, (330, 160))
    a += pig(pen, 400, 296, "straw", "scared", 0.32, pose="run")
    b, _ = B("Oh no, oh no! Brother Bricks, open up! The wolf is coming down from the sky!", 300, 14, 320, (404, 196))
    return a, b + sfx("EEEEK!", 330, 160, 30, -12, pen)


def p11(p):  # Bricks pulls Straw in; the door slams
    w, h = p.w, p.h
    tex = ""
    for r in range(1, 14):
        y = 300 - r * 20
        tex += f"M0 {y} H{w} "
        off = 10 if r % 2 else 30
        for x in range(off, int(w), 40):
            if not (126 < x < 254):
                tex += f"M{x} {y} V{y + 20} "
    a = pen.thin(tex)
    a += f'<path d="M126 300 V120 H254 V300 Z" fill="{pen.paper}" stroke="{pen.ink}" stroke-width="{pen.w}" stroke-linejoin="round"/>'
    a += pig(pen, 214, 300, "bricks", "determined", 0.42, flip=True)
    a += rot(pig(pen, 170, 300, "straw", "scared", 0.34, pose="run"), -24, 170, 260)
    a += pen.shape([f"M254 120 L300 104 L300 316 L254 300 Z"], pen.thin("M266 214 v16"))
    a += speed_lines(pen, 310, 140, 34, 14, 3, 0)
    b, _ = B("Jump all you like, Wolfy! Bricks don't care how high you climb!", 60, 12, 260, (210, 120))
    return a, b + sfx("SLAM!", 300, 292, 30, -10, pen)


def p12(p):  # cliffhanger: extreme close-up of the Wolf's toothy smile
    w, h = p.w, p.h
    a = wolf_portrait(pen, 560, 196, "toothy", 4.4)
    t, _ = C("The pigs cheered. But up on the beanstalk, the wolf smiled. He could see the stick house, and Sticks Pig was all alone...", 16, 14, 330)
    c2, _ = caption(pen, "To be continued...", w - 236, 14, 220, size=18)
    return a, t + c2


scenes = {i + 1: f for i, f in enumerate([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12])}
svg = page(pen, panels, scenes, TITLE)
print(publish(svg, TITLE, SUMMARY, os.path.join(PRODUCTION, "comic.html")))
export_panels(pen, panels, scenes, os.path.join(PRODUCTION, "panels"))
