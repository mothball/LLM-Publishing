# LLM-Publishing

A static archive of long-form technical monographs produced in conversation with Claude, published via GitHub Pages.

**Live at:** https://mothball.github.io/LLM-Publishing/

## Structure

```
.
├── index.html              # Archive index
├── assets/style.css        # Editorial stylesheet (serif, paper-like)
├── monographs/             # Per-monograph HTML pages
├── pdfs/                   # Original PDFs (uploaded as available)
├── build.py                # Page generator
├── content.py              # Monograph data (title, abstract, sections)
└── run_build.py            # `python3 run_build.py` regenerates the site
```

## Status

The HTML pages were reconstructed from fragments of the original chat
conversations and are **summaries, not the complete monographs**. Each page
links to a PDF at `pdfs/<slug>.pdf` once that file is uploaded; until then,
that link shows "upload pending."

To publish a full monograph: drop the original `.pdf` into `pdfs/` using the
filename listed on the corresponding HTML page, set `"pdf_available": True`
in `content.py`, and re-run `run_build.py`.

## Rendering

- **Math:** KaTeX auto-render from CDN — write `$inline$` or `$$display$$` in section bodies.
- **Code:** dark-on-warm code blocks, JetBrains Mono.
- **Typography:** Fraunces (display) / Newsreader (body) / JetBrains Mono (code), all from Google Fonts.

## License

The site infrastructure and stylesheet are MIT.
Monograph content reflects work-in-progress technical notes.
