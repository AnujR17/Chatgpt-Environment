# Scenario coverage and validation plan

17 October 2026. These are proposed fictional test fixtures and acceptance criteria, not records of actual customer claims or a list of automatic outcomes. The current HTML scripts only S2, S5, S3, S8 and S9. All five are prepaid, all set first-time-customer false, and all set unreachable false. A dropdown with 17 subjects is not coverage of 17 policies.

Original IDs S5 and S8 changed meaning across iterations. The suffixes below preserve both meanings rather than overwrite the source history. S1–S7 from the original frozen set remain relevant even when omitted from the current queue. See [CSV](scenario-matrix.csv) for needed facts, proposed handling and acceptance criteria for every case.

## Scenario index

| ID | Scenario | Third-iteration coverage | Priority |
| --- | --- | --- | --- |
| S1 | Clean missing item | Absent | High |
| S2 | Wrong item; one customer photo; prior refunds | Scripted; P5 conflation observed | High |
| S3 | Marked delivered; not received; above demo authority | Scripted; authority failure observed | Critical |
| S4 | First-time customer; damaged packaging; high value | Absent | High |
| S5-v1 | Restaurant permission has no reply | Replaced by new S5 meaning | High |
| S5-v2 | Unconsented substitution and fictional merchant cap | Scripted; cap arithmetic only | High |
| S6 | Cold/bland quality complaint | Subject available; no scripted case | High |
| S7 | Missing item first reported after 30 hours | Removed; upstream gate only asserted | High |
| S8-v1 | Case permission refused because item marked packed | Replaced by standing no-refund terms | High |
| S8-v2 | Fictional restaurant no-refund agreement | Scripted; invented funding behavior observed | High |
| S9 | Late delivery with prep delay, route incident and customer offline | Scripted; range remains undefined | High |
| V01 | COD report before delivery marking | Not scripted | High |
| V02 | COD already paid or reported after marking | Not scripted | High |
| V03 | Damaged packaging refused at doorstep | Not scripted | High |
| V04 | Damage discovered only after acceptance | Not scripted | High |
| V05 | Wrong veg/non-veg variant or declared allergen concern | Not scripted | High |
| V06 | Subjective taste complaint with no useful photograph | Not scripted | High |
| V07 | Illness, contamination or foreign-object concern | Not scripted | High |
| V08 | Unavailable item and customer refuses substitution | Not scripted | High |
| V09 | Substitution accepted but subsequently damaged | Not scripted | High |
| V10 | Paid add-on missing versus optional instruction ignored | Not scripted | High |
| V11 | One missing unit or component of a discounted combo | Not scripted | High |
| V12 | Fee-specific whole-order proposal | Not scripted | High |
| V13 | Tax-inclusive, exempt or different invoice tax treatment | Not scripted | High |
| V14 | Split payment, wallet, bank source and partial refund | Not scripted | High |
| V15 | Coupon or offer eligibility dispute | Not scripted | High |
| V16 | Midnight, next-day or missing timestamp | Not scripted | High |
| V17 | Authority boundary 500 and 501 rupees | Not scripted | Critical |
| V18 | Merchant mandate absent, expired or wrong outlet | Not scripted | High |
| V19 | Shared photo includes a person, address or payment detail | Not scripted | High |
| V20 | Earlier partial refund or duplicate complaint | Not scripted | High |
| V21 | Duplicate debit for one successful order | Not scripted | High |
| V22 | Debit with no order created | Not scripted | High |
| V23 | Approved refund not yet credited | Not scripted | High |
| V24 | Payment API timeout or rejected initiation | Not scripted | Critical |
| V25 | Location 99/100/101 m or low-accuracy/stale GPS | Not scripted | High |
| V26 | Customer unreachable; missing call log; delayed incident sync | Not scripted | High |
| V27 | Subject changed after item selection or multiple issues raised | Not scripted | High |
| V28 | Agent toggles computed authority to N/A | Not scripted | Critical |
| V29 | Unrelated precedent and missing past-condition data | Not scripted | Critical |
| V30 | Precedent fairness score and premature generated promise | Not scripted | High |
| V31 | No history; boundary of 90-day window; overturned complaint | Not scripted | High |
| V32 | Customer offline, on hold, review or ticket closed | Not scripted | High |
| V33 | Grievance month boundary and handoff delay | Not scripted | High |
| V34 | October 2026 versus January 2027 policy applicability | Not scripted | High |
| V35 | Native-app policy differs from public page | Not scripted | High |
| V36 | Instamart product-specific claim window | Not scripted | High |
| V37 | Alcohol OTP acceptance and two-hour clause | Not scripted | High |

## How to validate

Start with S2, S3, S5-v1, S5-v2, S7 and the Critical cases. Check the proposed rules' authority, arithmetic and state invariants before think-aloud sessions. Then cover COD, safety, payment failure, missing data and product boundaries. Use representative invoice and event fixtures, not only explanatory labels.

A case passes when the interface can represent a justified human proposal or pending investigation while enforcing execution authority, conserving money and preserving unresolved facts. Ambiguous cases can support multiple justified proposals. No fixed intended outcome should be chosen merely to make a participant agree with the designer.

For usability, compare like-for-like case information and counterbalance order where possible. Measure lookup effort, decision/proposal time, missed checks, authority mistakes, explanation quality and whether history/precedent changes reasoning. Document whether participants are actual agents, relevant-domain professionals or proxies. These sessions have not been performed in this audit.

## Invariants for implementation

- No status change or history entry grants payment authority.
- No unsupported no-photo or late-filing assumption auto-denies every complaint.
- No negative/overpaid/duplicate reversal; every fee and tax amount reconciles with the invoice.
- No processed promise before a confirmed execution event.
- A reviewer can see the original evidence, calculation, policy version and proposed action.
- A missing input is Unknown; an inapplicable condition is N/A with a reason.
- Precedent match indicators compare independently stored records.
- Customer remedy and party recovery remain separate, with unresolved settlement possible.
- Safety, privacy and complaint tracking persist across handoff, offline, hold and closure.
