"""Builds a production's page.

Usage:
  python3 .claude/skills/production-page/scripts/build_page.py outputs/<production>
      writes <production>/index.html, linking to the files beside it
  python3 .claude/skills/production-page/scripts/build_page.py outputs/<production> --share
      writes the share file: a self-sufficient copy of the page, named after the story
      (e.g. the-three-pigs-and-the-magic-bean.html), with the comic and panel images packed inside,
      ready to send to friends; then rebuild index.html so it mentions the file
  python3 .claude/skills/production-page/scripts/build_page.py outputs/<production> --standalone OUT.html
      the same self-sufficient page, written wherever you like

Reads whatever the production has so far (story.md, screenplay.md, comic.html, panels/*.svg, build/) and fills
the shared template (../assets/template.html). Run it again whenever a step adds something.
"""
import base64, html, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "assets", "template.html")


def inline(text):
    """Escape, then turn *stage directions* into italics."""
    return re.sub(r"\*([^*]+)\*", r"<em>\1</em>", html.escape(text))


def read_story(path):
    title, when, parts, summary = "", "", [], ""
    for line in open(path).read().splitlines():
        if line.startswith("# ") and not title:
            title = line[2:].strip()
        elif re.match(r"\d{4}-\d{2}-\d{2}", line) and not when:
            when = line.strip()
        m = re.match(r"\*\*(.+?):\*\*\s*(.*)", line)
        if m:
            if m.group(1) == "Summary":
                summary = m.group(2)
            else:
                parts.append((m.group(1), m.group(2)))
    return title, when, parts, summary


def render_screenplay(path):
    out, in_list = [], False
    for line in open(path).read().splitlines():
        if line.startswith("## "):
            if in_list: out.append("</ul>"); in_list = False
            out.append(f"<h3>{html.escape(line[3:])}</h3>")
        elif line.startswith("- "):
            if not in_list: out.append("<ul>"); in_list = True
            key, _, val = line[2:].partition(":")
            out.append(f"<li><b>{html.escape(key)}:</b>{inline(val)}</li>" if val else f"<li>{inline(line[2:])}</li>")
    if in_list: out.append("</ul>")
    return "\n".join(out)


def size(path):
    n = os.path.getsize(path)
    return f"{n / 1024:.0f} KB" if n >= 1024 else f"{n} B"


def share_name(title):
    """The share file's name: the story's title as a file name, e.g. the-three-pigs-and-the-magic-bean.html."""
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-") + ".html"


