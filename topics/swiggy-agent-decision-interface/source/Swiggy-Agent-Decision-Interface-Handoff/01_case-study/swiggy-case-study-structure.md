---
name: swiggy-case-study-structure
description: 13-stage case-study structure for the Swiggy Support Agent Decision Interface (1-week sprint, research-led, no agent access). Read before producing any stage of this case study.
status: structure agreed in principle; problem statement confirmed and methods reshuffled 2026-09-28; secondary research cross-verified against a teammate's independent pass 2026-09-29; no stage content written yet
---

# Swiggy Support Agent Decision Interface: Case-Study Structure

Framework: the 13-stage rulebook and citation legend from the workspace rulebook (file 04) and reference pack (file 05). `#N` numbers were checked against the Reference 1 table in the pack.

## Decisions made with the user
- Sprint project: **about 1 week**.
- Lead with **Research** (Overview carries a 3-line research headline; Research and Insights get the most weight).
- Three-layer model (raw data, derived insight, decision) is a **Define-stage `[Own]` framework**, carried through Ideation and Design.
- Problem is stated in full at stage 3 (no split with Define unless research justifies it).
- Testing and success metrics measure agent **decision time and effort**, never predicted outcomes.
- Framing: Swiggy already has an in-house Agent Workbench (see sources). This is a **hypothetical concept**, not a fix for a known Swiggy flaw.

## Confirmed Problem Statement, 2026-09-28
> Swiggy publicly documents support automation and has disclosed fraud detection, but its current cross-party refund-review workflow is not visible. We propose an order-centred agent panel that brings policy conditions, incident evidence, and appropriately contextualised customer, restaurant, and delivery-partner histories into one review — aiming to reduce investigation effort while protecting genuine claims.

This is the confirmed content for stage 3, verbatim as given, replacing the earlier looser framing ("reduce agent decision time and effort").

**Flag, checked against the core design principle:** "protecting genuine claims" is a fine *outcome* of a faster, better-informed human review — it is not something the interface itself computes. The interface must not score or classify which claims are "genuine"; it stays limited to surfacing traceable facts (policy conditions, evidence, dated history) and lets the agent reach that judgement. Worth restating explicitly in stage 3's assumptions line so this doesn't drift into a fraud-scoring feature later.

**Scope change this adds:** the original framing centred on the customer's side of the decision. This version explicitly widens it to **restaurant and delivery-partner history**, and names "incident evidence" as its own input alongside policy and history. Research for stages 4-5 now needs to cover those two additions, which the earlier secondary-research pass (customer-focused) did not — see the new `swiggy-cross-party-evidence-research.md` doc.

## Method reshuffle, 2026-09-28
**Why:** several methods first picked for stages 5, 6, 7 and 9 (Affinity Diagramming, How Might We, Cognitive Walkthrough, Empathy Map) are the standard defaults of almost any design-thinking course — the kind likely to already appear in other projects in this portfolio.

**Assumption, labelled:** memory holds only short summaries of the other 14-15 projects (a few stated facts each), not their full method ledgers, so an exact duplicate check isn't possible from here. Three projects do explicitly name **Double Diamond** as their process (Bike Dashboard, Drive Wise, MyJio Chatbot) — that's a phase model, not a Reference-1 method, so it sits outside this ledger, but it's flagged here since it's now a repeated choice regardless. No other project's summary names a Reference-1 method that collides with Swiggy's original picks. The reshuffle below is done anyway, on the reasoning that Affinity Diagramming, How Might We, Empathy Map and Cognitive Walkthrough are default enough to be a portfolio-wide repetition risk even where memory doesn't record them by name. **To resolve properly:** check the actual method lists of the finished case studies once they're in hand.

**The "one named method, one project" ledger stays skipped otherwise** — this reshuffle only removes the most generic defaults, it doesn't attempt the full ledger check.

**Swaps made** (old → new, with why the new one fits this project specifically, not just "something different"):

| Stage | Old | New | Why the new pick fits *this* project |
|---|---|---|---|
| Insights | Affinity Diagramming #3 | **Triangulation #115** | The Insights stage's real job here is combining four evidence tiers (Official / Reported / Anecdotal / Inferred) into one trustworthy read — that's what Triangulation names directly. Affinity Diagramming would just be clustering sticky notes that don't exist (no raw field data to cluster). |
| Insights (optional) | Empathy Map #45 | **Stakeholder Map #101** | The research doc's own Section 7 already found three parties a refund decision moves cost between (customer, restaurant, delivery partner) plus the email/fraud team. Mapping those relationships is traceable to the research; an Empathy Map would invent an agent's feelings with no agent access to source them from. |
| Ideation | How Might We #63 | **Creative Matrix #27** | Crosses the agent's actual decisions (the "must-check" conditions in Section 3) against the three interface layers (data / insight / decision support) to generate concepts cell by cell — this reuses the project's own three-layer model instead of a generic prompt format. |
| Testing | Cognitive Walkthrough #19 | **Think-aloud Protocol #109** | The project's own rule is that testing must measure decision *time and effort*, never a predicted outcome. Think-aloud on a peer walking the mock interface produces exactly that — hesitation points, re-reading, backtracking — in a way a step-by-step Cognitive Walkthrough checklist doesn't. |

