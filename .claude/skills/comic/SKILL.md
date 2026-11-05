---
name: comic
description: Turn a finished Three Little Pigs story into a one-page widescreen comic, published as a self-contained HTML file — the screenwriter agent plans the panels, then the panels are drawn in the project's monoline style, lettered, checked and published. Use this skill whenever the user asks to make, draw or illustrate a comic, a comic page or pictures of a story in this project, or types /comic, even if they only say "draw the last story".
---

**First rule:** never go outside this project folder (`3 Little Pigs - A`). Do not look at, read, copy, change or delete anything outside it. Put drafts and test renders in `tmp/` and delete them when you are done.

# Making a comic

This turns a story into a comic page and publishes it in the story's production folder, straight through with no review stop: the user wants a finished product, so make the judgement calls yourself and report what you did at the end. Two pieces do the work: the `screenwriter` agent plans the comic as a panel script, and the `monoline-art` skill draws it. Load the `monoline-art` skill before drawing; its "Comic pages" section and the worked example `outputs/2026-10-23-3-pigs-and-the-magic-bean/build/comic.py` show how a page is built.

## 1. Pick the story

Every story lives in its own production folder in `outputs/` (for example `outputs/2026-11-05-3-pigs-and-the-big-storm/`), with the story in `story.md`. Use the production the user names; otherwise use the newest folder in `outputs/` that has a `story.md` but no `comic.html` yet, or else simply the newest. If there are no stories yet, say so and suggest `/story` first. Everything this skill makes goes into that same folder: `screenplay.md` (the panel script), `build/comic.py` (the drawing script), `comic.html` (the comic) and `panels/` (each panel as its own image).

## 2. Get the panel script

Start the `screenwriter` agent. Give it the story file path (`<production>/story.md`) and the path to write the script to (`<production>/screenplay.md`), and ask it to follow its instructions. If the agent type is not available (for example, right after it was created, before Claude Code restarts), start a general-purpose agent and tell it to act exactly as described in `.claude/agents/screenwriter.md`.

When it replies, read the script and check it quickly yourself. Small panels hold little text, so join one speaker's consecutive bubbles in a panel into one bubble (same words). Since nobody else will review it, check that the panels follow the story in order, nobody jumps from place to place, the bubbles and captions are short, the last panel is the most dramatic shot on the page (usually an extreme close-up) carrying the cliffhanger and "To be continued...", and there are 8 to 12 panels in 2 or 3 rows. Fix small problems in the script yourself; send big ones back to the screenwriter once.

## 3. Plan the page

Give the script's rows and panel sizes to `plan_layout(...)` from `comic.py`, for example `plan_layout([["big", "square", "wide", "small"], ...], slants=..., top=96, margin=30, gutter=20)`. It searches for panel widths close to the wanted sizes that also pass `check_reading`: the page must read left to right, then top to bottom, with no gaps lining up between rows. Fitting four panels in every row is tight; if it finds nothing, move a panel to another row (the screenwriter's row split is a suggestion) or try another `seed`. Use 2 rows for up to about 8 panels and 3 rows for more, and mix upright and slanted dividers.

## 4. Draw the panels

Write `<production>/build/comic.py` following the worked example (it finds the toolkit from its own location, so copy its first lines as they are): one scene function per panel, in panel-local coordinates, using the cast (`cast.py`) and scenery (`scenery.py`). Follow the script's scene for each panel exactly: who is where, inside or outside, their pose and face. Letter with `caption`, `bubble` (tail pointing at the speaker) and `sfx` for every sound word, using the script's words as written. Place the words first and draw around them, so text never covers a face or the key action.

The screenwriter may ask for something the kit cannot draw yet: a close-up of a hand, a new prop, a new pose. Draw it in the panel script with the `mono.py` shapes, in the same style; if it is likely to come back in other stories (a new pose, a reusable prop), add it to `cast.py` or `scenery.py` instead.

## 5. Check and publish

Run the script, render the page and look at it (see "Working method" in the `monoline-art` skill for rendering, including the square-canvas trick on macOS). Check every panel: the action reads at a glance, characters and faces are big enough to see, text does not cover faces or action, bubble tails point at the right speaker, nothing important is cut by a slanted edge, and the reading order is clear. Fix and render again; two or three rounds are normal. If rendering is not possible on this machine, say so in the report.

The script ends by calling `publish(...)`, which writes `<production>/comic.html`, a single file with nothing external that opens in any browser, and `export_panels(...)`, which saves each panel to `<production>/panels/`. Then make the share file and rebuild the production page (the `production-page` skill), in this order, so the page mentions the share file: `python3 .claude/skills/production-page/scripts/build_page.py <production> --share`, then `python3 .claude/skills/production-page/scripts/build_page.py <production>`. The share file is a self-sufficient copy of the page named after the story (for example `the-three-pigs-and-the-magic-bean.html`), with the comic and panels packed inside. On macOS, open `index.html` for the user with `open`.

## 6. Report

Tell the user where the production page and the comic are, and tell them how to share it, in these words or close to them: "Want to share it? Send `<share file>` to your friends: it is a single file with the whole production inside, and it opens in any browser." Then say how many panels it has, and briefly what the screenwriter added beyond the story (in-between beats, close-ups, sound words). Mention anything you had to approximate. Delete the scratch files in `tmp/`.
