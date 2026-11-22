"""Build the public site or a separate founder review. Run from any directory."""
import argparse
from dataclasses import dataclass
from html import escape
from html.parser import HTMLParser
import os
from pathlib import Path
import re
import shutil
import tempfile
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET

from content import SECTIONS, articles
from pages import SITE, about, article_page, collection, footer, header, home, lab

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = "https://airesearchstrategy.com"
ASSETS = ("site.css", "lab.js", "lab-model.js", "handoff.webp", "mark.png")


@dataclass
class Page:
    path: str
    title: str
    summary: str
    body: str


def make_pages(root, review_dir=None):
    entries = articles(root / "content", {"example", "published"})
    if review_dir:
        entries += articles(review_dir, {"draft"})
    entries.sort(key=lambda item: (-item.order, item.slug))
    pages = [
        Page("/", SITE, "A research practice founded by Emil Alex investigating judgment, workflows, and intervention in human-AI work.", home(entries, bool(review_dir))),
        Page("/lab/", "The Intervention Lab", "Change one label in a synthetic research workflow and trace its effect on a recommendation.", lab()),
        Page("/about/", "About", "The purpose, founder, and research direction of AI Research Strategy.", about()),
    ]
    pages += [Page(f"/{key}/", title, desc, collection(key, entries)) for key, (title, desc) in SECTIONS.items()]
    pages += [Page(a.url, a.title, a.description, article_page(a)) for a in entries]
    if len({p.path for p in pages}) != len(pages):
        raise ValueError("Two entries have the same route. Give each piece a distinct filename.")
    return pages


def filename(route):
    return route.strip("/") + "/index.html" if route.strip("/") and route.endswith("/") else route.strip("/") or "index.html"


