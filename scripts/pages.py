"""Page composition. All routes used here are site-relative directory URLs."""
from html import escape as e
from content import SECTIONS, markdown

SITE = "AI Research Strategy"
NAV = [(f"/{key}/", name) for key, (name, _) in SECTIONS.items()] + [("/lab/", "Lab"), ("/about/", "About")]


def wordmark():
    return '<span class="mark" aria-hidden="true"><i></i><i></i><i></i><i></i></span><span>AI Research Strategy</span>'


def eyebrow(text, color=""):
    return f'<div class="eyebrow {color}"><span aria-hidden="true"></span>{e(text)}</div>'


def header(path):
    links = []
    for url, name in NAV:
        current = ' aria-current="page"' if url == path else ' aria-current="location"' if path.startswith(url) else ''
        links.append(f'<a href="{url}"{current}>{name}</a>')
    items = "".join(links)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="mast"><div class="wrap mast-inner">
<a class="wordmark" href="/" aria-label="{SITE}, home">{wordmark()}</a>
<nav aria-label="Main navigation" class="desktop-nav">{items}</nav>
<details class="mobile-menu"><summary>Menu <i aria-hidden="true"></i></summary><nav aria-label="Mobile navigation">{items}</nav></details>
</div></header>'''


def footer(review):
    edition = "Founder review edition" if review else "Independent research practice"
    links = " ".join(f'<a href="{url}">{name}</a>' for url, name in NAV)
    return f'''<footer><div class="wrap footer-inner"><div><a class="wordmark" href="/">{wordmark()}</a><p>{edition} · Founded by Emil Alex</p></div>
<nav aria-label="Footer">{links}</nav></div></footer>'''


def plate():
    return '''<figure class="plate"><div class="plate-image">
<img src="/assets/handoff.webp" width="1440" height="810" fetchpriority="high" alt="Fine blue traces converge at a handoff and spread out again. A copper path leaves the group and rejoins it at the decision boundary.">
<div class="plate-top"><span>Handoff study</span><span class="register" aria-hidden="true"></span></div>
<div class="plate-bottom"><span><i class="swatch"></i>Workflow</span><span><i class="swatch copper"></i>Human intervention</span></div>
</div><figcaption>A point of intervention between source and decision.</figcaption></figure>'''


def meta(article):
    draft = '<span class="draft">Founder review draft</span><span class="meta-dot">·</span>' if article.status == "draft" else ""
    return f'<div class="meta">{draft}<span>{e(article.kind)}</span><span class="meta-dot">·</span><span>{article.minutes} min read</span></div>'


def home(entries, review):
    featured = [next(a for a in entries if a.section == section) for section in SECTIONS]
    cards = []
    for a in featured:
        cards.append(f'''<article class="reading-card"><div class="section-label">{e(SECTIONS[a.section][0])}</div>
<h3><a href="{a.url}">{e(a.title)}</a></h3><p>{e(a.description)}</p>{meta(a)}</article>''')
    return f'''<section class="hero wrap"><div class="hero-copy">{eyebrow("Founding inquiry")}
<h1>Where does the<br><em>judgment go?</em></h1>
<p class="standfirst">When AI turns evidence into a recommendation, who gets to question the steps in between?</p>
<p class="hero-note">An independent research practice investigating how people and machines make decisions together.</p>
<div class="actions"><a class="button" href="/lab/#workbench">Explore the Lab</a><a class="text-link" href="#agenda">Research agenda</a></div></div>{plate()}</section>
<section class="shelf"><div class="wrap"><div class="section-head"><h2>From the journal</h2><span class="index-note">{'Founder review selection' if review else 'Selected reading'}</span></div>
<div class="reading-grid">{"".join(cards)}</div></div></section>
<section class="agenda wrap" id="agenda"><div>{eyebrow("Research agenda")}<h2>Three questions<br>guide the work.</h2></div><dl>
<dt>Where should the work be divided?</dt><dd>Look for the moment an observation becomes an interpretation. That boundary can tell us what a specialist should do and what the next person needs to see. <a href="/methods/">Explore Methods</a></dd>
<dt>Who can intervene, and when?</dt><dd>A reviewer might inspect a source, challenge a label, or reopen an earlier decision. Each requires a different kind of access. <a href="/lab/">Enter the Lab</a></dd>
<dt>What survives a correction?</dt><dd>Follow a changed interpretation downstream. Which conclusions still hold? Which decisions need to be made again? <a href="/field-notes/">Read Field Notes</a></dd>
</dl></section>'''


COLLECTION_NOTES = {
    "perspectives": ("A question to read with", "When an AI-assisted recommendation reaches a decision-maker, which judgments can they still inspect, challenge, and change?", "/lab/", "Follow a decision in the Lab"),
    "methods": ("Use a method", "Choose one recommendation from a piece of work you know. Bring the source, the interpretation, and the person who will act on it.", "/field-notes/when-one-label-moves/", "See a worked example"),
    "field-notes": ("How to read a bench note", "Look for the fixture, the change, the observed result, and the point where the example stops supporting a conclusion.", "/lab/", "Reproduce the experiment")
}


def collection(section, entries):
    title, description = SECTIONS[section]
    rows = []
    for a in entries:
        if a.section == section:
            rows.append(f'''<article class="list-entry"><div class="section-label">{e(a.kind)}</div><h2><a href="{a.url}">{e(a.title)}</a></h2>
