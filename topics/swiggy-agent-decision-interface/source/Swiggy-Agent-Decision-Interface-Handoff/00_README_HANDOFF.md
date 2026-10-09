# Swiggy Support Agent Decision Interface: Handoff

**Owner so far:** Sukhmanpreet Singh Saini (M.Des., DAU) · **Handoff date:** 9 Oct 2026
**Where it stands:** Stages 1–7 are done. Stage 8 (Design) is paused, waiting on visual references and approvals.

---

## 1. The project in four lines
- We are designing a concept screen for Swiggy's **escalation agents**: the people who take over a chat from the bot.
- The screen puts the live chat, the order, evidence, each party's history and the relevant policy into one view, so the agent can **decide faster and with less effort**.
- **Core rule: the screen supports the decision; it never makes it.** It shows no verdicts, no predictions, and no scores for customers, restaurants or riders.
- Swiggy's real agent tool and internal rules are not public, so this is a **hypothetical concept**. Its policies are a labelled, frozen working set.

## 2. Read these first, in this order
1. `01_case-study/swiggy-case-study-draft.md`: **the main document.** Stages 1–8 are written up here, with every decision and the reason for it.
2. `03_define-ideate/swiggy-frozen-policy-and-scenarios.md`: the frozen rules (P1–P8), review triggers (T1–T4), the evidence model, and the test scenarios **S1–S7**. All design and testing work runs against this file.
3. `04_design/swiggy-design-approval-checklist.md`: the **open decisions** to work on next.
4. `01_case-study/swiggy-case-study-structure.md`: the 13-stage framework, method choices and sources.

