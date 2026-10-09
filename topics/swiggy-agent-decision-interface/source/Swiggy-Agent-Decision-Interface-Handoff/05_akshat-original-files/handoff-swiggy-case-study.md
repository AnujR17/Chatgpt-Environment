# active-memory handoff: Swiggy Support Agent Decision Interface case study

**Handoff #1** · 2026-10-05 · Lineage: #1 (2026-10-05): Stage 4 Research completed (literature review, artifact analysis, gap analysis, simulated expert interview + independent verification); Customer Experience Audit started but not filed.

## 0. Instructions for Claude (read first)

You are continuing work from a previous chat. That chat is gone; this file is the complete context and the source of truth.

1. Read this whole file before replying.
2. Follow sections 3 (Style), 4 (Hard rules) and 5 (Corrections) in every reply, for the rest of this chat. They override your defaults.
3. Use the values in section 8 exactly. Never round, re-estimate, or "correct" them.
4. Do not suggest anything listed in section 7 (Changed / rejected) again unless the user brings it up.
5. Code word: None active.
6. Your first reply: at most 5 lines covering the goal, the current state, and the next step (section 11). Mention any files from section 13 that were not attached. Ask the questions in section 12 if there are any. End with "Ready to continue with <next step>?" Then wait for the user's go.

## 1. Mission
- **Goal:** Build the "Swiggy Support Agent Decision Interface" case study for Akshat's placement portfolio: a hypothetical order-centred agent panel for Swiggy support staff reviewing refund disputes, showing policy conditions, incident evidence, and customer/restaurant/delivery-partner histories.
- **Done looks like:** A complete 13-stage case study (Overview through Learnings) plus a Case Study (short) and Documentation (detailed) doc, feeding the portfolio website.
- **Why it matters / context:** 7-day sprint, deadline Tue 6 Oct 2026. This session covered the back half of Stage 4 (Research) and started the Customer Experience Audit.

## 2. About the user (as relevant to this work)
- Akshat Panchasara, MDes Intelligent User Experience Design (IUxD) student, Dhirubhai Ambani University (DAU), Gandhinagar, around Semester 3.
- Building a placement portfolio spanning UX research, interaction design, data visualization, AI-enabled design.
- Session attached to a claude.ai Project called "Portfolio" that holds docs for this and other projects (MedAssist, Digital Cheque, etc.).

## 3. Style & communication
- **Language:** English.
- **Tone:** Blunt, critical, direct. Not agreeable by default.
- **Reply length:** Short, crisp, to the point.
- **Formatting:** Bullet points with proper indentation. No em-dashes anywhere, ever.
- **Working style:** Check current date/time before executing. Check skills before answering and use the relevant one. Ask necessary clarifying questions before execution, but don't over-ask once answers are already supplied. Keep tabs on the user's in-progress tasks.
- **Avoid:** Em-dashes. Automatic agreement. Treating self-written verification as sufficient when independent verification is possible.

