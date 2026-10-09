---
name: swiggy-artifact-analysis
description: Stage 4 Artifact Analysis (#4) for the Swiggy Support Agent Decision Interface. Eight published dispute and support interfaces analysed for what they show, how they support decisions, and what to borrow or avoid.
researched: 2026-10-01
status: complete for documented artifacts; Swiggy customer-side chat flow moved to the Customer Experience Audit
---

# Artifact Analysis: Dispute and Support Interfaces

## 0. How to read this
- **Method:** each artifact was analysed from its **own published documentation** (help centre, merchant guide, developer docs, vendor page). No internal tool was accessed and no screenshots were captured. Field names are quoted from the docs.
- **Why these eight:** Swiggy's Agent Workbench has no public screens. These are the closest documented interfaces where a person reviews a disputed transaction, an order error or a support case.
- **Tags:** **[Official]** the company's own documentation; **[Vendor]** marketing content; **[Inferred]** our reasoning.
- **Lens:** every artifact is scored against the project's rules: order-centred, three parties, policy as conditions, deadlines, evidence provenance, no scores or verdicts, audit trail.

**Headline:** No documented interface combines all of what our panel needs. Card-dispute tools (Amex) are strongest on deadlines, reason codes and evidence rules but cover two parties. Food-delivery merchant tools (Uber Eats, DoorDash) show three-party cost and fault rules but are built for the restaurant, not a neutral reviewer. Agent workspaces (Zendesk, Kustomer) unify context but centre on the customer, and Kustomer adds the predictive scores our rules forbid. The white space is a neutral, order-centred review screen, which is this project's contribution.

---

## 1. Artifacts analysed

| # | Artifact | User | Source type |
|---|---|---|---|
| A1 | Amex Merchant dispute case view | Merchant | [Official] |
| A2 | Amex Chargeback Reason Code guide (AU) | Merchant | [Official] |
| A3 | Zendesk Agent Workspace and context panel | Support agent | [Official] |
| A4 | Kustomer unified agent workspace | Support agent | [Vendor] |
| A5 | Uber Eats Manager, order errors (AU) | Restaurant | [Official] |
| A6 | DoorDash Merchant Portal and Tablet, missing items | Restaurant | [Official] |
| A7 | Fini refund-operations audit log | Ops reviewer | [Vendor] |
| A8 | Uber Direct proof of delivery | Merchant / developer | [Official] (verified 29 Sep) |

---

## 2. Artifact by artifact

### A1. Amex merchant dispute case view [Official]
- **Shows:** "Status (your next action related to the Dispute), Disputes Amount, Transaction Amount, Transaction Date, Reason and Code, Case Type, Dispute Type, Days left to respond", plus notes from Amex.
- **Timeline:** "View Timeline Details" expands the case history.
- **Action:** two fixed choices. "I do not agree with the Card Member or I already issued a refund" or "I agree with the Card Member and I would like to provide a full refund."
- **Deadline:** "You must respond to a Dispute by the 'reply-by' date shown in your tool."
- **Search:** by Case #, Charge Reference #, Card Member Name, Card Member Number; results in a table.
- **Borrow:** the **status as "your next action"**, a visible **days-left counter**, a **reason code beside the claim**, and an **expandable timeline**.
- **Avoid:** nothing major; it is facts-only. The only gap is that it serves one side (the merchant).

### A2. Amex chargeback reason codes [Official]
- **Structure per code:** code number, title, chargeback reason, maximum time to raise a dispute (typically 120 days), maximum time to challenge (typically 20 days), excluded transactions, and **requirements to challenge** (the evidence that counts).
- **Examples:**
  - 4554 Goods not received: "Card Member did not receive, or only partially received goods and or services."
  - 4553 Not as described: goods "different than the written description provided by the Merchant at the time of purchase."
- **Borrow:** the strongest template found for **policy as conditions**. Each issue type has a fixed reason, a time window, exclusions and named evidence. Swiggy's issue types (missing, wrong, damaged, not delivered, late) can be written the same way.
- **[Inferred]:** this is exactly the gap Swiggy's own policy leaves open ("case to case", no food claim window, no evidence rule). The panel can show the condition and mark the parts Swiggy has not published as **"no published rule"**.

### A3. Zendesk Agent Workspace and context panel [Official]
- **Layout:** conversation in the centre ("from oldest to newest"), notifications and call console at the top, **context panel on the right**.
- **Context panel shows:** customer contact information and "interaction history", related records via lookup fields, help-centre article suggestions, side conversations, similar tickets with merge suggestions, approval requests, task lists, installed apps.
- **Channels:** email, chat and voice in one ticket, so agents "don't have to switch between dashboards".
- **Borrow:** the **three-zone layout** (conversation, work area, context) is the industry baseline agents already know. **Approval requests** inside the ticket match our value-ceiling routing.
- **Avoid:** the context is **about the customer and the ticket**, not the order. Restaurant and delivery-partner context would need extra apps or lookups.

### A4. Kustomer unified workspace [Vendor]
- **Timeline:** "a chronological history that blends prior conversations, operational events, and internal activity into one continuous stream", including purchases, returns and refund status.
- **AI layer:** "Summaries"; "Signals", which detect "sentiment changes, recurring issues, escalation risk, loyalty patterns, and churn indicators"; and a Copilot that can "suggest next steps".
- **Borrow:** the **single blended event timeline**, re-centred on the **order** instead of the customer.
- **Avoid:** "Signals" and suggested next steps are **predictions and recommendations about the customer**. These are the exact patterns the literature review shows people over-rely on (L1, L4), and they break the project's no-scores rule.

### A5. Uber Eats order errors, merchant view [Official]
- **Shows:** a "red indicator box that says Order Error" on affected orders; the order page shows "the reported error and the breakdown of your adjustment and net payout".
- **Report:** a CSV with "issue type, item(s) in error, customer refund amount, merchant charge amount and amount covered by Uber".
- **Rules made visible:** escalation to "a trained team" when a claim is "not filed in a reasonable time frame", "for high-value orders", "for orders with alcohol items", or "for first-time customers". Errors reported "more than 96 hours after order was placed" are not charged to the restaurant. Couriers "with a significant number of missing item reports" are "automatically flagged", and the restaurant is not charged for those refunds.
- **Borrow:**
  - **Cost split shown as three amounts**: customer refund, restaurant charge, platform cover. This is the clearest real example of showing who pays.
  - **Escalation criteria written as rules**, which the panel can show as "routed because: order value above ceiling".
- **Avoid:** the **automatic courier flag** is a derived label. Show the raw count of missing-item reports instead.

### A6. DoorDash missing items, merchant view [Official]
- **Flow:** Orders tab, open order, "Issue refund", choose whole order or specific items (or a dollar amount, or part of the tip), "Confirm refund". The Tablet flow is the same through "Issue with order".
- **Rules:** one self-serve refund per order; refunds within seven days; cannot refund more than the customer paid. A restaurant can claim its own refund when "The Dasher arrived at the store more than 20 minutes after the estimated order ready time".
- **Result:** a "Refunded to Customer" tag with the exact amount.
- **Borrow:** **item-level refund selection** (not only all-or-nothing) and a **hard cap** at the amount paid.
- **[Inferred]:** the 20-minute rule is a timing condition. It is a real example of "event time vs policy cutoff" that the panel's timeline can draw.

### A7. Fini refund audit log [Vendor]
- **Logged per decision:** "the policy version applied, the data points evaluated, the amount calculated, the action taken, and the confirmation timestamp".
- **Guardrails:** a "maximum autonomous payout threshold before escalation"; escalation triggers include "high-value disputes, repeat filers, legal threats, and chargeback notifications".
- **Gap:** the guide does not show what a human reviewer sees.
- **Borrow:** the **audit record fields**, applied to the human's decision: conditions shown, data version, agent's choice, reason given.
- **Avoid:** "repeat filers" as a trigger turns into a label about the customer. Show dated prior claims instead.

### A8. Uber Direct proof of delivery [Official]
- **Options:** signature, barcode, picture, ID, pincode; chosen by the merchant per delivery or vertical. A picture is automatic only for leave-at-door. Pictures kept 7 days on the dashboard and 30 days via API.
- **Borrow:** an **evidence type and origin tag** on each item: captured at delivery (platform), uploaded after the fact (customer), or none.
- **Caveat:** the page does not link this evidence to disputes.

---

## 3. Comparison against the project's rules

| Rule | A1 Amex case | A2 Amex codes | A3 Zendesk | A4 Kustomer | A5 Uber Eats | A6 DoorDash | A7 Fini | A8 Uber POD |
|---|---|---|---|---|---|---|---|---|
| Centred on the order or transaction | Yes | Yes | No (ticket, customer) | No (customer) | Yes | Yes | Yes | Yes |
| Shows all three parties | No (2) | No (2) | No | No | Partly (cost split) | No | No | No |
| Policy as named conditions | Partly (reason code) | **Yes** | No | No | Partly (escalation rules) | Partly (20-min, 7-day) | Partly (policy version) | No |
| Deadline or clock visible | **Yes** (days left) | Yes (120 / 20 days) | No | No | Rule only (96 h) | Rule only (7 days) | No | No |
| Evidence with type and origin | Partly | **Yes** (required docs) | No | No | No | No | No | **Yes** |
| Free of scores and predictions | Yes | Yes | Yes (panel doc) | **No** (Signals) | **No** (courier flag) | Yes | Partly | Yes |
| Audit trail of the decision | Timeline | No | No | Timeline | No | Refund tag | **Yes** | No |
| Neutral reviewer (not one side) | No | No | Yes | Yes | No | No | Yes | No |

**Read:** no artifact meets more than four of the eight rules. The ones that are neutral (A3, A4, A7) are not order-centred or show predictions. The ones that are order-centred (A1, A5, A6) serve one side.

---

## 4. Patterns to adopt
1. **"Your next action" status plus days left** (A1). One line tells the agent what is pending and how long remains.
2. **Issue type written as a reason code with conditions, time window, exclusions and required evidence** (A2). Gaps in Swiggy's policy show as "no published rule".
3. **Three-zone layout**: conversation, decision work area, context (A3). Familiar to agents, so lower learning cost.
4. **One timeline that blends order events, messages and actions, centred on the order** (A4 timeline, re-centred).
5. **Cost split as three amounts**: customer refund, restaurant charge, platform cover (A5).
6. **Escalation shown as the rule that fired**, not as a label (A5, A7).
7. **Item-level refund with a hard cap at the amount paid** (A6).
8. **Evidence tagged by type and origin** (A8).
9. **Audit record of the human decision**: conditions shown, data version, choice, reason (A7).

## 5. Anti-patterns to avoid
- **Predictive signals about the customer** such as sentiment, churn or escalation risk (A4).
- **Derived labels about a person**, such as an auto-flagged courier or "repeat filer" (A5, A7). Show dated raw counts instead.
- **Red "error" badges** that read as a verdict before review (A5). Use neutral status wording.
- **Customer-centred context only** (A3), which hides the restaurant and delivery-partner side.

---

## 6. Limits
- All analysis is from **published documentation**, not hands-on use. Screen layouts are described in words; no screens were seen directly.
- A4 and A7 are vendor marketing and may overstate features.
- A2 and A5 are Australian pages; rules may differ by market.
- Swiggy's own interfaces are not here: the customer-side support chat moves to the Customer Experience Audit, and the agent side has no public material.

---

## Sources
- A1 Amex, Managing a Dispute Case: https://www.americanexpress.com/us/merchant/support-center/disputes/managing-a-disputes-case.html
- A1 Amex, Searching for Disputes: https://www.americanexpress.com/us/merchant/support-center/disputes/searching-for-disputes.html
- A2 Amex Chargeback Codes (AU PDF): https://www.americanexpress.com/content/dam/amex/au/en/merchant/static/chargebackcodeguide.pdf
- A3 Zendesk, About the Agent Workspace: https://support.zendesk.com/hc/en-us/articles/4408821259930-About-the-Zendesk-Agent-Workspace
- A3 Zendesk, Using the context panel: https://support.zendesk.com/hc/en-us/articles/4408836526362-Using-the-context-panel-in-the-Zendesk-Agent-Workspace
- A4 Kustomer, Unified agent workspace: https://www.kustomer.com/resources/blog/unified-agent-workspace/
- A5 Uber Eats, Order Errors (AU): https://merchants.ubereats.com/au/en/order-errors
- A6 DoorDash, Missing item (merchants): https://help.doordash.com/en-us/merchants/article/what-do-i-do-if-a-customer-reports-an-item-is-missing
- A7 Fini, AI platforms for refund and dispute operations: https://www.usefini.com/guides/ai-platforms-refund-dispute-operations
- A8 Uber Direct, Proof of Delivery: https://developer.uber.com/docs/deliveries/guides/proof-of-delivery
