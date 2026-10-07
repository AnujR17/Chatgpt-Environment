# Digital Cheque — Target Case-Study Structure (Ideal-State Content Plan)
*The intended shape of the finished 13-stage case study: what SHOULD exist when done, independent of current progress. Not an executed record; nothing here is claimed as complete. Governed by planning/04 (framework) and planning/05 (reference pack).*

*Drafted 2026-09-23. Decisions this draft follows (from the user):*
- *Methods are chosen on fit alone. Sharing a method with My Alumnus is acceptable for this project.*
- *No cross-check against other projects' ledgers.*
- *Research requirements below are the **ideal** scope. The user will scale them down if time or access forces it.*
- *Role / team framing for the Overview is deferred.*

---

## Why this project is shaped differently

- **It is a service system, not an app.** A cheque is a promise between two people, processed by banks and enforced by courts. The case study proves the system logic (legal backbone, lifecycle, risk ownership) before showing screens.
- **Two-sided by nature.** Payer and payee need opposite things from the same instrument. Research is run in payer–payee **dyads** (both sides of one real relationship).
- **Law is a design material.** A legal track runs alongside the design track, with expert check-points at Define and Testing. Every claim keeps an evidence label: Statutory / Regulatory / Industry practice / Secondary finding / Hypothesis / Validated.
- **One pivotal decision point.** Which legal backbone the concept rests on: (A) bank-issued e-cheque under NI Act s.6, (B) payer-to-payee mandate relying on PSS Act 2007 s.25, or (C) a commitment layer wrapped around existing rails. This is the case study's main problem–solution pair.
- **Failure can't be tested live.** Dishonour, notices and courts are simulated, not staged with real money.

---

## The 13 stages

1. **Overview** `[Rec]` — Domain (fintech / legal-tech service design, India), role *(deferred — user to confirm solo/team)*, tools, M.Des Interaction Design context.

2. **Brief** `[Rec]` — 1–2 lines: a digital way to make, hold, track and enforce a future-dated promise to pay, carrying a cheque's trust and legal weight without its paper, delays and litigation burden.

3. **Problem** `[Rec]` — **Split with Define (justified).** Problem states what is observable: cheques are a small share of payment volume but still carry high-value, high-stakes payments; bounce litigation is a major share of trial-court pendency; no digital rail offers a person-to-person, future-dated, payee-holdable commitment. The *causal* claim (payees drive cheque demand for legal leverage) is still a hypothesis, so it is refined in Define only after primary research tests it.

4. **Research**
   - *Primary*: Interviews `#66` *(exempt)* in payer–payee dyads + expert interviews; Directed Storytelling `#42` ("walk me through your last cheque"); Critical Incident Technique `#29` (bounce and near-bounce stories); Contextual Inquiry `#26` (MSME month-end payment routines in shop/office); Fly-on-the-Wall Observation `#55` (bank branch cheque counter / drop-box); Personal Inventories `#81` (cheque registers, post-dated cheque bundles, return memos, legal notices — anonymised); Surveys `#104` *(exempt)* to size patterns across segments.
   - *Secondary*: Secondary Research `#93` *(exempt)*; Literature Reviews `#71` *(exempt)* (NI Act, PSS Act, RBI circulars, payments literature); Content Analysis `#23` (Section 138 judgments and Supreme Court guidelines); Horizon Scanning `#62` (cheque clearing phases, court digitisation, e-cheque status); Gap Analysis `#57` (cheque functions × digital rails); Artifact Analysis `#4` (paper cheque, return memo, Positive Pay flows in bank apps).

5. **Insights** — Affinity Diagramming `#3`; Laddering `#70` ("why a cheque?" → assurance → enforceability — separates real needs from assumptions); Mental Model Diagrams `#73` (payer vs payee model of "a promise to pay"); CSD Matrix `[D]` (certainties / suppositions / doubts, tied to the hypothesis list); Service Blueprint `#95` — current state, front stage (payer/payee) to back stage (banks, clearing) to support (courts); Stakeholder Maps `#101`; Journey Map `[D]` *(exempt)* current-state, per segment; Empathy Map `#45` *(budget-limited — optional; only if the payee persona needs it)*.

