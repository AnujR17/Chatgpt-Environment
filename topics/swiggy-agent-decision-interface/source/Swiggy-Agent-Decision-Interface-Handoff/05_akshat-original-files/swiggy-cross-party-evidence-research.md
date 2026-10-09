---
name: swiggy-cross-party-evidence-research
description: Research on restaurant-side history, delivery-partner-side history, incident evidence, and cross-party dispute-review precedent — the gaps opened by the refined problem statement (order-centred, cross-party panel). Companion to swiggy-refund-and-blocking-rules-research.md, which was customer-side only.
researched: 2026-09-28
---

# Cross-Party Evidence Research: Restaurant, Delivery Partner, Incident Evidence, Precedent

## 0. Why this doc exists
The refined problem statement calls for a panel that contextualises **customer, restaurant, and delivery-partner** histories together, plus **incident evidence**. The existing research doc (`swiggy-refund-and-blocking-rules-research.md`) is almost entirely customer-side — it has no restaurant or delivery-partner signals. This doc fills that gap and adds outside precedent for order-centred, cross-party review panels, since none of it is Swiggy-specific and the project's Research behaviour rule requires citing industry practice separately from Swiggy fact.

Same evidence tags as the companion doc: **[Official]** platform's own published material, **[Reported]** news/reporting, **[Anecdotal]** forums, **[Inferred]** reasoning without a source.

**Headline:** No platform — Swiggy included — publishes how restaurant history, delivery-partner history and incident evidence are actually weighed together in a single decision. What's public is (a) that this data exists and is tracked, and (b) in one case (Uber Eats), the *categories* of fault attribution. The weighing logic stays private everywhere.

---

## 1. Restaurant-side signals

### 1a. Swiggy [Official]
Swiggy's **Market Intelligence Dashboard** (launched 2024) gives restaurant partners a self-serve view of 30+ metrics across five tabs, including an **Operational Metrics tab covering "cancellations, availability, and complaints"** and benchmarking against ~30 similar restaurants nearby.
- This confirms Swiggy tracks restaurant-level cancellation and complaint rates internally.
- It is a **restaurant-facing growth tool**, not a support-agent tool. Whether a support agent sees the same or similar metrics when reviewing a specific order is **not stated anywhere found** — flagged as an open question, not assumed.
- Source: https://blog.swiggy.com/swiggy-catalyst/stay-ahead-of-the-game-with-swiggys-market-intelligence-dashboard/

### 1b. Uber Eats [Official, industry practice not Swiggy]
Uber Eats' merchant "Order Accuracy" report tracks an **Inaccurate Orders Rate**, breaks it down "by issue type," and shows a restaurant's "Top inaccurate items" by how often each was reported inaccurate. This is the clearest public example of a restaurant-side history metric a platform actively surfaces (to the restaurant, at least).
- Source: https://www.uber.com/en-GB/blog/your-guide-to-monitor-your-order-accuracy-on-uber-eats

### 1c. Zomato [Official + Reported]
Zomato re-did its rating system (2019 blog) but the fetch of that page was blocked by robots.txt — **could not verify** what currently feeds a restaurant's rating. Not cited further; flagged as unread.

