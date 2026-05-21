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
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css"
      integrity="sha384-nB0miv6/jRmo5UMMR1wu3Gz6NLsoTkbqJghGIsx//Rlm+ZU03BU6SQNC66uf4l5+" crossorigin="anonymous">
<link rel="stylesheet" href="{root}assets/style.css">
</head>
<body>
<div class="page">
<header class="masthead">
  <a href="{root}index.html" class="brand">LLM <em>Publishing</em></a>
  <nav>
    <a href="{root}index.html">Index</a>
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
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"
        integrity="sha384-7zkQWkzuo3B5mTepMUcHkMB5jZaolc2xDwL6VFqjFALcbeS9Ggm/Yr2r3Dy4lfFg" crossorigin="anonymous"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
        integrity="sha384-43gviWU0YVjaDtb/GhzOouOXtZMP/7XUzwPTstBeZFe/+rCMvRwr4yROQP43s0Xk" crossorigin="anonymous"
        onload="renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false},{left:'\\\\(',right:'\\\\)',display:false},{left:'\\\\[',right:'\\\\]',display:true}],throwOnError:false});"></script>
</body>
</html>
"""


def page(title, desc, body, root="../"):
    return HEAD.format(title=html.escape(title), desc=html.escape(desc), root=root) + body + FOOT


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
  fragments of the original conversation. It captures the abstract, structure,
  and key passages but is not the complete monograph. The full source
  (<code>.tex</code> / <code>.md</code> / <code>.pdf</code>) will replace this
  scaffold once uploaded to <code>/pdfs/</code>.
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
    Nine self-contained technical treatises produced in conversation
    with Claude across 2026 — orbital propagation, astrodynamics, scientific
    computing systems, viewshed geometry, weather forecasting infrastructure.
    Reconstructed here from conversation fragments; original PDFs to follow.
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