def document(page, review=False, production=False):
    title = SITE if page.path == "/" else f"{page.title} | {SITE}"
    canonical = ""
    if production and page.path != "/404.html":
        canonical = f'<link rel="canonical" href="{CANONICAL}{page.path}"><meta property="og:url" content="{CANONICAL}{page.path}">'
    badge = '<div class="review-strip">Founder review edition <span>· Drafts are marked in the journal</span></div>' if review else ""
    body = f'{badge}{header(page.path)}<main id="main" tabindex="-1">{page.body}</main>{footer(review)}'
    scripts = ""
    if page.path == "/lab/":
        scripts = '<script defer src="/assets/lab-model.js"></script><script defer src="/assets/lab.js"></script>'
    noindex = '' if production and page.path != "/404.html" else '<meta name="robots" content="noindex, nofollow">'
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title><meta name="description" content="{escape(page.summary, quote=True)}">
<meta property="og:title" content="{escape(title, quote=True)}"><meta property="og:description" content="{escape(page.summary, quote=True)}"><meta property="og:type" content="website">
<meta name="theme-color" content="#fafaf6">{noindex}{canonical}
<link rel="icon" href="/assets/mark.png" type="image/png"><link rel="stylesheet" href="/assets/site.css">{scripts}
</head><body>{body}</body></html>'''
    if review:
        source_dir = os.path.dirname(filename(page.path)) or "."
        def portable(match):
            key, route, fragment = match.groups()
            target = os.path.relpath(filename(route), source_dir)
            return f'{key}="{target}{fragment or ""}"'
        html = re.sub(r'(href|src)="(/[^"#]*)(#[^"]*)?"', portable, html)
    return html


class PageIndex(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.h1 = set(), [], 0

    def handle_starttag(self, tag, attrs):
        props = dict(attrs)
        if tag == "h1":
            self.h1 += 1
        if "id" in props:
            if props["id"] in self.ids:
                raise ValueError(f'Duplicate HTML id {props["id"]}')
            self.ids.add(props["id"])
        if tag == "img" and "alt" not in props:
            raise ValueError("Image requires alternative text")
        for key in ("href", "src"):
            if key in props:
                self.links.append(props[key])


def audit(folder):
    indexes = {}
    for path in folder.rglob("*.html"):
        index = PageIndex()
        index.feed(path.read_text(encoding="utf-8"))
        if index.h1 != 1 or "main" not in index.ids:
            raise ValueError(f"{path.name} needs one h1 and a main landmark")
        indexes[path.resolve()] = index
    for source, index in indexes.items():
        for link in index.links:
            parts = urlsplit(link)
            if parts.netloc or parts.scheme:
                continue
            if parts.path.startswith("/"):
                target = folder / parts.path.lstrip("/")
            else:
                target = source.parent / parts.path if parts.path else source
            if target.is_dir():
                target = target / "index.html"
            target = target.resolve()
            if not target.is_relative_to(folder.resolve()) or not target.is_file():
                raise ValueError(f"Missing or out-of-bounds link from {source.name}: {link}")
            if parts.fragment and (target not in indexes or parts.fragment not in indexes[target].ids):
                raise ValueError(f"Missing anchor from {source.name}: {link}")


def render(folder, root, review_dir=None, production=False):
    pages = make_pages(root, review_dir)
    pages.append(Page("/404.html", "Page not found", "Return to the journal.",
                      '<section class="wrap section-intro"><h1>Page not found</h1><p class="standfirst">This address has no entry in the journal.</p><div class="actions"><a class="button" href="/">Return home</a></div></section>'))
    for page in pages:
        dest = folder / filename(page.path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(document(page, bool(review_dir), production), encoding="utf-8")
    (folder / "assets").mkdir()
    for asset in ASSETS:
        shutil.copyfile(root / "assets" / asset, folder / "assets" / asset)
    robots = "User-agent: *\nDisallow: /\n"
    headers = "/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n"
    if production:
        robots = f"User-agent: *\nAllow: /\nSitemap: {CANONICAL}/sitemap.xml\n"
        sitemap = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
        for page in pages[:-1]:
            ET.SubElement(ET.SubElement(sitemap, "url"), "loc").text = CANONICAL + page.path
        ET.ElementTree(sitemap).write(folder / "sitemap.xml", encoding="utf-8", xml_declaration=True)
    else:
        headers += "  X-Robots-Tag: noindex, nofollow\n"
    (folder / "_headers").write_text(headers, encoding="utf-8")
    (folder / "robots.txt").write_text(robots, encoding="utf-8")
    audit(folder)
    return len(pages)


def build(root=ROOT, review_dir=None, production=False):
    root = root.resolve()
    if review_dir is not None:
        review_dir = review_dir.resolve()
        if production or not review_dir.is_dir() or review_dir.is_relative_to(root):
            raise ValueError("Review requires an existing draft folder outside the repository and a review build.")
    dest = root.parent / "review-site" if review_dir else root / "dist"
    if dest.is_symlink() or (dest.exists() and not (dest / ".airestra-generated").is_file()):
        raise ValueError(f"Refusing to replace an unrecognized output directory: {dest}")
    with tempfile.TemporaryDirectory(dir=dest.parent, prefix=".airestra-build-") as tmp:
        stage, previous = Path(tmp) / "new", Path(tmp) / "previous"
        stage.mkdir()
        count = render(stage, root, review_dir, production)
        (stage / ".airestra-generated").write_text("AI Research Strategy static build\n", encoding="utf-8")
        if dest.exists():
            dest.rename(previous)
        try:
            stage.rename(dest)
        except OSError:
            if previous.exists():
                previous.rename(dest)
            raise
    return dest, count


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--review-dir", type=Path, help="External Markdown directory for founder review")
    mode.add_argument("--production", action="store_true", help="Enable indexing and canonical URLs for the primary domain")
    args = parser.parse_args()
    target, count = build(review_dir=args.review_dir, production=args.production)
    print(f"Built and checked {count} HTML pages in {target}")
