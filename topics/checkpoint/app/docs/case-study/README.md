# Checkpoint case-study review

Start with the [11-page PDF](Checkpoint-case-study.pdf) or open [the presentation](index.html) from a local checkout. Keep `assets/` alongside the HTML for its native screenshots and bundled DM Sans font. Downloading the repository source preserves that folder layout.

- [Classroom brief and stage mapping](BRIEF-MAPPING.md): project type, subject, theme, CMA, technology, tools, core concepts and Empathize, Define, Ideate, Prototype.
- [Full case study](CASE-STUDY.md): secondary research, simulated personas, decisions, information architecture, real native screens and limits.
- [Feasibility discussion](FEASIBILITY.md): player benefit, scope alternatives, what works and what needs evaluation.
- [Sample session report](sample-session-report.pdf): scripted check-ins and feedback, not a participant result.
- [Native](verification.json), [phone browser](phone-verification.json) and [Windows CI](windows-verification.json) evidence.

Review code lives on `topic/checkpoint-case-study-20261118`; stable OTA remains 0.6.1. The review workflow runs native checks and uploads evidence only. It does not publish a release, update manifest or deploy a site.

Screenshots are actual native Qt captures on Linux using scripted demonstration states. Successful Windows CI separately checks native models, capture and interactions; downloading its screenshot artifact was blocked by the artifact host in this workspace. No physical webcam, real play session or user interview was performed for this review.

To rerun task checks in a development environment with the existing runtime dependencies installed:

```bash
PYTHONPATH=. python scripts/review_session_design.py
```

For the browser bridge check, install Playwright in the development environment and run `scripts/review_design_phone.py`. `CHECKPOINT_BROWSER` optionally selects an installed Chromium executable. These are development checks, not requirements for the packaged app.

The presentation links to the review branch for supporting Markdown and PDF documents. No Behance artwork is reproduced. Its four supplied pages were inaccessible; visual details and creator outcomes are not claimed as inspected.
