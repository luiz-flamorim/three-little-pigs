---
name: monoline-art
description: Draw art for the Three Little Pigs comic in the project's approved monoline style (one dark navy ink, thick outlines and thinner inside details, no fills or shading, clean geometry, one-point perspective), as SVG built with the bundled Python toolkit. Use this skill whenever drawing or changing anything visual for this project — a comic panel, a character (any pig or the Wolf), a pose or expression for the character sheet, a house, a prop, a background or the chaos element — and whenever the line weight, perspective or look of the art is being adjusted, even if the user does not say "monoline".
---

**First rule:** never go outside this project folder (`3 Little Pigs - A`). Do not look at, read, copy, change or delete anything outside it. Put drafts and test renders in `tmp/` and delete them when you are done. Before starting, read `CLAUDE.md` if it is not already in your context.

# Monoline art

This is the agreed art style for the comic. Look at `assets/reference-scene.png` before you draw: it is the approved test panel (the Wolf over the shoulder, the Straw Pig on the road, the straw house, the other two houses on the far hill). `scripts/example_scene.py` is the code that drew it, and it is the best worked example of everything below.

The style came from a reference picture the user chose: a potted plant drawn with one even dark navy line, rounded line ends, almond-shaped leaves with a single floating "vein" line inside, no fill and lots of white space. That picture is not kept in the repo, because it belongs to someone else; the description here is what matters.

## Why this style

Claude draws in code, so it is strongest with deliberate geometry and weakest with loose, painterly marks. Monoline plays to that strength, and because every shape is built from the same few primitives, a character drawn once can be redrawn identically in every panel, which is the hardest part of making a comic. Keep that in mind when you are tempted to add texture, shading or extra colour: those break the look and the consistency.

## The look

