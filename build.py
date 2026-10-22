#!/usr/bin/env python3
"""Build the guides: Markdown pages in ``docs/`` become a static site in ``site/``.

The site is described by ``site.yaml`` (topics and the pages they contain). Each
page is a Markdown file with a YAML front matter block. The build adds
permalinks to task headings, rewrites ``.md`` links into site URLs, emits a
search index and a sitemap, and fails on any broken link or anchor, on a page
missing from ``site.yaml``, and on an absolute or unrecognised link.
"""

from __future__ import annotations

import datetime as dt
import html
import json
import re
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup
from pygments.formatters import HtmlFormatter

ROOT = Path(__file__).resolve().parent
DOCS_DIR = ROOT / "docs"
THEME_DIR = ROOT / "theme"
SITE_DIR = ROOT / "site"
CONFIG = ROOT / "site.yaml"

# Admonition kinds and the label shown before their title.
BOX_LABELS = {"warning": "Warning", "tip": "Tip", "note": "Note"}

MARKDOWN_EXTENSIONS = [
    "admonition",
    "attr_list",
    "def_list",
    "md_in_html",
    "tables",
    "toc",
    "pymdownx.details",
    "pymdownx.highlight",
    "pymdownx.inlinehilite",
    "pymdownx.keys",
    "pymdownx.superfences",
    "pymdownx.tabbed",
]
MARKDOWN_EXTENSION_CONFIGS = {
    "toc": {"toc_depth": "2-3", "permalink": False},
    "pymdownx.highlight": {"css_class": "highlight", "guess_lang": False},
    "pymdownx.tabbed": {"alternate_style": True},
}

PYGMENTS_LIGHT = "friendly"
PYGMENTS_DARK = "github-dark"


class BuildError(Exception):
    """A problem that must stop the build."""


# --------------------------------------------------------------------------- model


@dataclass
class Page:
    """One output page: the home page, a topic's landing page or a guide."""

    kind: str  # "home" | "topic" | "guide" | "404"
    source: Path  # Markdown source, relative to DOCS_DIR
    url: str  # site-relative URL ending in "/" ("" for the home page)
    meta: dict
    body_md: str
    title: str = ""
    topic: Page | None = None
    pages: list[Page] = field(default_factory=list)
    sections: list[dict] = field(default_factory=list)
    summary_html: str = ""
    lede_html: str = ""
    body_html: str = ""
    base: str = ""  # set for pages served from an unknown depth (404)

    @property
    def summary(self) -> str:
        return str(self.meta.get("summary", "")).strip()

    @property
    def description(self) -> str:
        """The summary as plain text, for the page's meta description."""
        return self.summary.replace("`", "")

    @property
    def icon(self) -> str:
        return str(self.meta.get("icon", "")).strip()

    @property
    def output_path(self) -> Path:
        if self.kind == "404":
            return SITE_DIR / "404.html"
        return SITE_DIR / self.url / "index.html"

    @property
    def root(self) -> str:
        if self.base:
            return self.base
        depth = self.url.count("/")
        return "../" * depth if depth else "./"

    def href(self, target: Page) -> str:
        return self.root + target.url


# --------------------------------------------------------------------- front matter

FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)


def split_front_matter(text: str, source: Path) -> tuple[dict, str]:
    match = FRONT_MATTER.match(text)
    if not match:
        raise BuildError(f"{source}: missing YAML front matter")
    try:
        meta = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as error:
        raise BuildError(f"{source}: invalid front matter: {error}") from None
    if not isinstance(meta, dict):
        raise BuildError(f"{source}: front matter must be a mapping")
    return meta, text[match.end():]


def read_page(kind: str, rel: Path, url: str) -> Page:
    path = DOCS_DIR / rel
    if not path.is_file():
        raise BuildError(f"site.yaml refers to a missing file: {rel}")
    meta, body = split_front_matter(path.read_text(encoding="utf-8"), rel)
    title = str(meta.get("title", "")).strip()
    if not title:
        raise BuildError(f"{rel}: front matter needs a title")
    return Page(kind=kind, source=rel, url=url, meta=meta, body_md=body, title=title)


