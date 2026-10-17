# Proposed case-study policy v2.1

Status: candidate specification, 17 October 2026. This file proposes an auditable simulation policy for the case study. It is not adopted, not Swiggy's internal policy, and not a new customer contract issued on Swiggy's behalf. Original wireframes and policy files remain unchanged. Public findings and clause locators are in [sources.md](sources.md); the rules below are design proposals unless explicitly identified as a public-source record.

Follow-up: [GST and recommended baseline](gst-and-recommended-baseline.md) explains item/partial refunds, fee scope, invoice reversals versus compensation, and the recommended minimum implementation with agent criticality/effort. Use it to interpret F01–F05; the larger rule catalogue below is not a requirement to implement every feature immediately.

## 1. Scope and policy layers

Core: restaurant-food orders and related payment/refund handling. Instamart, alcohol, Genie, Dineout and memberships use separate policy profiles and can be routed out of this concept. Do not transfer a numeric condition merely because it belongs to the same company.

The interface must keep five records distinct:

| Record | Question | Example |
| --- | --- | --- |
| Customer remedy | What resolution is appropriate under the applicable terms and facts? | Refund a disputed paid item or investigate non-delivery |
| Evidence assessment | What has been recorded, and what does the human conclude it supports? | A photo exists; its relevance is still unassessed |
| Authorization | Who may approve/execute the proposed action? | Demo ₹500 agent cap, with second approval above it |
| Settlement | Which account ultimately bears approved cost? | Merchant charge pending contract/dispute review |
| Execution | Has money actually been requested, accepted, returned or failed? | Approved refund awaiting provider acknowledgement |

A settlement disagreement must not silently erase a remedy request. An evidence check must not grant authority. A decision log must not claim that a payment happened. The agent chooses a proposal, while authority and payment states reflect the actual permitted action.

## 2. Minimum source record for every displayed rule

Store rule ID/title, product and jurisdiction, source class, source URL/document ID, clause locator, verification date, known effective dates, policy version, applicability, factual inputs, result states, calculation, exception route and authorized role. Unknown effective dates remain unknown. A real merchant contract needs identity, applicable outlet, contract version, signatory/authorization record, effective period, covered issue types and permitted recovery rules. A fictional contract must show Simulation prominently, including on the summary line.

Use source classes: Published Swiggy; Law; Borrowed regional example; Reported; Hypothetical simulation; Human assessment. Owner is a decision provenance field, not external evidence. A mixed-source rule needs separate fields for its borrowed concept and invented threshold.

Computed condition states: Met, Not met, Unknown and N/A. Unknown means an input or applicable source is unavailable. N/A means the rule does not apply. Record the reason for N/A. Record an assessment separately instead of allowing a human to rewrite the original calculation. Exceptions are separate authorized decisions with reasons, not edited source facts.

## 3. Operational rules proposed for the prototype

