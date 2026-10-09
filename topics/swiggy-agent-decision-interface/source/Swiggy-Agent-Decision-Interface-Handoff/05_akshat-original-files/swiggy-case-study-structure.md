---
name: swiggy-case-study-structure
description: 13-stage case-study structure for the Swiggy Support Agent Decision Interface (1-week sprint, research-led, no agent access). Read before producing any stage of this case study.
status: structure agreed in principle; no stage content written yet
---

# Swiggy Support Agent Decision Interface: Case-Study Structure

Framework: the 13-stage rulebook and citation legend from the workspace rulebook (file 04) and reference pack (file 05). `#N` numbers were checked against the Reference 1 table in the pack. The "one named method, one project" ledger is intentionally skipped for now; the skeleton may change later.

## Decisions made with the user
- Sprint project: **about 1 week**.
- Lead with **Research** (Overview carries a 3-line research headline; Research and Insights get the most weight).
- Three-layer model (raw data, derived insight, decision) is a **Define-stage `[Own]` framework**, carried through Ideation and Design.
- Problem is stated in full at stage 3 (no split with Define unless research justifies it).
- Testing and success metrics measure agent **decision time and effort**, never predicted outcomes.
- Framing: Swiggy already has an in-house Agent Workbench (see sources). This is a **hypothetical concept**, not a fix for a known Swiggy flaw.

## Source material (verified vs not)
Verified, with limits:
- Swiggy engineering author (via DEV Community repost, not the original): in-house chat platform with five components including an Agent Workbench; state synced on human handoff; customer can choose a human. Bot resolution ~75% is the author's own figure, unverified. https://dev.to/abeyalex/chatbots-at-swiggy-9bp
- Databricks vendor case study: AI agent with backend order data, CRM action triggers, fallback to human agents. Does not state escalation triggers or agent tooling. https://www.databricks.com/blog/redefining-customer-support-swiggys-enterprise-scale-ai-agent-built-databricks
- Swiggy blog: GPT-4-powered support chatbot built with a third party; no agent-assist details. https://blog.swiggy.com/news/swiggys-generative-ai-journey-a-peek-into-the-future/
- Unofficial directory (third party): in-app chat 24/7, no phone number, escalation via email and @SwiggyCares. https://customer-service.wiki/swiggy-customer-service/
- Deccan Herald, June 2022: government asked platforms for complaint-redressal plans; issues not specified. https://www.deccanherald.com/business/govt-asks-swiggy-zomato-and-others-to-submit-plans-in-15-days-for-improving-complaint-redressal-1117838.html

Industry practice (not Swiggy):
- Zendesk Agent Workspace: conversation centre, context panel and knowledge search on the right. https://support.zendesk.com/hc/en-us/articles/4408821259930-About-the-Zendesk-Agent-Workspace
- CX Today (vendor-sponsored, small-study basis): agent-assist burdens (learning, compliance mismatch, irritating suggestions). https://www.cxtoday.com/contact-center/the-hidden-downsides-of-contact-center-agent-assist-technology-cyara/
- Cognitive-load paper (tpmap.org): theoretical, not peer-reviewed empirical; vocabulary only.
- Titles confirmed to exist, findings NOT yet read: Brynjolfsson, Li & Raymond, "Generative AI at Work" (QJE 2025); Parasuraman & Manzey (2010), "Complacency and Bias in Human Use of Automation".

Could not obtain: Swiggy refund-policy text (page returned no body), agent job descriptions (Scribd failed, Naukri blocks bots), Swiggy Bytes originals (robots.txt). No policy thresholds or agent-screen details exist publicly.

## The 13 stages

| # | Stage | Content | Tag | Status |
|---|---|---|---|---|
| 1 | Overview | Domain (support tooling), role, tools, context, 3-line research headline | `[Rec]` | Draftable now |
| 2 | Brief | Interface that helps agents decide faster without automating the decision | `[Rec]` | Draftable now |
| 3 | Problem | Full problem statement on agent decision effort; assumptions labelled | `[Rec]` | Draftable now |
| 4 | Research | Primary: expert Interview #66 with a former American Express design-team lead (an expert, not a support agent; label as such); Customer Experience Audit #33 done from the customer side of Swiggy chat. Secondary: Secondary Research #93, Literature Reviews #71, Artifact Analysis #4 (Zendesk and Swiggy sources above), Gap Analysis #57 | none | To do |
| 5 | Insights | Affinity Diagramming #3, Mental Model Diagrams #73; Empathy Map #45 only if useful | none | To do |
| 6 | Define | Hypothetical (assumption-based) Persona #82, refined problem statement, Value Opportunity Analysis #120, **three-layer model** | `[Own]` new | To do |
| 7 | Ideation | How Might We #63, Scenarios #92 + User Flow `[D]`, two layout alternatives compared, insight admissibility test (objective, traceable, no prediction) | `[Own]` new | To do |
| 8 | Design | Wireframe, Mockup, Prototype `[D]` of chat panel, customer panel, insights layer; every element labelled data, insight or decision support; policy shown as conditions checked against facts | `[D]` | To do |
| 9 | Testing | Heuristic Evaluation #60 and Cognitive Walkthrough #19 (core); Wizard of Oz #124 with peers only if time allows; Usability Report #117 | none | To do |
| 10 | Outcome | Only real results; if untested with agents, say so and name what would be measured (KPIs #69: decision time, effort) | `[Rec]` | After testing |
| 11 | Future Scope | Real-agent testing, real policy and data integration, edge cases | `[Rec]` | Later |
| 12 | Limitations | No agent access, no Swiggy policy or data, proxy interviews only | `[Rec]` | Later |
| 13 | Learnings | Written by the project owner in their own voice | `[Rec]` | Owner |

Hard rule kept: Outcome, Future Scope, Limitations are separate stages.

## 1-week sprint plan (draft, to confirm)
- Day 1: secondary research and source log; book the expert interview.
- Day 2: interview, customer-side audit, start synthesis.
- Day 3: Insights and Define (three-layer model, hypothetical persona).
- Day 4: Ideation, layout alternatives, admissibility test.
- Days 5-6: Design and prototype.
- Day 7: heuristic evaluation and walkthrough, write-up (stages 1-3, 10-12 drafted; 13 left to owner).

## Open items
- Interview questions for the expert (draft next).
- Read the two literature papers before citing any findings.
- Confirm whether the expert can also describe agent-tool practice, or only design-team practice.
- Whether to keep Empathy Map (budget-limited method).

## Session log
- 2026-09-25: files 04 and 05 analysed; connected folder empty; research pass done; structure and sprint decisions agreed.