- **One ink, two weights.** Ink `#141b26` (dark navy) on white. Outlines — the silhouette of every character, house, tree and prop — use the main weight; details inside a shape (faces, belly icons, fur marks, ear veins, teeth, windows, thatch) use the thinner detail weight, so the characters read first and the details second. Nothing is filled except tiny dots (eyes, nostrils, the Wolf's nose).
- **Rounded ends and joins**, never sharp line caps.
- **Few lines.** Say a thing with the fewest lines that still read: a tree is a leaf shape on a stick, fur is three small chevrons, grass is a zigzag. One floating detail line inside a shape (like the leaf vein) is the signature touch: use it on trees and ears, sparingly elsewhere.
- **White space** is part of the drawing. Leave the sky mostly empty.

## Build everything from geometry

Work on a mental grid and construct shapes from circles, arcs, straight lines and the vesica (pointed leaf) shape. The helpers in `scripts/mono.py` exist for exactly this: `circle`, `vesica`, `polygon`, `on_arc` (to place things evenly along a curve), `chevron`, `lerp` and `toward`.

- Characters are built from circles and simple polygons: the pig is a body circle, a head circle, a snout ellipse and a hat; the Wolf is a big body arc, a head circle, a snout with a round tip and two triangular ears.
- Repeat measurements: equal spacing, matching angles, matching sizes. Disorder is what makes line art look amateur.
- Keep details clear of other lines. A detail that nearly touches an edge looks like a mistake; give it room or move it.

## Lines never cross

This was the user's main correction, so check it every time. Where one thing passes in front of another, the line behind must stop with a small clean gap, not run through.

- Draw back to front: sky, horizon and far things, road, middle ground, then the closest characters.
- Draw every solid object with `pen.shape(parts, details)`. It paints a white halo first, so lines behind it break cleanly, then one merged outline of all its parts. Put every part of one object (head, snout and ears; body and arm) in the same `shape` call so they merge into a single outline with no inner seams.
- Open lines that pass in front of others (a trunk over the horizon, a hat brim, claws) use `pen.line(d, halo=True)`.
- Limbs and tails that belong behind a body are drawn before the body with no halo, so the body covers their ends.
- Remove small lines that a character would hide, like the road dashes behind the pig.

## Perspective

The user wants real depth in every panel, not flat side views.

- Put the horizon at a fixed height and pick one vanishing point on it. Every receding edge — road edges, house sides, roof ridges, thatch, fences — runs exactly to that point: compute it with `toward(point, VP, t)` rather than guessing.
- Faces that look straight at the camera are true rectangles; only receding faces slant.
- Show depth with size, overlap and spacing: near things big and overlapping far things; repeated marks (road dashes, posts) get shorter and closer together with distance.
- Vary the camera across a page: over-the-shoulder, low angle, wide shot, close-up. The reference panel is an over-the-shoulder shot with the Wolf huge in the foreground and the pig small in the middle.
- Far objects keep the same line weights; make them simpler, not thinner.

## Line weight

There are two weights, both set on the pen: `Pen(weight=..., detail=...)`. The outline weight is 3 for a 600×420 panel (roughly the panel width divided by 200), and the detail weight defaults to about 58% of it (1.75). The user expects to tweak both for the comic.

- `pen.shape(...)` and `pen.line(...)` draw outlines; `pen.thin(...)` draws inside details. Pass details to `pen.shape(parts, details)` built with `pen.thin`.
- Keep the same two weights within a panel, and the same visual weights across the page: if a panel is drawn at a different size, scale them with it. When a group is drawn with `transform=scale(k)`, use `pen.scaled(k)` so its lines keep their on-page weight.
- `example_scene.py` takes `--weight` and `--detail` so you can try a change quickly: `python3 .claude/skills/monoline-art/scripts/example_scene.py tmp/test.svg --weight 4 --detail 2`.
- A heavier weight clogs small details (at 4.5 the pig's face and the round window fill in). When going heavier, simplify or enlarge small details instead of keeping them.
- The halo gap (`gap`, default 4) is separate from the weight; raise it a little if crossings look cramped at heavy weights.

## Characters

The cast is drawn by `scripts/cast.py`, so every panel uses the same designs. Use its functions instead of redrawing a character by hand: `pig(pen, x, y, kind, expr, scale, flip, pose)`, `pig_portrait(...)` for head close-ups, `wolf(pen, x, y, expr, scale, flip, pose)` and `wolf_portrait(...)`. `(x, y)` is the point between the feet (or the centre of the head for portraits); `flip=True` mirrors the character to face the other way. If a design changes, change it in `cast.py` so it changes everywhere.

- **The pigs** share one body: a round head with soft leaf-shaped ears (each with a vein), a snout ellipse with two nostril dots, dot eyes, a round body with short legs and arms, and hooves marked with one small line. Each wears its mark on the belly: a **wheat ear** for the Straw Pig, a **twig with a leaf** for the Sticks Pig, a **little brick wall** for the Bricks Pig. They differ slightly in size (straw smallest, bricks biggest). Expressions: `happy`, `scared`, `teasing`, `determined`.
- **The Wolf** stands on two legs (the stories need him talking and climbing): a torso with a pale belly patch, long limbs, clawed hands and feet, a bushy tail, and a head in 3/4 view facing left with tall ears, a long muzzle and a dot nose. The lower jaw swings open around a hinge, and the teeth are sized to fit the gap so they never cross the jaw. Expressions: `grin` (mouth closed, one fang showing), `toothy` (a wide closed smile with every tooth and two long fangs, made for close-ups and cliffhangers), `snarl` (teeth bared), `roar` (wide open, big fangs) and `huff` (cheek puffed, breath lines). The open mouth and fangs are his signature: make them clear.
- **Poses.** Pigs (facing right): `stand`, `run`, `build` (carrying their material: a straw sheaf, a tied bundle of sticks, a brick), `tease` (hands on hips) and `cheer` (jumping, arms up). The Wolf (facing left): `stand`, `sneak` (tiptoe, hands dangling), `huff` (leaning back, hands on hips), `knock` (fist raised, knock marks), `climb` (arms up, one knee raised) and `pounce` (flying leap, shadow on the ground). Mix any pose with any expression; `flip=True` turns a character around.
- **The rigs.** Poses are plain numbers in `PIG_POSES` and `WOLF_POSES`: limbs are chains of joints (shoulder, elbow, hand; hip, knee, ankle, toe), plus a body `tilt`, a `lift` off the ground and a `head` turn. To add a pose, copy the closest one and move the joints, then render and look. Limbs that pass behind the body are drawn first; the front arm is drawn last with a halo, so it reads as in front.
- The approved character sheet is `assets/character-sheet.png`, drawn by `scripts/character_sheet.py`. Every character in every expression is also saved on its own in `assets/characters/` (for example `wolf-roar.svg`, `bricks-pig-determined.svg`), made by `scripts/export_characters.py`; run that script again after changing a design in `cast.py`, so the folder always matches the code. Every pose is saved too, in `assets/characters/poses/` (for example `straw-pig-run.svg`, `wolf-pounce.svg`), and all poses are shown on `assets/poses-sheet.png`, drawn by `scripts/poses_sheet.py`.

## Comic pages

A finished story becomes **one widescreen page (16:9, 1920×1080)** holding the whole story, published as a single self-contained HTML file. `scripts/comic.py` makes the page; `scripts/scenery.py` has the houses (`haystack`, `box_house` for sticks and bricks), `brick_wall`, `tree`, `bush`, `cloud`, `beanstalk`, `bean` and `speed_lines`. For over-the-shoulder shots, `wolf_back(...)` in `cast.py` draws the Wolf from behind, as in the reference panel. `outputs/2026-10-23-3-pigs-and-the-magic-bean/build/comic.py` is the worked example: read it before making a new page.

- **Panels.** `layout(rows)` cuts the page into rows of panels with the same gap everywhere; `plan_layout(size_rows)` finds widths for wanted panel sizes that also pass the reading check. Mix the shapes: rectangles, squares, and slanted dividers that make parallelograms (two slanted dividers side by side) or trapezoids (one). About 6–8 panels fit a page.
- **Reading order comes first.** People read a comic left to right, then top to bottom, and the page must make that the only natural path. Keep panels in rows separated by an unbroken horizontal gap, and never let a gap between panels line up with a gap in the row above: when gaps align, the eye reads down the page as if it were in columns (this happened on the first page, and the user read it the wrong way). Stagger them by at least 150px. `check_reading(panels)` checks both the order and the staggering; run it after every `layout(...)` and do not publish a page that fails. Free-form layouts such as Voronoi cells were considered and set aside, because corners where three panels meet make the order ambiguous.
- **Panel script first.** Before drawing, decide for each panel which story parts it holds, what it shows and from what camera. Stage directions (the italic actions) are drawn, not written; only spoken words go in speech bubbles, and the Storyteller's lines go in caption boxes. The closing panel carries the cliffhanger and "To be continued...".
- **Scenes.** Each panel's scene is a function that draws in the panel's own coordinates (0,0 at its top-left) and is clipped to the panel's shape. Keep important things away from slanted edges, which cut corners off. Use the cast and scenery functions, give each panel its own horizon and vanishing point, and vary the camera across the page.
- **Lettering.** `caption(...)` and `bubble(..., tail)` wrap the text and return their height so the next item can sit below; point each bubble's tail at the speaker's mouth. `sfx(...)` draws hollow sound-effect letters ("WHOOSH!"). Leave room for the words when placing characters: text first, then art around it.
- **Weights.** On the 1920-wide page use `Pen(weight=4, detail=2.3)`; panel borders are drawn a little heavier.
- **Publish.** `page(...)` assembles the title, panels and borders; `publish(svg, title, summary, path)` writes the HTML; `export_panels(...)` saves each panel as its own SVG. A comic lives in its story's production folder in `outputs/`: `comic.html`, `panels/` and `build/comic.py`.

## Working method

1. Plan the panel before drawing: camera, horizon height, vanishing point, what is near, middle and far, and where each character stands so nothing collides.
2. Write a small Python script in `tmp/` that imports `mono.py` and builds the panel, following `example_scene.py`.
3. Render it and look at it. On macOS: `qlmanage -t -s 1200 -o tmp/ tmp/panel.svg`, then read the PNG. Quick Look fills a square thumbnail, so a wide or tall drawing comes out zoomed and cut off: place it inside a square SVG first, then crop the PNG. Elsewhere, open the SVG in a browser and take a screenshot.
4. Check the list below, fix, and render again. Expect two or three rounds; a first draft is never right.
5. Delete the scratch files in `tmp/` when the work is saved where it belongs.

## Check before you call it done

- No line crosses another; every overlap has a clean gap.
- Every receding edge meets the vanishing point.
- Outlines at the main weight, inside details at the detail weight, no fills except the small dots.
- Each character reads at a glance, with the expression the story needs.
- Nothing important touches the panel edge or another object by accident.
