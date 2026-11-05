# 3 Little Pigs & 1 AI

A story machine for The Three Little Pigs, built with Claude Code. AI agents improvise a new chapter of the fable, it is turned into a comic, and everything lands on one page you can open in any browser or send to a friend.

Final piece of a mentorship programme, built to show how LLM agents with their own personas interact in a shared story.

<p align="center"><img src="links/production-page.png" width="100%" alt="The production page of The Three Pigs and the Magic Bean"></p>

## Quick start

You need [Claude Code](https://claude.com/claude-code) and Python 3.

1. Open Claude Code in this folder.
2. Type `/tell-me-a-story` (or just ask: "tell me a story").
3. Watch the agents improvise, then get the comic and its page.

To share, send the file named after the story (e.g. `the-three-pigs-and-the-magic-bean.html`): one file, everything inside.

Try the sample first: `outputs/2026-10-23-3-pigs-and-the-magic-bean/index.html`.

## How it works

<p align="center"><img src="links/workflow.svg" width="100%" alt="How it works: story, screenplay, panels, comic, then the page and share file; chaos may affect the story"></p>

1. **Story:** the agents improvise it like a role-playing game.
2. **Screenplay:** the screenwriter plans it as comic panels.
3. **Panels:** each panel is drawn in code, in one fixed style.
4. **Comic:** the panels are laid out on one widescreen page.

Each story becomes a **production**: a folder in `outputs/` with everything made from it, and a page that shows it all.

<details>
<summary><b>The agents</b></summary>

- **Storyteller** — the game master. Sets the scene, picks who acts next, closes on a cliffhanger.
- **Straw Pig** — easygoing and lazy. Builds fast, panics fast.
- **Sticks Pig** — a little lazy, a little careful.
- **Bricks Pig** — patient and hard-working. His house holds.
- **Wolf** — hungry, sly and theatrical. Tricks, huffs and puffs.
- **Screenwriter** — plans the finished story as a comic, shot by shot.
- **Journal Keeper** — not in the story. Logs the project's decisions.

Every turn is one short line, in words a 10-year-old can read. Everyone follows the improv rule "yes, and": accept what others bring in, and build on it.

</details>

<details>
<summary><b>Chaos</b></summary>

- After every turn, a real die is rolled.
- On a 1, chaos strikes the next player (up to 3 times per story).
- The first chaos brings in one thing from another tale, like Jack's magic bean.
- Later chaos is a twist: something already in the story used in a surprising way.
- A record keeps chaos fresh, so the same thing is not used twice.

</details>

<details>
<summary><b>The skills</b></summary>

- **`/tell-me-a-story`** — the one command: story, comic, page and share file, start to finish.
- **`/story`** — runs a new story: calls the agents in turn, saves each line, rolls the die.
- **`/comic`** — turns an existing story into a comic: screenplay, layout, drawing, publishing.
- **`monoline-art`** — the art style and the tools to draw it: the cast, scenery and page layout.
- **`production-page`** — builds each production's page and share file from one template.

</details>

<details>
<summary><b>The characters</b></summary>

Every character is a reusable drawing, so they look the same in every panel and every story. Each pig wears its mark on the belly: a wheat ear, a twig, a little brick wall.

<table>
  <tr>
    <td width="50%"><img src=".claude/skills/monoline-art/assets/character-sheet.png" alt="The character sheet"></td>
    <td width="50%"><img src=".claude/skills/monoline-art/assets/poses-sheet.png" alt="The poses sheet"></td>
  </tr>
  <tr>
    <td align="center">The cast and their expressions</td>
    <td align="center">Their poses</td>
  </tr>
</table>

</details>

## The comic

<p align="center"><img src="links/first-comic.png" width="100%" alt="The comic of The Three Pigs and the Magic Bean"></p>

- One widescreen page, 8 to 12 panels.
- Rectangles, squares and slanted panels, read left to right, top to bottom.
- Saved as a single HTML file.

## Files

```
outputs/                 # Your productions
.claude/
├── agents/              # The agents.
├── skills/              # The skills.
├── story-rules.md       # Rules of the story world.
├── tools/
│   └── turn.py          # Story mechanics: saves turns and rolls the die.
└── JOURNAL.md           # Every design decision, and why.
CLAUDE.md                # What Claude Code reads first.
links/                   # README images.
```

## Making of

<details>
<summary>How the art was found (click to open)</summary>

<br>

1. **Styles.** One test scene was drawn in many styles: gothic, surreal, paper puppets, ballpoint, rubber hose, 2.5D. Lesson: Claude draws best with clean geometry.
2. **Monoline.** One even line, inspired by a simple drawing. Rebuilt on a grid, with one vanishing point and no crossing lines.
3. **Two line weights.** Thick outlines, thin details: easier to read.
4. **The cast.** Reusable characters, each pig with a belly icon. Limbs became joints, so poses are just numbers.
5. **First comic.** Its panels read as columns, so a reading-order check was added. Some actions made no sense once drawn.
6. **Screenwriter.** Plans the in-between moments, close-ups and sound words, and ends on the most dramatic shot.
7. **Productions.** One folder and one page per story, designed step by step, plus a share file.

<table>
  <tr>
    <td width="50%"><img src="links/test-panel-one-weight.png" alt="The test panel with one line weight"></td>
    <td width="50%"><img src=".claude/skills/monoline-art/assets/reference-scene.png" alt="The test panel with two line weights"></td>
  </tr>
  <tr>
    <td align="center">One line weight</td>
    <td align="center">Two line weights</td>
  </tr>
</table>

</details>

## Status

Working and still being refined. Not yet run end to end (`/story` then `/comic`) in a fresh session.

Known limits:
- The comic font (Chalkboard SE) comes with macOS; other systems use a similar font.
- The drawing self-check needs macOS; elsewhere the comic is made without it.
- New things (a fallen house, an inside view) are drawn on the spot and may look rougher.
- Stories don't yet continue from the last cliffhanger.

## Next steps

- Run `/story` and `/comic` end to end in a fresh session.
- Embed a free font in the comic.
- Connect chapters through their cliffhangers.
- Grow the art kit.

## License

Use, change and share it, as long as you credit "3 Little Pigs & 1 AI" by Luiz Amorim and Lamine Sillah with a link to [this repository](https://github.com/luiz-flamorim/three-little-pigs). Code: MIT. Everything else: CC BY 4.0. See `LICENSE`.