| ID | Proposed rule | Inputs and visible result | Exception / acceptance criterion |
| --- | --- | --- | --- |
| G01 | Identify product, order and issue before choosing a policy profile | Service, order ID, original issue, confirmed issue(s), relevant policy version | Multiple complaints can coexist; changing a subject revalidates scope and clears incompatible draft amounts |
| G02 | Keep first complaint receipt separate from bot handoff and agent start | Server timestamps with timezone/date and source | An old complaint handed over today does not become newly filed today |
| G03 | Do not use an unverified hard claim cutoff | Display elapsed time; optionally a simulation target clearly labelled | Late discovery, bot delays, safety complaints and payment failures remain receivable; no invisible 24-hour gate |
| E01 | Track evidence availability separately from human assessment | Type, supplier, capture time if known, submission time, relevant items/claims and accessibility | Missing metadata is unknown; no inferred fabrication or automatic authenticity verdict |
| E02 | Permit more than a customer photograph | Chat account, receipt/order ID, packing/handoff logs, event records, permission records, relevant images where available | A missing item, taste issue or illness may not be photographically provable; offer alternatives/review rather than automatic denial |
| E03 | Make the agent's conclusion explicit | Not assessed / supports / insufficient / contradicts, with evidence links and rationale | Tags describe observations; they do not prove responsibility or grant a refund by themselves |
| E04 | Preserve timing context | Time from complaint and from evidence request, not only submission gap | A four-minute response to the agent must not be presented as a forty-minute unexplained delay |
| A01 | Separate case permission from settlement terms | Applicable SW-R reference, case authorization state or documented standing mandate, scope, amount/items, source and actor/time | Pending/refused/unknown authorization goes to a defined reviewer route. A simulated standing mandate is explicitly hypothetical |
| A02 | Use an authority table; keep ₹500 only as a demo parameter | Agent role, gross proposed refund, applicable cap, additional approvals | At ₹500 allow authorized execution; at ₹501 route to review. Do not let a status override increase authority |
| A03 | Add responsibility not established and, if needed, shared responsibility | Relevant events and a recorded human rationale | Review is possible without accusing a party. Delay of a case is recorded as waiting on an input, not an automatic fault finding |
| A04 | Make required review operational | Unresolved conflict, above authority, missing authorization or a policy conflict | Agent can record a proposed outcome; execution waits for appropriate approval. Reviewer receives the unchanged facts and reasons |
| A05 | Do not use customer history as a standalone reason for rejection | Context records, counts, outcomes and provenance | Prior refund or no history does not establish current claim validity. Any optional new-user review trigger must remain hypothetical and be evaluated for fairness |
| F01 | Work from the invoice rather than recalculate a universal tax | Quantity, net paid line amounts, allocated discounts/tax, charges, prior refunds and payment transactions | No double tax; include the relevant invoice document and reconciliation record |
| F02 | Name the refund scope directly | Refund affected items / refund all food items / refund entire payment / selected quantity or component | A combo component, add-on and one unit of a multi-unit line can be selected independently when priced allocation exists; entire payment must not conceal retained fees |
| F03 | Bound transaction reversal and compensation separately | Remaining paid balance versus separately authorized compensation budget | Sum of reversals cannot exceed captured balance less prior reversals; additional compensation is a different ledger entry |
| F04 | Keep fee treatment itemized and conditional | Delivery, packaging, platform fee, tips and source-specific refundable status | No blanket promise to refund every fee, no invented fee amount, and no unexplained deletion of fee lines |
| F05 | Separate customer refund from partner recovery | Refund amount, merchant recovery, platform share, unresolved recovery and contract reference | A ₹250 cap may be demonstrated only as a fictional settlement agreement; do not auto-charge a rider from a generic fault selection |
| C01 | Derive cancellation treatment from cause, stage and consent | Who initiated, acceptance/prep/pickup status, customer consent, disclosed cancellation terms | Non-customer causes, unavailable stock and disputed cancellation need separate routes; preserve the cancellation-fee source and applicable policy profile |
| C02 | Model substitution consent | Original item, replacement, contact attempt, affirmative consent record and supplied item | No reply is not consent. A confirmed substitution still needs quality and price checks, rather than immunity from every later complaint |
| C03 | Apply COD's special non-payment condition only to its defined event | COD paid status, report receipt and marked-delivered timestamp | A late marking/report dispute requires investigation; failure of that special condition is not a universal bar to later redress |
| D01 | Treat location and status as records, not receipt certification | Event time, distance, GPS accuracy, sync age, selected address, handover recipient if recorded | At 99/100/101 m no automatic responsibility conclusion. Missing location is Unknown |
| D02 | Treat rider call/wait/grace numbers as optional simulation configuration | Trigger event, reachable/unreachable state, attempts and actual timestamps | Borrowed seven-minute sequence is not a Swiggy fact; one-call and ten-minute values must be hypothetical. Compare stage timing with its actual applicable plan |
| D03 | Handle safety independently from compensation | Unsafe food, allergen/veg mismatch, foreign object, rider misconduct, immediate concern | Route to an appropriate safety process without asserting automatic eligibility/medical conclusions. Preserve the financial subcase and receipt time |
| X01 | Distinguish proposed, approved and executed refunds | Draft, pending approval, approved, request sent, provider accepted, processing, credited, failed or unknown | Only show processed wording when supported by the simulated execution event; show status/reference and next update |
| X02 | Use a payment-specific credit estimate | Verified method, chosen destination, initiation date, provider estimate, business-day calendar | Source estimates stay estimates; pending investigation is not counted as payment processing. See refund-credit-times.md |
| X03 | Avoid duplicate and inconsistent payment actions | Transaction ID, claim ID, prior refund balance, idempotency key and provider response | Retrying after timeout checks status first. Reopening cannot issue another refund simply by repeating Confirm |
| Q01 | Preserve the complaint across hold/review | Case ID, next owner, waiting-on reason, next update, original complaint date | Customer offline is not withdrawal or denial. An internal handling timer cannot stop grievance tracking |
| Q02 | Record a complete, amendable audit trail | Source version, inputs, evidence/assessment, amount, reason, approvals, partner-report sharing and payment events | Changes append a correction; do not overwrite the original facts or approval history |
| P01 | Minimize data exposure by purpose | Necessary report fields, redaction of photos, roles and access logs | A restaurant receives only relevant information; histories, full contact data and sensitive payment details are not casually forwarded. This is a design control, not a claimed statutory field list |
| S01 | Precedent matching requires an independent past-case model | Past/current issue, applicable policy/version, evidence pattern, condition states, amount/authority and material differences | Never compare current values with themselves. No match or partial match is explicit; party-history colors are not eligibility checks |
| S02 | Make precedent outcomes and generated text subordinate to case facts | Material differences, simulated QA provenance and editable draft | No unsupported fairness score or real QA claim. Never promise execution before authorization/payment state. A record of editing is not a substitute for checking the promise |

