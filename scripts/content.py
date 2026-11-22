"""The small Markdown subset used by this journal. All source text is escaped."""
from dataclasses import dataclass
from html import escape
from pathlib import Path
import re
from urllib.parse import urlsplit

SECTIONS = {
    "perspectives": ("Perspectives", "Arguments about where judgment lives and how research changes when machines share the work."),
    "methods": ("Methods", "Working frameworks you can take into a real decision, test with a colleague, and revise."),
    "field-notes": ("Field Notes", "Small experiments with visible inputs, reproducible results, and explicit limits.")
}


@dataclass(frozen=True)
class Article:
    section: str
    slug: str
    title: str
    description: str
    kind: str
    status: str
    order: int
    body: str

    @property
    def url(self):
        return f"/{self.section}/{self.slug}/"

    @property
    def minutes(self):
        return max(1, (len(self.body.split()) + 199) // 200)


def articles(folder, allowed_statuses):
    items = []
    for path in sorted(Path(folder).glob("*/*.md")):
        section, slug = path.parent.name, path.stem
        try:
            if section not in SECTIONS or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
                raise ValueError("Use a known section and a lowercase hyphenated filename")
            parts = path.read_text(encoding="utf-8").split("---\n", 2)
            if len(parts) != 3 or parts[0]:
                raise ValueError("Expected metadata between two --- lines")
            meta = {}
            for line in parts[1].strip().splitlines():
                key, sep, value = line.partition(":")
                if not sep or not value.strip() or key in meta:
                    raise ValueError("Invalid or repeated metadata field")
                meta[key] = value.strip()
            required = {"title", "description", "kind", "status", "order"}
            if set(meta) != required or not parts[2].strip():
                raise ValueError("Expected title, description, kind, status, order and a body")
            if meta["status"] not in allowed_statuses:
                raise ValueError(f"Allowed status in this source directory: {sorted(allowed_statuses)}")
            meta["order"] = int(meta["order"])
            items.append(Article(section, slug, body=parts[2].strip(), **meta))
        except (OSError, ValueError) as exc:
            raise ValueError(f"{path}: {exc}") from exc
    return items


def inline(source):
    token = re.compile(r"\[([^\[\]]+)\]\(([^\s()]+)\)|\*\*([^*]+)\*\*|\*([^*]+)\*|`([^`]+)`")
    output, end = [], 0
    for match in token.finditer(source):
        output.append(escape(source[end:match.start()]))
        label, href, strong, emphasis, code = match.groups()
        if href:
            parts = urlsplit(href)
            if not ((href.startswith("/") and not href.startswith("//")) or href.startswith("#") or (parts.scheme == "https" and parts.hostname)):
                raise ValueError(f"Unsupported link target {href!r}")
            output.append(f'<a href="{escape(href, quote=True)}">{escape(label)}</a>')
        elif strong:
            output.append(f"<strong>{escape(strong)}</strong>")
        elif emphasis:
            output.append(f"<em>{escape(emphasis)}</em>")
        else:
            output.append(f"<code>{escape(code)}</code>")
        end = match.end()
    return "".join(output) + escape(source[end:])


def markdown(source):
    """Paragraphs, level-two/three headings, blockquotes, and flat unordered lists."""
    output, headings, seen = [], [], set()
    for block in re.split(r"\n\s*\n", source.strip()):
        lines = block.splitlines()
        heading = re.fullmatch(r"(#{2,3}) (.+)", block)
        if heading:
            marks, title = heading.groups()
            base = re.sub("[^a-z0-9]+", "-", title.lower()).strip("-") or "section"
            anchor, serial = base, 1
            while anchor in seen:
                serial += 1
                anchor = f"{base}-{serial}"
            seen.add(anchor)
            if len(marks) == 2:
                headings.append((anchor, title))
            tag = f"h{len(marks)}"
            output.append(f'<{tag} id="{anchor}">{inline(title)}</{tag}>')
        elif all(line.startswith("- ") for line in lines):
            output.append("<ul>" + "".join(f"<li>{inline(line[2:])}</li>" for line in lines) + "</ul>")
        elif all(line.startswith("> ") for line in lines):
            output.append("<blockquote><p>" + inline(" ".join(line[2:] for line in lines)) + "</p></blockquote>")
        else:
            output.append("<p>" + inline(" ".join(lines)) + "</p>")
    return "\n".join(output), headings