**Kept as-is, checked and still the right fit:**
- Interviews #66, Secondary Research #93, Literature Reviews #71, KPIs #69, Usability Report — exempt from the no-repeat rule regardless.
- Personas #82 — exempt, and here explicitly hypothetical/assumption-based.
- Customer Experience Audit #33, Artifact Analysis #4, Gap Analysis #57 — specific to this research, not generic defaults.
- Mental Model Diagrams #73 — compares the agent's likely mental model against the policy's actual conditions; stays.
- Value Opportunity Analysis #120 — ties insights to value dimensions before Ideation; stays.
- Scenarios #92 — walks the three named edge cases (first-time user, conflicting signals, permission pending); stays.
- Heuristic Evaluation #60 — evaluated against this project's own neutrality/no-prediction heuristics, not a generic checklist; stays as the other Testing pillar.
- Wizard of Oz #124 — still conditional on time; stays if Day 7 allows it.

## Source material (verified vs not)
Verified, with limits:
- Swiggy engineering author (via DEV Community repost, not the original): in-house chat platform with five components including an Agent Workbench; state synced on human handoff; customer can choose a human. Bot resolution ~75% is the author's own figure, unverified. https://dev.to/abeyalex/chatbots-at-swiggy-9bp
- A 2026 Swiggy backend engineering job ad (startup.jobs) independently names "Agent Workbench" as a current CRM-team ownership area — a second, more recent, independent source for the same tool name, found via a teammate's cross-verification pass 2026-09-29 (see `swiggy-secondary-research-crossverification.md`). Still says nothing about what the screen shows.
- Databricks vendor case study: AI agent with backend order data, CRM action triggers, fallback to human agents. Does not state escalation triggers or agent tooling. Contains an internal contradiction flagged independently by both research passes: it claims "100% of customer queries... fully automated without human intervention" in the same document describing a designed human-fallback safeguard — treat its figures as marketing, not fact. https://www.databricks.com/blog/redefining-customer-support-swiggys-enterprise-scale-ai-agent-built-databricks
- Swiggy blog: GPT-4-powered support chatbot built with a third party; no agent-assist details. https://blog.swiggy.com/news/swiggys-generative-ai-journey-a-peek-into-the-future/
- Unofficial directory (third party): in-app chat 24/7, no phone number, escalation via email and @SwiggyCares. https://customer-service.wiki/swiggy-customer-service/
- Deccan Herald, June 2022: government asked platforms for complaint-redressal plans; issues not specified. https://www.deccanherald.com/business/govt-asks-swiggy-zomato-and-others-to-submit-plans-in-15-days-for-improving-complaint-redressal-1117838.html
- Swiggy Market Intelligence Dashboard (restaurant-facing, tracks cancellations/availability/complaints): https://blog.swiggy.com/swiggy-catalyst/stay-ahead-of-the-game-with-swiggys-market-intelligence-dashboard/
- Swiggy Group / Supr Daily case study (AWS, spot-checked verbatim 2026-09-29): estimates as many as 25% of refunds were issued incorrectly, primarily due to poor-quality or missing delivery photos, before Amazon Rekognition was used to automate photo-quality checks — the most concrete Swiggy-ecosystem number linking evidence quality to refund error found so far. https://aws.amazon.com/solutions/case-studies/suprdaily-case-study/
- NCH complaint figures (10,590 against Swiggy, ~912 refund-related; 7,938 against Zomato) and the CCPA probe's unresolved status — independently corroborated by two separate research passes reaching identical numbers from the same underlying Business Standard reporting (21 May 2025).

