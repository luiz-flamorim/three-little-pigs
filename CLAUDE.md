# CLAUDE.md

## First instruction — stay inside this project folder

This applies to every session and every agent or subagent working in this project, and it takes priority over everything below.

- No session or agent may go outside this project's root folder (`3 Little Pigs - A`). That means never checking, listing, searching, reading, accessing, investigating, copying, moving, creating, updating, or deleting any file or folder outside it, by any tool or command, for any reason.
- Temporary, scratch, or test files (including logs, caches and build output) must be created only in the project's own `tmp/` folder (git-ignored), never in the system temp directory or anywhere else, and deleted once they have served their purpose.
- If a task seems to need something outside the project folder, stop and ask the user instead of reaching outside it.

## What this project is

This project is the final demonstration piece of a mentorship programme. Its purpose is to test and showcase how LLM-based agents interact with one another, each holding its own persona, inside a shared improvised story: a retelling of **The Three Little Pigs**. The next phase turns each finished story into a comic: the whole story on one widescreen (16:9) page with panels of mixed shapes, published as a self-contained HTML file (see `README.md`, "Next steps").

## Project goal — a story machine others can run

This project will be published as a public git repository, so anyone can download it and run their own Three Little Pigs stories in Claude Code, like a story machine. Build everything with that user in mind: it must work from a fresh clone, with no setup that only exists on the author's machine. Every story becomes a production: a folder in `outputs/` named by date and title (`outputs/YYYY-MM-DD-3-pigs-and-<name>/`) that holds everything made from it — `story.md`, `screenplay.md`, `comic.html`, `panels/`, `build/` — and an `index.html` page that presents the whole production with links to each output, built from one shared template by the `production-page` skill. A user's productions and their chaos record (`.claude/chaos-used.md`) are git-ignored and created on first use; the author's first production (`outputs/2026-10-23-3-pigs-and-the-magic-bean/`) is published as the sample and as the comic skill's worked example.

The characters are agents, but agents alone are not always the right tool. Whenever a piece of work would be better packaged as a Claude Code skill (for example, a repeatable procedure a user should be able to start with a slash command), stop and tell the user before building it another way. Explain briefly why a skill fits, and let the user decide. Do not create a skill without the user's go-ahead.

## Files and who reads them

- `CLAUDE.md` (this file) — for the main session: how to work on and run the project. Subagents never see it.
- `.claude/story-rules.md` — the rules of the story world. Every story agent reads it on its first turn; it is also imported below for the game runner.
- **Records** — `.claude/JOURNAL.md` (the log of design decisions) and `.claude/chaos-used.md` (the chaos elements already used) only grow, so nothing loads them by default, to save time and tokens. Read the journal only when you need the history behind a decision, and then only the part you need (search it, or read the latest entries). Only `turn.py` reads the chaos record; agents never do.
- `.claude/agents/` — one file per agent persona. `.claude/skills/` — the project skills. `.claude/tools/turn.py` — the story runner's helper.
- `outputs/` — one folder per production. `links/` — images used by `README.md`.

## Agents

The cast is defined in `.claude/agents/`, one markdown file per persona. Each file holds the agent's persona and, where relevant, its action and turn rules; edit the persona there rather than duplicating it here.

- **storyteller** (`storyteller.md`) — the game master, in the background. It opens the story, picks who acts next after each turn (usually with no text of its own), speaks only now and then to switch scenes or fold in chaos, closes on a cliffhanger, and writes a short summary.
- **pig-straw** (`pig-straw.md`) — the first pig; easygoing, lazy, quick to build and quick to panic.
- **pig-sticks** (`pig-sticks.md`) — the second pig; a bit lazy but slightly more careful than the first.
- **pig-bricks** (`pig-bricks.md`) — the third pig; patient, hard-working, builds a house that holds.
- **wolf** (`wolf.md`) — the Big Bad Wolf; hungry, theatrical and persistent, tries to talk, trick, or huff and puff his way into each house.
- **screenwriter** (`screenwriter.md`) — not part of the story; plans a finished story as a comic: breaks it into panels, adds the in-between beats and close-ups that make the action clear, adds sound words, keeps the text short, and writes a panel script for the `/comic` skill.
- **journal-keeper** (`journal-keeper.md`) — not part of the story; appends dated, plain-language entries to `.claude/JOURNAL.md` whenever a real project decision is made.

All three pigs share the same actions: run from the wolf when outside, try to build once and run to a brother's house if it fails, and tease the wolf once safely inside. On a turn, each character does one thing in one line of 125 characters or fewer, in words a 10-year-old can read, and goes along with what others add. Nobody adds new characters or magic things, except the one chaos element per story.

## Skills

Repeatable procedures live as project skills in `.claude/skills/`, so anyone who clones the repo gets them.

- **tell-me-a-story** (`.claude/skills/tell-me-a-story/`) — the one command for users: runs the `story` skill, then the `comic` skill, then opens the production page and explains how to share it. Use it whenever the user asks for a story ("tell me a story", or `/tell-me-a-story`), unless they ask for only one step.
- **story** (`.claude/skills/story/`) — runs a new story: the main session becomes the game runner, starts with the `storyteller` agent, calls the cast in turn, saves every part with `.claude/tools/turn.py`, rolls chaos, and prints the story live. Use it alone when the user wants only the story (or types `/story`). The full step-by-step procedure is in its `SKILL.md`.
- **comic** (`.claude/skills/comic/`) — turns a finished story into a one-page widescreen comic, straight through with no review stop: the `screenwriter` agent writes the panel script, the page is drawn with `monoline-art`, checked for reading order, and published as a self-contained HTML file in the story's production folder, whose page is then rebuilt. Use it whenever the user asks for a comic (or types `/comic`).
- **production-page** (`.claude/skills/production-page/`) — builds each production's `index.html` from one shared template: the page that presents a production's story, screenplay, panels, comic and files, with the design agreed with the user. `/story` and `/comic` use it; it can also make a self-sufficient single-file page to share a production. It holds the template and a finished example.
- **monoline-art** (`.claude/skills/monoline-art/`) — the approved comic art style: one dark navy line of a single, adjustable weight, built from geometry, with one-point perspective and no crossing lines. Use it for any drawing for the comic. It holds the rules, the drawing toolkit (`scripts/mono.py`), and the approved reference panel.

## Conventions

- **Keep texts short.** Anything written for readers of the repo (README, page copy, docs) stays short: bullet lists over long paragraphs, one or two sentences per point.
- **Markdown is human readable.** Every `.md` file is written in complete, continuous strings per paragraph, with no mid-paragraph hard line breaks; let lines soft-wrap in the editor. Paragraphs, headings and list items are still separated by blank lines as normal Markdown.
- **Agent and skill files.** Subagents do not inherit this file, so every agent file and skill must open with the project boundary rule, and every story agent must be told to read `.claude/story-rules.md` on its first turn. Write agent files in short, simple language.
- **Record decisions.** When a meaningful decision is made (a new rule, agent, mechanic, skill or scope change), append a short entry (one or two sentences) to `.claude/JOURNAL.md` in the journal-keeper's format, without reading the whole file, and keep `README.md`, `.claude/story-rules.md` and this file in sync with the change.

## Imported context

@.claude/story-rules.md
