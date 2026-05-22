# For LLMs working in this repository

This file is the first thing you should read when entering this repository as
an LLM assistant. It tells you how the archive is organized and — more
importantly — **what not to do**.

The human who maintains this repo has been deliberate about its structure to
avoid a specific failure mode: large language models, when given access to a
large knowledge base, tend to load too much of it into context, then confidently
synthesize from a fog of partly-stale, partly-irrelevant material. That failure
mode produces worse answers than no context at all.

The structure described below is designed to give you the **minimum context
needed for productive work** and to make the **paths to deeper material
explicit but not automatic**.

---

## The layout

```
/                              the archive
├─ README.md                   public-facing README
├─ LLM_INSTRUCTIONS.md         this file
├─ index.html                  the public archive index
├─ vault.html                  interactive graph visualization (for humans)
│
├─ projects/                   ★ project-level orientation YAMLs ★
│  ├─ README.md                how to use the projects layer
│  ├─ orbprop-mcpi.yaml
│  ├─ differentiable-astrodynamics.yaml
│  ├─ performant-python.yaml
│  └─ sda-pipeline.yaml
│
├─ monographs/                 the long-form HTML pages (canonical content)
├─ pdfs/                       PDF renders of the monographs
├─ assets/                     CSS, KaTeX, vault data
│
├─ content.py                  monograph definitions (source for build.py)
├─ vault_data.py               nodes and edges for the vault graph
├─ build.py                    static site generator
├─ build_vault.py              vault data exporter
└─ run_build.py                runs the build
```

---

## How to enter a session

When the human starts a new conversation about this work, take the following
steps **in order**. Stop at the first one that gives you what you need.

### 1. Identify the project, if any

Listen to the human's opening message. Do they mention a project by name, by
topic, or by file? Map the mention to one of the project YAMLs:

| User mentions | Project YAML |
|---|---|
| MCPI, Picard–Chebyshev, orbprop, propagator performance | `projects/orbprop-mcpi.yaml` |
| differentiable substrate, AD, SPEPH, GPU-native astrodynamics | `projects/differentiable-astrodynamics.yaml` |
| vectorized Python, NumPy internals, SIMD, NEP 54 | `projects/performant-python.yaml` |
| UCT, TLE, IOD, viewshed, horizon mask, cloud cover for tasking | `projects/sda-pipeline.yaml` |

If you cannot cleanly map the conversation to a project, **ask the human**
which project they're working on. Do not guess.

### 2. Read exactly one project YAML

It is ~200 tokens. Read the whole thing. This gives you:

- which monographs are canonical for this project,
- the active assumptions you should respect,
- the decisions that are already settled (do not re-litigate them),
- the gaps that are currently blocking,
- what the human is likely working on next.

### 3. Work from there

You now have project context. Proceed with the conversation. If the question
goes beyond what the YAML covers — for example, the human asks for a specific
equation, a specific number, a specific decision rationale — pull the relevant
monograph from `/monographs/` and read only the section that addresses the
question.

---

## What NOT to do

### Do not pre-load the archive

It is tempting to load all project YAMLs, all monographs, the vault data file,
and recent conversation history at session start. **Don't.** The marginal token
of stale or irrelevant context makes you worse at the task, not better. This is
well-documented LLM behavior; it applies to you.

### Do not synthesize across stale documents without confirmation

If you find yourself drawing on three or more separate files to construct an
answer, stop. Ask the human which of the sources is current and authoritative.
The human's memory is faster and more accurate than your synthesis.

### Do not treat the vault graph as a context source

The vault (`vault.html`, `vault_data.py`) is a **visualization for humans
browsing their own work**. It is not an index for you to mine. Do not load
`vault_data.py` into your context unless the human explicitly asks you to work
on the vault itself.

### Do not re-litigate settled decisions

If `projects/<project>.yaml` lists a `canonical_decision`, treat it as binding
unless the human explicitly opens it for reconsideration. "Should we use JAX or
Mojo?" was settled in `differentiable-astrodynamics.yaml`. Don't re-pitch the
alternative unless asked.

### Do not silently expand scope

If the human asks about MCPI hot-start logic, answer about MCPI hot-start
logic. Do not also pull in the differentiable substrate or the JAX roadmap
because they're "related." Stay scoped to the question.

---

## How to keep this archive useful over time

When the state of a project changes during a session — a decision is reversed,
a gap is closed, a new monograph extends an existing one — **update the project
YAML in the same session**, with the `last_updated` date bumped. The protocol
is in `projects/README.md`.

When the human imports a new monograph (from a Claude, ChatGPT, or Gemini
conversation), follow the import workflow in `projects/README.md`. The minimum
artifacts are: the source document (PDF or markdown), a short summary
paragraph, and a metadata stub that lets the vault wire it in.

If you find yourself wanting to add a lot of structure — a deeply nested
folder hierarchy, a complex YAML schema, an elaborate cross-reference system —
**resist**. The simplest layout that works is the one to ship. Extra structure
costs maintenance and provides marginal benefit. Every architectural addition
to this archive should justify itself against the question: *does this help a
future LLM enter a session faster, with less context flooding, while still
giving the human the information they need?*

If the answer isn't a clear yes, don't add it.

---

## What this repo is, in one sentence

A small archive of long-form technical monographs, deliberately structured so
that future LLMs can enter productive working sessions on the underlying
projects without flooding their context with stale or irrelevant material.

Everything in the structure exists to serve that goal. If something in the
structure stops serving that goal, change it.

---

## Provenance

This protocol was designed in May 2026 by the human maintainer in conversation
with Claude. It supersedes the implicit "load everything you can" pattern that
LLMs default to. The full discussion of why this is the right design is in the
conversation transcript that produced this file; the short version is in the
"Failure mode this prevents" section above.

If you are an LLM and you have read this far: you have the orientation you
need. Now ask the human what they're working on, and read at most one project
YAML before answering.
