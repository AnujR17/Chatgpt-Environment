# Policy validation report

As of 17 October 2026. This report uses Evidence Mapping, a Content Audit and Scenario Analysis: trace each screen rule to a source, test its scope, then check the behavior and the cases it excludes. Findings about the prototype are separate from proposals for the next version.

## Answer about the original ZIP

Yes. The original refund/blocking research explicitly cited Terms of Use and Cancellation & Refund Policy, quoted sections and recorded contradictions. Frozen v1.1 then used those resources in P1–P8. However, it also explicitly borrowed competitor structure and introduced numeric placeholders. The first ZIP therefore contains evidence of reference and synthesis, not Swiggy's internal policy manual. See [sources.md](sources.md) for exact files and resource locators.

## What changed between the supplied artifacts

| Artifact | What its content establishes | Consequence for the audit |
| --- | --- | --- |
| Original ZIP v1.1 | Six food issue types; P3 24 h; P6 case permission; P8 ₹500; S1–S7; tagged mixed-source policy | Historical baseline, not entirely official |
| Earlier S2 HTML uploaded 10 October | Mostly static conditions, incomplete interactions | Reviewed previously; not current behavior |
| Agent Panel1 HTML supplied 17 October | Says policy v1.3; customer-photo-only model; permission states and four cases S2/S5/S3/S8; explicit conditions/amount checks | A revised iteration, not a duplicate of the first S2 file |
| Second Iteration HTML | Says frozen v2.0; removes P3/T3 and assumes upstream gating; changes P6 to standing terms; adds R1–R5 and 17 subjects; introduces tax arithmetic, S9 and star-case behavior | A substantial policy-model change, beyond layout refinement |
| Third Iteration HTML | Keeps v2.0 model; reorders panels; changes rider display; adds party-record similarity colors and always-matched precedent counts | Current artifact; data availability, numeric thresholds and match logic need independent justification |

Statements such as Owner or agreed date in the HTML record fictional/design choices. They are not proof of a merchant contract. A source tag Borrowed is incomplete when the borrowed concept and the invented number have different origins.

## P1–P8 audit

| ID | Third-iteration implementation | Evidence assessment | Required correction or treatment |
| --- | --- | --- | --- |
| P1 | 17 subjects; each listed subject immediately Met; bot subject prefilled | Useful taxonomy, but several additions are explicitly outside the original six | Separate complaint classification from factual validation. Record user confirmation and handle multiple simultaneous issues. Payment, conduct and food need different routes. |
| P2 | Default liability hidden inside P1 detail | Mixed SW-T/UE-ERR precedent; no case-level fault determination | Keep indicative responsibility distinct from established facts, customer remedy and settlement. Add unresolved/shared responsibility. |
| P3 | Removed; comment says 24 h is an upstream gate | Original threshold was hypothetical; no support for a real food gate found in SW-R/SW-T | Do not silently discard older complaints. Retain first-report time and a labelled operational target only if needed; accept exceptions and preserve routing history. |
| P4 | Adds COD condition but always Unknown; all five supplied cases prepaid | Clause is supported at its narrow SW-R scope; implementation untested | Model paid/not paid, status transition, report time, disputes over marking time and escalation after the special non-payment condition no longer applies. |
| P5 | Photo count alone yields Met; all item/quality/packaging subjects require a customer photo | Hypothetical requirement; availability is not relevance or assessment | Keep availability and human assessment separate. Permit no-photo/unsupported-upload alternatives; do not require a photo to demonstrate taste, illness or a missing object conclusively. |
| P6 | Full / cap / none restaurant contract; excess automatically assigned to Swiggy | Explicitly Owner/Hypothetical. Not equivalent to SW-R D.4 | Restore authorization as its own concept. Model merchant settlement under a separate fictional contract module; no contract cap establishes the customer's remedy. |
| P7 | Affected lines plus newly computed 5%; whole order for some subjects; all partial lines selectable | Prototype accounting proposal; not established as a universal official entitlement | Use invoice-derived net paid amounts, tax treatment, quantity, discounts, earlier refunds and fee rules. Mark proposed remedy caps as simulation rules. |
| P8 | ₹500; amount above limit gets Not met, but Confirm still works | Amount remains hypothetical; implementation fails its own authority model | Label demo threshold; enforce a reviewer route for execution above authority. Let the agent propose an outcome without treating proposal as authorized payment. |