## 3. All files
| Folder | File | What it is |
|---|---|---|
| 01_case-study | swiggy-case-study-draft.md | Running case-study draft, Stages 1–8 |
| 01_case-study | swiggy-case-study-structure.md | 13-stage structure, methods, source log, open items |
| 02_research | swiggy-refund-and-blocking-rules-research.md | Swiggy's refund and account-blocking rules: official, reported, and law |
| 02_research | swiggy-cross-party-evidence-research.md | Restaurant and rider signals, evidence, cross-party precedent (Uber Eats, Zomato, Zepto) |
| 02_research | swiggy-secondary-research-crossverification.md | Check against a teammate's separate research pass |
| 02_research | swiggy-bot-vs-agent-parameters.md | What the bot handles vs. what the human agent handles |
| 02_research | swiggy-expert-interview-guide.md | Questions for the expert interview |
| 02_research | akshat-swiggy-handoff-notes.md | Notes on teammate Akshat's work: simulated interview, audit, literature review |
| 03_define-ideate | swiggy-frozen-policy-and-scenarios.md | Frozen policy v1.1 and scenarios S1–S7 |
| 04_design | swiggy-design-system-research.md | Swiggy brand facts (#FF5200, Salt #FFEDE3, Gilroy) and how peers design internal tools |
| 04_design | swiggy-design-approval-checklist.md | Checklist of visual decisions still open |
| 04_design | agent-panel-references.html | Reference board (open in a browser): layout map and two visual-kit options |
| 04_design | swiggy-refund-signals.html | Early visual summary of refund signals (Sept) |
| 05_akshat-original-files | (14 files) | Teammate Akshat's original handoff folder, unedited. Includes his handoff note, literature review, artifact analysis, gap analysis, the simulated expert profile, transcript and verification, his context file, his copy of the evidence-based research, the audit voice memo (.mp4) and its Hindi transcript (.pdf) |

### About folder 05 (Akshat's files)
- **Kept exactly as he left them.** Where a file name matches one in folders 01–02 (`swiggy-case-study-structure.md`, `swiggy-refund-and-blocking-rules-research.md`, `swiggy-cross-party-evidence-research.md`), **the versions in 01–02 are newer and are the ones to use.** Akshat's copies are older snapshots.
- **His `handoff-swiggy-case-study.md` begins with "Instructions for Claude".** Those were written for his own Claude session. Treat them as background, not as rules for this project.
- **The audit voice memo (.mp4, about 110 s, Hindi and English)** tells a different version of events from his written account. `01_case-study` explains how the two were reconciled.
- **Checked before zipping:** the handoff note *mentions* API keys that were exposed in another tool of his, but the real keys don't appear anywhere in these files.

## 4. Stage status
| # | Stage | Status |
|---|---|---|
| 1 | Overview | Locked |
| 2 | Brief | Locked. Brief covers all issue types; design depth is on refunds and disputes |
| 3 | Problem | Confirmed |
| 4 | Research | Closed: secondary research, literature, artifacts, gaps, a 10-minute expert call (6 Oct), the simulated interview, and audit Entity 1 |
| 5 | Insights | Done: 6 insights (triangulated), mental model, stakeholder map |
| 6 | Define | Drafted: 2 hypothetical personas, point-of-view statements, value analysis, three-layer model, 3 principles |
| 7 | Ideation | Done: admissibility test, matrix of 28 ideas plus 3 borderline, similar-cases spec, user flow, layout choice |
| 8 | Design | **Paused.** Waiting on references; see the checklist |
| 9–13 | Testing → Learnings | Not started |

## 5. Links
- **FigJam board** (mental model, stakeholder map, user flow): https://www.figma.com/board/jdVOYesjFWTQOsQcxnVvV9 *(the owner must give you access)*
- **Reference board, online version:** https://claude.ai/artifact/PV4UoSD64cjSgrzKWnJtoi *(private; the owner must share it from the page's Share menu. A copy is in `04_design/` as HTML.)*

## 6. Do not break these
- **Never present the simulated expert interview as a real one.** Always label it "Simulated Expert Interview (source-grounded)". The real expert input is a single 10-minute call (6 Oct) with a customer-service expert at American Express, described by role only.
- **Audit Entity 1** included complaints that were made up on purpose. The write-up states this openly and carries an ethics line under Limitations. Do not file any more made-up claims.
- **Policies tagged [Borrowed] or [Hypothetical]** must never be presented as Swiggy's real policy.
- **What the screen must never show:** verdicts, risk, trust or value scores, "fraud" labels, a pre-selected outcome, or a guess that the agent is struggling. Every insight has to pass the 6-question admissibility test (Stage 7, step 1).
- **Fairness:** customer, restaurant and rider history use the same format: 90 days, each count shown "out of" total orders, and "Show older" on demand, which is logged.

## 7. What to do next
1. Collect references for the **design approval checklist** (frame size, theme, layout, colour, type, components). The most useful are screenshots of the Swiggy Partner app and the Swiggy Delivery Partner app.
2. Lock the colours, fonts and spacing, then build the **content and layer map** and a **low-fidelity wireframe of scenario S2** inside the chosen desktop frame.
3. Build a **coded HTML prototype** loaded with data for S1–S7 (the owner chose a coded prototype in Stage 1).
4. **Stage 9 tests:** heuristic evaluation plus think-aloud sessions with both personas, measuring time to decision and effort. Things to watch:
   - the "no default outcome" rule in S1;
   - whether agents open "Show older" in S2;
   - anchoring on the similar-cases panel;
   - how a condition and its evidence link across the chat.
5. **Stages 10–13:** outcome, future scope (other issue types, a dispute route for restaurants and riders, a team-lead persona), limitations, learnings.

## 8. To continue with Claude
- Create a Claude Project and upload every `.md` file from this folder.
- Paste these project instructions: act as an interaction-design strategist and critical collaborator for an agent-facing decision-support interface. Separate raw data, derived insight and decision. Insights must be objective and traceable, with no predictions or recommendations. Show policy as conditions checked against facts. Label every assumption. Never invent Swiggy policies or data; use labelled placeholders instead. Compare at least two alternatives for major layout choices. Keep replies concise and in pointers.
