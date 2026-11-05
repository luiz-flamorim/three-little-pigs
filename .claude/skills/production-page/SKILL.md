---
name: production-page
description: Build or rebuild the production page (index.html) of a Three Little Pigs production in outputs/ — the one clean page that presents a production's story, screenplay, panels, comic and files, from the project's shared template. Use this skill after a story or a comic is made, whenever the user asks to update, rebuild, share or redesign a production page, or asks for a single file to share a whole production.
---

**First rule:** never go outside this project folder (`3 Little Pigs - A`). Do not look at, read, copy, change or delete anything outside it. Put drafts and test renders in `tmp/` and delete them when you are done.

# The production page

Every story is a production: a folder in `outputs/` named `YYYY-MM-DD-3-pigs-and-<name>/` that holds everything made from it — `story.md`, `screenplay.md`, `comic.html`, `panels/` and `build/`. Its `index.html` presents the whole production on one page, the same way for every user. The page is filled from one template, `assets/template.html`, by `scripts/build_page.py`; never write a page by hand, because every production page must look the same.

`assets/example.html` is a finished page for the sample production, made self-sufficient (the comic and the panel images are packed inside it), so it opens anywhere. Open it in a browser to see what a complete page looks like. It is over 1 MB of drawings, so do not read it as text; read `assets/template.html` to understand the page's structure.

## Building it

```
python3 .claude/skills/production-page/scripts/build_page.py outputs/<production>
```

This writes `outputs/<production>/index.html`, linking to the files beside it. It shows whatever the production has so far: right after `/story` that is only the story, and the other sections say what is still to come; after `/comic` everything is there. Run it again whenever a step adds or changes something. On macOS, open the page for the user with `open`.

## Sharing

Every finished production gets a **share file**: a self-sufficient copy of the page, named after the story (for example `the-three-pigs-and-the-magic-bean.html`), with the comic and panel images packed inside, so it works on its own when sent by email or chat. Make it, then rebuild the page, so the page's "All files" section tells the reader which file to send:

```
python3 .claude/skills/production-page/scripts/build_page.py outputs/<production> --share
python3 .claude/skills/production-page/scripts/build_page.py outputs/<production>
```

`/comic` does this as its last step and tells the user, in plain words: "Want to share it? Send `<share file>` to your friends: it is a single file with the whole production inside, and it opens in any browser." In a shared copy, "All files" shows a short note instead of links, because the friend does not have the folder.

`--standalone OUT.html` writes the same self-sufficient page anywhere. That is how `assets/example.html` was made:

```
python3 .claude/skills/production-page/scripts/build_page.py outputs/2026-10-23-3-pigs-and-the-magic-bean --standalone .claude/skills/production-page/assets/example.html
```

## The design (agreed with the user)

The page was designed together with the user, step by step. Keep these choices when changing the template, and change the template rather than one page, so every production stays the same.

- **Look:** clean and minimal. A very light grey page (`#f9f9f8`) with white buttons and cards, dark navy ink (`#141b26`), and a Courier typewriter font, which gives the page a screenplay feel. The header (date, title, summary) is centred, with generous space above the title.
- **Units:** only `rem` and percentages, never pixels (1rem = 16px), so the page scales with the reader's font setting.
- **Menu:** the buttons sit in a menu that sticks to the top of the screen while scrolling, all the same width, centred, laid out with flexbox (not grid). The button of the section being read is highlighted, and so is the one just clicked while the page glides to it. Jumps scroll smoothly (instantly for readers who ask for reduced motion). A round back-to-top button appears once the reader scrolls down.
- **Order:** the sections follow the order things are made: the story, the screenplay, the panels, the comic, then all files. The menu buttons follow the same order.
- **Introductions:** each section opens with a fixed italic paragraph explaining that step (the story as a role-playing game with a die roll and chaos; the screenplay as a director planning shots; the panels drawn in code with puppet characters; the comic laid out to read in order). They are part of the template and never mention skills or agents.
- **Content:** the story shows each speaker's name before their line, with stage directions in italics; the screenplay is shown open, with no toggle; the panels are a grid of thumbnails, each opening on its own; the comic is shown in the page with a button to open it alone; all files appear as a folder tree whose folders open and close.
- **Phones:** below 37.5rem, the page keeps a 15% margin on each side, the buttons go two per row at equal width, and the title shrinks. The sticky menu still spans the full screen, with a −21.4286% margin (15% of the screen expressed against the 70%-wide content).

## Checking a change

After changing the template, rebuild the sample production's page and look at it: at full width, and at phone width by placing it in a 390px-wide `iframe` inside a test page in `tmp/`. On macOS, render with `qlmanage -t -s 1200 -o tmp/ <file>`; Quick Look cannot scroll, so to see a lower section, render a copy with the sections above it removed. Rebuild `assets/example.html` too, so the example matches the template, and delete the test files when done.
