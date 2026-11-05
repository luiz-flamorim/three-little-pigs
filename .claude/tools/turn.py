"""Story runner helper. Usage:
  turn.py new "Title"                          create the production folder outputs/YYYY-MM-DD-3-pigs-and-<name>/
                                               with its story.md; prints the story file's path, then the final title.
                                               If a production with the same name exists, this one becomes
                                               Part II, Part III... in both the folder name and the title.
  turn.py add FILE "Speaker" [--chaos "what"]  read a turn from stdin, check its length, append it,
                                               then roll the chaos die for the next turn.
                                               Pass --chaos when this turn was a CHAOS turn, to record it first.
"""
import os, random, re, sys
from datetime import datetime

LIMIT = 125            # every turn, Storyteller included
SUMMARY_LIMIT = 255    # the closing Summary paragraph
CHAOS_LOG = ".claude/chaos-used.md"
MAX_CHAOS = 3


CHAOS_HEADER = ("# Chaos used\n\nOutside elements already brought into your stories, one line per chaos event. "
                "It is your own record: git ignores it, and the game runner tells each chaos player which recent ones to avoid.\n\n")


def chaos_lines():
    if not os.path.exists(CHAOS_LOG):
        os.makedirs(os.path.dirname(CHAOS_LOG), exist_ok=True)
        open(CHAOS_LOG, "w").write(CHAOS_HEADER)
    return [l for l in open(CHAOS_LOG).read().splitlines() if l.startswith("- ")]


def story_chaos(stem):
    return [l[2:].rsplit(" (", 1)[0] for l in chaos_lines() if l.endswith(f"({stem})")]


OUTPUTS = "outputs"


def roman(n):
    out = ""
    for v, r in ((1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
                 (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")):
        while n >= v:
            out += r; n -= v
    return out


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def production_name(title):
    """'The Three Pigs and the Magic Bean' -> '3-pigs-and-the-magic-bean'."""
    m = re.match(r"\s*(the\s+)?(three|3)\s+(little\s+)?pigs\s+and\s+(.*)$", title, re.I)
    rest = m.group(4) if m else title
    return "3-pigs-and-" + slugify(rest)


def stem_of(path):
    """The production a story file belongs to: its folder name (every story file is called story.md)."""
    base = os.path.splitext(os.path.basename(path))[0]
    return os.path.basename(os.path.dirname(os.path.abspath(path))) if base == "story" else base


cmd = sys.argv[1]
if cmd == "new":
    now = datetime.now()
    title = sys.argv[2].strip()
    name = production_name(title)
    # verification loop: the same story name already used (on any date) makes this one Part II, III...
    os.makedirs(OUTPUTS, exist_ok=True)
    same = [d for d in os.listdir(OUTPUTS)
            if os.path.isdir(os.path.join(OUTPUTS, d)) and re.fullmatch(rf"\d{{4}}-\d{{2}}-\d{{2}}-{re.escape(name)}(-part-[ivxlcdm]+)?", d)]
    part = len(same) + 1
    folder = f"{OUTPUTS}/{now:%Y-%m-%d}-{name}"
    if part > 1:
        folder += f"-part-{roman(part).lower()}"
        title += f", Part {roman(part)}"
    while os.path.exists(folder):                      # same name twice in one day at the same part: never overwrite
        part += 1
        folder = f"{OUTPUTS}/{now:%Y-%m-%d}-{name}-part-{roman(part).lower()}"
        title = re.sub(r", Part [IVXLCDM]+$", "", title) + f", Part {roman(part)}"
    os.makedirs(folder)
    path = f"{folder}/story.md"
    open(path, "w").write(f"# {title}\n\n{now:%Y-%m-%d, %H:%M}\n")
    print(path)
    print(f"title: {title}")
elif cmd == "add":
    path, speaker = sys.argv[2], sys.argv[3]
    stem = stem_of(path)
    text = re.sub(r"\n\s*Next:.*$", "", sys.stdin.read().strip()).strip()
    limit = SUMMARY_LIMIT if speaker == "Summary" else LIMIT
    if len(text) > limit:
        sys.exit(f"TOO LONG: {len(text)}/{limit} characters, not saved")
    if "--chaos" in sys.argv:
        element = sys.argv[sys.argv.index("--chaos") + 1]
        # the first chaos in a story brings in the new element; later ones are twists on it
        if story_chaos(stem):
            element = "twist: " + element
        open(CHAOS_LOG, "a").write(f"- {element} ({stem})\n")
    open(path, "a").write(f"\n**{speaker}:** {text}\n")
    story = open(path).read()
    parts = story.count("\n**") - story.count("\n**Summary:**")
    if speaker == "Summary":
        sys.exit(f"saved, {len(text)}/{limit} characters, summary (story has {parts} parts)")
    print(f"saved, {len(text)}/{limit} characters, part {parts}")
    used = story_chaos(stem)
    if len(used) >= MAX_CHAOS:
        print(f"next turn: no chaos (limit of {MAX_CHAOS} reached)")
    else:
        roll = random.randint(1, 4)
        if roll != 1:
            print(f"next turn: no chaos (roll {roll})")
        elif not used:
            new = [l for l in chaos_lines() if not l.startswith("- twist: ")]
            avoid = "; ".join(l[2:].rsplit(" (", 1)[0] for l in new[-10:]) or "nothing yet"
            print(f"next turn: CHAOS new element (roll 1, event 1 of {MAX_CHAOS}). Avoid: {avoid}")
        else:
            print(f"next turn: CHAOS twist (roll 1, event {len(used) + 1} of {MAX_CHAOS}). "
                  f"Use only what is already in the story, such as: {used[0]}")
