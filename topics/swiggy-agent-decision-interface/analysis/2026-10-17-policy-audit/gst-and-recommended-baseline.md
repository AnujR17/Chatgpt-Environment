# GST, realistic policy baseline and implementation priorities

Recommendation dated 17 October 2026. This follows the source audit and the user's questions about tax, fees, operational realism and the effort required to improve the third iteration. It recommends a narrower implementation of [candidate v2.1](proposed-policy-v2.1.md); it does not adopt that candidate, issue terms on Swiggy's behalf or modify the supplied prototype.

## Verdict

The problem and the broad workflow are grounded in published policies and documented marketplace practices. The third iteration is a plausible simulation, but it is not validated as Swiggy's internal support system. Some precise thresholds and contract arrangements are invented. Several implemented checks also fail to enforce the prototype's own assumptions.

Proceed with a restaurant-food refund decision interface. Keep the evidence, conversation and decision layout. Correct the money calculation, authority and case states before adding more policy checks. Do not attempt to reconstruct the entire company's contracts or operating system from consumer terms. Merchant and rider agreements would help validate their own obligations and settlement rules; they would not independently prove an agent's authority, available evidence fields or payment execution workflow.

## 1. What GST means for a refund

Separate three questions: what the customer should receive, which invoiced supply is being reduced, and how the responsible business accounts for tax. Section 34 of the CGST Act provides a credit-note mechanism for specified invoice corrections, returns and deficient supplies, subject to conditions. It is not a universal promise that every support payout reverses every charge. See [CBIC's annotated section 34](https://taxinformation.cbic.gov.in/content-page/explore-act/1000304/1000001).

For the case study, use this proposed working rule: **when an approved remedy reverses an invoiced item price, return that item's eligible paid allocation, including its attributable invoiced GST, after prior refunds.** It is a transparent simulation rule consistent with invoice reversal, not a claim that Swiggy always uses this calculation. A platform-funded payment may instead leave the original invoice/tax unchanged. Record which treatment applies.

For covered restaurant services through an e-commerce operator, [Circular 167/23/2021-GST](https://www.gstcouncil.gov.in/sites/default/files/2024-06/circular-167-2021-gst.pdf), FAQs 9–10, assigns restaurant-service invoicing to the operator and distinguishes other supplies. It does not make every component taxable at 5%. Use actual invoice documents and the applicable supplier/tax configuration; the support agent should not infer the issuer or rate from a generic legal-page paragraph. The fetched Swiggy terms contain broad merchant/PDP tax wording that should not override applicable tax law or the actual invoice.

An invoiced cancellation can involve a credit note and a supplier-side tax adjustment: [Circular 137/07/2020-GST](https://cbic-gst.gov.in/pdf/Circular_Refund_137_7_2020.pdf) illustrates this for cancelled services invoiced in advance. That illustration does not establish all restaurant refund entitlements. Finance handles tax documentation; the customer does not need to apply to the GST portal for an ordinary app refund.

### Worked examples

Assume the invoice explicitly records Item A as ₹200 taxable value plus ₹10 GST, total ₹210, with no discount and no previous refund. The 5% is an example from this fictional invoice, not a hardcoded product rule.

| Remedy | Proposed customer amount | Tax/accounting meaning |
| --- | --- | --- |
| Reverse the entire Item A price | ₹210 | Reverse ₹200 value and its ₹10 invoiced GST through the appropriate accounting process |
| Reverse half of Item A's price as a genuine invoice adjustment | ₹105 | ₹100 value plus ₹5 attributable tax, if the adjustment qualifies for that treatment |
| Offer ₹50 goodwill while leaving the invoice unchanged | ₹50 | No automatic extra ₹2.50; it is a separately classified payment, not necessarily a GST credit note |
| Refund one unit of an identical two-unit line recorded as ₹400 + ₹20 GST | ₹210 | Select quantity one and its invoiced allocation |
| Item A already had ₹60 reversed | At most ₹150 more against this paid line allocation | Prior refunds reduce reversal capacity; extra compensation needs separate authority |

If the displayed ₹210 already includes GST, its included tax at 5% is ₹210 × 5/105 = ₹10. Do not add another 5%. If two approved lines carry different recorded tax rates, sum their own allocations rather than taxing their combined value at 5%.

Discounted example: a ₹200 pre-tax line with a ₹40 merchant-funded invoice discount has ₹160 taxable value and, in this example, ₹8 tax. Its eligible full reversal is ₹168, not ₹210. A platform-funded coupon, gift balance or third-party subsidy may have a different invoice/payment allocation. Read those records; do not assume all coupons reduce taxable value or restore all offers automatically.

The label “partial refund” is insufficient. It can mean a complete refund of one item in a larger order, a proportional price reduction, or a fixed support payment. Ask the agent to select scope and remedy type; let the financial system provide the corresponding calculation. Ordinary invoice reversal must stay within remaining captured payment and line allocation; any separately authorized goodwill remains visible as an additional amount.

This distinction is real accounting practice. The [GST Council's September 2025 newsletter](https://gstcouncil.gov.in/sites/default/files/2025-10/september_newsletter.pdf), pp. 8–9, summarizes commercial/financial credit notes that do not reduce the original tax liability. It concerns post-sale discounts, not a restaurant refund SOP; it supports distinguishing a payment from a tax reversal. The original circular endpoint was unavailable in this check.

### Delivery, packaging, platform fees and other charges

**Refunding all food does not automatically mean refunding the entire checkout payment.** Specify the selected components.

| Component | Recommended case-study treatment | Evidence boundary |
| --- | --- | --- |
| Affected food item and its recorded tax | Reverse eligible paid item allocation when an item-price refund is approved | Proposed valuation rule; not a verified Swiggy internal formula |
| Packaging | Refund the affected item's explicitly allocated packaging when the remedy covers that charge; shared packaging needs a recorded allocation or review | Not necessarily a separately rated service; follow invoice treatment |
| Delivery and surge | Assess the delivery service and applicable fee policy separately. Propose reversal for attributable complete non-delivery; do not automatically refund delivery for one missing side dish | Recommendation for the simulation; actual service terms/authorization still needed |
| Platform fee | Show the current published non-refundable wording, the actual amount and an exception/review route | [Swiggy Terms of Use](https://www.swiggy.com/terms-and-conditions), section 6, expressly describe a non-refundable platform fee; do not promise automatic repayment or treat that wording as settling every statutory dispute |
| Handling, small-cart, rain/late-night and other charges | Store a rule per actual charge and issue; show included, retained or awaiting review with reason | No verified universal allocation/refund formula was supplied |
| Tip, membership benefit and coupon restoration | Treat separately; do not invent cash value for an unused discount or absent fee | Requires the applicable product/payment record |

If an invoiced fee itself is reversed, include its attributable recorded tax in the proposed gross fee reversal; if the original fee/supply remains unchanged, its tax is not automatically reversed because a food item was refunded. A separate compensatory payment covering a retained fee is another possibility and must be labelled accurately.

Use clear labels: “Refund affected items”, “Refund all food items”, and “Refund entire payment”. Before confirmation show included charges, retained charges, tax included, prior refunds, destination and total. A genuine entire-payment reversal returns all captured components; do not use that label if any original charge remains withheld. Cancellation fees and other retained amounts must be disclosed separately.

### What should stay out of the agent's workflow

Do not expose GST return forms, ITC decisions or tax-rate selection to the support agent. Show invoice/credit-note references and any exception requiring finance review. A refund receipt, a GST credit note and a commercial credit are different records, even when linked to the same complaint.

The current annotated section 34 includes a 2025 proviso and marks a 2026 addition as awaiting notification. Do not apply uncommenced wording or an old September filing deadline from outdated copies. Supplier tax-adjustment deadlines are not customer complaint cutoffs. A goodwill label also does not, by itself, establish a tax exemption: [Circular 178/10/2022-GST](https://cbic-gst.gov.in/pdf/cir-178-08-2022-cgst.pdf) explains why the underlying arrangement matters. This report recommends a finance classification field, not an automatic tax conclusion for every payment.

## 2. The policy documents we should make

Do not create a comprehensive customer legal contract for an internal-agent design exercise. Create four linked, concise project documents. Existing candidate v2.1 and the source register contain much of the necessary content.

1. **Scope and provenance:** restaurant food; applicable terms and version; published, borrowed or simulated status of each rule. Route alcohol, Instamart, Genie and memberships to their own profile.
2. **Agent resolution handbook:** issue categories, evidence alternatives, permissible actions, approvals, exceptions, reasons and review ownership. Include accepted/refused/pending merchant authorization as distinct states. Published merchant-permission wording must not be silently replaced by a fictional recovery contract.
3. **Refund calculation and communication specification:** item/quantity/discount/tax allocation, fee treatment, earlier refunds, money versus goodwill, payment destination, initiation/credit estimates and failure handling.
4. **Authority and recovery appendix:** configurable simulation role limits; actual authorization if later obtained; separate merchant recovery and dispute states. Add rider deductions only if actual applicable obligations, authority, due process and recovery mechanisms are known.

The handbook is a working policy for this case study. Customer-facing copy should disclose the remedy, amount, retained charges, expected next event and grievance route. It should not present an invented internal threshold as a customer contractual restriction.

## 3. Minimum operational baseline

| Rule group | Recommended baseline | Why it matters to the agent |
| --- | --- | --- |
| Scope and complaint receipt | Identify order, product, issue, first receipt and applicable policy; receive late complaints without an invented 24-hour hard denial | Prevents using the wrong policy or losing a complaint during bot handoff |
| Evidence | Separate availability from human assessment. Allow account, receipt, chat and event records as appropriate; photo absence is not automatic failure | A missing item or illness is not always photographically provable |
| Responsibility | Allow “not established”; preserve conflicting facts and reasons | The agent can seek review without making an unsupported accusation |
| Resolution | Select affected item/quantity, all food, entire payment, other remedy or reasoned rejection. Replacement only where actually available and authorized | Gives the amount a clear basis and avoids promising unavailable fulfillment |
| Amount | Use recorded discounts, tax, charges, prior refunds and payment allocation; separate compensation | Prevents overpayment, short payment and double tax |
| Permission and authority | Record applicable merchant authorization and agent role approval separately; uncertain/refused permission and excess authority go to a named review owner | “Eligible” does not mean “I may execute this action” |
| Financial execution | Proposed → awaiting approval if required → approved → requested → provider status. Support failed, pending and reconciled outcomes | A recorded choice is not evidence of money returned |
| Communication and follow-up | Give an amount breakdown, source destination, current status, appropriate credit estimate, case reference and review/grievance path | Lets the agent explain the result and handle the next contact accurately |
| Safety and privacy | Linked urgent safety route for illness, contamination, allergen or threatening conduct; reveal only relevant evidence to partners | Financial handling must not swallow a safety report; partner views need bounded access |
| Context | History is contextual, with totals and provenance; no automatic denial from counts, new-user status, a GPS point or a prior case | Keeps the present complaint assessable on its facts |

These are proposed design requirements. Evidence availability and the exact review/approval roles still need operational research. The [Consumer Protection (E-Commerce) Rules, 2020](https://consumeraffairs.gov.in/public/upload/files/E%20commerce%20rules_1732703966.pdf) support meaningful complaint and grievance handling; they do not specify our invented thresholds or this exact UI.

## 4. Practical scenario policy

| Situation | Baseline route to demonstrate | What must not be asserted |
| --- | --- | --- |
| One item/unit missing or wrong | Assess the claim; propose affected paid allocation including recorded tax; assess attributable packaging separately | One missing item always warrants all checkout fees |
| Unconsented substitution | Record ordered/received items and absence/presence of consent; propose an authorized remedy for the affected supply | Any substitution is permitted because a merchant has a recovery cap |
| Whole order not received | Reconcile status, relevant handoff/contact evidence and customer account; review conflict; propose full relevant reversal, with each fee decision visible | GPS within 100 metres or “delivered” status proves receipt |
| Leakage, tampering or unusable food | Assess affected scope; use applicable public terms and evidence; route safety concerns separately | Every photo proves cause or every claim must have a photo |
| Illness, allergen or contamination | Record and route promptly; keep financial assessment linked and open | An OTP, delay or cash refund settles the safety incident |
| Late or cold food | Assess promised timing, actual service and affected supply; choose an authorized case-specific remedy | An alcohol two-hour clause creates a general meal refund entitlement |
| Customer cancellation or unreachable buyer | Review cause, stage, contact record and disclosed cancellation conditions | One call, seven minutes or a generic status proves a charge is justified |
| COD issue before delivery completion | Preserve the published reporting/status condition and avoid treating unpaid cash as captured funds | A prepaid refund workflow fits every COD case |
| Debit but no order / duplicate payment | Reconcile the actual transaction and any pending reversal | Pay an item refund in addition to the same pending payment reversal |
| Earlier refund not received | Inspect initiation, destination, provider reference and applicable estimate; trace/escalate | Create another refund merely because the first has not credited |
| Permission missing, amount above limit or evidence conflict | Record the proposal and route to a reviewer; preserve customer updates | Changing a condition to N/A grants authority |
| Previously refunded or discounted item | Use remaining payment/line allocation and original offer terms | Menu price equals refundable cash or every coupon is reinstated |

The existing 48-scenario matrix is a coverage backlog, not a requirement for 48 screens. Start with six walkthroughs: one missing item, attributable whole-order non-delivery, contested delivery, above-limit/permission-pending, refund-not-received and a safety complaint. Test prior refunds, inclusive tax, discounts, late discovery, unavailable evidence and COD as boundary variants.

## 5. Implementation effort and agent criticality

Effort below is relative to the supplied standalone third-iteration HTML. It is a design/engineering estimate from code review, not a delivery commitment. “Small” means bounded copy/condition work, “medium” means multiple connected fields/states, and “large” means a new model/integration or workflow. Production integration effort is separate.

| Change | Prototype effort | Criticality for an agent | Recommendation |
| --- | --- | --- | --- |
| Label simulation/source scope; remove the unsupported claim that a 24-hour gate is already handled upstream | Small | High: policy credibility and complaint access | Do now; no upstream enforcement was verified |
| Rename full-refund scopes and make fee inclusion explicit | Small–medium | Critical: wrong customer promise/amount | Do now |
| Enforce the existing demo approval cap; require reviewer state and override reasons | Small–medium | Critical: unauthorized action | Do now; cap remains hypothetical |
| Replace “photo exists = evidence satisfied” with a human assessment | Small–medium | Critical: unsupported decisions | Do now |
| Add unknown responsibility and a review owner | Small–medium | High: blocked/conflicting cases | Do now |
| Replace flat 5% with invoice-based item/quantity/discount/tax/fee/prior-refund records | Medium–large | Critical: incorrect money | Highest data-model priority |
| Separate proposed, approved, initiated, pending, failed and credited states | Medium–large | Critical: false completion and repeat payouts | Highest workflow priority |
| Separate merchant permission from recovery cap/platform contribution | Medium–large | Critical: unsupported authorization or charges | Do before claiming end-to-end resolution |
| Correct payment-method estimates and add trace/escalation status | Small for table; medium for follow-up state | High: repeated contacts and misleading promises | Do in core flow |
| Add linked safety route and basic scoped partner disclosure | Small–medium to demonstrate; large to operate | High, urgent in relevant cases | Demonstrate route; do not build a full safety operation |
| Remove false Star-case match percentages and unvalidated Fairness/QA scores | Small | High: misleading evidence of correctness | Remove now |
| Rebuild independent precedent data and evaluate matching | Medium–large | Optional initially; potential benefit unproven | Defer until the core flow works |
| Live payments, reconciliation, GST documents, contract ingestion, partner disputes and deduction appeals | Large production work | Operationally critical if actually deployed | Document dependencies; simulate responsibly in the case study |

There is no evidence that an entire visual redesign is necessary. The major overhaul is the financial/state model if the concept claims an end-to-end operational workflow. A clear simulation can demonstrate that model with fictional invoices and events without building payment infrastructure or a GST filing system.

## 6. Is this real practice?

**Directly grounded:** consumer refund/cancellation wording; a payment-method credit-time table; merchant permission in the published policy; formal grievance handling; the invoice/credit-note distinction. These establish specific facts, not the entire internal workflow.

**Supported as a pattern elsewhere:** affected-item adjustments including tax and the separation of customer compensation from merchant charges are documented on [Uber Eats Australia's order-error page](https://merchants.ubereats.com/au/en/order-errors/) and [DoorDash's merchant error-charge page](https://help.doordash.com/en-us/merchants/article/what-are-order-error-adjustments). These are regional merchant-facing examples. A merchant charge formula is not itself a customer's entitlement or a Swiggy rule.

**Plausible but unverified here:** role-based approvals, standing mandates, evidence consolidation, delivery telemetry, pending investigations and case linking. They can be demonstrated as explicitly proposed capabilities; actual field access, contracts, staffing and service targets remain unknown.

**Unsupported as facts or defective in this prototype:** precise Swiggy ₹500/₹250 limits, automatic platform/rider cost assignments, a generic 24-hour food gate, the numeric delivery rules, photo-existence as proof, a blanket 5% calculation, perfect precedent matches and invented Fairness/QA results. Remove the factual claim, label a necessary simulation assumption, or repair the behavior. Research cannot validate a self-comparison bug.

For stronger operational validation, obtain a redacted applicable merchant agreement plus refund annexure/mandate; rider terms plus actual delivery/contact/cancellation instructions; an agent authority/escalation matrix; anonymized invoice/credit-note/refund receipts; and walkthroughs with actual food-delivery support practitioners. These would validate particular assumptions. Until then, describe the work as a publicly researched, human-led support concept, and report testing as concept evaluation rather than measured Swiggy operational improvement.

## Recommended next scope

Correct the core flow and use the six walkthroughs above to test whether an agent can explain: **what is known, what remains uncertain, what can be offered, how the amount was calculated, who can authorize it, and what happens next.** Keep partner settlement and precedent matching secondary. That is a concrete and defensible case-study scope without inventing a company's internal operating policy.
