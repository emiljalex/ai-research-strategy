# AI Research Strategy

An independent research practice founded and led by Emil Alex. This repository contains the public website, a set of inspectable examples, and a deterministic Intervention Lab.

## Read and run

[Open the public preview](https://ai-research-strategy-preview.pages.dev/). The intended permanent address is `https://airesearchstrategy.com`.

The site builds to ordinary HTML, CSS, images, and JavaScript. Python 3.9 or newer runs the publisher with its standard library. The prebuilt illustration ships with the source. Node 18 or newer runs the Lab tests.

```sh
python3 scripts/build.py
python3 -m http.server 8000 --bind 127.0.0.1 --directory dist
```

Open `http://127.0.0.1:8000/`. Reading and navigation work without client-side JavaScript. The Lab uses local JavaScript and invented source material. It sends no prompts or source accounts to an external service.

## Publish a piece

1. Write a Markdown file outside the public checkout while the piece is under review. Use a section folder named `perspectives`, `methods`, or `field-notes`. The lowercase hyphenated filename becomes its permanent URL.
2. Start with the front matter below. Use paragraphs, `##` or `###` headings, flat `- ` lists, blockquotes, emphasis, inline code, and Markdown links. Separate blocks with a blank line. Site links use directory URLs such as `/lab/#workbench`. For external sources, use absolute HTTPS links.
3. Preview with `python3 scripts/build.py --review-dir ../founder-review`. Open `../review-site/index.html` in a browser. To carry the complete review edition as one file, run `python3 scripts/review_copy.py ../founder-review ../Founder-Preview.html`.
4. After founder approval, copy the file into the matching folder under `content/` and change its status to `published`. Keep the draft original outside the checkout. Public Git history is visible even if a file is later removed.
5. Run the checks below, commit the approved file to `main`, and deploy the public build. Section indexes update automatically. The highest `order` in each section leads its index and appears on Home. Ties sort by filename.

```markdown
---
title: A question worth investigating
description: One sentence describing the argument or experiment.
kind: Essay
status: draft
order: 20
---
Begin with the decision or observation.

## What changed

Describe the evidence and its limits.
```

The three public starter pieces use the status `example`. They are a reading prompt, a worksheet, and a bench note about the included fixture. The public build accepts `example` and `published` only. Review adds external files marked `draft` and writes outside the checkout. Only the public `dist/` belongs on Pages.

## Site structure

| Location | Contents |
| --- | --- |
| `content/` | Publishable Markdown by section |
| `scripts/pages.py` | Home, section introductions, article layout, Lab, and About |
| `scripts/content.py` | Metadata and Markdown rendering |
| `scripts/build.py` | Static publisher and link and fragment validation |
| `assets/` | Styles, original handoff illustration, icon, Lab fixture and controls |
| `tests/` | Publishing boundaries and the Lab decision rule |

The offline founder copy includes a Markdown download on each draft. Optionally pass `--source-archive PATH` to `review_copy.py` to include a clean public source ZIP, created with `git archive --format=zip HEAD`, on its About page.

To change the Lab, edit `assets/lab-model.js` and the accompanying bench note together. The optional `scripts/draw_figure.py` regenerates the original illustration and icon with Pillow. The website build uses the committed artwork.

## Checks

```sh
python3 -m unittest discover -s tests -v
node --test tests/lab.test.js
python3 scripts/build.py
```

The publisher checks every internal link, fragment, image alternative, page heading count, and main target. A rejected build preserves the previous output. A clean production build adds canonical metadata and a sitemap. Preview builds request no indexing in both HTML and headers. Anyone with the hosted preview address can view the public examples.

## Cloudflare Pages

**Preview.** The `ai-research-strategy-preview` project uses Pages Direct Upload in the existing Cloudflare account. Rebuild with `python3 scripts/build.py`. Upload the contents of `dist/` to a new deployment for this exact project. The dashboard accepts a folder or a ZIP with `index.html` at its root. Leave the local build marker `.airestra-generated` out of upload archives. The preview needs no purchased domain.

**Canonical site.** When the repository and domain are ready, create a Git-connected Pages project named `ai-research-strategy` in the same account. Grant the Cloudflare GitHub app access to `emiljalex/ai-research-strategy` only. Use production branch `main`, the repository root, no framework preset, and output directory `dist`. Use this build command to keep branch previews out of search results and enable indexing only for the promoted main branch:

```sh
if [ "$CF_PAGES_BRANCH" = "main" ]; then python3 scripts/build.py --production; else python3 scripts/build.py; fi
```

Create the canonical project when public promotion is approved. Pages keeps its deployment mode for the life of each project, so the preview has its own name. A Pages custom domain attaches under **Custom domains** on the canonical project.

## Domains and redirects

Both registrations require founder approval before purchase. Register both domains in the same existing Cloudflare account. Activate the primary zone and attach `airesearchstrategy.com` to the canonical Pages project. Wait for the primary HTTPS certificate before sending visitors there.

In the `airestra.com` zone, create proxied DNS records for the apex and `www`. For a redirect-only zone, a proxied apex A record with the reserved originless address `192.0.2.1` and a proxied `www` CNAME to that apex are sufficient. Wait for an active edge certificate covering the apex and `www`. Add a **Single Redirect** on this alias zone with the following settings.

| Setting | Value |
| --- | --- |
| Match expression | `http.host in {"airestra.com" "www.airestra.com"}` |
| Dynamic target | `concat("https://airesearchstrategy.com", http.request.uri.path)` |
| HTTP status | `302` |
| Preserve query string | Enabled |

The host match handles HTTP and HTTPS and avoids a loop on the primary hostname. Place it before any overlapping redirect. The temporary rule keeps a future standalone use of Airestra possible. Disable the rule and update alias DNS if the brand later gets its own site.

Verify both aliases with HTTP and HTTPS, the root, and a known deep link with a query. The first response should be `302` with the complete HTTPS primary URL in `Location`. Following it should reach the requested page. Check the primary certificate, canonical tags, and sitemap before announcement.

```sh
curl -sSI 'https://www.airestra.com/methods/map-a-handoff/?from=alias'
curl -sSI 'http://airestra.com/lab/?from=alias'
curl -fsSL 'https://airesearchstrategy.com/robots.txt'
```

Cloudflare references cover [Pages Git integration](https://developers.cloudflare.com/pages/get-started/git-integration/), [Direct Upload](https://developers.cloudflare.com/pages/get-started/direct-upload/), [custom domains](https://developers.cloudflare.com/pages/configuration/custom-domains/), and [Single Redirect settings](https://developers.cloudflare.com/rules/url-forwarding/single-redirects/settings/).

## Rights

The founder has not selected a license for the code or editorial work.
