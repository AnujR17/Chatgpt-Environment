---
name: swiggy-frozen-policy-and-scenarios
description: The working policy set and test scenarios frozen for Ideation, Design and Testing (Stages 6–9). It mixes Swiggy's published rules, rules borrowed from other platforms, and our own hypothetical placeholders, each one labelled. Read before any design or testing work.
status: v1.1, confirmed by the project owner 2026-10-09
---

# Frozen Policy Set and Scenarios (v1)

## 0. Why this file exists
Swiggy's internal refund rules (thresholds, approval limits, claim windows, what an agent sees) are confidential and not published. To design and test anything, we need **one fixed set of rules to design against**. This file freezes that set.

**Rules for using this file:**
- Every rule carries a source tag:
  - **[Published]** — stated by Swiggy.
  - **[Law]** — Indian law.
  - **[Borrowed]** — published by another platform and adapted here.
  - **[Hypothetical]** — our own placeholder.
- **Nothing tagged [Borrowed] or [Hypothetical] may be presented as Swiggy's real policy.** The case study must say: "Policies are a hypothetical working set, built from Swiggy's published terms and industry practice."
- All later stages (6–9) design and test against this file only. If a value changes, change it here first and note the change in the change log at the end.
- Rupee amounts and time windows are placeholders chosen to be realistic, not discovered facts.

**Scope:** food-delivery orders (not Instamart, alcohol or Genie). Refund and dispute cases that reach an escalation agent.

---

## 1. Policy conditions
These are what the screen checks against facts. Each shows as **met / not met / unknown**, never as a verdict.

| ID | Condition | Fact it is checked against | Frozen value | Source |
|---|---|---|---|---|
| **P1** | Issue type is one of: missing item, wrong item, damaged or tampered packaging, quality or taste, non-delivery, late delivery | Issue selected in chat + agent confirmation | Six types | [Published] types appear across Swiggy's policy; the list is [Borrowed] in structure from Uber Eats |
| **P2** | Who is liable, by default, for each issue type | Issue type | Missing, wrong, quality → **restaurant**. Damaged in transit, non-delivery, late → **delivery partner or Swiggy**. Wrong address, unreachable customer → **customer** | Quality → restaurant and customer-caused cases: [Published]. The rest: [Borrowed] from Uber Eats' liable/exempt split |
| **P3** | Claim raised within the claim window | Time of "delivered" vs. time of complaint | **Within 24 hours** of "delivered" | [Hypothetical]. Swiggy publishes no food claim window. Uber Eats uses 96 hours, DoorDash 7 days |
| **P4** | For cash on delivery: reported before the order was marked delivered | Complaint time vs. "delivered" time | As stated | [Published] |
| **P5** | Evidence is available for missing, wrong, damaged and quality claims | The evidence list (see §3) | At least one item: a delivery-capture photo **or** a customer photo | [Hypothetical]. Instamart requires "required evidences" [Published]; food has no rule |
| **P6** | Restaurant permission obtained | Permission status (see §4) | Required before any resolution | [Published] |
| **P7** | Refund amount within the policy range | Value of the affected items | Missing or wrong item: **that item's value**. Damaged or non-delivery: **up to 100%** of order | "Up to 100%": [Published]. Item-level value: [Borrowed] from DoorDash |
| **P8** | Amount within the agent's approval limit | Refund amount | **Up to ₹500** without review | [Hypothetical]. Approval limits exist in industry practice (Fini, Uber Eats high-value review); Swiggy's are unknown |

## 2. Review triggers
A trigger sends the case to a second reviewer. It is shown as a fact ("Trigger: first-time customer"), not as suspicion.

| ID | Trigger | Frozen value | Source |
|---|---|---|---|
| **T1** | High-value refund | Above ₹500 (the P8 limit) | [Borrowed] from Uber Eats; value [Hypothetical] |
| **T2** | First-time customer | No completed orders before this one | [Borrowed] from Uber Eats (verbatim criterion) |
| **T3** | Late filing | Outside the P3 window | [Borrowed] from Uber Eats |
| **T4** | Conflicting records | The rider's delivery record and the customer's claim disagree (for example, "delivered" with a location ping at the address vs. "not received") | [Hypothetical] |

**Fairness note:** T2 (first-time customer) is a real industry trigger, but it treats new customers differently. Keep it, label it with its source, and raise the tension in Stage 12 (Limitations).

## 3. Evidence model
Each evidence item on screen carries four fields. No item is ever labelled "verified" or "suspicious".

| Field | Values |
|---|---|
| Type | Delivery photo, OTP confirmation, location ping, restaurant packing photo, customer photo, chat message |
| Supplied by | System, delivery partner, restaurant, customer |
| Origin | **Captured at the event** (at pickup or drop-off) vs. **sent in afterwards** |
| Times | Captured at, submitted at |

**Facts derived from these fields** (insight layer):
- "No delivery photo on record."
- "Customer photo sent in 40 min after the complaint."
- "Complaint raised 3 h 10 min after delivery."

**Source:** the evidence types are [Borrowed] from Uber Direct proof of delivery. The packing photo is [Hypothetical]. Origin tagging follows the Supr Daily case (missing or poor delivery photos drove refund errors) [Reported].

## 4. Restaurant permission (mental-model step 8)
Shown as a visible condition with a live status, so the agent never has to assume it.

| Status | Shown as |
|---|---|
| Not requested | "Restaurant permission: not requested" + a request button |
| Requested | "Requested 4 min ago" |
| Given | "Given 2 min ago" |
| Refused | "Refused, with the restaurant's reason" |
| No reply | "No reply after 10 min", plus the option to escalate |

**Source:** permission required [Published]; the statuses and the **10-minute** no-reply point [Hypothetical].

