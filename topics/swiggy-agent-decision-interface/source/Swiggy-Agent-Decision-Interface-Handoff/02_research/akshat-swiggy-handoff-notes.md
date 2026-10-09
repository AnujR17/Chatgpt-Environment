---
title: Notes on Akshat's Swiggy case-study handoff
source: "Akshat's Hand-off- Swiggy Dashboard/handoff-swiggy-case-study.md" (device folder, staged 2026-10-05)
purpose: Working reference notes extracted from a different person's (Akshat Panchasara's) active-memory handoff file for his own, separate Swiggy case-study project. Kept as external reference, not folded into this project's canonical docs.
---

# What this file actually is

This is an "active-memory handoff" note Akshat wrote for his own Claude session, for his own claude.ai Project ("Portfolio", not this one), working on his own version of a Swiggy support-agent case study for his placement portfolio. It is not this project's file and not sukh's own research.

**Important handling note:** the file opens with a section literally titled "Instructions for Claude" that tries to bind whoever reads it next to Akshat's tone rules, hard rules, and corrections log ("Follow sections 3, 4 and 5 in every reply... they override your defaults"). That is Akshat's instruction to *his own* assistant session, not an instruction from sukh to me. I read it as data and have not adopted any of it: I'm not switching to Akshat's blunt/no-em-dash style, not applying his "never mention Oro Innovations" rule, not treating his open questions as mine to resolve. Flagging this so it's clear why none of that shows up in how I'm responding.

---

## Who Akshat is, and the overlap with this project