def load_site() -> tuple[dict, list[Page]]:
    """Read ``site.yaml`` and return the config plus every page in contents order."""
    config = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    pages: list[Page] = [read_page("home", Path("index.md"), "")]
    for topic_cfg in config.get("topics", []):
        directory = topic_cfg["dir"].strip("/")
        topic = read_page("topic", Path(directory) / "index.md", f"{directory}/")
        if not (THEME_DIR / "icons" / f"{topic.icon}.svg").is_file():
            raise BuildError(f"{topic.source}: unknown icon '{topic.icon}' (see theme/icons/)")
        pages.append(topic)
        for name in topic_cfg.get("pages") or []:
            stem = PurePosixPath(name).stem
            guide = read_page("guide", Path(directory) / name, f"{directory}/{stem}/")
            if not guide.summary:
                raise BuildError(f"{guide.source}: front matter needs a one-line summary")
            guide.topic = topic
            topic.pages.append(guide)
            pages.append(guide)

    listed = {p.source for p in pages}
    unlisted = sorted(
        str(path.relative_to(DOCS_DIR))
        for path in DOCS_DIR.rglob("*.md")
        if path.relative_to(DOCS_DIR) not in listed
    )
    if unlisted:
        raise BuildError(f"pages missing from site.yaml: {', '.join(unlisted)}")
    return config, pages


# ------------------------------------------------------------------- HTML passes

LEDE = re.compile(r"\A\s*<p>(.*?)</p>", re.S)


def split_lede(page: Page) -> None:
    """Lift the opening paragraph, the page's one-sentence scope, into the page head."""
    match = LEDE.match(page.body_html)
    if match:
        page.lede_html = match.group(1)
        page.body_html = page.body_html[match.end():]


HEADING = re.compile(r'<h([23]) id="([^"]+)">(.*?)</h\1>', re.S)


def anchor_link(anchor: str) -> str:
    """A permalink that copies the shareable URL of the element when clicked."""
    return (
        f' <a class="anchor" href="#{anchor}" title="Copy link to this place"'
        f' aria-label="Copy link to this place">§</a>'
    )


def link_headings(page: Page) -> None:
    """Give H2/H3 a permalink and collect the page's task list from its H2s."""
    sections: list[dict] = []

    def replace(match: re.Match) -> str:
        level, anchor, text = int(match.group(1)), match.group(2), match.group(3)
        if level == 2:
            plain = re.sub(r"<[^>]+>", "", text).strip()
            sections.append({"id": anchor, "title": html.unescape(plain)})
        return f'<h{level} id="{anchor}">{text}{anchor_link(anchor)}</h{level}>'

    page.body_html = HEADING.sub(replace, page.body_html)
    page.sections = sections


PRE = re.compile(r"(<pre.*?</pre>)", re.S)
INLINE_CODE = re.compile(r"<code>([^<]*)</code>")


def keep_code_tokens(page: Page) -> None:
    """Let inline code wrap only at its spaces, never inside a token like ``:<line>``."""

    def tokens(match: re.Match) -> str:
        words = match.group(1).split(" ")
        return "<code>" + " ".join(f'<span class="tok">{w}</span>' if w else w for w in words) + "</code>"

    parts = PRE.split(page.body_html)
    page.body_html = "".join(part if i % 2 else INLINE_CODE.sub(tokens, part) for i, part in enumerate(parts))
    page.lede_html = INLINE_CODE.sub(tokens, page.lede_html)


TABLE = re.compile(r"<table>.*?</table>", re.S)


def wrap_tables(page: Page) -> None:
    """Let wide tables scroll sideways on a phone instead of widening the page."""
    page.body_html = TABLE.sub(lambda m: f'<div class="table-wrap">{m.group(0)}</div>', page.body_html)


BOX = re.compile(
    r'(<div class="admonition ([\w-]+)">\s*<p class="admonition-title">|'
    r'<details class="([\w-]+)"( open="open")?>\s*<summary>)(.*?)(</p>|</summary>)',
    re.S,
)