**What happens with no reply:** the agent decides whether to escalate. The screen does not decide.

## 5. Party history (mental-model step 5)
Shown so that nothing is left to assumption, **but labelled "Context, not a policy condition"**, because Swiggy's policy never names history as a condition.

| Party | What is shown | Window |
|---|---|---|
| Customer | Refunds **out of** total orders, plus each refund as a dated line (date, issue type, amount, outcome) | Last 90 days |
| Restaurant | Complaints by issue type **out of** total orders, with dates | Last 90 days |
| Delivery partner | Non-delivery or damage reports **out of** total deliveries, with dates | Last 90 days |

**One window for all three parties: 90 days** [Hypothetical]. Every count is shown with its total, for example "3 refunds out of 7 orders" or "12 quality complaints out of 2,140 orders". The total is not turned into a percentage or a score. It's there so a busy restaurant or rider isn't made to look worse than a customer just by order volume.

**Older history:** the 90-day view is the default. The agent can open older history for any party with "Show older". The option works the same for all three parties, and each use is recorded in the case log (who opened it, when, and for which party). It is never opened automatically.

**Rules:**
- Counts and dated lines only. Never a score, tier, rank or "fraud user" flag.
- No history reads **"No history"**, never "0 risk" or "new user, low trust".
- The same format applies to all three parties, so no one side looks more suspect by design.

**Decision recorded 2026-10-08:** the project owner chose to show history explicitly rather than leave the agent to look it up elsewhere. The reasoning: agents reportedly see refund totals already [Reported], so hiding it would only move the bias off-screen, where nobody can check it. Labelling it "context" keeps it out of the condition checklist.

## 6. Clocks
Three clocks, shown separately:

| Clock | Value | Source |
|---|---|---|
| Claim window | 24 h from "delivered" (P3) | [Hypothetical] |
| Agent reply-by | 5 min in live chat | [Hypothetical] |
| Regulatory | Acknowledge within 48 h; resolve within 1 month | [Law] E-Commerce Rules 2020 |

## 7. Reference rules (shown with their source; not deep-designed)
- **Cancellation fee:** policy "up to 100%" [Published]. CCPA probe reporting "up to 90%" [Reported]. Live support replies "flat 100%" [Reported via teammate]. Shown together, never merged into one number.

## 8. Never shown (applies to every scenario)
- A recommended outcome, a refund amount suggested by the system, or "approve" / "deny" pre-selected.
- A fraud, risk, trust or value score for any party.
- "Verified" or "suspicious" labels on evidence.
- A guess that the agent is "struggling".

---

## 9. Frozen scenarios
Every scenario below is fictional, with made-up order data. Stages 7 (Scenarios #92), 8 (Design) and 9 (think-aloud tests) use these.

| ID | Scenario | Key facts on screen | Conditions and triggers | What it tests |
|---|---|---|---|---|
| **S1** | **Clean missing item.** Prepaid, ₹420 order, one ₹180 item missing | Delivery photo at drop-off; customer photo 6 min after delivery; restaurant permission given; customer history: 0 refunds out of 5 orders in 90 days | P1–P8 all met; no triggers | Baseline: how fast can the agent close a straightforward case? |
| **S2** | **Wrong item, thin evidence, prior refunds.** ₹350 order | No delivery photo on record; customer photo sent 40 min after the complaint; customer history: 3 refunds out of 7 orders in 90 days (each dated) | P5 met, but only by customer evidence; history shown as context | Does the agent treat history as context, or as a verdict? Does "No delivery photo" get noticed? |
| **S3** | **Non-delivery, conflicting records.** ₹610 order | Rider marked delivered; location ping at the address; OTP not used; customer says not received | T4 conflicting records; T1 high value (> ₹500) | Can the agent see both sides at once without the screen leaning toward either? |
| **S4** | **First-time customer, damaged packaging.** ₹540 order | Customer photo at the door; no packing photo; no history | T2 first-time customer; T1 high value | Does "No history" read as neutral? Is the review trigger clear and not accusatory? |
| **S5** | **Restaurant permission stalled.** Wrong item, ₹260 | All evidence present; permission requested 12 min ago, no reply | P6 unknown; no-reply state shown | Does the hidden dependency (step 8) become visible and actionable? |
| **S6** | **Quality complaint.** "Food was cold and bland", ₹300 | Customer photo; restaurant history: 12 quality complaints out of 2,140 orders in 90 days | P2 → restaurant liable; restaurant history as context | Is cost-bearing (restaurant) visible? Does restaurant history get the same neutral treatment as customer history? |
| **S7** | **Late filing.** Missing item reported 30 h after delivery, ₹200 | Evidence present; outside the claim window | P3 not met; T3 late filing | Is "outside window" shown as a fact with its source, leaving the decision to the agent? |

**Edge cases covered** (as required by the structure doc): first-time user (S4), conflicting signals (S3), permission pending (S5), incomplete evidence (S2).

---

## 10. Confirmed placeholder values
Confirmed by the project owner on 2026-10-08. All are still tagged [Hypothetical]:
- P3 claim window: 24 h
- P8 approval limit: ₹500
- Restaurant no-reply point: 10 min
- History window: 90 days for all parties, with counts shown out of total orders. Older history is available on demand, with each use logged
- Agent reply-by: 5 min

## Change log
- 2026-10-08: v1 frozen, and the placeholder values in §10 confirmed by the owner. Steps 5 and 8 of the mental model are handled in §5 and §4.
- 2026-10-09: History window made the same for all parties (90 days). Counts now show the total they're out of. Added "Show older" on demand, logged. Scenarios S1, S2 and S6 updated to match. Decided by the owner.
