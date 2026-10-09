---
name: swiggy-cross-party-evidence-research
description: Research on restaurant-side history, delivery-partner-side history, incident evidence, and cross-party dispute-review precedent — the gaps opened by the refined problem statement (order-centred, cross-party panel). Companion to swiggy-refund-and-blocking-rules-research.md, which was customer-side only. Cross-verified against a teammate's independent research pass, 2026-09-29 — see swiggy-secondary-research-crossverification.md.
researched: 2026-09-28
---

# Cross-Party Evidence Research: Restaurant, Delivery Partner, Incident Evidence, Precedent

## 0. Why this doc exists
The refined problem statement calls for a panel that contextualises **customer, restaurant, and delivery-partner** histories together, plus **incident evidence**. The existing research doc (`swiggy-refund-and-blocking-rules-research.md`) is almost entirely customer-side — it has no restaurant or delivery-partner signals. This doc fills that gap and adds outside precedent for order-centred, cross-party review panels, since none of it is Swiggy-specific and the project's Research behaviour rule requires citing industry practice separately from Swiggy fact.

Same evidence tags as the companion doc: **[Official]** platform's own published material, **[Reported]** news/reporting, **[Anecdotal]** forums, **[Inferred]** reasoning without a source.

**Headline:** No platform — Swiggy included — publishes how restaurant history, delivery-partner history and incident evidence are actually weighed together in a single decision. What's public is (a) that this data exists and is tracked, and (b) in one case (Uber Eats), the *categories* of fault attribution and its escalation triggers. The weighing logic stays private everywhere.

**Cross-verification note, 2026-09-29:** a teammate ran an independent secondary-research pass and reached the same headline conclusion. Their pass also surfaced new comparator evidence (DoorDash, Zepto, a Swiggy-group evidence-quality figure, and a concrete instance of AI-manipulated evidence) added into §1, §2 and §3 below, plus escalation-criteria detail added to §4a. Two of these were spot-checked directly against primary sources; see `swiggy-secondary-research-crossverification.md` for the full comparison.

---

## 1. Restaurant-side signals

### 1a. Swiggy [Official]
Swiggy's **Market Intelligence Dashboard** (launched 2024) gives restaurant partners a self-serve view of 30+ metrics across five tabs, including an **Operational Metrics tab covering "cancellations, availability, and complaints"** and benchmarking against ~30 similar restaurants nearby.
- This confirms Swiggy tracks restaurant-level cancellation and complaint rates internally.
- It is a **restaurant-facing growth tool**, not a support-agent tool. Whether a support agent sees the same or similar metrics when reviewing a specific order is **not stated anywhere found** — flagged as an open question, not assumed. A teammate's independent research pass checked this same question and found nothing new either; still open.
- Source: https://blog.swiggy.com/swiggy-catalyst/stay-ahead-of-the-game-with-swiggys-market-intelligence-dashboard/

### 1b. Uber Eats [Official, industry practice not Swiggy]
Uber Eats' merchant "Order Accuracy" report tracks an **Inaccurate Orders Rate**, breaks it down "by issue type," and shows a restaurant's "Top inaccurate items" by how often each was reported inaccurate. This is the clearest public example of a restaurant-side history metric a platform actively surfaces (to the restaurant, at least).
- Source: https://www.uber.com/en-GB/blog/your-guide-to-monitor-your-order-accuracy-on-uber-eats

### 1c. Zomato [Official + Reported]
Zomato re-did its rating system (2019 blog) but the fetch of that page was blocked by robots.txt — **could not verify** what currently feeds a restaurant's rating. Not cited further; flagged as unread.

### 1d. DoorDash and an older Zomato rejection rule — published numeric thresholds [Official / Reported, industry practice not Swiggy]
Neither of these was independently re-verified in this pass; both are narrowly specific and plausibly sourced from a teammate's independent research.
- **DoorDash** "Order Remade Policy" (merchant help centre): a courier arriving more than **20 minutes** after the estimated order-ready time qualifies for a remake, claimed within **7 days**, for perishable items only.
- **Zomato**, an older rule (Deccan Herald): a restaurant's daily rejection rate above **3%** led to next-day suspension; a rejected order paid the customer **25% of order value** (minimum ₹25, maximum ₹200).