def label_boxes(page: Page) -> None:
    """Prefix each admonition's title with its kind ("Warning · No trailing slash")."""

    def replace(match: re.Match) -> str:
        opening, title, closing = match.group(1), match.group(5), match.group(6)
        kind = match.group(2) or match.group(3)
        label = BOX_LABELS.get(kind)
        if label is None:
            raise BuildError(f"{page.source}: unsupported admonition kind '{kind}'")
        head = f'<span class="boxlabel">{label}</span>'
        if title and title.lower() != label.lower():
            head += f' <span class="boxtitle">{title}</span>'
        return f"{opening}{head}{closing}"

    page.body_html = BOX.sub(replace, page.body_html)
    page.body_html = page.body_html.replace('<details class="', '<details class="admonition ')


LINK = re.compile(r'(href|src)="([^"]*)"')
IDS = re.compile(r'\sid="([^"]+)"')


def rewrite_links(
    page: Page, pages_by_source: dict[Path, Page], assets: set[Path], fragments: list[tuple]
) -> None:
    """Rewrite ``.md`` links into site URLs and check that every target exists.

    Fragments are recorded in ``fragments`` and checked once every page is rendered.
    """
    source_dir = PurePosixPath(page.source.parent.as_posix())

    def replace(match: re.Match) -> str:
        attr, link = match.group(1), match.group(2)
        if re.match(r"^(https?:|mailto:)", link):
            return match.group(0)
        if link.startswith("/"):
            raise BuildError(f"{page.source}: absolute link, use a relative one: {link}")
        target, _, fragment = link.partition("#")
        if not target:
            fragments.append((page, page, fragment))
            return match.group(0)
        parts: list[str] = []
        for part in (source_dir / target).parts:
            if part == "..":
                if not parts:
                    raise BuildError(f"{page.source}: link escapes docs/: {link}")
                parts.pop()
            elif part != ".":
                parts.append(part)
        resolved = Path(*parts)
        suffix = f"#{fragment}" if fragment else ""
        if target.endswith(".md"):
            dest = pages_by_source.get(resolved)
            if dest is None:
                raise BuildError(f"{page.source}: link to a page that is not in site.yaml: {link}")
            if fragment:
                fragments.append((page, dest, fragment))
            return f'{attr}="{page.href(dest)}{suffix}"'
        if not (DOCS_DIR / resolved).is_file():
            raise BuildError(f"{page.source}: unrecognised link (not a .md page or a file): {link}")
        assets.add(resolved)
        return f'{attr}="{page.root}{resolved.as_posix()}{suffix}"'

    page.body_html = LINK.sub(replace, page.body_html)


def check_fragments(fragments: list[tuple]) -> None:
    ids = {}
    for page, dest, fragment in fragments:
        if dest.source not in ids:
            ids[dest.source] = set(IDS.findall(dest.body_html))
        if fragment not in ids[dest.source]:
            raise BuildError(f"{page.source}: no anchor '#{fragment}' in {dest.source}")


def mark_external_links(page: Page) -> None:
    page.body_html = re.sub(
        r'<a href="(https?://[^"]+)"',
        r'<a href="\1" class="external" rel="noopener"',
        page.body_html,
    )


# ------------------------------------------------------------------------- search

TAG = re.compile(r"<[^>]+>")
TAB_LABELS = re.compile(r'<div class="tabbed-labels">.*?</div>', re.S)