## Review triggers and rider rules

| Rule | Validation result | Case-study treatment |
| --- | --- | --- |
| T1 high value | UE-ERR supports a high-value review concept; ₹500 is invented, even where the row says only Borrowed | Use Borrowed concept + Hypothetical value; define whether measured on claim, proposed refund or remaining authority |
| T2 first-time customer | Traceable to regional UE-ERR, not demonstrated for Swiggy | Optional simulation only; assess fairness, including IN-EC 4(11)(b); no automatic suspicion or denial |
| T3 late filing | Original fictional timing rule; now absent | Restore late-discovery coverage and distinguish filing from settlement protection |
| T4 conflicting records | Useful hypothetical review route | Treat GPS/event-vs-claim conflict as unresolved facts, not an adverse finding |
| R1 100 metres | Hypothetical distance threshold; no Swiggy source located | Show recorded distance with timestamp/accuracy/source; cannot certify handover or guilt |
| R2 one call | UE-WAIT supports call/contact workflow; exact count is a design adaptation | Distinguish call attempted, connected, duration and unavailable logs; label count hypothetical |
| R3 seven-minute wait | A seven-minute workflow exists in UE-WAIT | Borrowed regional process, not Swiggy policy; missing wait data must stay Unknown, not fail |
| R4 ten-minute grace | Hypothetical | Delay is not automatically a rider breach; separate prep, dispatch, pickup, route, promised-time revisions and incidents |
| R5 incident logged before marking | Hypothetical | Missing/late incident reporting cannot establish an incident did not occur; handle offline sync and emergencies |

The 96-hour reference in the original frozen file is materially misdescribed if used as a general customer refund cutoff. UE-ERR uses it in the non-partner-charge section from order placement. DD-ERR also separates customer compensation from merchant-debit protection. Neither supports a hidden Swiggy 24-hour eligibility gate.

## Other source/scope corrections

1. The original research put a public-place address restriction in a general cancellation list. SW-T places that paragraph under 9a, alcoholic beverages. Do not apply it to ordinary meal delivery without a separate applicable source. Alcohol OTP acceptance is also not a universal food no-refund condition.
2. A cancellation right to charge, a policy penalty ceiling, an actual checkout fee and a reported regulatory probe are different records. The old 100/90/100 discussion should not imply that a media percentage itself overrides the applicable order policy.
3. A publication saying an outcome is final does not eliminate statutory remedies. Read SW-T section 7 with SW-R and IN-EC. Apparent drafting tension should be flagged for policy-owner interpretation, not silently resolved by whichever sentence produces denial.
4. No general customer-photo mandate or absence of rider photos was established. SW-NC is historical evidence of a photo flow; it does not prove current use. The choice to simulate no rider/restaurant photos must stay a scenario/data-availability assumption.
5. Hardcoded GST is too broad. IN-GST distinguishes the invoice/service context and specified premises. Use the actual order invoice; avoid adding tax again to a tax-inclusive amount or refunding more tax than was paid. A simulation may explicitly assume 5%, tax-exclusive prices and no discounts.
6. Source estimates for credit time, grievance acknowledgement/redress and internal chat handling time answer different questions. The prototype's universal 3–5-day closing sentence is not validated by the checked credit table. See [refund-credit-times.md](refund-credit-times.md).
7. The 2026 e-commerce amendment announcement is future-effective from 1 January 2027. Track it as a future version; do not describe it as already operative for October scenarios. The underlying amendment Gazette was not separately reviewed here.
8. The DPDP field-exclusion note overstates specificity: IN-DP establishes phased commencement, not a statutory list of fields for this restaurant report. Limit the report to necessary data as a design safeguard, with explicit purpose and access controls.

