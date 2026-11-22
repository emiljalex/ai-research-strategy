"""Pack the founder edition as a single, offline HTML file outside the checkout."""
import argparse
import base64
from html import escape
from pathlib import Path
import re

from build import ROOT, build, make_pages
from content import articles, markdown
from pages import SITE, footer, header

ROUTER = """
const view = document.getElementById("publication");
const pages = new Map(Array.from(document.querySelectorAll("template[data-path]"), page => [page.dataset.path, page]));
let currentPath = "";
function openPage() {
  const [path, anchor] = (location.hash.slice(1) || "/").split("#");
  const page = pages.get(path) || pages.get("/");
  const changed = currentPath !== page.dataset.path;
  if (changed) {
    view.replaceChildren(page.content.cloneNode(true));
    document.title = page.dataset.title;
    currentPath = page.dataset.path;
    mountInterventionLab();
  }
  const target = anchor && document.getElementById(anchor);
  if (target) {
    target.scrollIntoView();
    if (target.id === "main") target.focus({ preventScroll: true });
  } else if (changed) {
    document.getElementById("main").focus({ preventScroll: true });
    window.scrollTo(0, 0);
  }
}
window.addEventListener("hashchange", openPage);
openPage();
"""


def pack(drafts, output, source_archive=None):
    output = output.resolve()
    if output.is_relative_to(ROOT) or output.suffix.lower() != ".html":
        raise ValueError("Choose an HTML output file outside the public repository.")
    build(ROOT, drafts)
    assets = ROOT / "assets"
    artwork = base64.b64encode((assets / "handoff.webp").read_bytes()).decode("ascii")
    rule = base64.b64encode((assets / "lab-model.js").read_bytes()).decode("ascii")
    icon = base64.b64encode((assets / "mark.png").read_bytes()).decode("ascii")
    private_entries = {entry.url: entry for entry in articles(drafts, {"draft"})}
    source_link = ""
    if source_archive:
        archive_data = base64.b64encode(source_archive.read_bytes()).decode("ascii")
        source_link = f'<p><a class="button" href="data:application/zip;base64,{archive_data}" download="ai-research-strategy-source.zip">Download public repository source</a></p>'
    templates, print_drafts = [], []
    for page in make_pages(ROOT, drafts):
        if page.path == "/about/" and source_link:
            page.body = page.body.replace("</div></div></div>", source_link + "</div></div></div>")
        body = header(page.path) + f'<main id="main" tabindex="-1">{page.body}</main>' + footer(True)
        if page.path in private_entries:
            entry = private_entries[page.path]
            source = drafts / entry.section / f"{entry.slug}.md"
            data = base64.b64encode(source.read_bytes()).decode("ascii")
            download = f'<a class="button" download="{entry.slug}.md" href="data:text/markdown;base64,{data}">Download draft Markdown</a>'
            body = body.replace('<div class="endnote">', f'<div class="endnote">{download} &nbsp; ')
            formatted, _ = markdown(entry.body)
            print_drafts.append(f'<article class="wrap"><header class="article-head"><h1>{escape(entry.title)}</h1><p>Founder review draft</p></header><div class="prose">{formatted}{download}</div></article>')
        def inner_link(match):
            href = match[1]
            if href == "/assets/lab-model.js":
                return f'href="data:text/javascript;base64,{rule}"'
            if href.startswith("#"):
                return 'href="#' + page.path + href + '"'
            return f'href="#{href}"' if href.startswith("/") else match[0]
        body = re.sub(r'href="([^"]+)"', inner_link, body)
        body = body.replace('src="/assets/handoff.webp"', f'src="data:image/webp;base64,{artwork}"')
        title = SITE if page.path == "/" else f"{page.title} | {SITE}"
        templates.append(f'<template data-path="{page.path}" data-title="{escape(title, quote=True)}">{body}</template>')
    scripts = "\n".join((assets / name).read_text(encoding="utf-8") for name in ("lab-model.js", "lab.js"))
    css = (assets / "site.css").read_text(encoding="utf-8")
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow"><link rel="icon" href="data:image/png;base64,{icon}"><title>{SITE} | Founder review</title>
<style>{css}</style></head><body><div class="review-strip">Founder review edition <span>· Drafts are marked in the journal</span></div>
<div id="publication"><noscript>The three founder drafts follow. Enable JavaScript for the complete site and interactive Lab.{"".join(print_drafts)}</noscript></div>
{"".join(templates)}<script>{scripts}\n{ROUTER}</script></body></html>'''
    output.write_text(html, encoding="utf-8")
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("drafts", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--source-archive", type=Path, help="Optional ZIP made with git archive HEAD")
    args = parser.parse_args()
    print(pack(args.drafts.resolve(), args.output, args.source_archive))
