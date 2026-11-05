---
name: story
description: Run a new improvised Three Little Pigs story with the project's agent cast (Storyteller, Straw Pig, Sticks Pig, Bricks Pig, Wolf), acting as the game runner — calling each agent in turn, saving every part with turn.py, rolling chaos, and printing the story live. Use this skill whenever the user asks to start, tell, run, play or generate a story, a new chapter or a new episode in this project, even if they just say "let's go" or "another one".
---

**First rule:** never go outside this project folder (`3 Little Pigs - A`). Do not look at, read, copy, change or delete anything outside it. Put temporary files in `tmp/` and delete them when you are done. The rules in `.claude/story-rules.md` apply to every story.

# Running a story

You are the game runner. You never write story content yourself: you call the agents, save their turns, and show them to the user. The agents are defined in `.claude/agents/`, and `.claude/tools/turn.py` does the mechanical steps (making the file, checking length, saving, rolling chaos). Run every command from the project root, because `turn.py` uses paths relative to it.

The story is improvised by the agents, so the quality depends on them getting the right context at the right time. Most of the steps below exist because an earlier test story went wrong without them; `.claude/JOURNAL.md` records which.

## 1. Open the story

Start the `storyteller` agent and ask for its opening (there is no chaos roll before the opening). It replies with a `Title:` line, one scene-setting line and a `Next:` line. Create the story file with the title:

```
python3 .claude/tools/turn.py new "The Three Pigs and the <Something>"
```

This creates the story's production folder, `outputs/YYYY-MM-DD-3-pigs-and-<name>/`, named by today's date and the title, with the story in `story.md`. It prints the story file's path, then the final title. Every folder of one production holds everything made from that story (later, the comic too). If a story with the same name already exists, `turn.py` makes this one Part II, Part III and so on, in both the folder name and the title; use the title it prints. The Storyteller's title should read "The Three Pigs and the <something>"; if it does not, ask it once for a title in that form before creating the folder. Save the opening line as the first part (step 2).

## 2. Save each turn

Pipe the turn text into `turn.py add`:

```
printf '%s' "<turn text>" | python3 .claude/tools/turn.py add <file> "<Speaker>"
```

It removes the `Next:` line, checks the length (125 characters for everyone, 255 for the Summary), saves the part as `**Speaker:** text`, prints the part number, and rolls the chaos die for the next turn. Speaker names are exactly: Storyteller, Straw Pig, Sticks Pig, Bricks Pig, Wolf, Summary.

- If it says `TOO LONG`, nothing was saved: send the turn back to the same agent to shorten, then save the new version.
- When the Storyteller replies with only a `Next:` line, save nothing. That is its normal background move.

## 3. Show it live

After each saved part, print it in the terminal in the same `**Speaker:** text` format, followed by the chaos result for the next turn, so the user can follow the story as it happens.

## 4. Chaos

Only call the next agent after `add` has printed its chaos line, because that line decides what the next player is told.

- Chaos always goes to the next player, never the Storyteller. If the Storyteller acts next, carry the chaos over to the player it names.
- `CHAOS new element`: add this to that player's message: `CHAOS: new element. Bring in one character or object from another story. Avoid: <the list it printed>`
- `CHAOS twist`: add this: `CHAOS: twist. Add nothing new; use <what it printed> or something else already in the story in a surprising, clever way.`
- When saving that player's turn, add `--chaos "<short description>"` to the `add` command, so the element or twist is recorded in `.claude/chaos-used.md` before the next roll. That file is each user's own record (git-ignored); `turn.py` creates it on first use.
- The script stops rolling after 3 chaos events per story, and only the first event may bring in something new.

## 5. Call the next agent

Follow the Storyteller's `Next:` line. A player does one thing, then control goes back to the Storyteller.

- Start each agent once. Its first turn reads the story rules and the story file. After that, continue it with SendMessage instead of starting a new one.
- In every later message, paste the parts saved since that agent last acted, and tell it not to read any files or use any tools. Rereading files made agents slow (one Storyteller turn took 3.5 minutes).
- Tell the Storyteller which part it is on, out of 12, which players have not acted yet, and how many times it has spoken in the middle of the story (it should speak only about twice).

## 6. Finish

- When the Storyteller writes `Next: END`, its closing line with the cliffhanger is the last part.
- If part 11 is reached first, ask the Storyteller to close the story in part 12.
- Then ask the Storyteller for the summary paragraph (start, middle, ending and cliffhanger, up to 255 characters) and save it with the speaker `Summary`.
- Build the production page (the `production-page` skill) with `python3 .claude/skills/production-page/scripts/build_page.py <production folder>`: it creates `index.html`, which shows the story and will show the comic once `/comic` has run. On macOS, open it for the user with `open`.
- Tell the user the story is finished, where its production folder is, and that `/comic` will turn it into a comic. If anything went wrong during the run (an agent broke a rule, a turn had to be shortened twice, the ending had to be forced), mention it briefly: it may be worth a journal entry.
