---
name: tell-me-a-story
description: The one command for the whole Three Little Pigs story machine — improvise a new story with the agents, turn it into a comic, and publish its production page and share file, straight through. Use this skill whenever the user says "tell me a story", "start a story", "make a story", "let's play", "continue the story" or types /tell-me-a-story, unless they explicitly ask for only the story (/story) or only a comic of an existing story (/comic).
---

**First rule:** never go outside this project folder (`3 Little Pigs - A`). Do not look at, read, copy, change or delete anything outside it. Put temporary files in `tmp/` and delete them when you are done.

# Tell me a story

One command runs the whole production, with no stops for review. You orchestrate; the other skills do the work.

1. **Say what will happen**, in one line: the agents will improvise a story live, then it becomes a comic and a page to share.
2. **The story.** Load the `story` skill and follow it to the end (if the user asked to continue an earlier story, follow its "continue" step to make the next chapter): the agents improvise, every turn is saved and shown live, the summary is written, and the production page is built. Do not stop to offer `/comic`; go straight on.
3. **The comic.** Load the `comic` skill and follow it for the production just made: screenplay, layout, drawing, checks, the share file and the rebuilt page. Before it starts, tell the user in one line that the comic is being made; it takes a while.
4. **The end.** Open the production page for the user (on macOS, with `open`). Then report in a few short lines: the story's title, where its production page is, and how to share it: "Want to share it? Send `<share file>` to your friends: it is a single file with the whole production inside, and it opens in any browser."

If a step fails, say so plainly, keep what was made (the story is still saved in its production folder), and tell the user they can finish with `/comic` later.