<p>{e(a.description)}</p>{meta(a)}</article>''')
    side_title, side, url, link = COLLECTION_NOTES[section]
    return f'''<div class="wrap"><header class="section-intro">{eyebrow("Journal")}<h1>{title}</h1><p class="standfirst">{description}</p></header>
<div class="collection-grid"><div>{"".join(rows)}</div><aside class="margin-card"><h2>{side_title}</h2><p>{side}</p><a class="text-link" href="{url}">{link}</a></aside></div></div>'''


def article_page(a):
    body, headings = markdown(a.body)
    contents = "".join(f'<li><a href="#{anchor}">{e(label)}</a></li>' for anchor, label in headings)
    name = SECTIONS[a.section][0]
    return f'''<article class="wrap"><header class="article-head"><a class="back-link" href="/{a.section}/">{name}</a>
<h1>{e(a.title)}</h1><p class="standfirst">{e(a.description)}</p>{meta(a)}</header>
<div class="reader-grid"><aside class="contents"><nav aria-label="In this piece"><p class="section-label">In this piece</p><ul>{contents}</ul></nav></aside>
<div class="prose">{body}<div class="endnote"><a class="text-link" href="/{a.section}/">Return to {name}</a></div></div></div></article>'''


def lab():
    return f'''<div class="wrap"><header class="section-intro lab-intro"><div>{eyebrow("Lab · Interactive study")}<h1>The Intervention Lab</h1>
<p class="standfirst">Change one interpretation. Follow what happens to the decision.</p></div><p class="lab-context">Three fictional accounts from a library pickup service. A fixed rule turns their labels into a proposed next step. Every change runs in your browser.</p></header>
<section id="workbench" class="bench" aria-labelledby="bench-title"><div class="bench-header"><h2 id="bench-title">The pickup notice</h2><span class="fixture-tag">Synthetic example</span></div>
<noscript><p class="no-js">The interactive controls need JavaScript. <a href="/field-notes/when-one-label-moves/">Read the full before-and-after comparison.</a></p></noscript>
<div class="workbench-controls" hidden><div class="bench-columns">
<div class="bench-source"><h3>Inspect a source</h3><form id="revision">
<label for="account">Source account</label><select id="account"><option value="0">Account A</option><option value="1" selected>Account B</option><option value="2">Account C</option></select>
<blockquote id="account-quote"></blockquote><p class="current">Current interpretation <strong id="current-label"></strong></p>
<label for="interpretation">Change interpretation</label><select id="interpretation"><option value="entrance">Finding the entrance</option><option value="hours">Opening hours</option><option value="expiry">Hold expiration</option></select>
<button type="submit" class="button" id="apply" disabled>Apply revision</button></form></div>
<div class="bench-result"><h3>Trace the consequence</h3><p class="section-label">Accounts by interpretation</p>
<div class="count-row" id="count-entrance"><span>Finding the entrance</span><output aria-label="Finding the entrance count">2</output><div class="meter" aria-hidden="true"></div></div>
<div class="count-row" id="count-hours"><span>Opening hours</span><output aria-label="Opening hours count">0</output><div class="meter" aria-hidden="true"></div></div>
<div class="count-row" id="count-expiry"><span>Hold expiration</span><output aria-label="Hold expiration count">1</output><div class="meter" aria-hidden="true"></div></div>
<div class="decision"><span class="section-label">Proposed next step</span><p id="lab-action"></p><small id="lab-reason"></small></div></div></div>
<div class="history"><div><h3>Revision history</h3><p id="empty-log">The original labels are in place.</p><ol id="history-list"></ol></div><div class="history-actions"><button id="undo" disabled>Undo last change</button><button id="reset" disabled>Reset example</button></div></div>
<p id="lab-status" class="sr-only" role="status" aria-live="polite"></p></div></section>
<div class="lab-after"><h2>What the rule assumes</h2><div><p>Each account receives one label. A unique leading label triggers a suggested action. A tie prompts another inquiry. You can revise the labels and undo a revision. The rule and the source accounts stay fixed.</p><div class="actions"><a class="text-link" href="/field-notes/when-one-label-moves/">Read the bench note</a><a class="text-link" href="/assets/lab-model.js" download="intervention-model.js">Download the decision rule</a></div></div></div></div>'''


def about():
    return f'''<div class="wrap"><header class="section-intro">{eyebrow("About the practice")}<h1>AI Research Strategy</h1>
<p class="standfirst">An independent research practice founded and led by Emil Alex.</p></header><div class="reader-grid about-body"><aside class="contents"><p class="section-label">Founder</p><p class="founder-name">Emil Alex</p></aside><div class="prose">
<h2>Why this practice exists</h2><p>When a machine takes part in research, some of the most consequential decisions move into the middle of the work. Someone decides which passage to retain, which interpretation to pass on, and when a conclusion is ready to act on. Those choices deserve the same attention as the final recommendation.</p>
<p>AI Research Strategy studies how to make that work visible. Its scope spans research methods, product development, organizational decisions, and the everyday tasks that carry knowledge between people.</p>
<h2>How the work develops</h2><p>A perspective puts an argument on the table. A method makes part of that argument usable. A field note records what happened in a bounded trial. The Lab opens the mechanism so a reader can challenge it directly.</p>
<p>Emil sets the research direction and reviews the writing. Examples identify their sources or explicitly describe invented material. An observation from a demonstration carries only the weight that the demonstration can support.</p>
<h2>The longer view</h2><p>The ambition is a body of methods, experiments, and technical work that others can examine and eventually help develop. The starting point is small enough to question in detail. <a href="/lab/">Open the first experiment.</a></p>
</div></div></div>'''