Industry practice (not Swiggy):
- Zendesk Agent Workspace: conversation centre, context panel and knowledge search on the right. https://support.zendesk.com/hc/en-us/articles/4408821259930-About-the-Zendesk-Agent-Workspace
- CX Today (vendor-sponsored, small-study basis): agent-assist burdens (learning, compliance mismatch, irritating suggestions). https://www.cxtoday.com/contact-center/the-hidden-downsides-of-contact-center-agent-assist-technology-cyara/
- Cognitive-load paper (tpmap.org): theoretical, not peer-reviewed empirical; vocabulary only.
- Uber Eats: explicit merchant-liable / merchant-exempt fault categories, courier error-pattern auto-flagging, structured proof-of-delivery (photo, signature, barcode+timestamp, ID photo), and — spot-checked verbatim 2026-09-29 — a named escalation-trigger list (high-value orders, alcohol orders, first-time customers, late-filed claims) routed to a trained review team. The clearest cross-party precedent found; see `swiggy-cross-party-evidence-research.md`.
- Zomato "karma score": a reliability score spanning customers and riders, with the CEO admitting it "sometimes cannot definitively assign responsibility" — and a named worker association disputing its fairness. Direct precedent for the fairness risk this project must avoid reproducing.
- DoorDash's published "Order Remade Policy" (20-minute courier-lateness threshold, 7-day claim window, perishables only) and an older Zomato restaurant-rejection-rate rule (>3% daily rejection → suspension; 25% of order value refunded, min ₹25 / max ₹200) — both via a teammate's research pass, not independently re-verified — are the first evidence found anywhere that platforms *do* sometimes publish numeric thresholds, which Swiggy does not.
- Zepto (Business Standard, Dec 2025): "a mix of automated systems and human review" for refund-fraud detection, with ML flags plus periodic manual checks — third Indian-market comparator, via a teammate's research pass, not independently re-verified.
- Agent-effort / AHT industry benchmarks (ContactBabel, SQM Group, Salesforce State of Service, HBR/Soroco app-toggling study, Verint) — vendor/vendor-adjacent survey data, not Swiggy-specific, relevant to the Testing-stage KPI list (screen/lookup count, toggle count, time-to-decision) and to the brief's real-time-constraint framing. Via a teammate's research pass, not independently re-verified; see `swiggy-secondary-research-crossverification.md` §2g.
- Titles confirmed to exist, findings NOT yet read directly by this project: Brynjolfsson, Li & Raymond, "Generative AI at Work" (QJE 2025); Parasuraman & Manzey (2010), "Complacency and Bias in Human Use of Automation"; "Improving Dispute Resolution in Two-Sided Platforms: The Case of Review Blackmail," Management Science 69(10), 2022. **Caution added 2026-09-29:** a teammate's research pass reports having read partial/excerpt text of the first two and cites specific figures from them (an 82%-vs-33% automation-reliability failure-detection contrast; a 14% average / 34% novice productivity gain). Those figures are relayed secondhand and have not been verified against the primary source by this project directly — treat as [Reported via teammate] until one of us reads the paper itself. The Management Science paper remains fully unread by both research passes.

