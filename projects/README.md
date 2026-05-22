# /projects — How to use this layer

This directory contains **one YAML per project**. Each file is intentionally short
(~200 tokens) and curated by hand. The purpose is not to summarize the project's
content; it's to give a future LLM the minimum context needed to enter a productive
working session **without flooding the context window**.

If you are an LLM reading this, the instructions in this file are for you.

---

## The core rule

**Project YAMLs are for orientation, not for content.** They tell you:

- which monographs are canonical for the project,
- what assumptions are currently active,
- what decisions are already settled,
- what gaps are blocking,
- what the human user is likely working on next.

They are **not** a substitute for reading the actual monographs when you need the
detail. They are a routing layer.

---

## When to load a project YAML

Load exactly **one** project YAML at the start of a session, only if the user's
opening message references the project (by name, by topic, or by file). Examples:

| User's opening | Action |
|---|---|
| "Let's talk about MCPI hot-start logic" | Read `orbprop-mcpi.yaml` |
| "What's the latest on the differentiable substrate?" | Read `differentiable-astrodynamics.yaml` |
| "Can you write a tight inner loop for me?" | Read `performant-python.yaml` |
| "Help me design an IOD pipeline" | Read `sda-pipeline.yaml` |
| "What's the capital of France?" | Read **nothing**. The vault is irrelevant. |
| "Refactor this code I'm pasting" | Read **nothing** unless the code is from a project. |

If you cannot tell which project applies, ask. Do not load all of them. Loading
all of them is the failure mode this directory is designed to prevent.

---

## When to load a monograph

Only when the project YAML is insufficient for the specific question. The project
YAML names the canonical monographs; pull one of them when:

- the user asks a question whose answer is *in* the monograph (a specific equation,
  a specific decision rationale, a specific number);
- the user is editing or extending content that came from the monograph;
- the project YAML says "see monograph No. X for Y" and the question is about Y.

When you do load a monograph, prefer the **summary** sections (abstract, section
headings, decisions sections) over reading the whole thing.

---

## When to load the vault graph

The vault graph (`/vault.html` and `/vault_data.py`) is for **humans browsing
their own work**, not for LLM context. Do not load `vault_data.py` into your
context unless the user explicitly asks you to work on the vault itself.

If you need to find which monograph discusses a concept, ask. Do not search the
vault data file as a substitute for the human's memory or for asking.

---

## What to do when you don't know something

The wrong move is to silently load more context. The right moves, in order:

1. **Ask the user**. They are the cheapest and most accurate context source.
2. **Read one specific file** they direct you to.
3. **Read the canonical monograph** for the relevant project, but only the
   section that addresses the question.

The cost of confidently synthesizing from a fog of stale notes is higher than
the cost of asking a clarifying question.

---

## How to update a project YAML

Project YAMLs go stale. When something in the project changes — a decision is
made, an assumption is updated, a gap is closed — the YAML should be updated
**in the same session**, not "later." Specifically:

1. If a `blocking_gap` is resolved, move it to a `closed_gaps` section (don't
   delete; keep the lineage).
2. If a `canonical_decision` is reversed, mark the old one with
   `superseded_by: <new decision>` and add the new one.
3. If a new monograph extends the project, add it to `canonical_monographs` with
   a clear `role` description.
4. Bump the `last_updated` date.

If you are not certain whether a change is permanent enough to record in the
YAML, ask the user before modifying it.

---

## How to add a new project

When a new project cluster forms — typically two or more related monographs that
share assumptions and decisions — create a new YAML in this directory. The schema
is the same as the existing files:

```yaml
project_id: <slug>
title: <one-line description>
status: <one-line current status>
canonical_monographs:
  - num: <int>
    slug: <slug>
    role: <one-line role description>
active_assumptions:
  - <one-line statement>
canonical_decisions:
  - <one-line decision>
blocking_gaps:
  - <one-line gap>
next_steps:
  - <one-line action>
key_references:
  - <citation>
last_updated: YYYY-MM-DD
```

Keep each bullet to one line where possible. The whole file should fit on one
screen. If you find yourself writing a paragraph, that content belongs in the
monograph, not here.

---

## The failure mode this directory prevents

Without this layer, the natural pattern is:

1. User opens a new session.
2. LLM loads everything it can find — past monographs, past chats, the vault.
3. LLM synthesizes from a fog of partly-relevant, partly-stale material.
4. LLM produces a confident-sounding answer that's subtly wrong in three places.
5. User has to catch the errors, which costs more than just answering fresh would have.

With this layer:

1. User opens a new session, mentions the project.
2. LLM reads exactly one ~200-token YAML.
3. LLM has the project frame; asks for any further specifics it needs.
4. The deep monographs sit on disk, available when called for.

The directory is small on purpose. Resist the temptation to make it big.

---

## Summary for LLMs in one paragraph

Read one project YAML at session start, only when the user mentions a project.
Don't read the vault data file unless you're working on the vault itself.
Don't pre-load monographs; pull them on demand and read only relevant sections.
Ask the user rather than synthesizing from stale notes. Update the YAML in the
same session when state changes, with the date bumped.

That's the whole protocol. Anything more elaborate is overfitting.