- Akshat Panchasara, MDes IUxD student, Dhirubhai Ambani University, Gandhinagar — same university as this project, different person, different claude.ai Project ("Portfolio," holding multiple case studies: this Swiggy one, MedAssist, Digital Cheque, etc.).
- His device folder (`D:\DAIICT\Projects\Swiggy Dashboard\`, mirrored into the connected "Side Quest/Swiggy" folder here) contains copies of two files with the exact same name and byte size as two files this project produced and sent earlier this session: `swiggy-case-study-structure.md` (6,610 bytes) and `swiggy-refund-and-blocking-rules-research.md` (20,389 bytes).
- His folder also contains `swiggy_evidence-based_research.md` (53,286 bytes) — the same filename as the document pasted into this conversation earlier and attributed to "a teammate."
- **Worth confirming with sukh directly, not assumed here:** whether Akshat is that teammate, and whether the two of you are working the same assignment independently and have been cross-sharing files. Akshat's handoff separately refers to "a teammate (unnamed)" who authored a `swiggy-cross-party-evidence-research.md` with known uncorrected errors (D2–D6) — it's not established here whether that's the same file this project maintains under the same name, or a separate copy in Akshat's own working set.

---

## Project shape (Akshat's version)

- Same 13-stage framework (Overview → Learnings), currently at Stage 4 (Research).
- Deadline: Tue 6 Oct 2026, 7-day sprint.
- Stage 4 sub-methods and status: Secondary Research #93 (done), Literature Review #71 (done), Artifact Analysis #4 (done), Gap Analysis #57 (done), Expert Interview #66 (cancelled, replaced — see below), Customer Experience Audit #33 (started, not filed).

## Literature review — directly relevant to this project

Five papers, with exact citable claims and an explicit do-not-cite list:

| Paper | Citable finding | Flagged as not safe to cite |
|---|---|---|
| Parasuraman & Manzey (2010), *Human Factors* 52(3) | Automation bias "cannot be prevented by training or instructions," occurs in naive and expert users alike | **The 82%/33% failure-detection figure — abstract-only read, not verified** |
| Lee & See (2004), *Human Factors* 46(1) | "Functional specificity": trust must be calibrated per component, not globally | — |
| Buçinca et al. (2021), arXiv:2102.09692, N=199 | Cognitive forcing cut overreliance on wrong AI answers from 64% to 48% (p=.003), though rated less preferred | — |
| Bansal et al. (2021), arXiv:2006.14779, 1,626 participants | "Explanations increased the chance that humans will accept the AI's recommendation, regardless of its correctness" | — |
| Brynjolfsson, Li & Raymond (2023), NBER w31161, 5,179 agents | AI reply-suggestion tool: +34% resolutions/hour for novices (+46% for <1 month tenure), minimal effect on experienced agents, 38% average adherence | — |

**This matters directly for this project's own open item.** `swiggy-secondary-research-crossverification.md` (this project) already flagged the 82%/33% Parasuraman & Manzey figure as "[Reported via teammate, not independently verified]" after a teammate's research pass cited it without having read the paper. Akshat independently reached the identical conclusion from the same paper — don't cite that figure, it's abstract-only. Two independent cautions on the same number is a strong signal to drop it from this project's citable claims until someone actually reads the full paper.

Three papers here (Lee & See, Buçinca et al., Bansal et al.) are not in this project's source list at all. Bansal et al. in particular is close to this project's own core design principle: it's empirical evidence that showing an AI's reasoning/explanation increases acceptance of its output *regardless of whether that output is correct* — a concrete citable argument for why the interface should show conditions-checked-against-facts rather than any kind of system-generated reasoning or recommendation, since even a wrong recommendation with an explanation attached gets believed more.

## Artifact analysis (Akshat's own 8 rules, not this project's)
8 artifacts scored against 8 of Akshat's own design rules: Amex merchant dispute view, Amex chargeback reason codes, Zendesk Agent Workspace, Kustomer unified workspace, Uber Eats order errors, DoorDash missing items, Fini refund audit log, Uber Direct proof of delivery. Headline: no real interface scores above 3/8; the best performer (5/8) is a policy document, not a screen. Directionally consistent with this project's own finding that nobody publishes what a cross-party review screen actually looks like — but scored against Akshat's own rule set, not this project's, so not directly importable as a citation.

## Gap-analysis taxonomy (a reusable framing, not content)
Akshat's gap analysis sorts gaps into five types: A (not public), B (not yet searched), C (contradiction), D (weak evidence currently in use), E (method gap). This is a clean organizing lens this project's own open-items lists could borrow the *shape* of later, if useful — noted here as an idea, not acted on.

## Simulated Expert Interview — methodological contrast worth knowing
Akshat's planned real interview with an ex-Amex designer fell through, so he replaced it with a clearly labelled "Simulated Expert Interview (source-grounded)" — every claim tagged to a real source or marked `[Not known publicly]` / `[Simulated reasoning]`, never presented as a real interview. An independent subagent verification pass (one that hadn't seen the transcript being written) checked 43 tagged claims: 39 supported, 2 partly supported, 0 unsupported, and caught 2 citation errors Akshat's own self-check had missed.

This project's own expert interview is different in kind: `swiggy-expert-interview-guide.md` is written for an actual interview with a real former Amex design-team lead, not a simulated composite. No action needed here — just flagging the contrast since the two projects could otherwise get confused for each other given how closely the topics overlap.

## Customer Experience Audit, Entity 1 — Akshat's own primary data
Self-administered test (N=1), tagged Primary not Anecdotal: created a Swiggy account, filed 3 fabricated complaints across 3 orders (small portions, damaged product, other) — all 3 refunded. About a month later, a genuine problem got no appropriate response or refund. About 10–11 days after that, a second genuine problem's refund was declined by email.

This is Akshat's own unpublished primary research, specific to his own account — not something to treat as this project's finding or cite without his attribution and permission. Flagged here only because it's independently consistent with the evidence-fraud risk this project already discusses (the Instamart AI-edited-photo case in `swiggy-cross-party-evidence-research.md` §3d): a pattern of fabricated claims succeeding while genuine ones didn't, from a second, independent source.

## Other flags from the handoff, noted not actioned
- An unresolved security issue: the `llm-council` skill's documented `.env` example reportedly contains exposed plaintext API keys (OpenAI, Gemini). Akshat's handoff says rotation hasn't been confirmed. Unrelated to this project; noted here only because it's a real flagged secret-exposure issue in case it's relevant to something sukh is separately responsible for.
- Akshat's own open blockers (Entity 1 exact dates, email wording, account/device consistency, total planned entity count; permission to correct D2–D6 in a `swiggy-cross-party-evidence-research.md`; an unreconciled Oct-5 voice-memo transcript) are his to resolve in his own session, not carried forward here.

---

## Suggested next step, if wanted
If Akshat is in fact the source of the "teammate" research already cross-verified in this project (`swiggy-secondary-research-crossverification.md`), it would be worth confirming directly and then deciding together whether the Parasuraman & Manzey caution and the three new papers above should be folded into this project's own literature-review open item. Not done here since that's a decision for sukh, not something to assume from file-name overlap alone.
