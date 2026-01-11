# Tech Blog Agentic AI

## Project Overview
Tech Blog Agentic AI is a canonical-first content automation system built in Python.

The system takes one canonical article (plain text) as the single source of truth and generates:
- Blogger-ready HTML
- WordPress (Gutenberg) compatible HTML
- Image placeholders with ALT logic
- SEO metadata package

No content rewriting or regeneration occurs after the canonical article is defined.

---

## Core Design Principle
Canonical Immutability

Once the canonical article is written, it is never modified.
All outputs are deterministic transformations of the same source.

This prevents:
- SEO dilution
- Content drift
- Editorial inconsistencies

---

## High-Level Architecture

canonical_article.txt
        ↓
     run_agent.py
        ↓
+------------------+
|   renderer.py    | → blogger.html
|                  | → wordpress.html
+------------------+
        ↓
seo_generator.py → seo_package.json

---

## Execution Flow

1. Write the canonical article:
input/canonical_article.txt

2. Run the pipeline:
python run_agent.py

3. The system generates CMS-ready outputs automatically.

---

## Output Structure

output/
├── canonical_article.txt
├── blogger.html
├── wordpress.html
└── seo_package.json

Each output is generated directly from the canonical article
without modifying the source content.

---

## Why This Project Exists
Most AI content tools rewrite content multiple times,
causing SEO instability and editorial problems.

This project enforces:
- Single source of truth
- Predictable publishing output
- CMS-safe automation

---

## Tech Stack
- Python
- File-based pipeline
- Deterministic HTML rendering
- SEO metadata generation

---

## Intended Use Cases
- SEO-safe blog automation
- Blogger & WordPress publishing
- Content teams requiring editorial discipline
- Canonical-first AI workflows

---

## Key Learnings
- Canonical-first architecture is critical for SEO
- Separation of content and presentation simplifies automation
- Deterministic pipelines are safer than generative rewrites