def build(folder, standalone=None):
    folder = folder.rstrip("/")
    story_path = os.path.join(folder, "story.md")
    title, when, parts, summary = read_story(story_path) if os.path.exists(story_path) else (os.path.basename(folder), "", [], "")
    has = lambda name: os.path.exists(os.path.join(folder, name))
    panels = sorted(f for f in os.listdir(os.path.join(folder, "panels"))) if has("panels") else []

    # menu and sections follow the order things are made: story, screenplay, panels, comic
    buttons = []
    if has("story.md"): buttons.append('<a class="button" href="#story">The story</a>')
    if has("screenplay.md"): buttons.append('<a class="button" href="#screenplay">The screenplay</a>')
    if panels: buttons.append('<a class="button" href="#panels">The panels</a>')
    if has("comic.html"): buttons.append('<a class="button" href="#comic">The comic</a>')
    buttons.append('<a class="button" href="#files">All files</a>')

    story = "".join(f'<p><span class="who">{html.escape(w)}</span> {inline(t)}</p>' for w, t in parts) or '<p class="empty">The story is still being told.</p>'
    if has("screenplay.md"):
        n = len([1 for l in open(os.path.join(folder, "screenplay.md")) if l.startswith("## ")])
        screenplay = f'<p class="note">{n} panels, planned by the screenwriter.</p><div class="screenplay">{render_screenplay(os.path.join(folder, "screenplay.md"))}</div>'
    else:
        screenplay = '<p class="empty">No screenplay yet. Run /comic to plan and draw this story.</p>'
    def panel_src(f):
        if not standalone:
            return f"panels/{f}"
        data = base64.b64encode(open(os.path.join(folder, "panels", f), "rb").read()).decode()
        return f"data:image/svg+xml;base64,{data}"
    num = lambda f: int(re.sub(r"[^0-9]", "", f) or 0)
    panel_grid = ('<div class="panels">' + "".join(
        f'<a href="{panel_src(f)}" target="_blank"><img src="{panel_src(f)}" alt="Panel {num(f)}" loading="lazy">Panel {num(f)}</a>'
        for f in panels) + "</div>") if panels else '<p class="empty">The panels appear here once the comic is drawn.</p>'
    if has("comic.html") and standalone:
        comic_html = open(os.path.join(folder, "comic.html")).read()
        comic = f'<iframe class="comic" srcdoc="{html.escape(comic_html, quote=True)}" title="The comic"></iframe>'
    elif has("comic.html"):
        comic = ('<iframe class="comic" src="comic.html" title="The comic"></iframe>'
                 '<p class="open-comic"><a class="button primary" href="comic.html">Open the comic on its own</a></p>')
    else:
        comic = '<p class="empty">No comic yet. Run /comic to draw this story.</p>'

    def tree(path, rel=""):
        """The production folder as a folder tree: files first, then each folder as an open/close toggle."""
        items = sorted(os.listdir(path))
        files_ = [f for f in items if os.path.isfile(os.path.join(path, f)) and not f.startswith(".") and not (rel == "" and f == "index.html")]
        dirs = [d for d in items if os.path.isdir(os.path.join(path, d)) and not d.startswith(".") and d != "__pycache__"]
        out = ""
        for f in files_:
            r = f"{rel}{f}"
            out += f'<li class="file"><a href="{html.escape(r)}">{html.escape(f)}</a><span>{size(os.path.join(path, f))}</span></li>'
        for d in dirs:
            count = sum(len(fs) for _, _, fs in os.walk(os.path.join(path, d)))
            out += (f'<li><details><summary><b>{html.escape(d)}/</b><span>{count} file{"s" if count != 1 else ""}</span></summary>'
                    f'<ul>{tree(os.path.join(path, d), f"{rel}{d}/")}</ul></details></li>')
        return out
    if standalone:
        files = ('<p class="empty">This is a shared copy of the production. The full folder, with every file, '
                 'stays with whoever made it.</p>')
    else:
        files = f'<ul class="tree">{tree(folder)}</ul>'
        share = share_name(title)
        if has(share):
            files = (f'<p class="share">Want to share it? Send <a href="{html.escape(share)}">{html.escape(share)}</a> to your friends: '
                     'it is a single file with the whole production inside, and it opens in any browser.</p>') + files

    kicker = "The Three Little Pigs" + (f' <span class="date">· {html.escape(when.split(",")[0])}</span>' if when else "")
    page = open(TEMPLATE).read()
    for key, val in {"TITLE": html.escape(title), "KICKER": kicker, "SUMMARY": inline(summary) or "",
                     "SUMMARY_PLAIN": html.escape(summary), "BUTTONS": "".join(buttons), "COMIC": comic,
                     "PANELS": panel_grid, "STORY": story, "SCREENPLAY": screenplay, "FILES": files}.items():
        page = page.replace("{{" + key + "}}", val)
    out = standalone or os.path.join(folder, "index.html")
    open(out, "w").write(page)
    return out


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--share" in args:
        title = read_story(os.path.join(args[0], "story.md"))[0] if os.path.exists(os.path.join(args[0], "story.md")) else os.path.basename(args[0].rstrip("/"))
        print(build(args[0], standalone=os.path.join(args[0], share_name(title))))
    else:
        out = args[args.index("--standalone") + 1] if "--standalone" in args else None
        print(build(args[0], standalone=out))