6. **Define** — Persona `[D]` *(exempt)* built as payer–payee pairs for the primary segment (MSME buyer–supplier) and secondary (tenant–landlord); refined Problem Statement; Jobs-to-be-done `[Own]`; Kano Analysis `#68` (must-be vs performance vs delighter capabilities of a digital cheque); Value Opportunity Analysis `#120`; Feasibility/Desirability/Viability Scorecard `[D]` with *legal* feasibility scored explicitly. **Legal checkpoint 1:** advocate reviews the refined problem and constraints list.

7. **Ideation** — How Might We `#63` (from the opportunity areas); Metaphors `#74` (IOU, escrow, promissory note, locker — what *is* a digital cheque?); Creative Matrix `#27` (segments × opportunity areas); Scenarios `#92` (dual-cited as User Flow `[D]` where drawn as a flow); Role-playing `#90` (enacting the handover and holding of a promise); Storyboards `#103`; Design Workshops `#39` / Participatory Design `#80` with 4–6 MSME owners; Backcasting `#6` (from a future where paper cheques are retired). **Decision point:** concept direction A / B / C chosen with a Weighted Matrix `#123`, alternatives documented with reasons for rejection.

8. **Design** — Future-state Service Blueprint `#95`; instrument state model `[Own] — new, to be created` (issued → accepted → due → presented → paid / failed → notice → settled / escalated); Information Architecture per role; User Flow / Wireflow / Wireframe / Mockup / Prototype `[D]`; Design System `[D]`. `[Dom]` B2B / multi-role convention — payer, payee and bank/admin views documented and justified separately. `[Dom]` fintech/legal-tech convention *— to be added to Reference 3 after verification (candidate sources: RBI digital payment security directions, India's 2023 dark-patterns guidelines; neither verified yet)*.

9. **Testing** — Usability Testing `#118` with Think-aloud Protocol `#109`; Wizard of Oz `#124` (faked bank back end so issuing, holding and failure feel real); Simulations `#98` / Experience Prototyping `#49` (a simulated bounce, notice and settlement path); Stakeholder Walkthrough `#102` (advocate + bank officer check whether the records would stand up); Heuristic Evaluation `#60`; Semantic Differential `#94` (does it feel formal/binding enough vs casual like UPI?). **Legal checkpoint 2** sits here.

10. **Outcome** `[Rec]` — Prototype proof, KPIs `#69` *(exempt)* (task success, trust score change, error recovery on the failure path), Usability Report `[D]` *(exempt)*. No deployment claims.

11. **Future Scope** `[Rec]` — Bank / NPCI pilot path, regulatory recommendations via Civic Design & Policy `#17`, expansion to institutional and lending segments.

12. **Limitations** `[Rec]` — No live bank or payment-network integration; legal analysis is research, not legal validation; sample drawn from Gujarat; failure paths simulated, not observed live.

13. **Learnings** `[Rec]` — Reserved for the project owner's own voice only. Never drafted on their behalf.

---

## Ideal research requirements (to be scaled down by the user if needed)

| Activity | Ideal scope | Why this size |
| --- | --- | --- |
| Dyad interviews — MSME buyer + supplier (primary segment) | 6 pairs = 12 people | Enough for patterns to repeat within one fairly uniform group; a widely cited study (Guest et al., 2006) found most themes emerge within ~12 interviews |
| Dyad interviews — tenant + landlord (secondary segment) | 3 pairs = 6 people | Tests whether the payee-leverage pattern holds outside business credit |
| Individual interviews — large person-to-person payments | 3 people | Checks the high-value, one-off case |
| Individual interviews — lenders (NBFC / informal) | 2 people | Security-cheque practice from the demanding side |
| Expert interviews | 5: s.138 advocate, bank branch/ops officer, chartered accountant, NBFC collections staff, fintech product person | Legal, bank-process and business-accounting constraints |
| Contextual inquiry | 4–6 MSME sessions (ideally at month-end) | Observe real payment routines, not recalled ones |
| Bank branch observation | 2 sessions | Stages 4–8 of the lifecycle in person |
| Artefact collection | 20+ anonymised items | Evidence for registers, post-dated bundles, return memos, notices |
| Survey | ~150 responses across segments | Size the patterns found in interviews; allows rough segment splits |
| Content analysis — judgments | 30–50 s.138 judgments | Recurring evidence and timing failures that records could fix |
| Participatory workshop | 1 session, 4–6 MSME owners | Co-create concept directions with the primary segment |
| Usability testing | 2 rounds × (5 payers + 5 payees) = 20 sessions | ~5 users per group per round finds most issues; two rounds show improvement |
| Stakeholder walkthrough | 2 experts (advocate + banker) | Checks whether records hold up for the "invisible users" |

**Ideal timeline: about 16 weeks.**

| Weeks | Phase |
| --- | --- |
| 1–2 | Secondary + legal research, ethics, recruitment (partly done in the Foundation Analysis doc) |
| 3–6 | Primary research: dyads, experts, contextual inquiry, branch observation, artefacts, survey |
| 7–8 | Synthesis and Define; legal checkpoint 1 |
| 9–10 | Ideation, workshop, concept decision A/B/C |
| 11–12 | Service architecture, state model, flows, wireframes |
| 13–15 | Prototype, test round 1, iterate, test round 2; legal checkpoint 2 |
| 16 | Outcome, write-up |

Ethics: no account numbers or unredacted cheques collected; names anonymised in all notes; consent for recordings.

---

## Projected methods list (not locked — nothing executed yet)

Directed Storytelling `#42`, Critical Incident Technique `#29`, Contextual Inquiry `#26`, Fly-on-the-Wall Observation `#55`, Personal Inventories `#81`, Content Analysis `#23`, Horizon Scanning `#62`, Gap Analysis `#57`, Artifact Analysis `#4`, Affinity Diagramming `#3`, Laddering `#70`, Mental Model Diagrams `#73`, Service Blueprint `#95`, Stakeholder Maps `#101`, Kano Analysis `#68`, Value Opportunity Analysis `#120`, How Might We `#63`, Metaphors `#74`, Creative Matrix `#27`, Scenarios `#92`, Role-playing `#90`, Storyboards `#103`, Design Workshops `#39`, Participatory Design `#80`, Backcasting `#6`, Weighted Matrix `#123`, Usability Testing `#118`, Think-aloud Protocol `#109`, Wizard of Oz `#124`, Simulations `#98`, Experience Prototyping `#49`, Stakeholder Walkthrough `#102`, Heuristic Evaluation `#60`, Semantic Differential `#94`, Civic Design & Policy `#17`.

*Shared with My Alumnus's projected list by user decision:* Contextual Inquiry, Gap Analysis, Artifact Analysis, Affinity Diagramming, Mental Model Diagrams, Value Opportunity Analysis, How Might We, Scenarios, Usability Testing, Think-aloud Protocol, Heuristic Evaluation, Simulations.

Budget-tracked: Empathy Map `#45` — optional here; use only if the payee persona needs it.

*All `#N` numbers checked against the 125-method list in planning/05.*

---

## Open items
- [ ] Overview role (solo / team) — user to confirm later.
- [ ] Draft and verify a fintech / legal-tech `[Dom]` entry for Reference 3.
- [ ] User to confirm or scale down the ideal research requirements.
- [ ] Legal open questions carried from the Foundation Analysis doc (future-dated instrument vs "payable on demand"; acceptable signature standard; NI Act vs PSS Act route).

## Source material audited so far
- Digital Cheque — Foundation Analysis (Claude Doc, 2026-09-23): secondary research only.
- No primary research exists yet.
