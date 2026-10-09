---
name: swiggy-secondary-research-crossverification
description: Cross-verification of a teammate's independent secondary-research pass against this project's own research docs — corroborations, new evidence, contradictions, and open-question status changes. Read alongside swiggy-refund-and-blocking-rules-research.md, swiggy-cross-party-evidence-research.md and swiggy-bot-vs-agent-parameters.md, which this doc points into.
researched: 2026-09-29
sources: cowork
---

# Cross-Verification: Teammate's Secondary Research vs This Project's Research

## 0. What this is
A teammate ran an independent secondary-research pass ("swiggy_evidence-based_research.md", provided 2026-09-29) using the same evidence-tier convention this project already uses (Official / Law / Reported / Anecdotal / Inferred). This doc checks that pass against the three research docs already in this project, flags what corroborates, what's new, what contradicts, and what it changes for open questions. Two of the teammate's more load-bearing new claims were spot-checked directly against primary sources in this pass (Section 2a, 2b); the rest are relayed at the teammate's stated tier and have not been independently re-fetched, which is noted wherever it matters.

**Overall read:** nothing here overturns the existing research. It corroborates the highest-stakes shared facts (NCH complaint numbers, SHIELD's scope, the E-Commerce Rules timelines), adds real new comparator evidence (DoorDash, Zepto, Supr Daily), and surfaces one genuine discrepancy worth designing around (the cancellation-fee percentage, Section 3 below).

---

## 1. Corroborated — independent convergence, raises confidence
Two independently-run research passes landing on the same fact is stronger evidence than either alone. These matched exactly:

- **NCH complaint volume:** 10,590 complaints against Swiggy, ~912 refund-related, 7,938 against Zomato — both docs cite the same underlying Business Standard (21 May 2025) reporting and arrive at identical figures.
- **CCPA probe status:** suo motu, started around October 2024, "likely to direct" revisions — both find the same unresolved status; neither found a final order.
- **SHIELD device intelligence:** May 2024, framed around promo abuse and delivery-partner abuse; neither pass found any statement that it feeds refund decisions. Teammate adds direct executive quotes (SHIELD's Gautam Sehgal; Swiggy's Trust & Safety lead Dolly Sureka) this project's doc didn't have — useful attribution, same conclusion.
- **E-Commerce Rules 2020:** 48-hour grievance acknowledgement, one-month resolution — matches.
- **Uber Eats fault-category model:** merchant-liable/merchant-exempt split, structured proof-of-delivery, courier auto-flagging for repeated missing-item reports — matches `swiggy-cross-party-evidence-research.md` §4a exactly, from a different regional page of the same Uber Eats material. Teammate's version has escalation-criteria detail ours didn't — see Section 2a below.
- **Swiggy's refund-policy page not rendering on fetch** — both passes independently hit the same wall and worked from search-indexed excerpts instead. Confirms this is a page-level issue, not a one-off tooling failure on either side.

---

## 2. New evidence — extends the existing docs

### 2a. Uber Eats escalation criteria — spot-checked, confirmed verbatim
Fetched directly from https://merchants.ubereats.com/au/en/order-errors (teammate cited a different regional mirror; same content):
- *"We escalate cases to a trained team for investigation and review before making refund decisions for requests that are: Not filed in a reasonable time frame, For high-value orders, For orders with alcohol items, For first-time customers."*
- *"We track customer refund history and block customers who abuse our refund policy."*
- *"Delivery people who have a significant number of missing item reports... are automatically flagged... Partners are not charged for any refunds associated with deliveries from these delivery people."*

This is a concrete, named escalation-trigger list (value ceiling, alcohol, first-time customer, late filing) that `swiggy-cross-party-evidence-research.md` §4a didn't have — it only had the fault-category split, not the escalation triggers. **Directly usable** for the Design stage's approval/exception-queue idea, and for the expert interview's questions on value ceilings. Added to that doc's §4a below.

### 2b. Supr Daily / AWS Rekognition — spot-checked, confirmed verbatim
Fetched directly from https://aws.amazon.com/solutions/case-studies/suprdaily-case-study/:
- *"The company estimates that as many as 25 percent of refunds were issued incorrectly, primarily due to poor quality or missing delivery photos."*
- Context: Supr Daily could only manually review 5-10% of delivery photos before automating quality checks with Amazon Rekognition.

Supr Daily is a Swiggy Group company (grocery/milk subscription arm). This is the single most concrete **Swiggy-ecosystem** number connecting evidence quality to refund-error rate found in either research pass — stronger than anything sourced from a rival. Added to `swiggy-cross-party-evidence-research.md` §3.

### 2c. Agent Workbench — second, more recent, independent source
Not independently re-fetched (job-ad aggregator, lower stakes), but specific and plausible: a 2026 Swiggy backend engineering job ad (startup.jobs) lists "CRM (Agent Workbench, Customer Touchpoint Automation, Live Tracking Screen)" as a current team ownership area. `swiggy-bot-vs-agent-parameters.md`'s open question notes the bot/agent/backend split is "built from one process description, not confirmed architecture" (the 2021-era DEV.to engineering repost). A second, independent, more recent (2026) source naming "Agent Workbench" as a live team responsibility **partially** resolves that — the name and team are now corroborated twice. What the screen actually shows an agent is still not stated anywhere.

### 2d. New comparators not in either doc before — DoorDash and an older Zomato rule
- **DoorDash** "Order Remade Policy" (Official, merchant help centre): courier arrives more than 20 minutes after the estimated ready time, claim made within 7 days, perishable items only.
- **Zomato**, older rule (Deccan Herald, Reported): restaurant daily rejection rate above 3% led to next-day suspension; a rejected order paid the customer 25% of order value (minimum ₹25, maximum ₹200).

Neither claim independently re-verified this pass (both narrowly specific and plausibly sourced). What matters for this project: both docs note repeatedly that **no numeric threshold has been found anywhere for Swiggy** — not for lateness, not for refund percentages. These two examples show numeric, published thresholds do exist in the industry (DoorDash's 20-minute/7-day rule, Zomato's 3%/25% rule). That reframes Swiggy's silence on thresholds as a choice some competitors don't make, rather than something no platform publishes.

### 2e. New comparator — Zepto
Business Standard (Dec 2025) quotes Zepto VP Karthic Somalinga: "a mix of automated systems and human review," ML models that "flag suspicious or inconsistent refund activity in real time, supported by periodic manual checks," and exploration of open-source AI-image-manipulation detectors. Single-source quote, treated as [Reported] and not independently re-verified. Gives a third close Indian-market comparator alongside Zomato and (now) DoorDash.

### 2f. New — a concrete, named instance of the evidence-fraud risk this project already discusses abstractly
Business Today (26 Nov 2025) reports an Instamart case where a customer allegedly used an AI image tool with the prompt "apply more cracks" to produce a photo showing 20+ cracked eggs (one egg was actually cracked); Swiggy issued a full refund of roughly ₹245. Not independently re-verified — single media report citing a social-media post, so treat as [Reported, single incident, do not generalise], the same caution this project already applies to anecdotal evidence elsewhere.

This matters because `swiggy-cross-party-evidence-research.md` §3b already made an **[Inferred]** argument that customer-submitted, after-the-fact evidence is structurally weaker than platform-captured, at-the-moment-of-delivery evidence (Uber's proof-of-delivery model). This incident turns that inferred risk into a documented one — it's no longer just a hypothesis about why an evidence-type distinction would matter.

### 2g. New — agent-effort and AHT benchmarks (nothing comparable existed in either doc)
Industry surveys with no Swiggy-specific figure attached, all [Reported], none independently re-verified this pass:
- ContactBabel US/UK Decision-Makers' Guides 2024: mean service-call handling time rising year over year (442s US 2023, up from 306s in 2012).
- Salesforce State of Service, 6th edition: "58% of agents at underperforming organizations toggle between multiple screens to find what they need — compared to 36% at high performers," and agents spend "just 39% of their time servicing customers."
- HBR (Aug 2022, citing log data from 137 users, authors from vendor Soroco): workers toggle between applications "roughly 1,200 times each day," losing "roughly 9% of their time."
- Verint 2026 survey: "In 45% of calls, agents spend an average of three minutes searching for answers."

None of this is Swiggy-specific, and all of it is vendor or vendor-adjacent survey data — cite as industry-practice context, not fact about Swiggy. But it's directly relevant to this project's own Testing-stage rule (measure decision time and effort, never predicted outcomes) and to the brief's real-time constraint ("the agent is mid-conversation and cannot study a dense dashboard"). Worth carrying into the Testing-stage KPI list as candidate effort metrics: screen/lookup count, toggle count, time-to-decision.

### 2h. Literature papers — partial progress on a standing open item, with a caution
This project's open items already list: *"Read the three literature/academic papers before citing any findings."* The teammate's pass states it read the "abstract and partial full text" of Parasuraman & Manzey (2010) and "full working paper text excerpts" of Brynjolfsson, Li & Raymond, citing specific figures (an 82% vs 33% failure-detection rate under variable vs constant automation reliability; a 14% average / 34% novice productivity gain from AI assistance).

**This is not a clean resolution of that open item.** Neither of us has opened either paper directly — these figures are relayed secondhand through the teammate's research into this doc. Treat them as [Reported via teammate, not independently verified] until one of us reads the primary source. The Management Science dispute-resolution paper (already logged as unread in `swiggy-case-study-structure.md`) remains completely unread by both passes.

---

## 3. Contradiction flagged — the cancellation-fee percentage
Three different numbers now exist for what should be one rule, across the two research passes combined:

1. The Refund Policy itself: Swiggy "shall have a right to charge **100%**" of order value on customer cancellation, to compensate merchants and delivery partners.
2. CCPA-probe reporting (both docs, same Business Standard / MediaNama source): regulators are scrutinising cancellation charges of **up to 90%**.
3. Teammate's addition — two live @Swiggy / @SwiggyCares support replies on X stating a flat, non-graduated **100%** cancellation fee applies "even one second after" placing an order, with no mention of a lower tier.

This is worth designing around, not resolving by picking one number. It suggests the *policy* text (100%, phrased as a ceiling — "up to"), the *regulatory characterisation* (up to 90%, implying some real-world graduation), and the *live support answer* (a flat 100%, no graduation) may not actually agree with each other. An interface surfacing this condition should show the policy figure, flag that regulator reporting and live support statements differ from it, and let the agent see the discrepancy rather than silently normalising to one number. Added as a new gap row to `swiggy-refund-and-blocking-rules-research.md` §10.

A second point, not a new contradiction but worth repeating because it bears on how much to trust vendor material generally: the Databricks blog (already cited in `swiggy-case-study-structure.md` as making unverified claims) says its Swiggy AI agent achieved "100% of customer queries... fully automated without human intervention" in the same document that describes a designed "graceful fallback to human agents." Teammate's pass flags this same internal contradiction independently — it reinforces, rather than changes, this project's existing stance of treating vendor-published automation figures (including the ~75% bot-resolution figure already logged as unverified) as marketing claims, not fact.

---

## 4. Open questions — status update
- *"Whether a support agent sees restaurant/delivery-partner metrics at all"* (`swiggy-cross-party-evidence-research.md`) — **still open**. Teammate's pass found the same thing: the Market Intelligence Dashboard is confirmed restaurant-facing only; nothing on agent-side visibility either way.
- *"Bot/agent/backend split — not confirmed architecture"* (`swiggy-bot-vs-agent-parameters.md`) — **partially resolved**. Agent Workbench is now named by two independent sources three-plus years apart. What the screen shows an agent is still unconfirmed.
- **New question, worth putting to the expert interviewee:** does anything like Uber Eats' named escalation triggers (value ceiling, alcohol, first-time customer, late filing) exist in Swiggy's tooling? Nothing found either way. The interviewee's Amex background (card-dispute review, likely including value ceilings and escalation tiers) makes this a natural fit for the existing interview guide, if there's room to extend it later.
- **New question for the Define stage:** should "evidence type" (captured-at-delivery vs. submitted-after-the-fact vs. none) become its own visible condition, now that the Instamart egg-tray case (Section 2f) gives it a real, not just hypothetical, justification? Recommendation: yes, raise it explicitly when the three-layer model is applied to evidence.

---

## 5. Pointer edits made as a result of this cross-verification
- `swiggy-cross-party-evidence-research.md`: added DoorDash/Zomato-rejection comparator (§1), Zepto comparator (§2), Supr Daily evidence-quality figure and the Instamart AI-evidence case (§3), the spot-checked Uber Eats escalation criteria (§4a), and a note pointing back to this doc.
- `swiggy-refund-and-blocking-rules-research.md`: added the three-numbers cancellation-fee discrepancy to §10 (Contradictions and gaps).
- `swiggy-bot-vs-agent-parameters.md`: updated the open question to reflect the second Agent Workbench source.
- `swiggy-case-study-structure.md`: added the new comparators, the AHT/effort-benchmark literature, and the literature-reading caution to Source material and Open Items, plus a session-log entry.

## Sources
Primary source for all claims above not independently re-fetched: the teammate's document, "swiggy_evidence-based_research.md" (provided 2026-09-29) — see that document for its own full citation list (66 numbered sources).

Independently spot-checked in this pass:
- [Order Errors | Uber Eats merchant help](https://merchants.ubereats.com/au/en/order-errors) — escalation criteria, refund-history tracking, courier auto-flagging confirmed verbatim.
- [Supr Daily case study | AWS](https://aws.amazon.com/solutions/case-studies/suprdaily-case-study/) — 25%-incorrect-refunds figure confirmed verbatim.
