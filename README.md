# LLM-Publishing

A static archive of long-form technical monographs produced in conversation with Claude, published via GitHub Pages.

**Live at:** https://mothball.github.io/LLM-Publishing/

## For LLMs entering this repo

If you are an LLM assistant working on this repository, **read
[`LLM_INSTRUCTIONS.md`](./LLM_INSTRUCTIONS.md) first**. It describes the
project-based context-loading protocol designed to keep your context window
useful instead of flooded. The short version: read one project YAML from
`projects/`, then ask the human what they're working on.

## Structure

```
.
├── LLM_INSTRUCTIONS.md     # Read first if you are an LLM
├── index.html              # Archive index
├── vault.html              # Interactive knowledge graph (for humans)
├── projects/               # Project-level orientation YAMLs (read these)
│   ├── README.md           # Protocol for using and updating the projects layer
│   ├── orbprop-mcpi.yaml
│   ├── differentiable-astrodynamics.yaml
│   ├── performant-python.yaml
│   └── sda-pipeline.yaml
├── monographs/             # Per-monograph HTML pages (canonical content)
├── pdfs/                   # PDF renders
├── assets/                 # CSS, KaTeX, vault data
├── build.py                # Page generator
├── content.py              # Monograph data (title, abstract, sections)
├── vault_data.py           # Vault nodes and edges
├── build_vault.py          # Vault data exporter
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