## Third-iteration behavior findings

These checks ran in headless Chromium with external requests blocked and no JavaScript page errors. A test-only in-memory hook exposes existing model functions for inspection; the preserved HTML is unchanged. Actual UI controls exercised S3 confirmation and subject change. See [runtime record](third-iteration-behavior.json).

| Finding | Reproduction/result | Why it matters |
| --- | --- | --- |
| Authority is displayed but not enforced | S3: choose Full refund, Swiggy and a reason. Confirm is enabled; ₹696 is recorded despite P8 Not met and T1/T4 | A human may recommend an exception, but it is not equivalent to having payment authority |
| Match counts are tautologies | Open S2 Star case, then change Subject to charged/order-not-placed/double-charge. It still shows 8/8 policies and 3/3 triggers matched to the same curry precedent | `drawers()` renders current status = current status; no independently stored past-case predicate vector exists |
| Matching omits important fields | P7/P8 are excluded from policy match vector; policy version and evidence assessment are not compared | A perfect-match claim is unsupported even before the tautology is fixed |
| Authority statuses can be relabelled | P8 can be changed to N/A without a rationale; the log records status/time only | An assessment note should not rewrite a numeric authority rule |
| Evidence existence is conflated | S2 P5 Met before any photo tag/assessment | Checkmarks can appear to validate the complaint beyond what was checked |
| Settlement is invented | S8 no-refund terms produce ₹168 automatically assigned to Swiggy; S5 demonstrates a cap split | These are fictional cost-allocation rules, not validated by consumer terms |
| No payment execution state | `decide()` records a decision; closing text says processed; simulated report follows after final closing sentence | Separate approval, queued payment, accepted payment request, settled refund and failure. The toy prototype does not actually pay money |
| Denial range can become Unknown | For a subject without a published range, P7 stays Unknown even if the selected action is denial | Evaluate applicability: amount-range check may be N/A for no refund, with denial rationale assessed separately |
| Scope changes can use stale affected flags | Subject can change but existing item `aff` flags persist; full amount falls back to all items when no affected total | An issue change needs re-confirmed affected scope; payment reconciliation cannot reuse food valuation by default |

The star feature's ±1 raised/upheld-count similarity colors ignore denominators. Its invented Fairness /5 and QA labels need a real rubric and explicit simulated status. They are not evidence of a fair decision or proof that cases should be matched by party histories. The older project prohibited using party history for matching; this is a substantive design change to review.

## Native-app and screenshot answer

We fetched public mobile-oriented terms/refund links and extracted the public page payload. Their complete HTTP responses matched their ordinary web counterparts in this retrieval. An initial narrow composite was followed by ten readable phone screenshots. Those later captures show A–D, the complete credit table across two images, the COD condition, F for alcohol, the alcohol OTP/two-hour notes and an Instamart-policy link. Their visible wording is consistent with the fetched source. See the [mobile-screen observations](../../source/incoming/2026-10-17/mobile-policy-screen-observations.md).

No installed customer/restaurant/rider app or authenticated order screen was accessed. We cannot claim to have verified personalized help options, experiment-specific wording, product claim windows, coupons, merchant contracts or in-app consent records. A proper capture record should include service, app version, city, date, page path, order stage and a redacted screenshot/export; do not share OTPs, payment credentials or unredacted customer data. Access to those artifacts is an evidence gap, not a reason to invent internal rules.

## What should be on the agent screen

Customer-facing terms; applicable order-specific conditions; evidence availability and human assessment; a proposed remedy; a distinct authorization state; a distinct settlement estimate; payment status; complaint tracking and exception routing. Each rule needs source, scope, version/effective date, inputs, unknown/N/A behavior and escalation route. A read-only merchant contract can inform settlement only when its authenticity and applicability are established or explicitly simulated.

The [candidate policy](proposed-policy-v2.1.md) makes these distinctions operational. The [scenario matrix](scenario-coverage.md) defines the evidence needed to exercise them. Neither is a claim about a real internal Swiggy SOP or a silently adopted replacement for the original project decisions.