## 4. Hard rules (word for word)
1. "never mention Oro Innovations in any context, response, or output, not in code, websites, documents, or conversation" (user's standing memory preference)
2. "No use of em-dashes." (project instruction, applies to every output)
3. "Keep the answers short, crisp and to-the-point."
4. "Ask necessary and relevant questions every time before execution in order to get proper context."
5. "Before giving an answer, check skills and use the necessary ones for the task at hand."
6. "Before the execution, get the current time and date in order to establish a good flow of work as per schedule."
7. "Keep tabs on me by asking questions on updates of a task at hand or something that I mention I am working upon."
8. "Save the files/links that are I share as per the type of thing it is." (e.g. a Behance case study goes to reference, a class presentation goes to notes)
9. "It is not necessary to say 'yes' in every question or response, do critical thinking and be blunt. Be straight-forward and question every thing I say. No need to agree in everything."
10. Swiggy panel design rules (hard constraints on the concept itself): show facts and policy conditions only; NO verdicts, scores, or predictions of customer/restaurant/delivery-partner intent; every screen element labelled data, insight, or decision-support; every assumption explicitly labelled; no "value tier" or "fraud user" flag of any kind; the whole concept is framed as hypothetical, since Swiggy already has a real Agent Workbench this project has no access to.

## 5. Corrections log
| # | Claude did | The user wanted |
|---|---|---|
| 1 | Read "use the Amex profile for the interview" as a proposal to switch the entire case-study domain to Amex | Domain stays Swiggy always. Amex is only the simulated expert's background knowledge, used if public Amex data is strong enough. |
| 2 | Spawned 2 live subagents (one as Expert, one as Interviewer) per direct instruction, to run the interview as a real back-and-forth | Mechanism is structurally broken here: subagent hand-off only returns a summary, never verbatim tagged text. Abandoned after Q1, flagged to user, interview written directly by Claude in one pass under the same locked profile instead. |
| 3 | Wrote my own inline "Verification Log" for the interview transcript (claimed 46/48 supported, 0 missed) | Self-grading was weaker than it should be: missed 2 real citation errors. An independent subagent, that had not seen the transcript being written, re-checked every claim against the source files and caught both. |
| 4 | Independent verifier's own output file (`swiggy-expert-interview-verification.md`) contained 11 em-dashes | Project rule is zero em-dashes everywhere. Manually rewritten with commas/semicolons/periods before saving or sending. |
| 5 | Treated a Oct-5 voice-memo PDF as more Customer Experience Audit detail on the same Entity 1 | Transcript was badly garbled (large Hindi portions dropped) and described a different sequence of events than the Oct-1 text account. User told Claude to ignore that file for this handoff. Not reconciled; still open. |

## 6. Decisions
| Decision | Why |
|---|---|
| Combined expert profile (card-dispute ops, Amex-style, plus marketplace trust-and-safety) instead of a pure Amex persona | A pure Amex persona only covers 2 of 3 parties (no courier/delivery-partner angle); Amex's own internal agent screen isn't public either, so a pure-Amex persona gains nothing over the combined one. |
| Real expert interview replaced with a "Simulated Expert Interview (source-grounded)" | Original expert (ex-Amex dashboard designer) interview was cancelled. Every claim in the simulated version is tagged to a real source file or marked [Not known publicly] / [Simulated reasoning]; never presented as a real interview. |
| Interview written directly by Claude, not via live 2-subagent relay | Subagent hand-off mechanism only returns summaries; incompatible with "no paraphrase, every claim exactly tagged" requirement. Subagent use kept for the one-shot independent verification pass only (no live-reply problem there). |
| Independent verification (fresh subagent, hadn't seen the transcript being written) governs over Claude's own inline check | Matches the project's own stated principle (seen in gap analysis and literature review) that self-grading is weaker than blind verification. |
| Teammate's `swiggy-cross-party-evidence-research.md` errors (D2-D6) NOT corrected yet | Not Claude's file to edit without explicit go-ahead. Asked twice, no answer yet. |

## 7. Changed / rejected
- Real interview with ex-Amex dashboard designer → cancelled → replaced with simulated, source-grounded interview (expert unavailable).
- Switch entire case-study domain to Amex → rejected by user; domain stays Swiggy, Amex only informs the simulated persona.
- Live 2-subagent interview relay (Expert agent + Interviewer agent conversing) → abandoned after Q1 (architectural limitation) → direct single-pass authorship by Claude, same locked rules.
- ❌ Claude's own first-draft "Verification Log" (46/48 supported, 2 partly supported, missed 2 real errors) → replaced with the independent verifier's results (39/43 supported, 2 partly supported, 0 unsupported, correctly flagging the 2 citation errors the inline check missed).

## 8. Data & facts (exact)

**Sprint:** 7-day sprint, deadline Tue 6 Oct 2026. This handoff written Mon 5 Oct 2026, 20:08 IST.

**13-stage case study framework:** Overview, Brief, Problem, Research, Insights, Define, Ideation, Design, Testing, Outcome, Future Scope, Limitations, Learnings. Currently in **Stage 4 (Research)**.

**Stage 4 sub-methods:**
| Method | ID | Status |
|---|---|---|
| Secondary Research | #93 | Done (earlier session) |
| Literature Review | #71 | Done, this session |
| Artifact Analysis | #4 | Done, this session |
| Gap Analysis | #57 | Done, this session |
| Expert Interview | #66 | Cancelled, replaced by Simulated Expert Interview, done this session |
| Customer Experience Audit | #33 | Started, not filed (Entity 1 pending clarification) |

**Literature review: 5 papers, load-bearing numbers, cite exactly as follows:**
| Paper | Key citable finding | Do not cite |
|---|---|---|
| Parasuraman & Manzey (2010), *Human Factors* 52(3) | Automation bias "cannot be prevented by training or instructions," occurs in naive and expert users alike | The 82%/33% failure-detection figure (abstract-only read, not verified) |
| Lee & See (2004), *Human Factors* 46(1) | "Functional specificity": trust must be calibrated per component, not globally |  |
| Buçinca et al. (2021), arXiv:2102.09692, N=199 | Cognitive forcing cut overreliance on wrong AI answers from 64% to 48% (p=.003); rated less preferred |  |
| Bansal et al. (2021), arXiv:2006.14779, 1,626 participants, 3 tasks | "Explanations increased the chance that humans will accept the AI's recommendation, regardless of its correctness" |  |
| Brynjolfsson, Li & Raymond (2023), NBER w31161, 5,179 agents | AI reply-suggestion tool: +34% resolutions/hour for novices (+46% for <1 month tenure), "minimal impact" on experienced agents, 38% average adherence |  |

**Artifact analysis:** 8 artifacts (A1 Amex merchant dispute case view, A2 Amex chargeback reason codes, A3 Zendesk Agent Workspace, A4 Kustomer unified workspace, A5 Uber Eats order errors, A6 DoorDash missing items, A7 Fini refund audit log, A8 Uber Direct proof of delivery) scored against 8 project design rules. **No interface meets more than 3 of 8 rules; A2 (a policy doc, not a screen) is the best at 5 of 8.**

**Gap analysis:** Type A (not public) 12 gaps, Type B (not yet searched) 11 gaps, Type C (contradiction) 5 gaps, Type D (weak evidence in use) 12 gaps (includes D2-D6, 5 uncorrected errors in teammate's file), Type E (method gap) 5 gaps.

**Simulated expert interview:** 16 questions across 5 parts, persona "Expert S1 (simulated)." Independent verification: of 43 tagged `[Source: ...]` claims, **39 SUPPORTED, 2 PARTLY SUPPORTED, 0 UNSUPPORTED**. All 9 `[Not known publicly]` tags confirmed genuine (map to gaps A1, A3, A4, A7, A9). No smuggled verdicts/scores/predictions found.

**The 2 citation errors found and fixed in the transcript:**
1. Q3 (Instamart AI-edited cracked-egg photo): was tagged "citing Business Standard" → corrected to "citing Business Today and The Logical Indian."
2. Q12 (Zomato CEO quote "can never be fully right"): was tagged "cross-party evidence research file, citing...India News Network" → corrected to "deep research report, citing Exchange4media."

**Customer Experience Audit, Entity 1 (as told in text on 1 Oct 2026, not yet written into a doc):**
- Created a new Swiggy account.
- Registered 3 fake complaints on 3 separate orders (small portions, damaged products, other), all 3 refunded.
- About a month later, a genuine problem occurred: no appropriate response or refund.
- About 10-11 days after that, another genuine problem: refund declined via email.
- Tagged as **Primary (self-administered test), N=1**, not Anecdotal, since Akshat ran it himself. Still only one data point, one account, one city, one app version.

**Still-open blocker on Entity 1:** approximate/exact dates for all 5 events, exact or remembered wording of the decline email, whether account/device/payment method changed between the fake and genuine claims, whether the account was ever blocked/warned/restricted, total number of entities planned for the audit.

**Security issue flagged, not confirmed resolved:** the `llm-council` skill's documented `.env` example contains exposed plaintext API keys (`OPENAI_API_KEY=sk-proj-...`, `GEMINI_API_KEY=AQ...`). User has not confirmed rotation.

## 9. People, terms & names
- **People:** Akshat Panchasara, owner of this work (MDes IUxD student). A teammate (unnamed) authored `swiggy-cross-party-evidence-research.md`, which has known uncorrected errors.
- **Terms & nicknames:** "Expert S1" = the simulated composite interview persona. "Simulated Expert Interview (source-grounded)" = the required exact label for Stage 4's interview, must never be called a real interview. "Not known publicly" = the exact tag for a confirmed public-data gap.
- **Names in use:** File naming convention in the Portfolio project is `Documentation/Swiggy - <Title>`. Device folder is `D:\DAIICT\Projects\Swiggy Dashboard\`. Working filename stem is `swiggy-<topic>.md` (lowercase, hyphenated).

## 10. Work state
| Item | Status | Version / location | Notes |
|---|---|---|---|
| Literature Review | Final | `Documentation/Swiggy - Literature Review` + device + `/home/claude/` | 5 papers, see section 8 |
| Artifact Analysis | Final | `Documentation/Swiggy - Artifact Analysis` + device | 8 artifacts, A1-A8 |
| Gap Analysis | Final | `Documentation/Swiggy - Gap Analysis` + device | A-E gap types |
| Simulated Expert Profile | Locked | `Documentation/Swiggy - Simulated Expert Profile` + device | Governs the interview's rules and 16-question guide |
| Simulated Expert Interview Transcript | Final, verified | `Documentation/Swiggy - Simulated Expert Interview Transcript` + device | 2 citation fixes applied; 0 em-dashes confirmed |
| Expert Interview Verification | Final | `Documentation/Swiggy - Expert Interview Verification` + device | 11 em-dashes manually fixed before delivery |
| Customer Experience Audit | Not started as a doc | None yet | Entity 1 data supplied in chat, blocked on user answers (section 8, section 12) |
| Teammate's cross-party-evidence file corrections (D2-D6) | Not done | `swiggy-cross-party-evidence-research.md` (device only) | Blocked on user permission |

## 11. Next steps
1. **Next action:** Get the Entity 1 clarifications (exact/approx dates, decline email wording, account/device consistency, block status, total planned entity count), then write `Documentation/Swiggy - Customer Experience Audit`.
2. Reconcile or discard the Oct-5 garbled voice-memo PDF against the Oct-1 text account of Entity 1 (set aside this session per user instruction, still unresolved).
3. Get explicit permission to correct D2-D6 in the teammate's `swiggy-cross-party-evidence-research.md`.
4. Confirm whether the exposed OpenAI/Gemini API keys in the `llm-council` skill file have been rotated.
5. Once the audit is filed, move to Stage 5 (Insights / affinity diagram) and Stage 6 (Define).

## 12. Open questions ⚠️
- Permission to correct the teammate's file (D2-D6 errors): yes/no, still unanswered after being asked twice.
- Customer Experience Audit: exact dates for the 5 Entity 1 events, exact/remembered decline email wording, device/account consistency, block status, and total planned entity count.
- Whether the Oct-5 voice-memo PDF is a replacement, a second separate test, or the same event told differently; unresolved, set aside for this handoff.
- Whether the exposed API keys in `llm-council`'s `.env` example have been rotated.

## 13. Re-attach checklist
- [ ] `swiggy-cross-party-evidence-research.md`: only on the device (`D:\DAIICT\Projects\Swiggy Dashboard\`), not in the Portfolio project docs. Needed if the new chat is not device-linked and must correct D2-D6.
- [ ] `swiggy-refund-and-blocking-rules-research.md`: same, device only, needed for any further audit or refund-policy work if not device-linked.
- [ ] `swiggy_evidence-based_research.md`: same, device only, the 53KB deep research report underlying most citations.

---
<sub>Audit: 13/13 sections · 10 rules · 5 corrections · 1 open discrepancy noted · secrets removed: none found (API keys mentioned are already flagged to the user, not reproduced here) · generated by active-memory</sub>
