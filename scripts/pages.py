"""Page composition. All routes used here are site-relative directory URLs."""
from html import escape as e
from content import SECTIONS, markdown
from rollout import instrument

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
<nav aria-label="Footer">{links} <a href="https://github.com/emiljalex/ai-research-strategy">Source on GitHub</a></nav></div></footer>'''


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
    selection = [next(a for a in entries if a.section == section) for section in SECTIONS]
    reading = "".join(f'''<article class="reading-row"><div class="section-label">{e(SECTIONS[a.section][0])}</div><div><h3><a href="{a.url}">{e(a.title)}</a></h3><p>{e(a.description)}</p></div>{meta(a)}</article>''' for a in selection)
    return f'''<section class="wrap opening"><div class="opening-copy"><p class="author-line"><a href="/about/">Emil Alex</a><span>Independent research practice</span></p>
<h1>Start with the decision.<br><em>Rebuild the work.</em></h1>
<p class="opening-deck">AI changes what it costs to produce an answer. Research can change which questions an organization asks, who gets heard, and what it decides to build.</p>
<p class="opening-detail">AI Research Strategy investigates how to divide that work between people and machines, and who has the authority to change its course.</p>
<div class="actions"><a class="button" href="#agenda">Explore the research agenda</a><a class="text-link" href="/lab/">Visit the Lab</a></div></div>{instrument()}</section>
<section class="argument-band"><div class="wrap argument-inner"><div>{eyebrow("The proposition")}<h2>When the answer gets cheaper, the expensive mistake moves upstream.</h2></div><div><p>Imagine arriving with conclusive evidence on Friday, one day after the team committed its engineering budget. A faster synthesis helps only if someone can still change Thursday’s choice.</p><p>This practice starts at that moment of commitment. It asks what evidence could move it, whose experience would count, and how a team would hear about a mistake in time to act.</p><a class="text-link" href="/methods/before-the-budget-closes/">Try the decision brief</a></div></div></section>
<section class="agenda wrap inquiry" id="agenda"><div>{eyebrow("Research agenda")}<h2>Four questions<br> worth pursuing.</h2><p class="agenda-lede">These are open investigations. Each has a way to put its central claim under pressure.</p></div><div class="inquiry-list">
<details open><summary>What can research still change?</summary><p>Before a product team funds a direction, identify a live alternative and the person who can choose it. Test whether researchers can name evidence that would switch the investment.</p><a href="/methods/before-the-budget-closes/">Use the decision brief</a></details>
<details><summary>What gets lost at a handoff?</summary><p>Ask two analysts to interpret the same ambiguous service request. Pass one a label and give the other the passage and a rival reading. Track which errors each can find and repair.</p><a href="/lab/#workbench">Try an interpretation change</a></details>
<details><summary>When can a dependable system give poor advice?</summary><p>A rule can run correctly every time while overlooking the people a policy will affect. Change the scope of a pilot and inspect which records still support it.</p><a href="/lab/rollout-rehearsal/">Run the rollout rehearsal</a></details>
<details><summary>How does an organization learn what to ask next?</summary><p>Follow a puzzling observation across planning cycles. Look for the moment it changes a category, a recruitment decision, or the terms of a later debate. The proposed study would trace that lineage.</p></details></div></section>
<section class="shelf"><div class="wrap"><div class="section-head"><h2>On the reading desk</h2><span class="index-note">{'Founder review selection' if review else 'Selected work'}</span></div><div class="reading-desk">{reading}</div></div></section>
<section class="wrap founder-band"><div>{eyebrow("Behind the practice")}<h2>Emil Alex</h2></div><div><p>An industrial designer by training, Emil spent eight years researching enterprise products. He brings that experience to a question about power as much as technique. When a system recommends a course of action, who understands it well enough, and has the standing, to change it?</p><a class="text-link" href="/about/">Meet the founder</a></div></section>'''


COLLECTION_NOTES = {
    "perspectives": ("A question to read with", "Which organizational choices are still open when evidence arrives, and who can reopen one after a correction?", "/lab/", "Follow a decision in the Lab"),
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


def section_navigation(title, items):
    return f'''<aside class="contents"><nav class="wide-contents" aria-label="{title}"><p class="section-label">{title}</p><ul>{items}</ul></nav>