**Why this matters:** both research passes, independently, found no numeric threshold anywhere for Swiggy's own refund or lateness rules — everything is "up to," "case to case," or unstated. These two examples show that published, numeric thresholds do exist elsewhere in the industry. That reframes Swiggy's silence on thresholds as a platform choice, not something no platform ever discloses.

**Gap:** No source, anywhere, describes a restaurant-side metric shown *at the point of an individual refund decision* (only aggregate, backward-looking dashboards for the restaurant's own use, or — for DoorDash/Zomato — published rules with no visible per-case screen behind them).

---

## 2. Delivery-partner-side signals

### 2a. Swiggy [Official / Reported]
No public source describes delivery-partner performance history (on-time rate, complaint count, fault flags) in a form usable for a specific dispute. This is a **confirmed gap**, not an assumption — checked again in the teammate's independent pass with the same result.

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

### 2e. Zepto — a third close Indian-market comparator [Reported]
Business Standard (Dec 2025) quotes Zepto VP Karthic Somalinga: Zepto uses "a mix of automated systems and human review," with ML models that "flag suspicious or inconsistent refund activity in real time, supported by periodic manual checks," and is exploring open-source AI-image-manipulation detectors given rising AI-edited-photo fraud. Single-source quote, not independently re-verified — treated as [Reported]. Alongside Zomato's karma score and DoorDash's published threshold (§1d), this gives three distinct rival approaches to the same underlying problem: an opaque score (Zomato), a published rule with no visible screen (DoorDash), and a stated automated-plus-manual mix with no detail on the screen (Zepto). None of the three show what a human reviewer actually sees.

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

### 3c. Supr Daily / AWS Rekognition — a Swiggy-group evidence-quality figure [Reported, vendor case study — spot-checked verbatim]
Fetched directly from https://aws.amazon.com/solutions/case-studies/suprdaily-case-study/: *"The company estimates that as many as 25 percent of refunds were issued incorrectly, primarily due to poor quality or missing delivery photos."* Supr Daily (Swiggy Group's grocery/milk subscription arm) could only manually review 5-10% of delivery photos before automating quality checks with Amazon Rekognition to give delivery partners instant feedback on photo quality. This is the single most concrete **Swiggy-ecosystem** number connecting evidence quality to refund-error rate found anywhere in this research — stronger than anything sourced from a rival, because it's Swiggy's own group company, not an outside platform.

### 3d. A concrete, named instance of AI-manipulated evidence [Reported, single incident — do not generalise]
Business Today (26 Nov 2025) reports an Instamart case where a customer allegedly used an AI image tool with the prompt "apply more cracks" to produce a photo showing 20+ cracked eggs (one egg was actually cracked); Swiggy issued a full refund of roughly ₹245. Not independently re-verified in this pass — a single media report citing a social-media post — so treat with the same caution this doc already applies to anecdotal evidence elsewhere. It matters here because it turns the [Inferred] argument in 3e below from a hypothesis into a documented example.

### 3e. Implication for the interface [Inferred, now partly evidenced by 3d]
The two evidence models are structurally different — Swiggy's "evidence" is customer-submitted, after the fact, unspecified in form; Uber's is platform-captured, at the moment of delivery, fixed in form. An order-centred panel should show which kind of evidence exists for a given order (captured-at-delivery vs. submitted-after-the-fact vs. none), since that difference changes how much weight a fact can bear — this is itself a neutral, traceable fact, not a judgement. This was originally an inferred design argument with no concrete example behind it; §3d now gives it one (a real, dated, reported case where after-the-fact, customer-submitted photo evidence was reportedly fabricated). The argument for a visible evidence-type flag is accordingly stronger than when this doc was first written, and is carried forward as a Define-stage question in `swiggy-secondary-research-crossverification.md` §4.

---

## 4. Cross-party / order-centred review panels: outside precedent

### 4a. Uber Eats' fault-category model, with escalation criteria [Official, industry practice not Swiggy — spot-checked verbatim, 2026-09-29]
This is the closest real-world precedent to "policy shown as conditions checked against facts, not a verdict" that the project's core design principle already commits to. Uber Eats names concrete, disjoint categories:
- **Merchant-liable:** missing/incorrect items, wrong order, food quality/condition, non-delivery when the merchant used its own delivery staff.
- **Merchant-exempt:** late delivery, non-delivery via an Uber courier, damage or condition issues tied to delivery.
- Refunds are also withheld outright on "any indicator of potentially fraudulent activities" — an unappealable, unexplained override sitting above the category logic.
- **Escalation criteria, confirmed verbatim against https://merchants.ubereats.com/au/en/order-errors:** *"We escalate cases to a trained team for investigation and review before making refund decisions for requests that are: Not filed in a reasonable time frame, For high-value orders, For orders with alcohol items, For first-time customers."* The same page also states Uber Eats "track[s] customer refund history and block[s] customers who abuse [the] refund policy," and that couriers with a significant number of missing-item reports "are automatically flagged" with the merchant then not charged.
- Source: https://www.uber.com/gb/en/blog/order-error-adjustments-best-practices/ ; escalation criteria confirmed at https://merchants.ubereats.com/au/en/order-errors

**Design read [Inferred]:** this is evidence that a **named, disjoint fault-category list**, paired with a **named set of escalation triggers** (value, alcohol, first-time customer, timing), is an implementable, real-world pattern — directly reusable as the backbone of the interface's policy-condition checklist and its approval/exception-queue idea, extended to cover Swiggy's own categories (customer / restaurant / delivery partner / Swiggy) from the companion doc's Section 2.

### 4b. Zendesk Agent Workspace context panel [Official, generic CRM — not order-specific, not Swiggy]
Zendesk's own documentation describes the context panel as showing "contact information about the customer and the customer's interaction history," plus related records and relevant help-center articles, organised as a row of switchable icons. This is a **generic customer-support pattern**, not built around an order or a multi-party dispute — useful as a baseline of "what a context panel normally shows," which this project's brief already goes well beyond by requiring restaurant and delivery-partner context too.
- Source: https://support.zendesk.com/hc/en-us/articles/4408836526362-Using-the-context-panel-in-the-Zendesk-Agent-Workspace

### 4c. Airbnb Resolution Center [inconclusive]
Airbnb's own help article does not describe the Resolution Center's evidence or decision process in usable detail — the page found covers a different, EU-regulatory complaints process. **Not cited further.**

### 4d. Academic angle, title confirmed / not yet read by this project directly [Reported]
"Improving Dispute Resolution in Two-Sided Platforms: The Case of Review Blackmail," *Management Science*, Vol. 69, No. 10 (2022) — a real, peer-reviewed paper on platform dispute resolution, listed on both ACM and INFORMS. **Findings not read yet** — per this project's own rule, nothing from it should be cited until it's actually read. A teammate's independent research pass also left this unread. Added to the same "confirmed to exist, not yet read" list as the two papers already logged in the case-study structure doc.
- https://pubsonline.informs.org/doi/10.1287/mnsc.2022.4655

---

## 5. What this changes for the interface [Inferred, checked against project rules]
- **New decision supported:** "Does the restaurant's or delivery partner's own recent record change how this specific claim reads?" — this is additive to, not a replacement for, the customer-side facts already covered.
- **Objective, traceable version:** plain counts by party, same pattern as the customer side — "this restaurant: 4 packaging complaints in 30 days" / "this delivery partner: 2 non-delivery flags in 30 days" — dated, sourced, no computed score.
- **The line not to cross, now with two real-world examples of what crossing it looks like:** Zomato's karma score and Uber's "significant error pattern" auto-flag are exactly the kind of derived reliability score this project's no-prediction rule rules out — and Section 2c above shows a real, documented fairness objection to that approach. That strengthens rather than just illustrates the case for showing raw, dated counts instead of any score.
- **Evidence-type tag, now with a concrete case behind it (§3c-3e):** for a given order, whether evidence was captured at the moment of delivery (Uber POD-style), submitted after the fact by the customer, or doesn't exist for this order type — a neutral fact about evidentiary strength, not a verdict on the claim.
- **Fault-category checklist, sharpened, now with escalation triggers too:** Uber Eats' four-way disjoint category list, plus its named escalation criteria (value, alcohol, first-time customer, timing), is a workable template for turning Swiggy's own fault-attribution rule (companion doc, Section 2) into the kind of checkable condition list — and approval-queue trigger set — the Design stage needs, rather than a vaguer "who's at fault" prompt.
- **Confirmed gap, not filled:** nobody — Swiggy, Zomato, Zepto, or Uber — publishes what a human reviewer's screen actually shows, or how restaurant/delivery-partner/customer signals get weighed against each other. That gap is the case study's own contribution area, not something more searching will resolve.

---

## Sources

Official (Swiggy)
- Market Intelligence Dashboard: https://blog.swiggy.com/swiggy-catalyst/stay-ahead-of-the-game-with-swiggys-market-intelligence-dashboard/

Official (industry practice, not Swiggy)
- Uber Direct proof-of-delivery docs: https://developer.uber.com/docs/deliveries/guides/proof-of-delivery
- Uber Eats order accuracy guide: https://www.uber.com/en-GB/blog/your-guide-to-monitor-your-order-accuracy-on-uber-eats
- Uber Eats order error adjustments & fault categories: https://www.uber.com/gb/en/blog/order-error-adjustments-best-practices/
- Uber Eats merchant escalation criteria (spot-checked verbatim, 2026-09-29): https://merchants.ubereats.com/au/en/order-errors
- Zendesk context panel: https://support.zendesk.com/hc/en-us/articles/4408836526362-Using-the-context-panel-in-the-Zendesk-Agent-Workspace
- DoorDash Order Remade Policy: https://help.doordash.com/en-us/merchants/article/what-do-i-do-if-a-customer-reports-an-item-is-missing

Reported (vendor case study, spot-checked verbatim)
- Supr Daily / AWS case study, 25% incorrect-refund figure: https://aws.amazon.com/solutions/case-studies/suprdaily-case-study/

Reported
- Outlook Business, Zomato karma score: https://www.outlookbusiness.com/news/inside-zomatos-karma-score-what-deepinder-goyal-reveals-about-fraud-refunds
- TechStory, Zomato rider churn/fraud: https://techstory.in/zomato-ceo-lifts-the-lid-on-gig-worker-churn-and-fraud-challenges/
- India News Network, karma-system scrutiny by Telangana Gig and Platform Workers Association: https://www.indianewsnetwork.com/en/zomato-defends-karma-system-amid-scrutiny-gig-worker-practices-20260105
- Deccan Herald, older Zomato restaurant-rejection rule (via teammate's research, not independently re-verified): restaurant rejection-rate and payout rule
- Business Standard (Dec 2025), Zepto's automated-plus-manual refund review (via teammate's research, not independently re-verified)
- Business Today (26 Nov 2025), Instamart AI-edited-photo refund case (via teammate's research, not independently re-verified)

Academic, title confirmed / not read
- "Improving Dispute Resolution in Two-Sided Platforms: The Case of Review Blackmail," Management Science 69(10), 2022: https://pubsonline.informs.org/doi/10.1287/mnsc.2022.4655

Could not access / inconclusive
- Zomato's 2019 ratings-system blog post (robots.txt blocked).
- Airbnb Resolution Center process detail (page found covers a different EU complaints process, not host-guest disputes).
- Uber Eats "managing refunds for missing or incorrect orders" merchant help page (404).

See also
- `swiggy-secondary-research-crossverification.md` — full comparison against a teammate's independent research pass, including two spot-checks, one flagged contradiction (cancellation-fee percentage, logged in `swiggy-refund-and-blocking-rules-research.md` §10), and open-question status changes.