## 4. Proposed issue-specific treatments

These are simulation treatments, not automatic legal verdicts. Keep applicable public-source notes on demand and let a reviewer resolve ambiguity.

- Missing/wrong/customization/add-on: record the ordered and supplied item, affected quantity, allowed substitutions and the exact paid allocation. An agent may propose the affected paid value; no-photo cases still have a review path.
- Inadequate quantity: distinguish a count discrepancy from a subjective portion concern; capture the advertised quantity/size where it exists.
- Quality/taste: separate preference from apparent nonconformity, temperature, spoilage and safety concerns. A photograph cannot prove taste or absence of illness. Request appropriate evidence without requiring unsafe retention/handling of food.
- Packaging damage/tampering: preserve acceptance/refusal timing, packaging facts and any affected contents. Do not force a post-delivery discovery into a doorstep-refusal scenario.
- Non-delivery/wrong handover: compare address supplied, location accuracy, event times, delivery instructions and any recipient record. The handover remains disputed when only proximity is known.
- Lateness: preserve the stated schedule, later estimate revisions and reason/event chain. A working grace period may be useful for a demo but cannot erase the applicable remedy/review route.
- Payment charged/no order, duplicate debit and earlier refund missing: split authorization hold, captured transaction, failed payment/reversal, duplicate capture and pending refund. Each requires transaction reconciliation rather than the price of an affected curry.
- Offer/coupon: capture the exact offer version, basket eligibility, restaurant/date/method conditions and what was shown before payment. Do not borrow another promotion's limits.
- Rider conduct or food safety: create a linked safety route and a financial route; avoid losing either while switching subject.

## 5. Financial examples for consistent fictional data

Example A: a line is explicitly tax-exclusive ₹240, with no allocated discount and invoice GST ₹12. Its paid allocation is ₹252. A proposed affected-item refund of ₹252 is internally coherent for this simulation. If ₹240 was tax-inclusive, adding ₹12 again is wrong.

Example B: tax-exclusive affected line ₹300 plus invoice tax ₹15 gives ₹315. A fictional contract permits ₹250 merchant recovery, with a separately authorized demo platform budget for ₹65. The screen must state Customer refund ₹315, Merchant recovery ₹250, Platform contribution ₹65, Contract: Simulation. If the budget/contract is unavailable, recovery remains unresolved; do not invent a debit or promise a payment.

Example C: a ₹252 paid allocation already has a ₹100 refund. Remaining reversal capacity is ₹152. Any extra goodwill amount needs its own authority and ledger.

Example D: a ₹696 proposal exceeds the demo ₹500 role limit. The agent can propose it; the case remains pending second approval until the reviewer acts. The UI cannot describe it as processed because Confirm was pressed.

Example E: a successful order payment and a second failed debit are different transactions. Reverse/reconcile only the appropriate transaction. A missing-item refund must not accidentally duplicate a provider's pending reversal.

Example F: an invoice records an item as ₹200 taxable value plus ₹10 GST. An approved full price reversal is ₹210; a qualifying half-price invoice adjustment is ₹105. A separately approved ₹50 goodwill payment is not automatically ₹52.50 and need not amend the original invoice. Fees and their taxes follow each selected charge's treatment. These are simulation examples, not a claim about Swiggy's actual credit-note process.

## 6. Candidate wording for the prototype handbook

> This prototype uses fictional cases and a labelled working policy. Public terms are cited by product and clause. Numeric operating limits and contract examples are simulation assumptions. A complaint is assessed from its case evidence; party history does not determine the outcome. Refund proposals, approvals, settlement responsibility and payment status are shown separately. Unresolved cases receive a review route and tracking reference. Refund credit estimates depend on the payment method and begin from a confirmed initiation event. Applicable consumer rights and grievance routes remain available.

This is prototype explanatory text, not a substitute for Swiggy's terms or a representation that Swiggy approved the concept.

## 7. Version and evaluation criteria

The prototype should display candidate v2.1 only after the project owner adopts it. Store this draft alongside v1.1/v1.3/v2.0 and provide a change log mapping each old ID to the new role. Retain the original content and highlight changed assumptions.

A rule is ready for the prototype when it has a source/simulation label, applicability, unknown/N/A states, correct arithmetic, defined authority, a review path and at least one boundary scenario. A scenario passes when the system records a policy-consistent human action or clearly pending review, not when an agent always chooses one preferred refund outcome. No claim of better fairness or faster handling is made until appropriate testing.