Could not obtain: Swiggy refund-policy text (page returned no body — a teammate's independent pass hit the identical fetch failure and worked from search excerpts too, confirming this is a page-level issue), agent job descriptions (Scribd failed, Naukri blocks bots), Swiggy Bytes originals (robots.txt), Zomato's ratings-methodology page (robots.txt), Airbnb Resolution Center process detail. No policy thresholds, agent-screen details, or cross-party weighing logic exist publicly anywhere checked, Swiggy or otherwise — with the narrow exception of DoorDash's and the older Zomato rule's numeric thresholds above, which are published but still say nothing about what a reviewer's screen shows.

## The 13 stages

| # | Stage | Content | Tag | Status |
|---|---|---|---|---|
| 1 | Overview | Domain (support tooling), role, tools, context, 3-line research headline | `[Rec]` | Draftable now |
| 2 | Brief | Interface that helps agents decide faster without automating the decision | `[Rec]` | Draftable now |
| 3 | Problem | Confirmed statement above: order-centred, cross-party (customer/restaurant/delivery-partner) panel; reduces investigation effort; assumptions labelled, including the no-scoring flag | `[Rec]` | **Confirmed** |
| 4 | Research | Primary: expert Interview #66 with a former American Express design-team lead (an expert, not a support agent; label as such); Customer Experience Audit #33 done from the customer side of Swiggy chat. Secondary: Secondary Research #93, Literature Reviews #71, Artifact Analysis #4 (Zendesk, Uber Eats, Swiggy sources above), Gap Analysis #57. Now covers customer, restaurant, and delivery-partner sides, plus incident-evidence and cross-party precedent (see `swiggy-cross-party-evidence-research.md`), and has been cross-verified against a teammate's independent secondary-research pass (see `swiggy-secondary-research-crossverification.md`) | none | Customer-side + cross-party pass done and cross-verified; expert interview still to do |
| 5 | Insights | **Triangulation #115** (combining Official/Reported/Anecdotal/Inferred evidence), Mental Model Diagrams #73; **Stakeholder Map #101** only if useful | none | To do |
| 6 | Define | Hypothetical (assumption-based) Persona #82, refined problem statement, Value Opportunity Analysis #120, **three-layer model** | `[Own]` new | To do |
| 7 | Ideation | **Creative Matrix #27** (agent decisions × three interface layers), Scenarios #92 + User Flow `[D]`, two layout alternatives compared, insight admissibility test (objective, traceable, no prediction) | `[Own]` new | To do |
| 8 | Design | Wireframe, Mockup, Prototype `[D]` of chat panel, customer panel, insights layer; every element labelled data, insight or decision support; policy shown as conditions checked against facts | `[D]` | To do |
| 9 | Testing | Heuristic Evaluation #60 and **Think-aloud Protocol #109** (core, measures decision time/effort directly); Wizard of Oz #124 with peers only if time allows; Usability Report #117 | none | To do |
| 10 | Outcome | Only real results; if untested with agents, say so and name what would be measured (KPIs #69: decision time, effort) | `[Rec]` | After testing |
| 11 | Future Scope | Real-agent testing, real policy and data integration, edge cases | `[Rec]` | Later |
| 12 | Limitations | No agent access, no Swiggy policy or data, proxy interviews only | `[Rec]` | Later |
| 13 | Learnings | Written by the project owner in their own voice | `[Rec]` | Owner |

Hard rule kept: Outcome, Future Scope, Limitations are separate stages.

## 1-week sprint plan (draft, to confirm)
- Day 1: secondary research and source log; book the expert interview.
- Day 2: interview, customer-side audit, start synthesis.
- Day 3: Insights (triangulation, mental model, stakeholder map) and Define (three-layer model, hypothetical persona).
- Day 4: Ideation (Creative Matrix, scenarios), layout alternatives, admissibility test.
- Days 5-6: Design and prototype.
- Day 7: heuristic evaluation and think-aloud walkthrough, write-up (stages 1-3, 10-12 drafted; 13 left to owner).

## Open items
- Interview questions for the expert (drafted; see `swiggy-expert-interview-guide.md`). A teammate's research pass suggests additional candidate questions (evidence provenance at Amex, whether risk scores were ever deliberately hidden from reviewers, reason-codes-as-checklist vs free text, audit-trail granularity) — not added to the guide since the user asked for it to stay to bare questions only; logged here in case there's room to extend it before the interview happens.
- Read the three literature/academic papers before citing any findings (two named earlier, plus the Management Science dispute-resolution paper found in the cross-party research pass). A teammate's pass reports partial reading of two of the three — treat their cited figures as unverified by us until read directly; see Source material above.
- Confirm whether the expert can also describe agent-tool practice, or only design-team practice.
- Whether Wizard of Oz fits in the Day 7 time budget.
- When the other case studies are finished, re-check this reshuffle against their actual method ledgers (see "Method reshuffle" note above — done on an unverified assumption).
- Open question carried from the cross-party research: whether a support agent sees restaurant/delivery-partner metrics at all, given Swiggy's Market Intelligence Dashboard is restaurant-facing only — nothing found confirms or denies agent-side visibility, including in the teammate's independent pass.
- New from the 2026-09-29 cross-verification: the cancellation-fee percentage has three different published/reported/live-support figures (100% policy, up to 90% per CCPA-probe reporting, flat 100% per live @Swiggy support replies) — see `swiggy-refund-and-blocking-rules-research.md` §10 for the full flag and its design implication.
- New from the 2026-09-29 cross-verification: whether "evidence type" (captured-at-delivery vs. submitted-after-the-fact vs. none) should become its own visible policy condition at the Define stage, now that a concrete AI-manipulated-evidence case exists (Instamart egg-tray, Nov 2025) rather than just the inferred risk.

## Session log
- 2026-09-25: files 04 and 05 analysed; connected folder empty; research pass done; structure and sprint decisions agreed.
- 2026-09-28: reshuffled Insights/Ideation/Testing methods away from portfolio-generic defaults (Affinity Diagramming, How Might We, Empathy Map, Cognitive Walkthrough) toward picks specific to this project's own evidence-tagging and three-layer framework; ledger check against other projects flagged as unverifiable from memory alone.
- 2026-09-28: problem statement confirmed (order-centred, cross-party panel); ran a second research pass on restaurant history, delivery-partner history, incident evidence, and cross-party precedent (Uber Eats, Zomato, Zendesk) to cover the scope this statement adds; written up in `swiggy-cross-party-evidence-research.md`.
- 2026-09-29: expert interview guide drafted, then simplified to bare numbered questions only per the project owner's instruction; see `swiggy-expert-interview-guide.md`.
- 2026-09-29: cross-verified this project's three research docs against a teammate's independent secondary-research pass. Corroborated the NCH complaint figures, SHIELD's scope, and the E-Commerce Rules timelines; added new comparator evidence (DoorDash, Zepto, a Swiggy-group evidence-quality figure from Supr Daily, and a concrete AI-manipulated-evidence case); spot-checked two load-bearing new claims directly against primary sources (both confirmed verbatim); flagged one real discrepancy (three different cancellation-fee percentages across policy, regulatory reporting, and live support replies); partially resolved the Agent Workbench open question with a second, independent source. Full comparison in `swiggy-secondary-research-crossverification.md`.