**Gap:** No source, anywhere, describes a restaurant-side metric shown *at the point of an individual refund decision* (only aggregate, backward-looking dashboards for the restaurant's own use).

---

## 2. Delivery-partner-side signals

### 2a. Swiggy [Official / Reported]
No public source describes delivery-partner performance history (on-time rate, complaint count, fault flags) in a form usable for a specific dispute. This is a **confirmed gap**, not an assumption.

### 2b. Zomato [Reported]
- CEO Deepinder Goyal: Zomato runs a **"karma score"** covering both customers *and* riders, used to judge who's "more likely to be right" in a dispute. About **5,000 delivery partners are terminated monthly**, mostly for repeated fraud.
- Important admission, direct quote: fraud is "not accidental most of the time," but the karma system **"sometimes cannot definitively assign responsibility."** That's a competitor's own leadership acknowledging the same fault-attribution uncertainty this project's research doc already found in Swiggy's contradictory refund terms.
- Sources: https://www.outlookbusiness.com/news/inside-zomatos-karma-score-what-deepinder-goyal-reveals-about-fraud-refunds , https://techstory.in/zomato-ceo-lifts-the-lid-on-gig-worker-churn-and-fraud-challenges/

### 2c. Fairness scrutiny of that karma system [Reported]
The Telangana Gig and Platform Workers Association publicly disputes the karma system's fairness: "ratings, penalties and the risk of losing future orders can strongly influence delivery behaviour," and disputes that responsibility is being fairly assigned. This is a **real, citable instance** of the exact fairness risk the project brief asks us to watch for — a computed reliability score shaping outcomes for people who can't see or contest it.
- Source: https://www.indianewsnetwork.com/en/zomato-defends-karma-system-amid-scrutiny-gig-worker-practices-20260105

### 2d. Uber Eats [Official, industry practice not Swiggy]
Uber Eats' order-error policy states couriers "with significant error patterns" are **"automatically flagged."** This is the one platform that explicitly confirms a delivery-side history flag exists and feeds into fault decisions — though, as with everything else, it doesn't say what the flag looks like to a human reviewer or what threshold trips it.
- Source: https://www.uber.com/gb/en/blog/order-error-adjustments-best-practices/

---

## 3. Incident evidence: what gets captured, and how

### 3a. Already known (from the companion doc) [Official, Swiggy]
- Instamart: refund/replacement requires "the required evidences" from the buyer (type unspecified) plus merchant permission.
- Alcohol: the OTP given to the delivery partner counts as accepted delivery — a single, binary, timestamped piece of evidence.
- Food orders: no written evidence rule found at all.

### 3b. Uber Direct proof-of-delivery [Official, industry practice not Swiggy]
Uber's own delivery API documents a structured evidence bundle per order:
- a **photo** of the order at the drop-off point,
- a **signature** and recipient name,
- a **barcode scan** with timestamp and outcome,
- **ID-verification photos** where age/ID checks apply,
- retained 7 days on the merchant dashboard, 30 days via API.
This is the most concrete, named model of "incident evidence" found anywhere in this research — a fixed, structured evidence set captured **at the moment of delivery**, not gathered after the fact from the customer. Its use in actual dispute resolution isn't documented publicly, consistent with the pattern seen everywhere else: platforms publish what evidence exists, not how it's weighed.
- Source: https://developer.uber.com/docs/deliveries/guides/proof-of-delivery

**Implication for the interface [Inferred]:** the two evidence models are structurally different — Swiggy's "evidence" is customer-submitted, after the fact, unspecified in form; Uber's is platform-captured, at the moment of delivery, fixed in form. An order-centred panel should show which kind of evidence exists for a given order (captured-at-delivery vs. submitted-after-the-fact vs. none), since that difference changes how much weight a fact can bear — this is itself a neutral, traceable fact, not a judgement.

---

## 4. Cross-party / order-centred review panels: outside precedent

### 4a. Uber Eats' fault-category model [Official, industry practice not Swiggy]
This is the closest real-world precedent to "policy shown as conditions checked against facts, not a verdict" that the project's core design principle already commits to. Uber Eats names concrete, disjoint categories:
- **Merchant-liable:** missing/incorrect items, wrong order, food quality/condition, non-delivery when the merchant used its own delivery staff.
- **Merchant-exempt:** late delivery, non-delivery via an Uber courier, damage or condition issues tied to delivery.
- Refunds are also withheld outright on "any indicator of potentially fraudulent activities" — an unappealable, unexplained override sitting above the category logic.
- Source: https://www.uber.com/gb/en/blog/order-error-adjustments-best-practices/

**Design read [Inferred]:** this is evidence that a **named, disjoint fault-category list** (not a free-text "who's at fault?" judgement call) is an implementable, real-world pattern — directly reusable as the backbone of the interface's policy-condition checklist, extended to cover Swiggy's own categories (customer / restaurant / delivery partner / Swiggy) from the companion doc's Section 2.

### 4b. Zendesk Agent Workspace context panel [Official, generic CRM — not order-specific, not Swiggy]
Zendesk's own documentation describes the context panel as showing "contact information about the customer and the customer's interaction history," plus related records and relevant help-center articles, organised as a row of switchable icons. This is a **generic customer-support pattern**, not built around an order or a multi-party dispute — useful as a baseline of "what a context panel normally shows," which this project's brief already goes well beyond by requiring restaurant and delivery-partner context too.
- Source: https://support.zendesk.com/hc/en-us/articles/4408836526362-Using-the-context-panel-in-the-Zendesk-Agent-Workspace

### 4c. Airbnb Resolution Center [inconclusive]
Airbnb's own help article does not describe the Resolution Center's evidence or decision process in usable detail — the page found covers a different, EU-regulatory complaints process. **Not cited further.**

### 4d. Academic angle, title confirmed / not yet read [Reported]
"Improving Dispute Resolution in Two-Sided Platforms: The Case of Review Blackmail," *Management Science*, Vol. 69, No. 10 (2022) — a real, peer-reviewed paper on platform dispute resolution, listed on both ACM and INFORMS. **Findings not read yet** — per this project's own rule, nothing from it should be cited until it's actually read. Added to the same "confirmed to exist, not yet read" list as the two papers already logged in the case-study structure doc.
- https://pubsonline.informs.org/doi/10.1287/mnsc.2022.4655

---

## 5. What this changes for the interface [Inferred, checked against project rules]
- **New decision supported:** "Does the restaurant's or delivery partner's own recent record change how this specific claim reads?" — this is additive to, not a replacement for, the customer-side facts already covered.
- **Objective, traceable version:** plain counts by party, same pattern as the customer side — "this restaurant: 4 packaging complaints in 30 days" / "this delivery partner: 2 non-delivery flags in 30 days" — dated, sourced, no computed score.
- **The line not to cross, now with a real-world example of what crossing it looks like:** Zomato's karma score and Uber's "significant error pattern" auto-flag are exactly the kind of derived reliability score this project's no-prediction rule rules out — and Section 2c above shows a real, documented fairness objection to that approach. That strengthens rather than just illustrates the case for showing raw, dated counts instead of any score.
- **Evidence-type tag, new:** for a given order, whether evidence was captured at the moment of delivery (Uber POD-style), submitted after the fact by the customer, or doesn't exist for this order type — a neutral fact about evidentiary strength, not a verdict on the claim.
- **Fault-category checklist, sharpened:** Uber Eats' four-way disjoint category list is a workable template for turning Swiggy's own fault-attribution rule (companion doc, Section 2) into the kind of checkable condition list the Design stage needs, rather than a vaguer "who's at fault" prompt.
- **Confirmed gap, not filled:** nobody — Swiggy, Zomato, or Uber — publishes what a human reviewer's screen actually shows, or how restaurant/delivery-partner/customer signals get weighed against each other. That gap is the case study's own contribution area, not something more searching will resolve.

---

## Sources

Official (Swiggy)
- Market Intelligence Dashboard: https://blog.swiggy.com/swiggy-catalyst/stay-ahead-of-the-game-with-swiggys-market-intelligence-dashboard/

Official (industry practice, not Swiggy)
- Uber Direct proof-of-delivery docs: https://developer.uber.com/docs/deliveries/guides/proof-of-delivery
- Uber Eats order accuracy guide: https://www.uber.com/en-GB/blog/your-guide-to-monitor-your-order-accuracy-on-uber-eats
- Uber Eats order error adjustments & fault categories: https://www.uber.com/gb/en/blog/order-error-adjustments-best-practices/
- Zendesk context panel: https://support.zendesk.com/hc/en-us/articles/4408836526362-Using-the-context-panel-in-the-Zendesk-Agent-Workspace

Reported
- Outlook Business, Zomato karma score: https://www.outlookbusiness.com/news/inside-zomatos-karma-score-what-deepinder-goyal-reveals-about-fraud-refunds
- TechStory, Zomato rider churn/fraud: https://techstory.in/zomato-ceo-lifts-the-lid-on-gig-worker-churn-and-fraud-challenges/
- India News Network, karma-system scrutiny by Telangana Gig and Platform Workers Association: https://www.indianewsnetwork.com/en/zomato-defends-karma-system-amid-scrutiny-gig-worker-practices-20260105

Academic, title confirmed / not read
- "Improving Dispute Resolution in Two-Sided Platforms: The Case of Review Blackmail," Management Science 69(10), 2022: https://pubsonline.informs.org/doi/10.1287/mnsc.2022.4655

Could not access / inconclusive
- Zomato's 2019 ratings-system blog post (robots.txt blocked).
- Airbnb Resolution Center process detail (page found covers a different EU complaints process, not host-guest disputes).
- Uber Eats "managing refunds for missing or incorrect orders" merchant help page (404).