<details class="compact-contents"><summary>{title}</summary><nav aria-label="{title}"><ul>{items}</ul></nav></details></aside>'''


def article_page(a, entries=()):
    body, headings = markdown(a.body)
    contents = "".join(f'<li><a href="#{anchor}">{e(label)}</a></li>' for anchor, label in headings)
    name = SECTIONS[a.section][0]
    series = ""
    if a.series:
        related = [item for item in entries if item.series == a.series and item.url != a.url]
        links = "".join(f'<li><a href="{item.url}">{e(item.title)}</a></li>' for item in related)
        series = f'<aside class="series"><p class="section-label">Series · {e(a.series)}</p><ul>{links}</ul></aside>' if links else ""
    return f'''<article class="wrap"><header class="article-head"><a class="back-link" href="/{a.section}/">{name}</a>
<h1>{e(a.title)}</h1><p class="standfirst">{e(a.description)}</p>{meta(a)}</header>
<div class="reader-grid">{section_navigation("In this piece", contents)}
<div class="prose">{body}{series}<div class="endnote"><a class="text-link" href="/{a.section}/">Return to {name}</a></div></div></div></article>'''


def lab():
    return f'''<div class="wrap"><header class="section-intro lab-intro"><div>{eyebrow("Lab · Interactive study")}<h1>The Intervention Lab</h1>
<p class="standfirst">Change one interpretation. Follow what happens to the decision.</p></div><p class="lab-context">Three fictional accounts, one interpretive choice. This study isolates the right to correct a label after handoff. A fixed rule runs in your browser.</p></header>
<div class="companion"><div><span class="section-label">Companion experiment</span><h2><a href="/lab/rollout-rehearsal/">The rollout rehearsal</a></h2></div><p>Change the proposed pilot and trace evidence, routing and the product owner’s authority to sign.</p></div>
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
    sections = (("background", "From objects to organizations"), ("practice", "A way of working"), ("institution", "The longer view"))
    items = "".join(f'<li><a href="#{anchor}">{name}</a></li>' for anchor, name in sections)
    return f'''<div class="wrap"><header class="founder-intro"><div>{eyebrow("About the practice")}<h1>Emil Alex</h1><p class="standfirst">Founder of AI Research Strategy. Researcher, designer, and builder of human-AI working methods.</p></div>
<aside class="founder-question"><span class="section-label">A question behind the work</span><p>Who can change a decision after the evidence changes?</p></aside></header>
<div class="reader-grid about-body">{section_navigation("In this introduction", items)}<div class="prose">
<h2 id="background">From objects to organizations</h2><p>A person can complete a request on a screen and still have no way to get it fulfilled. Someone on the other side has to understand it, have the authority to act, and fit it into a working day. Which of those people gets to define whether the product works?</p>
<p>Emil came to questions like this through industrial design, an MFA in Interaction Design and an MBA in Design Strategy. He spent eight years in enterprise product research at ServiceNow. Studying work from the perspectives of employees, operators and administrators gives him a particular starting point. The person using an interface and the person absorbing its consequences may sit in different parts of an organization.</p>
<p>That changes the assignment a researcher can take on. A team asking whether a feature is usable might also need to know who is entitled to use it, who can honor its promise, and whether funding that feature would solve the problem anyone actually faces.</p>
<h2 id="practice">A way of working</h2><p>Emil founded this practice to investigate how AI changes the design of the work itself. He starts with a consequential choice, works backward to the evidence it needs, and asks which operations a machine can take on. The divisions matter. A system can match a record to a rule. Deciding whether the rule describes success for the people affected is a separate piece of research.</p>
<p>The Lab makes that distinction inspectable. In one study a reader can revisit the source behind an interpretation, replace the label and watch the recommendation change. In another, widening a pilot to include the night crew makes a previously adequate evidence packet incomplete. Both rules are available to examine. Their behavior is reproducible. Their assumptions are open to challenge.</p>
<p>These are choices about the researcher's role. Research can enter while priorities and budgets are still negotiable. It also needs room to pursue an observation that has no sponsor yet. Emil wants a practice capable of doing both, and of explaining how one kind of inquiry informs the other.</p>
<h2 id="institution">The longer view</h2><p>The immediate work is to publish arguments with enough detail to dispute them, make methods practical enough to try, and document what happens when a demonstration fails. Over time the ambition is a shared research practice where other practitioners can bring competing explanations, repeat experiments, and improve the tools.</p>
<p>One way to engage now is to take an example apart. Open the rollout rehearsal, widen its scope, then decide what additional evidence you would require before putting the pilot in front of real workers.</p><div class="actions"><a class="button" href="/lab/rollout-rehearsal/">Enter the rehearsal</a><a class="text-link" href="/methods/">Explore the methods</a></div></div></div></div>'''