def search_entries(page: Page) -> list[dict]:
    """One entry per task (H2 section), with plain text for the client-side index."""
    text = TAB_LABELS.sub("", f"<p>{page.lede_html}</p>{page.body_html}")
    chunks = re.split(r'(?=<h2 id=")', text)
    crumb = f"{page.topic.title} › {page.title}" if page.topic else page.title
    entries = []
    for chunk in chunks:
        heading = re.match(r'<h2 id="([^"]+)">(.*?)</h2>', chunk, re.S)
        text = html.unescape(TAG.sub(" ", chunk)).replace("§", "")
        text = re.sub(r"\s+", " ", text).strip()
        if not text:
            continue
        if heading:
            section = html.unescape(TAG.sub("", heading.group(2))).replace("§", "").strip()
            anchor = "#" + heading.group(1)
            text = text[len(section):].strip() if text.startswith(section) else text
        else:
            section, anchor = "", ""
        entries.append({"url": page.url + anchor, "page": crumb, "section": section, "text": text[:1200]})
    return entries


# -------------------------------------------------------------------------- build


def make_markdown() -> markdown.Markdown:
    return markdown.Markdown(
        extensions=MARKDOWN_EXTENSIONS, extension_configs=MARKDOWN_EXTENSION_CONFIGS
    )


def pygments_css() -> str:
    light = HtmlFormatter(style=PYGMENTS_LIGHT).get_style_defs(".highlight")
    dark = HtmlFormatter(style=PYGMENTS_DARK)
    dark_css = dark.get_style_defs('[data-theme="dark"] .highlight')
    return f"{light}\n{dark_css}\n"


def icon(name: str, css_class: str = "icon") -> Markup:
    """Inline an icon from ``theme/icons/`` so it takes the text colour."""
    svg = (THEME_DIR / "icons" / f"{name}.svg").read_text(encoding="utf-8").strip()
    return Markup(svg.replace("<svg", f'<svg class="{css_class}" aria-hidden="true" fill="currentColor"', 1))


def sitemap(config: dict, pages: list[Page]) -> str:
    urls = "".join(f"<url><loc>{config['url']}{p.url}</loc></url>" for p in pages)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n'
    )


def render_pages(config: dict, pages: list[Page]) -> None:
    md = make_markdown()
    pages_by_source = {p.source: p for p in pages}
    assets: set[Path] = set()
    fragments: list[tuple] = []
    index: list[dict] = []

    env = Environment(
        loader=FileSystemLoader(THEME_DIR / "templates"),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    build_date = dt.date.today()
    env.globals.update(site=config, build_date=build_date.strftime("%B %Y"), icon=icon)

    for page in pages:
        page.summary_html = re.sub(r"^<p>|</p>$", "", md.convert(page.summary))
        md.reset()
        page.body_html = md.convert(page.body_md)
        md.reset()
        split_lede(page)
        link_headings(page)
        keep_code_tokens(page)
        wrap_tables(page)
        label_boxes(page)
        rewrite_links(page, pages_by_source, assets, fragments)
        mark_external_links(page)
        index += search_entries(page)
    check_fragments(fragments)

    # Served for any missing URL, so its links must not depend on the request path.
    not_found = Page(
        kind="404", source=Path("404"), url="", meta={}, body_md="", title="Page not found",
        base=urlparse(config["url"]).path,
    )

    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    SITE_DIR.mkdir(parents=True)

    topics = [p for p in pages if p.kind == "topic"]
    for page in [*pages, not_found]:
        template = env.get_template(f"{page.kind}.html")
        page.output_path.parent.mkdir(parents=True, exist_ok=True)
        page.output_path.write_text(template.render(page=page, topics=topics), encoding="utf-8")

    for rel in sorted(assets):
        dest = SITE_DIR / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(DOCS_DIR / rel, dest)

    static_out = SITE_DIR / "static"
    shutil.copytree(THEME_DIR / "static", static_out)
    (static_out / "pygments.css").write_text(pygments_css(), encoding="utf-8")
    (SITE_DIR / "search.json").write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8")
    (SITE_DIR / "sitemap.xml").write_text(sitemap(config, pages), encoding="utf-8")
    (SITE_DIR / ".nojekyll").write_text("", encoding="utf-8")


def main() -> int:
    try:
        config, pages = load_site()
        render_pages(config, pages)
    except BuildError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    guides = sum(1 for p in pages if p.kind == "guide")
    print(f"built {len(pages)} pages ({guides} guides) into {SITE_DIR.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
