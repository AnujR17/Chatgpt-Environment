---
name: swiggy-case-study-draft
description: Running draft of the Swiggy Support Agent Decision Interface case study, written stage by stage in order. Read alongside swiggy-case-study-structure.md.
status: Stages 1–7 done; Stage 8 pre-approval (waiting on owner's visual references, 2026-10-09)
---

# Swiggy Support Agent Decision Interface — Case Study Draft

## Stage 1 — Overview `[Rec]`

**Status:** Locked 2026-10-05.

**Domain:** Customer-support tooling. A decision-support interface for human support agents at a food-delivery platform, focused on refund and dispute review.

**Role:** Interaction designer. Solo concept project.

**Tools:** Coded prototype (HTML/React) for the design stage.

**Context:** A one-week sprint. Swiggy already runs an in-house support tool, the Agent Workbench (named in a Swiggy engineering post and, separately, in a 2026 Swiggy job listing). This project is a hypothetical concept, not a fix for a known Swiggy flaw. It was built without access to support agents, internal policy or real data.

**Research headline:**
1. Swiggy says its support automation exists but does not show what a human reviewer's screen looks like. No platform checked publishes this. Uber Eats and DoorDash publish fault categories and thresholds, but not reviewer screens.
2. Evidence quality is a documented risk. A Swiggy-group case study (Supr Daily) estimates that up to 25% of refunds were issued incorrectly, mainly because of poor or missing delivery photos. A reported Instamart case (Nov 2025) involved an AI-edited complaint photo.
3. Research on automation bias (Parasuraman & Manzey, 2010) finds that training or instructions cannot prevent it. That is why this interface shows facts and policy conditions and never gives a verdict.

**Notes carried forward:**
- Line 3 cites the paper's qualitative finding only. The 82%/33% figure stays out until someone reads the full paper.
- Tools: only a coded prototype is listed. Stage 8 also calls for a wireframe and a mockup. Decide at Stage 8 whether to wireframe in code or on paper. This also affects how much fits into Days 5–6.

## Stage 2 — Brief `[Rec]`

**Status:** Locked 2026-10-06.

**Source:** Self-initiated.

**Brief:** Design an interface for Swiggy's escalation agents, the people who take over a chat when the bot hands it to a human or the customer asks for one. The interface brings the live chat, the order, the history of everyone involved and the relevant policy into one view. The aim is to help the agent reach a decision faster, with less effort, and explain it to the customer. **The interface supports the decision. It never makes it.**

**User:** The escalation agent. Swiggy's support system hands state over to a human agent, and customers can choose to talk to one (Swiggy engineering post, via DEV Community repost).

**Scope:**
- The brief covers every type of support issue an escalation agent handles.
- Design and testing focus on one area: refund and dispute review (missing or wrong items, quality, delivery problems). This is where a decision affects three parties (customer, restaurant, delivery partner). It is also where the public complaint data points: about 912 of 10,590 National Consumer Helpline complaints against Swiggy were about refunds (Business Standard, May 2025).
- Other issue types (payments, account, coupons, cancellations) go to Future Scope (Stage 11).

**Stated constraint:** Traceable insights. Every derived insight shows the raw data or policy condition it comes from, so the agent can see why it appears.

**Carried to Stage 6 (Define) as design principles:**
- Real-time use: the agent is mid-chat and can only glance at the screen.
- Fairness to all three parties: customer, restaurant and delivery-partner history is shown neutrally. Zomato's disputed "karma score" is the cautionary example.

**Notes carried forward:**
- *Assumption, labelled:* Swiggy's real routing tiers are not public. "Escalation agent" is our term for the human who receives a handed-over chat. We are not claiming Swiggy uses that job title.
- The brief is wider than the Stage 3 problem statement on purpose. Stage 3 stays order-centred and cross-party. Stage 11 must list the other issue types so the gap is stated openly.

## Stage 3 — Problem `[Rec]`

**Status:** Confirmed 2026-09-28. Copied here from the structure doc, unchanged.

> Swiggy publicly documents support automation and has disclosed fraud detection, but its current cross-party refund-review workflow is not visible. We propose an order-centred agent panel that brings policy conditions, incident evidence, and appropriately contextualised customer, restaurant, and delivery-partner histories into one review — aiming to reduce investigation effort while protecting genuine claims.

**Assumptions line (to be shown with the statement):** "Protecting genuine claims" is an outcome of a faster, better-informed human review. The interface does not judge which claims are genuine. It shows traceable facts (policy conditions, evidence, dated history) and the agent makes the call.

## Stage 4 — Research

**Status:** Closed 2026-10-08.

### Methods used
| Method | Type | Status |
|---|---|---|
| Expert Interview #66 | Primary, real | Done: one 10-minute call, 6 Oct 2026 |
| Simulated Expert Interview (source-grounded) | Secondary, simulated | Done (team, 1 Oct). 43 claims traced, 0 unsupported |
| Customer Experience Audit #33 | Primary, team (Entity 1) | Written up from both sources; gaps marked as not recorded |
| Secondary Research #93 | Secondary | Done; checked against a teammate's separate research pass |
| Literature Reviews #71 | Secondary | Done (team): 5 papers, with a do-not-cite list |
| Artifact Analysis #4 | Secondary | Done (team): 8 artifacts |
| Gap Analysis #57 | Secondary | Done (team): gaps sorted into types A to E |

### Expert Interview #66 (real)
**Expert:** Customer service expert, American Express. Named by role only.
**Date and format:** 6 Oct 2026. Short call, about 10 minutes.
**Label:** He is a customer-service expert, not a Swiggy support agent. His points are expert opinion, not observed agent behaviour.

**What he said (as reported by the interviewer):**
1. Everything on the agent's screen should help the agent reach a decision in less time.
2. Insights shown to the agent are already based on policy.
3. Evidence is shown to the agent in a way that is easy to take in. *He didn't describe the format. The design translation below is ours, not Amex's.*
4. Suggestion: when an agent is struggling with a problem, show how a "star agent" solved a similar problem.

**What each point means for the design:**
- **Point 1** confirms the brief and the success measure (decision time and effort). Use it as Stage 4's headline quote.
- **Point 2** supports showing policy as conditions checked against facts, which this project already chose.
- **Point 3** supports a separate, easy-to-read evidence section. See "Design translation: evidence display" below.
- **Point 4** goes to Stage 7 (Ideation). See "Design translation: similar cases" below.

### Design translation: evidence display (from Point 3)
*Our own reasoning. It builds on the expert's point, the simulated interview (Q3, Q4) and the research files. It does not describe how Amex's real screen looks.*

**What the agent is deciding at this moment:** whether each policy condition is met, and whether the evidence for it holds up.

| Layer | What appears | Why it saves time |
|---|---|---|
| **Data** | Each evidence item has a type (photo, OTP, delivery timestamp, location ping, chat message, restaurant packing photo). It also shows who supplied it (system, rider, restaurant or customer), when it was captured and when it was submitted. | The agent doesn't have to open each item to learn what it is and where it came from. |
| **Insight (objective)** | 1. Evidence is grouped under the policy condition it relates to. 2. Missing evidence is shown as a plain fact, for example "No delivery photo on record". 3. Time gaps are shown as plain facts, for example "Complaint raised 3 h 10 min after delivery" or "Customer photo submitted 40 min after complaint". 4. Each item is tagged as captured at the event or sent in afterwards. | Answers the agent's real question ("is this condition supported?") without them having to piece it together. A gap that would otherwise take searching becomes visible straight away. |
| **Decision support** | The agent links each item to the condition it supports or fails, and that link is saved to the case log. | Turns the decision into a checklist the agent works through. The case log then shows why the decision was made. |

**Never shown:** "verified" or "suspicious" badges, image-manipulation scores, or any "likely fraud" signal. Each of these is a verdict presented as a fact, which the core design rule forbids.

**Two layouts compared:**
- **A. Chronological timeline.** All events in time order (order placed, picked up, delivered with photo, complaint, customer photo). *Strong:* it shows order of events and timing gaps clearly, which helps with claim windows. *Weak:* the agent still has to work out which item proves which condition.
- **B. Grouped by policy condition.** Each condition is a card, with its evidence listed underneath. *Strong:* it matches the decision the agent is making, one condition at a time. *Weak:* order of events is harder to see.
- **Recommendation:** use B as the main view, with a single-line timeline strip above it. The agent decides condition by condition, so B shortens the path most. The strip keeps timing visible, which matters for claim windows and for the "submitted afterwards" check. *To test at Stage 9 (think-aloud): do agents read the strip, or skip it?*

**Assumption, labelled:** Swiggy's real evidence fields aren't public. The fields above are hypothetical placeholders, based on Uber Direct's published proof-of-delivery types and the Supr Daily photo case.

### Design translation: similar cases (from Point 4)
*Decisions made by the project owner on 2026-10-08. Details still to be worked out at Stage 7.*

**Decided:**
1. **The agent opens it (option C).** The system never decides that an agent is "struggling".
2. **Precedent cases come first (option B).** These are past cases with the same issue type and the same pattern of policy conditions met or not met. The match uses visible facts, not similarity scoring.
3. **Reply phrasing comes second (option A).** Each precedent case can show how the outcome was explained to the customer. This is shown only after the agent has decided.
4. **"Star agent" is defined by measurable criteria.** The project owner set resolution time per issue category as the base measure. The other criteria are proposed below.

**Proposed "star agent" criteria** (*all thresholds are placeholders; Swiggy's real metrics aren't public*):

| Criterion | What it guards against |
|---|---|
| Resolution time within the issue category (the owner's base measure) | Slow handling |
| The case wasn't reopened and the customer didn't come back about the same order within N days | Speed bought by leaving issues unresolved |
| The decision wasn't overturned on later review or escalation | Speed bought by being wrong |
| The decision was logged against policy conditions (complete record) | Fast decisions with no reasons recorded |
| A minimum number of cases in that category | One lucky fast case making someone a "star" |

**Why speed alone isn't enough:** the team's own audit (Entity 1, below) found that fabricated claims were refunded with "no questions asked". That kind of case is resolved fastest. Ranking on time alone would make exactly that handling the model to copy.

**Open for Stage 7:**
- **What the agent sees when they open it.** Showing 2 or 3 cases, including ones with *different* outcomes where they exist, helps stop the agent copying a single answer. Bansal et al. (2021) found that people accept an explained answer more often whether or not it's correct.
- **How cases are labelled.** Call them "reference cases" rather than naming star agents. Ranking colleagues by name on screen is a fairness and morale risk.
- **Which layer this belongs to.** It's decision support. Each case carries a label: "a past case, not a recommendation".

**Literature link:** Brynjolfsson, Li & Raymond (2023) studied a tool that learned from top agents' conversations. Novice agents resolved 34% more cases per hour, and experienced agents changed little. That tool suggested replies; it didn't decide cases. This supports option A as the lower-risk part of the idea.

### Simulated Expert Interview (source-grounded), supplement
Team work (1 Oct 2026). A composite expert, "Expert S1", answered only from public sources. It is **not a real interview** and must always carry the word "simulated". The most relevant answers:
- **Q2:** Show policy as named conditions, not free text or a decision tree.
- **Q3:** Tag each piece of evidence with its type and origin. Never use a "verified" or "suspicious" badge.
- **Q4:** Keep three deadlines separate: the claim window, the reply-by date and the regulatory clock.
- **Q6:** Show history as dated counts, never as a single score.

### Customer Experience Audit #33: Entity 1 (team)
**Sources:** (1) A teammate's written account given on 1 Oct 2026. (2) The same teammate's voice memo of 5 Oct 2026: 110 seconds, Hindi and English, with an automatic transcript that lost most of the Hindi. Re-transcribing the audio wasn't possible from this workspace, so the reading of source 2 below is partly inferred from a broken transcript.

**What each source says:**
| | Written account (1 Oct) | Voice memo (5 Oct) |
|---|---|---|
| Account | A new account created for the test | The same account for cases 1–2; a new login with a different phone number and ID for case 3 |
| Fabricated claims | 3, on 3 orders (small portion, damaged product, other), all refunded | 2 on the same account (the second "maybe three weeks" later), both refunded; 1 more on the new account, refunded |
| Genuine claims | 2: the first about a month later got no proper response or refund; the second, 10–11 days after that, was refused by email | 1 genuine wrong-order case refunded "no questions asked" through the chatbot. The closing line seems to say genuine cases were *not* refunded, but this part of the transcript is unclear. |

**Reconciled finding (only what both sources agree on):**
- **Every fabricated claim was refunded, in both accounts.** That is 3 of 3 in the written account and 3 of 3 in the memo, including one from a fresh account.
- **Genuine claims got inconsistent treatment.** The written account reports both refused. The memo reports at least one refunded, with an unclear closing line. The two sources can't be fully reconciled, so the case study reports "inconsistent" and doesn't claim either version.

**Not recorded in either source:** exact dates, the refusal email's wording, whether the device or payment method changed, and whether the account was ever blocked or warned. These are written up as "not recorded" rather than estimated.

**Strength of evidence:** primary, but self-reported by one tester, with a few claims and a partly unclear recording. It shows that the problem exists; it doesn't show how often it happens. It matches the published evidence: the Supr Daily estimate that up to 25% of refunds were issued incorrectly, and the Instamart AI-edited photo case.

**What it means for the design:** the review lacked any visible check of evidence. A fabricated claim and a genuine one appear to have gone through the same chatbot path, which supports the evidence-display design above. **It must not lead to a "fraud likelihood" feature.** The response is to make evidence and its origin visible, not to score customers.

**Reporting rule:** some complaints in this test were fabricated. The write-up must say so plainly and add an ethics line under Limitations (Stage 12). It is reported as a finding about how evidence gets checked, not as a neutral test. No further fabricated claims are to be made for this project.

### Stage 12 lines this stage creates
- "The expert interview was a single 10-minute call with a customer service expert outside food delivery. A source-grounded simulated interview supplements it and is labelled as simulated."
- "The customer experience audit includes complaints the tester fabricated to see how refunds are checked. All fabricated claims were refunded. Whether those refunds were returned is not recorded. The method is ethically questionable and is reported here as it happened."

## Stage 5 — Insights

**Status:** Done 2026-10-08.

**Methods:** Triangulation #115 (core), Mental Model Diagram #73 (based on inference and labelled as such), Stakeholder Map #101.

**Evidence tiers used for triangulation:**
- **[O]** Official: platform terms or pages.
- **[L]** Law.
- **[R]** Reported: news or vendor case studies.
- **[A]** Anecdotal: forums.
- **[P]** Primary: the 6 Oct expert call and the team audit.
- **[S]** Simulated expert interview.
- **[Lit]** Literature.
- **[I]** Our own inference.

**Rule:** an insight is kept only if at least 3 different tiers support it. An insight backed only by [I] is not an insight.

### Key insights

**Insight 1. The policy lists the conditions but leaves the outcome to discretion, so the agent's judgement fills every gap.**
- **Evidence:**
  - [O] Refunds are decided "case to case". Swiggy's "decision… shall be final and binding". Amounts are "up to 100%".
  - [O] The Terms of Use and the Refund Policy contradict each other on who must be at fault.
  - [R] A chat support executive told Business Standard that a customer "value tier" shapes outcomes.
  - [P] The expert said insights are built on policy.
  - [S] Q2: policy works best as named conditions.
- **Tiers:** 4 (O, R, P, S).
- **What it means for the design:** show each policy condition next to the fact it's checked against. Where Swiggy has published no threshold, say so on screen ("No published threshold"). Don't let a made-up number fill the gap.

**Insight 2. Refund mistakes come mainly from weak evidence, not from a lack of customer history.**
- **Evidence:**
  - [R] Supr Daily, a Swiggy-group company: up to 25% of refunds were issued incorrectly, "primarily due to poor quality or missing delivery photos".
  - [R] Instamart case: an AI-edited egg photo got a full refund.
  - [P] Team audit: every fabricated claim was refunded.
  - [O] Uber Direct's proof of delivery is captured at the moment of delivery.
  - [O] Swiggy has no written evidence rule for food orders.
  - [S] Q3: tag every piece of evidence with its type and origin.
- **Tiers:** 4 (R, P, O, S).
- **What it means for the design:** evidence gets its own section. For each item, show where it came from, when it was captured, and whether anything is missing. This is the opposite of a fraud score: it shows what the evidence is and leaves the judging to the agent.

**Insight 3. Wherever history is collected, it turns into a single score. That score is opaque and disputed, and people trust it too much.**
- **Evidence:**
  - [R] Swiggy's reported customer "value tier" and "fraud user" flag.
  - [R] Zomato's "karma score" covers customers and riders. Zomato's CEO admits it "sometimes cannot definitively assign responsibility". A gig-workers' association disputes it.
  - [O] Uber Eats automatically flags couriers with "significant error patterns".
  - [Lit] Bansal et al. (2021): an explanation raises acceptance "regardless of correctness".
  - [Lit] Parasuraman & Manzey (2010): automation bias can't be trained away.
  - [S] Q6.
- **Tiers:** 4 (R, O, Lit, S).
- **What it means for the design:** show history as dated counts per party, never as a score or label. A first-time user shows "No history", which must never read as "low risk".

**Insight 4. A refund decision shifts cost between three parties, yet the agent's view appears to be customer-only.**
- **Evidence:**
  - [O] Cancellation charges exist "to compensate the Merchants and Delivery Partners". Food-quality issues are the restaurant's liability. No resolution happens without the restaurant's permission.
  - [R] MediaNama: restaurants say refunds are taken from their payouts without proof, with no way to dispute.
  - [A] A delivery partner was reportedly fined ₹850.
  - [R] The only public description of what the agent sees mentions the customer profile and refunds in the last 3 months. Restaurant data sits in a restaurant-facing dashboard.
- **Tiers:** 3 (O, R, A).
- **What it means for the design:** show who would bear the cost as a plain fact, plus a short record for each party. Show restaurant permission as a visible condition with its status (pending or given), not as a hidden wait.
- **Assumption, labelled:** we don't know whether Swiggy agents see restaurant or rider data today.

**Insight 5. The goal is speed, but speed with no checks rewards the wrong cases.**
- **Evidence:**
  - [P] The expert: every screen element should cut decision time.
  - [P] Team audit: fabricated claims were refunded "no questions asked".
  - [A] The bot offers 20–30% partial refunds or coupons.
  - [R] Repeat complainers are moved to email after "two or three" cases.
  - [Lit] Brynjolfsson et al. (2023): help from top agents' conversations lifts novices most.
  - [Lit] Buçinca et al. (2021): making people pause and reason cuts over-reliance, but they like it less.
- **Tiers:** 4 (P, A, R, Lit).
- **What it means for the design:** save time on *looking things up*, not on *checking*. Every second saved should come from fewer screens and searches, not from skipping a condition. This is also why the "star agent" criteria pair speed with safeguards against unresolved and overturned cases.

**Insight 6. Rules and deadlines differ depending on the source, and the agent has no single version to rely on.**
- **Evidence:**
  - [O] The policy says a cancellation fee of "up to 100%".
  - [R] Coverage of the CCPA probe says "up to 90%".
  - [R] Live @SwiggyCares replies say a flat 100%. *(Via a teammate, not re-checked.)*
  - [L] The law requires acknowledgement within 48 hours and resolution within 1 month.
  - [O] Instamart's claim window varies by product. Food orders have none.
  - [S] Q4: keep the separate clocks separate.
- **Tiers:** 4 (O, R, L, S).
- **What it means for the design:** label every rule with its source. Show where sources disagree instead of quietly choosing one. Show the claim window, the reply-by time and the regulatory clock as three separate clocks.

**Dropped (fewer than 3 tiers):**
- "Agents can approve refunds only up to a limit." [I] only; the limits are not public.
- "Device signals feed refund decisions." [R] only, and the source frames them around promotion abuse.

### Mental Model Diagram #73 (inferred)
*Every step in the agent column is [Inferred] from the research. No agent was observed.*

| # | What the agent likely does or thinks [I] | What the policy actually checks | Gap = design target |
|---|---|---|---|
| 1 | Reads the bot handover and the chat so far | — | The handover may not say what the bot already offered (20–30%, coupon) |
| 2 | Works out what went wrong | Issue type [O] | Customers' words don't match the policy's categories |
| 3 | Checks when it happened | Order stage and timing; COD reported before "delivered" [O] | Timestamps are spread across systems |
| 4 | Looks for proof | "Required evidences" (Instamart only) [O]; none for food | No rule for food, so the agent decides what counts as "enough" |
| 5 | Looks at the customer's past refunds | Not a policy condition. Reported practice: refunds in the last 3 months, value tier [R] | **The biggest gap.** History seems to weigh in, but the policy never names it |
| 6 | Decides who is at fault | Fault attribution, the policy's main variable [O] | Restaurant and rider records may not be visible |
| 7 | Picks an amount | "Up to 100%", "proportionate", "case to case" [O] | No published threshold |
| 8 | Waits for, or assumes, the restaurant's OK | Restaurant permission required [O] | Hidden dependency with no visible status |
| 9 | Explains the outcome to the customer | — | Wording is left to the agent or templates |

**Key reading:** steps 5 and 8 are where the agent's likely thinking and the written policy pull furthest apart. Step 5 weighs something the policy never names. Step 8 depends on something the screen doesn't show.

### Stakeholder Map #101
| Stakeholder | What a refund decision costs or gives them | What they can see | Can they dispute it? |
|---|---|---|---|
| Customer | Refund, coupon or denial; possible account limits | Chat, outcome; no reasons for a block [A] | Yes, outside Swiggy: helpline (NCH), consumer commissions [L] |
| Escalation agent (our user) | Time, accuracy, accountability | Reported: customer profile and 3-month refunds [R] | — |
| Restaurant | Deductions from payouts [R]; liability for quality [O] | Its own complaint metrics, in a restaurant-facing dashboard [O] | Reportedly no dispute route [R] |
| Delivery partner | Fines; removal from the platform (Zomato example) [R/A] | Not documented | Not documented |
| Swiggy: bot, email/fraud team, Trust & Safety | Refund cost; fraud losses | Full data, including SHIELD device signals [R] | Its decision is "final and binding" [O] |
| Regulator (CCPA), courts | Enforces the law | Complaint volumes: 10,590 against Swiggy [R] | Can override Swiggy [L] |

**Key reading:** the people who carry the cost of a decision (restaurant, delivery partner) see the least and have the weakest means of disputing it. Showing each party's record neutrally is a fairness requirement, not just a helpful extra.

### Diagrams
Both are in FigJam: https://www.figma.com/board/jdVOYesjFWTQOsQcxnVvV9
- Swiggy Agent Mental Model vs Policy (Inferred)
- Swiggy Refund Decision Stakeholder Map

### Decision carried forward (2026-10-08)
Steps 5 and 8 of the mental model will be shown on the agent's screen, so nothing is left to assumption:
- **Step 5:** party history is shown as dated counts, labelled "Context, not a policy condition".
- **Step 8:** restaurant permission is shown as a condition with a live status.

Swiggy's real rules are confidential, so a frozen working set of policies and scenarios now governs Stages 6–9. See `swiggy-frozen-policy-and-scenarios.md`.

## Stage 6 — Define `[Own]`

**Status:** Drafted 2026-10-08.

**Methods:** Personas #82 (hypothetical, based on assumptions), a refined problem statement written as a POV (point-of-view) statement, Value Opportunity Analysis #120 (one row per stakeholder), the three-layer model, and design principles.

### Personas #82: two, both hypothetical
**Why two:**
- The literature shows that newer and experienced agents get very different value from support tools. Brynjolfsson et al. (2023) found +34% resolutions per hour for novices and little change for experienced agents.
- Our two biggest gaps fail in different ways for each. A newer agent doesn't know what to check. An experienced agent checks from habit and skips steps 5 and 8.
- Two personas give Stage 9 two test conditions. A third (team lead or second reviewer) is out of scope for this sprint and goes to Stage 11.

**Labelling rule:** neither persona is drawn from interviews with Swiggy agents, because none were possible. Every trait is either tied to a Stage 5 insight or labelled [Assumption]. The names are placeholders.

| | **Persona A: "Ananya" (hypothetical)** | **Persona B: "Rohit" (hypothetical)** |
|---|---|---|
| Role | Escalation agent, chat support | Escalation agent, chat support |
| Tenure | 6 weeks [Assumption] | 2 years [Assumption] |
| Working context | Takes over chats from the bot. May handle more than one chat at a time [Assumption, common industry practice; not confirmed for Swiggy] | Same |
| Main goal | Get the decision right and not be overruled later | Close cases quickly without reopens |
| How they work today [Inferred] | Reads the policy slowly and switches between screens to find each fact (Insight 1) | Works from memory and pattern. Checks past refunds first (mental-model step 5) and assumes the restaurant will agree (step 8) |
| Main frustration | Rules don't give a number, so every partial refund feels like a guess (Insight 1) | Rules and deadlines differ by source, and live replies contradict the policy (Insight 6) |
| Risk if the screen fails them | Over-relies on whatever the screen shows first, a risk of automation bias (Insight 3) | Skips checks to stay fast and rewards the wrong cases (Insight 5) |
| What they need from the screen | Every condition next to its fact, with the source shown | Hidden dependencies and missing evidence that stand out without slowing them down |
| "Similar cases" feature (Stage 7) | Likely heavy use | Likely occasional use |

### Refined problem statement: POV
*The Stage 3 statement stays locked. These POV statements narrow it for Ideation.*

- **Ananya:** A newly trained escalation agent needs every policy condition and its matching fact in one view, **because** the policy leaves the outcome to judgement (Insight 1) and she has no habits yet to fill the gaps.
- **Rohit:** An experienced escalation agent needs missing evidence and pending dependencies to be impossible to overlook, **because** speed built on habit skips checks (Insight 5) and assumes restaurant permission (step 8).
- **Shared:** Escalation agents need to see conditions, evidence and each party's record, with nothing left to assumption, **so that** they can decide faster without checking less.

### Value Opportunity Analysis #120: by stakeholder
*The ratings (Low / Medium / High) are our own judgement [I], based on the Stage 5 evidence noted in each row. "Today" means the current state as reported by research. "With concept" is the expected value. It is not measured.*

| Stakeholder | Value today | Value with concept | Where the change comes from |
|---|---|---|---|
| Escalation agent | Low | **High** | Conditions, evidence, permission and history in one view, with fewer screens and look-ups (Insights 1, 5) |
| Customer (genuine claim) | Medium | **High** | Decisions are tied to evidence, not to a reported "value tier", so a genuine claim isn't refused because of history alone (Insights 2, 3) |
| Restaurant | Low | **Medium** | Cost-bearing is visible, and its record is shown in the same neutral format as the customer's. It still has no dispute route; that's outside this screen (Insight 4) |
| Delivery partner | Low | **Medium** | Its record is shown in a neutral format, and delivery evidence is shown with its origin (Insights 2, 4) |
| Swiggy (platform) | Medium | **High** | Fewer evidence-driven errors (the Supr Daily 25% case), and a case log that records why each decision was made (Insights 2, 5) |
| Regulator / courts | — | **Medium** | The case log helps meet the 48-hour acknowledgement and 1-month resolution rules (Insight 6) |

**Key reading:** the biggest jumps are for the agent and the platform. The smallest are for the restaurant and the rider. The concept makes their side visible, but it can't give them a voice. Stage 11 must say this.

### The three-layer model `[Own]`
Every element in Stages 7 and 8 must be labelled with one of these layers.

| Layer | What it is | Rule | Example (from the frozen policy file) |
|---|---|---|---|
| **Data** | Raw facts from systems or parties | Shown as recorded, with source and time | "Delivery photo, captured at drop-off, 19:42, by delivery partner" |
| **Derived insight** | Data that has been grouped, compared, counted or checked against a policy condition | Must be objective and traceable to the data or rule behind it. It may summarise or compare. It must never predict, score or recommend | "Complaint raised 3 h 10 min after delivery: within the 24 h window (P3)" · "No delivery photo on record" · "3 refunds in 90 days (dated)" |
| **Decision support** | Tools that help the agent act on their own decision | The agent chooses; the system records why | Linking evidence to conditions, requesting restaurant permission, opening similar past cases, reply wording after the decision |
| *(not allowed)* | Verdicts, predictions, scores | Never shown | "Likely fraud", a risk score, "Approve" pre-selected |

### Design principles
1. **Glanceable mid-chat.** Any fact the agent needs is readable within a few seconds while they're typing. Dense detail opens only on demand. *(Carried over from the Brief.)*
2. **Fair to all three parties.** Customer, restaurant and rider history use the same format and the same neutral wording. No side gets a label the others don't. *(Carried over from the Brief.)*
3. **Nothing left to assumption.** Every dependency (restaurant permission, missing evidence, history, review triggers) is shown with its current status, including "unknown" and "none". *(Owner decision, 2026-10-08.)*

*Also in force but not repeated here: traceable insights (a constraint stated in the Brief) and the core rule that the screen supports the decision and never makes it.*

## Stage 7 — Ideation `[Own]`

**Status:** Done 2026-10-09. Layout A chosen.

**Order of work:** 1 admissibility test → 2 Creative Matrix → 3 similar-cases spec → 4 scenarios and user flow → 5 two layouts compared.

### Step 1: Insight admissibility test
An idea reaches the screen only if it passes **all six** questions.

| # | Question | Fails if… |
|---|---|---|
| Q1 | **Objective:** would any two agents read the same value from the same data? | It uses judgement words ("suspicious", "likely", "high risk") |
| Q2 | **Traceable:** can the agent see its source, and open the data or rule behind it in one step? | The source is hidden, or the number can't be checked |
| Q3 | **No prediction:** does it describe what is recorded, not what will or probably will happen? | It shows a probability, confidence level, forecast or trend label |
| Q4 | **No prescription:** does it leave the decision to the agent? | It recommends, pre-selects or auto-sends an outcome |
| Q5 | **Fair:** where it concerns a party, is the same form applied to all three parties? | Only one party gets a label, flag or extra scrutiny |
| Q6 | **Saves time:** does it remove a look-up, a screen switch or a mental calculation? | It adds reading without removing any work (clutter) |

**Results:** **Pass**, or **Fail** with the failing question. Where possible, a failed idea gets a **fix**: an objective version that does pass.

### Step 2: Creative Matrix #27
**Rows:** the agent's decisions, taken from the mental-model steps. **Columns:** the three layers. Each idea has an ID (for example M3.2) so later stages can refer to it.

| Agent decision | Data | Derived insight | Decision support |
|---|---|---|---|
| **D1. What went wrong?** | **M1.1** The customer's own words, plus the issue the bot recorded | **M1.2** Issue mapped to a policy category with its default liable party: "Missing item → restaurant liable by default (P2)" | **M1.3** One tap to confirm or correct the category (logged) |
| **D2. When did it happen?** | **M2.1** Order events with timestamps (accepted, picked up, delivered, complaint) | **M2.2** "Complaint 3 h 10 min after delivery: within 24 h window (P3)". For cash on delivery: "Reported before delivered? No (19:49 vs 19:42)" | **M2.3** Timeline strip with policy cut-off times marked |
| **D3. Is there proof?** | **M3.1** Evidence items with type, supplier, origin and times | **M3.2** Evidence grouped under the condition it relates to. **M3.3** Gaps stated as facts: "No delivery photo on record". **M3.4** Gap between capture and submission: "Customer photo sent 40 min after complaint" | **M3.5** Agent links each item to a condition (logged). **M3.6** Ask the customer for more evidence, using a ready-made message |
| **D4. Who is at fault?** | **M4.1** Rider record (marked delivered, location ping, OTP used or not), restaurant packing photo | **M4.2** Conflicting records shown side by side: "Rider: delivered, 19:42, location at address · Customer: not received" (T4) | **M4.3** Agent selects the at-fault party, and the screen shows who bears the cost: "Cost falls on: restaurant" |
| **D5. Has the restaurant agreed?** | **M5.1** Permission status with timestamps | **M5.2** "No reply after 10 min" | **M5.3** Request / remind / escalate buttons |
| **D6. What is each party's record?** | **M6.1** Dated refund and complaint lines for all three parties | **M6.2** Counts with totals: "3 refunds out of 7 orders in 90 days", "No history" | **M6.3** "Show older" (logged, same for all parties) |
| **D7. How much, and can I approve it?** | **M7.1** Order items with prices | **M7.2** Total of the items the agent selected: "₹180". **M7.3** "Above ₹500 approval limit → review (T1)" | **M7.4** Item checkboxes. The agent picks the items, and the screen adds up the amount |
| **D8. Does it need review?** | **M8.1** The facts that set off each trigger | **M8.2** "Review trigger: first-time customer (T2, borrowed from Uber Eats)", with its source | **M8.3** Send to reviewer with the case log attached |
| **D9. How do I explain it?** | **M9.1** What the bot already offered: "Bot offered 25% coupon, 19:51" | **M9.2** The conditions the agent linked, listed for the reply | **M9.3** Reply templates that cite the policy condition. **M9.4** Wording from similar past cases, shown after the decision (see step 3) |
| **Across all decisions** | — | — | **M0.1** Case log: what the agent linked, opened and decided, with times. **M0.2** "Similar cases" panel, opened by the agent (specified in step 3) |

#### Ideas that failed, and their fixes
| Idea | Fails | Why | Fix (passes) |
|---|---|---|---|
| Auto-classify the chat into an issue type with a "92% confidence" score | Q3 | It's a guess shown as a fact | M1.1 + M1.3: show the bot's category and the customer's words; the agent confirms |
| AI image-tampering / authenticity score on customer photos | Q1, Q3 | A verdict presented as a number | M3.1 + M3.4: show where the photo came from and when it was submitted |
| "Most likely at fault" suggestion | Q3, Q4 | Prediction and prescription | M4.2: show the conflicting records side by side |
| "Repeat refunder" tag, or a "refunds rising ↑" trend arrow | Q1, Q3, Q5 | A label and a trend reading on one party | M6.1 + M6.2: dated lines and counts with totals |
| System-suggested refund amount | Q4 | It decides for the agent | M7.4: the agent picks the items and the screen adds them up |
| "Approve" button pre-selected when every condition is met | Q4 | A default outcome is a recommendation | No default. Approve, partial and deny carry equal visual weight |
| Auto-send the decision and reply to the customer | Q4 | It removes the agent from the decision | M9.3: the agent edits and sends |

#### Borderline: owner decision needed
| Idea | Concern | Option |
|---|---|---|
| **B1.** Photo time-stamp from the file's own data: "Photo taken 18:02, before delivery at 19:42" | Passes Q1–Q4 (it's a recorded fact), but reads like an accusation. And customers' phones may strip this data, so it would show unevenly | Show it only when recorded, worded neutrally, or leave it out |
| **B2.** Restaurant's average preparation delay for this order vs. its usual | Needs a comparison baseline; risks looking like a score on the restaurant | Leave out, or show only "Prepared 22 min after acceptance" (this order only) |
| **B3.** Live count of other open complaints against the same restaurant today | Objective, but invites pattern-thinking during one case | Leave out, or show as a dated count only (like M6.2) |

#### Owner decisions on step 2 (2026-10-09)
- **All 28 passing ideas kept.** Step 5 (layout) decides what shows first and what opens on demand.
- **All three borderline ideas kept, with conditions:**
  - **B1** (photo's own timestamp): shown only when the photo file actually records it. Worded neutrally: "Photo time (from file): 18:02". When it's missing, the screen says "Not recorded".
  - **B2** (preparation time): this order only. No comparison with the restaurant's usual times.
  - **B3** (open complaints today): **extended to all three parties to meet Q5 (fairness).** It was proposed for the restaurant only, but a count shown for one party and not the others fails Q5. It is shown as a dated count with its total, the same way as M6.2.
- **"No default outcome" rule (approve, partial and deny shown with equal weight, nothing pre-selected): considered, not locked.** Stage 9 will test it in scenario S1, the clean case. If it adds friction there, revisit it. Any exception has to be written into the case study.

### Step 3: "Similar cases" spec (M0.2)
**Layer:** decision support. **Personas:** mainly Ananya (newer agent); Rohit uses it occasionally.

**1. How it opens**
- Only when the agent taps "Similar cases". It never opens by itself, and the system never decides the agent is "struggling".
- Each open, and each case viewed, is recorded in the case log.

**2. Which past cases count ("reference cases")**
A resolved case joins the pool only if it meets every criterion below. *All thresholds are [Hypothetical].*

| Criterion | Value |
|---|---|
| Resolution time (owner's base measure) | At or below the usual (median) time for that issue category |
| Not reopened | The customer didn't come back about the same order within 7 days |
| Not overturned | The decision wasn't reversed on review or escalation |
| Reasons recorded | The decision was logged against policy conditions |
| Enough cases behind it | The handling agent has at least 20 resolved cases in that category |
| Current rules | Resolved under the same policy version, within the last 90 days |

**3. How cases are matched**
- Matching uses visible facts only, and the match must be exact:
  - same issue type (P1);
  - same pattern of conditions met, not met or unknown (P3–P8);
  - same evidence pattern (delivery photo yes/no, customer photo yes/no).
- The panel shows what it matched on, for example: "Matched on: missing item · 5 conditions · evidence pattern".
- **Never used for matching:** any party's history, identity or location. A first-time customer gets matched exactly like anyone else.
- **If fewer than 2 cases match:** the panel says "No closely matching cases". It doesn't quietly loosen the match. The agent can drop one matching fact themselves, and the panel then shows which one was dropped.

**4. What the agent sees**
- **2–3 case cards.** Where matching cases ended differently, the cards include each different outcome, so the agent doesn't get one answer to copy.
- **Each card shows:** issue type, conditions pattern, evidence present, outcome and amount, time taken to resolve, and which evidence the agent linked to which condition.
- **Reply wording (option A):** stays folded away until the agent has recorded their own decision. Then it shows how that case's outcome was explained to the customer.
- **Label on every card:** "Past case, for reference only. Not a recommendation."
- **No agent names, no star icon, no ranking.** The cards are called "reference cases".

**5. Admissibility check (step 1 questions)**
| Q | Result | Note |
|---|---|---|
| Q1 Objective | Pass | Exact match on stated facts |
| Q2 Traceable | Pass | Shows what was matched on; every case can be opened |
| Q3 No prediction | Pass | Shows past cases, not a forecast |
| Q4 No prescription | **Conditional pass** | Passes only if cases with different outcomes are shown together, with no "most common" highlight and no outcome percentages |
| Q5 Fair | Pass | No party is labelled; history is never used to match |
| Q6 Saves time | Pass for Ananya, lower for Rohit | Test both at Stage 9 |

**6. Known risks**
- **Anchoring:** agents may copy the first card they see. Mitigation: show differing outcomes, and fold away reply wording until the agent decides. *Test at Stage 9.*
- **A narrow pool:** strict criteria plus exact matching may often return "No closely matching cases" in this concept. That is acceptable; it's honest.
- **The criteria score agents:** they are used only to choose which cases enter the pool. No agent sees a rank, and no names are shown. Stage 12 must note that this still judges agents' work.

**Step 3 signed off by the owner (2026-10-09):**
- No outcome counts in the panel.
- Reply wording shows only after the agent records a decision.
- The reference-case thresholds stay as drafted.

### Step 4: Scenarios #92 + user flow
**The flow diagram is in FigJam:** "Escalation Agent User Flow (Stage 7)", https://www.figma.com/board/jdVOYesjFWTQOsQcxnVvV9

**Main flow:** the agent is chatting throughout. F3 to F6 happen *while* they talk to the customer, and the 5-minute reply-by clock (§6 of the frozen file) runs alongside.

| Step | What the agent does | Ideas used |
|---|---|---|
| F1 | The chat is handed over. The agent reads the customer's words, the issue the bot recorded and what the bot already offered | M1.1, M9.1 |
| F2 | Confirms or corrects the issue type, and sees the default liable party | M1.3, M1.2 |
| F3 | Glances at the condition checklist (P3–P8), the review triggers and the three clocks | M2.2, M2.3, M5.1, M7.3, M8.2 |
| F4 | For any condition that's unmet or unknown: checks the evidence and links it to the condition. If evidence is missing, asks the customer for it | M3.1–M3.6, B1 |
| F5 | Restaurant permission: requests it or sends a reminder. After 10 minutes with no reply, the agent decides whether to escalate | M5.1–M5.3 |
| F6 | Reads each party's record and the context: conflicting records, preparation time, open complaints today | M4.1, M4.2, M6.1–M6.3, B2, B3 |
| F7 | *Optional:* opens similar cases | M0.2 |
| F8 | Decides fault and outcome (full, partial with items selected, deny), or sends to review if a trigger fired or the amount is over the limit | M4.3, M7.4, M8.3 |
| F9 | Replies to the customer using a template that cites the policy condition. Reference wording from similar cases is now shown | M9.3, M9.4 |
| F10 | Case log saved | M0.1 |

**How each scenario moves through the flow:**
| Scenario | Path | What it tests in the flow |
|---|---|---|
| S1 Clean missing item | F1 → F3 (all met) → F5 (given) → F8 → F9 → F10 | The shortest path, and the "no default outcome" rule under consideration |
| S2 Thin evidence, past refunds | F3 → F4 ("No delivery photo"; customer photo 40 min later) → F6 (3 out of 7) → F7? → F8 | Whether history is treated as context; whether the agent opens "Show older" |
| S3 Conflicting records | F3 (T1, T4) → F6 (records side by side) → review | Whether the screen leans toward one side |
| S4 First-time customer | F3 (T1, T2) → F6 ("No history") → review | Whether "No history" reads as neutral |
| S5 Permission stalled | F5 → no reply after 10 min → the agent decides | Whether the dependency is visible and actionable |
| S6 Quality complaint | F2 (restaurant liable) → F6 (12 out of 2,140) → F8 | Whether who bears the cost is clear, and whether restaurant history gets the same treatment as customer history |
| S7 Late filing | F3 (P3 not met, T3) → F8 or review | Whether "outside window" is shown as a fact, with the decision left to the agent |

### Step 5: Two layouts compared
**The brief's three parts are:** live chat, customer information, and a separate derived-insights layer.

**Layout A: three columns**
- **Left (≈35%):** chat.
- **Middle (≈35%):** case information: order, evidence, party records, permission.
- **Right (≈30%):** insights: condition checklist, triggers, clocks, similar cases.

**Layout B: chat plus a panel organised condition by condition**
- **Left (≈40%):** chat.
- **Right (≈60%):** one panel, read top to bottom:
  1. **Status strip:** clocks, triggers, permission chip, timeline strip.
  2. **Condition cards (P3–P8):** each card shows the condition, its status and the fact behind it, with the linked evidence inline and the source shown.
  3. **Context section:** party records and B2/B3. Collapsed, with summary chips.
  4. **Decision bar** (Approve / Partial / Deny / Review), plus a drawer for similar cases.
- **Layer labels:** each element is tagged Data, Insight or Decision support. Insight lines get a distinct tint, so the insights layer stays visibly separate inside the cards.

| Criterion | A: three columns | B: condition-organised panel |
|---|---|---|
| Glanceable mid-chat | Medium. The eye moves across three columns | **High.** One column beside the chat, read top to bottom |
| Matches the flow F3–F8 | Partial. A condition is in one column and its evidence in another | **Strong.** Evidence sits inside its condition card (Insight 2) |
| Insights layer kept separate (brief) | **Strong.** Its own column | Medium. Separate as a *layer* (tint and labels), not as a column |
| Nothing left to assumption | Medium. Permission and history sit in the middle column and may be missed | **Strong.** The status strip always shows permission, triggers and "No history" chips |
| Fairness (three parties look equal) | Equal | Equal, provided the collapsed context section summarises all three parties together |
| Ananya (newer agent) | Clear separation, but more cross-referencing | **Guided top-to-bottom path** |
| Rohit (experienced) | Familiar CRM pattern (Zendesk-like) | Fast if the status strip is enough; may find the cards long |
| Building the coded prototype (Days 5–6) | Similar effort | Similar effort |

**Recommendation: Layout B.** It follows the order in which the agent actually decides (F3–F8), keeps evidence next to the condition it supports, and makes dependencies impossible to overlook.

**Flag, not changed silently:** B keeps the brief's derived-insights layer as a visually separate *layer* (tinted lines and labels) rather than a separate *column*. That reads the brief's "separate derived-insights layer" differently from Layout A. The project owner needs to confirm this reading. If "separate" must mean a separate panel, choose A.

**Owner decision on step 5 (2026-10-09): Layout A (three columns) goes to Stage 8.**

The recommendation was B. The owner chose A, which keeps the brief's three parts as three visible columns. The owner also confirmed that a visual layer would have been an acceptable reading of "separate", so the choice was made on preference, not on the brief.

**Weak points of Layout A to design around in Stage 8:**
1. **A condition and its evidence sit in different columns.** Fix: selecting a condition in the insights column highlights its linked evidence in the middle column, and the reverse.
2. **Permission and history may be missed in the middle column.** Fix: a status strip at the top of the insights column always shows the permission status, the review triggers and the "No history" or count chips for all three parties.
3. **The eye moves across three columns.** Fix: keep a fixed order inside each column, matching flow steps F3 to F6, and keep the clocks in one fixed spot.

These fixes go into Stage 8 and are tested in Stage 9 (think-aloud).

**Stage 7 status:** done 2026-10-09.

## Stage 8 — Design `[D]`

**Status:** Pre-approval, 2026-10-09. Visual decisions are on hold until the owner shares references.

**Decided so far:**
- **Layout change (owner):** chat moves to the centre, and a queue rail is added on the far left. Proposed order: queue → case info → chat → insights and decision. *Flagged; waiting on the owner's references.*
- **Queue rule (approved):** only the agent's own pending chats. Each shows issue type and wait time, sorted by wait time. No priority score or customer label.
- **References set (approved):** see the reference board artifact.
- **Fixed frame:** from now on, every layout is shown inside one fixed desktop frame. The size is to be chosen in checklist item A1.

**Open:** see `swiggy-design-approval-checklist.md` (frame and theme, layout, colour, type, shape, components, icons, motion, accessibility).

**Brand basis:** Swiggy Brand Book (2026): Orange #FF5200, Salt #FFEDE3, Gilroy. The book has no product-UI guidance, so the agent-tool kit is our proposal. See `swiggy-design-system-research.md`.
