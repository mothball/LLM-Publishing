"""Build the static site from monograph definitions."""
import html
import json
import os
import re
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).parent
MONO_DIR = ROOT / "monographs"
MONO_DIR.mkdir(exist_ok=True)


HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — LLM-Publishing</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{root}assets/katex/katex.min.css">
<link rel="stylesheet" href="{root}assets/style.css">
</head>
<body>
<div class="page">
<header class="masthead">
  <a href="{root}index.html" class="brand">LLM <em>Publishing</em></a>
  <nav>
    <a href="{root}index.html">Index</a>
    <a href="{root}vault.html">Vault</a>
    <a href="https://github.com/mothball/LLM-Publishing">GitHub</a>
  </nav>
</header>
"""

FOOT = """
<footer class="colophon">
  Reconstructed from past conversation snippets ·
  <a href="https://github.com/mothball/LLM-Publishing">View source on GitHub</a>
</footer>
</div>
<script src="{root}assets/katex/katex.min.js"></script>
<script src="{root}assets/katex/contrib/auto-render.min.js"></script>
<script>
document.addEventListener("DOMContentLoaded", function() {{
  renderMathInElement(document.body, {{
    delimiters: [
      {{left: '$$', right: '$$', display: true}},
      {{left: '$',  right: '$',  display: false}},
      {{left: '\\\\(', right: '\\\\)', display: false}},
      {{left: '\\\\[', right: '\\\\]', display: true}}
    ],
    throwOnError: false
  }});
}});
</script>
</body>
</html>
"""


def page(title, desc, body, root="../"):
    return HEAD.format(title=html.escape(title), desc=html.escape(desc), root=root) + body + FOOT.format(root=root)


def monograph_html(m):
    """Render one monograph page from a dict."""
    pdf_link = f'<a href="../pdfs/{m["pdf"]}">Download PDF</a>' if m.get("pdf_available") \
        else '<span style="color:var(--ink-faint)">PDF: upload pending</span>'

    parts = []
    parts.append(f'''
<header class="mono-header">
  <div class="eyebrow">Monograph № {m["num"]:02d} · {m["date"]}</div>
  <h1>{m["title"]}</h1>
  {"<p class='subtitle'>" + m["subtitle"] + "</p>" if m.get("subtitle") else ""}
  <div class="byline">
    <span>{m["format"]} · {m.get("length","")}</span>
    <span>{pdf_link}</span>
  </div>
</header>
''')

    parts.append(f'''
<aside class="reconstruction-notice">
  <strong>Reconstruction notice.</strong> This page is a summary rebuilt from
  fragments of the original conversation. The linked PDF is a PDF render of
  <em>this reconstruction</em>, not the original monograph. To replace it with
  the full source, drop the real <code>.pdf</code> into <code>/pdfs/</code>
  using the same filename.
</aside>
''')

    parts.append('<article class="prose">')

    if m.get("abstract"):
        parts.append('<h2 id="abstract">Abstract</h2>')
        parts.append(m["abstract"])

    if m.get("toc"):
        parts.append('<div class="toc"><div class="toc-title">Contents</div><ol>')
        for t in m["toc"]:
            parts.append(f'<li>{t}</li>')
        parts.append('</ol></div>')

    for sec in m.get("sections", []):
        sid = re.sub(r'[^a-z0-9]+', '-', sec["heading"].lower()).strip('-')
        parts.append(f'<h2 id="{sid}">{sec["heading"]}</h2>')
        parts.append(sec["body"])

    if m.get("closing"):
        parts.append('<hr class="ornament">')
        parts.append('<h2 id="status">Status & provenance</h2>')
        parts.append(m["closing"])

    parts.append('</article>')

    return page(m["title"], m.get("abstract_text", m["title"])[:150], "".join(parts))


def index_html(monographs):
    items = []
    for m in monographs:
        items.append(f'''
<li>
  <div class="ordinal">{m["num"]:02d}</div>
  <div>
    <h2><a href="monographs/{m["slug"]}.html">{m["title"]}</a></h2>
    <p class="blurb">{m["blurb"]}</p>
  </div>
  <div class="meta">
    <span class="date">{m["date"]}</span>
    <span class="format">{m["format"]}</span>
  </div>
</li>
''')

    body = f'''
<section class="hero">
  <h1>A small archive of <em>monographs</em>.</h1>
  <p class="lede">
    Ten self-contained technical treatises produced in conversation
    with Claude across 2026 — orbital propagation, astrodynamics, scientific
    computing systems, viewshed geometry, weather forecasting infrastructure.
    Reconstructed here from conversation fragments; original PDFs to follow.
  </p>
  <p class="lede" style="font-size: 1.02em; margin-top: 1rem;">
    See also the <a href="vault.html"><strong>Vault</strong></a> — an interactive
    graph of the concepts, tools, decisions, assumptions, and unrealized gaps
    that connect these monographs to one another.
  </p>
</section>
<ul class="monograph-list">{"".join(items)}</ul>
'''
    return page("A small archive of monographs", "A curated archive of long-form technical monographs.", body, root="")


# ============================================================
# MONOGRAPH DEFINITIONS — newest first
# ============================================================

MONOGRAPHS = []  # populated below

print("build.py loaded; MONOGRAPHS to be defined in content.py")
