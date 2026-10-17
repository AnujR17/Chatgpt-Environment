# Source register and original lineage

Checked 17 October 2026. A retrieved page is evidence of publicly available wording, not evidence of an agent's internal authority or a merchant's private contract. No clear effective date was located in the fetched main legal text; preserve retrieval date and do not backdate it to the fictional 8 October orders.

## Sources that the earliest ZIP actually used

The original [refund/blocking research](../../source/Swiggy-Agent-Decision-Interface-Handoff/02_research/swiggy-refund-and-blocking-rules-research.md) explicitly cites Swiggy's Refund Policy and Terms of Use in its Sources section. Sections 2 and 3 quote and summarize decision authority, refunds and cancellations; section 10 records drafting tensions. The original [cross-party research](../../source/Swiggy-Agent-Decision-Interface-Handoff/02_research/swiggy-cross-party-evidence-research.md) cites Uber Eats, Uber Direct, DoorDash, AWS/Supr Daily and Swiggy's restaurant dashboard. The original [frozen v1.1](../../source/Swiggy-Agent-Decision-Interface-Handoff/03_define-ideate/swiggy-frozen-policy-and-scenarios.md) explicitly maps those sources to P1–P8/T1–T4 and labels placeholders.

This proves the documents referred to terms and used them in the working policy. It does not independently prove every historical fetch or that full source documents were read then. The research cross-verification itself says some material came from indexed excerpts and some teammate claims were not re-fetched. There was no complete versioned official-policy snapshot or actual Swiggy internal policy in the ZIP. The later v1.3 and v2.0 standalone policy documents are not present among the supplied original ZIP files; their rules can be traced in the HTML, not assumed to have an independently supplied canonical specification.

## Primary source register

| ID | Resource and locator | Checked evidence | What it can establish | Limit |
| --- | --- | --- | --- | --- |
| SW-R | [Swiggy Cancellation & Refund Policy](https://www.swiggy.com/refund-policy), A, B, D.1–D.5, COD paragraph, F | Direct HTTP 200; public JSON legal text extracted; search-index text also examined | Consumer-facing cancellation/refund wording | No internal approval limits or general food claim-window threshold found |
| SW-T | [Swiggy Terms of Use](https://www.swiggy.com/terms-and-conditions), sections 1, 4, 6, 7, 9a, 19 | Direct HTTP 200; legal text extracted | Service scope, merchant relationship, charges, referral to refund policy, grievance contact | Section 9a is alcohol-specific; do not transplant it to ordinary food |
| SW-A | [App-oriented terms](https://www.swiggy.com/terms-and-conditions?is_app=true), [app-oriented refund policy](https://www.swiggy.com/refund-policy?is_app=true) | Direct HTTP 200; both identical to ordinary responses in this check | Public app-oriented legal pages | Query parameter is not proof of an authenticated native-app session |
| SW-P | [Swiggy Privacy Policy](https://www.swiggy.com/privacy-policy), information collected/use/disclosure/grievance headings | Direct HTTP 200; legal text extracted | General data handling notice | Does not establish the fields or retention period available to an agent |
| IM-R | [Instamart cancellation/refund policy](https://instamart.in/instamart-cancellation-refund-policy), Cancellation and Refunds | Direct HTTP 200; text read | Instamart-specific exceptions, product-page claim window and evidence requirements | A grocery rule is not a restaurant-food rule |
| IN-EC | [Consumer Protection (E-Commerce) Rules, 2020](https://consumeraffairs.gov.in/public/upload/files/E%20commerce%20rules_1732703966.pdf), English pp. 8–11 | Official PDF downloaded and text read | Consumer protections and grievance duties | Apply the right entity/model and distinguish seller duties from marketplace duties |
| IN-EC27 | [PIB announcement, 10 September 2026](https://www.pib.gov.in/newsite/erelcontent.aspx?lang=2&reg=48&relid=294532) | Official announcement read | Announces 2026 amendments and 1 January 2027 commencement | Future-effective watch item; underlying amendment Gazette not separately audited here |
| IN-GST | [Circular 167/23/2021-GST](https://www.gstcouncil.gov.in/sites/default/files/2024-06/circular-167-2021-gst.pdf), FAQ 9–10; [Notification 05/2025](https://gstcouncil.gov.in/sites/default/files/2025-01/ctr05-2025.pdf) | Official PDFs read | Invoice responsibility and specified-premises context | Not a refund valuation rule or support for a blanket 5% constant |
| IN-PAY | [RBI failed-payment framework](https://www.rbi.org.in/commonman/Upload/English/Notification/PDFs/CIRCULAR677EC931A7A65E4D99AA957D8E85BC0A2A.PDF), UPI merchant-payment row | Official PDF downloaded and read | Failed-transaction reversal framework | A failed payment differs from a successful payment later refunded for missing food; confirm applicable current payment-system rules before exact promises |
| IN-DP | [DPDP commencement notification, G.S.R. 843(E)](https://www.meity.gov.in/static/uploads/2025/11/c56ceae6c383460ca69577428d36828b.pdf), p. 2 | Official notification read | Phased commencement of listed Act provisions | Enactment in 2023 does not mean every substantive duty is operative on 17 October 2026 |
| UE-ERR | [Uber Eats Australia order errors](https://merchants.ubereats.com/au/en/order-errors/), escalation, non-partner-charge cases, adjustments | Official page read | Borrowed escalation/settlement precedent | Regional Uber policy, not Swiggy; 96 hours relates to merchant adjustments, measured from order placement |
| UE-WAIT | [Uber Ireland delivery guidance](https://www.uber.com/ie/en/deliver/basics/tips-for-success/delivering-orders/), unreachable-customer steps | Official page read | Borrowed call/wait process with a seven-minute timer | Regional courier guidance; not a Swiggy requirement or general seven-minute rule |
| DD-ERR | [DoorDash US error charges/disputes](https://help.doordash.com/en-us/merchants/article/what-are-order-error-adjustments), calculations and merchant protection | Official page read | Borrowed customer-remedy/merchant-debit separation and dispute process | Merchant settlement rules, not universal customer entitlements |
| UD-POD | [Uber Direct proof of delivery](https://developer.uber.com/docs/deliveries/guides/proof-of-delivery) | Official developer guide read | Possible evidence/verification types and product-specific capture | Does not establish Swiggy's actual food-delivery fields |
| SW-NC | [Swiggy no-contact deliveries](https://blog.swiggy.com/news/introducing-no-contact-deliveries/), 19 March 2020 | Official historical blog read | Historical example of a delivery photo flow | Does not establish current deployment or a requirement on every order |
| AWS-SD | [AWS/Supr Daily case study](https://aws.amazon.com/solutions/case-studies/suprdaily-case-study/) | Vendor page re-opened | Evidence-quality design rationale | Different service and vendor-reported estimate; no refund eligibility or authority rule |
| SW-STORE | [Swiggy Google Play listing](https://play.google.com/store/apps/details?id=in.swiggy.android&hl=en_IN) | Public store listing opened | Public app identity/listing | Reviews are anecdotes, not policy; no native app inspected |

## Mobile captures supplied during the audit

Ten readable phone captures show the relevant cancellation/refund sections and complete credit-time table. See [observations](../../source/incoming/2026-10-17/mobile-policy-screen-observations.md). This is direct user-supplied evidence of displayed wording, complementary to SW-A. It does not supply private contracts, personalized help logic or internal authority limits.

## GST follow-up sources, 17 October

Read [GST and recommended baseline](gst-and-recommended-baseline.md) for the application to item refunds, fee treatment and compensation. [Fetch metadata](gst-followup-fetch-record.json) records successful downloads and access limitations; no complete third-party text is republished.

| ID | Resource and locator | Checked evidence | Use and limit |
| --- | --- | --- | --- |
| IN-GST34 | [CBIC annotated CGST Act section 34](https://taxinformation.cbic.gov.in/content-page/explore-act/1000304/1000001), subsections 1–2 and amendment footnotes | Official-domain search-index text read; direct browser open failed | Credit-note framework and amendment cautions. Indexed text can lag commencement notifications; not a claim of a complete notification-history audit or a customer filing deadline |
| IN-GST137 | [Circular 137/07/2020-GST](https://cbic-gst.gov.in/pdf/Circular_Refund_137_7_2020.pdf), table items 1–3 | Direct HTTP 200, PDF downloaded and text read | Invoiced cancellation/return accounting examples; not a universal restaurant refund valuation rule |
| IN-GST178 | [Circular 178/10/2022-GST](https://cbic-gst.gov.in/pdf/cir-178-08-2022-cgst.pdf), paragraphs 7–7.1.4 and cancellation discussion | Browser PDF plus direct HTTP 200 download/text | Payment classification depends on the underlying arrangement; do not automatically add 5% to goodwill or declare every compensatory payment exempt |
| IN-GST25N | [GST Council September 2025 newsletter](https://gstcouncil.gov.in/sites/default/files/2025-10/september_newsletter.pdf), pp. 8–9, summary of Circular 251/08/2025 | Direct HTTP 200, PDF downloaded and relevant text read | Official summary distinguishes financial/commercial credit notes without original tax reduction. Original circular endpoint returned HTTP 503; do not claim the original was fully reviewed |

## Compact verified clause digest

SW-R: A reserves a 100% cancellation charge; B distinguishes non-customer causes. D.1 concerns damaged/tampered packaging refused at delivery; D.2 addresses attributable non-delivery; D.4 requires merchant permission; D.5 contains estimated credit times. The COD paragraph conditions non-payment on reporting before delivery status is recorded. F is alcohol-specific. No general 24-hour food cutoff, ₹500 authority, ₹250 restaurant cap or 100-metre rule was found here.

SW-T: section 1 covers website and app; section 4 assigns merchant complaint-redress responsibility; section 6 discusses order/charges, including a non-refundable platform-fee statement; section 7 refers refunds to SW-R; section 9a addresses alcohol; section 19 supplies a grievance route. Broad liability disclaimers should be read alongside the specific refund policy and applicable law, not converted into an automatic denial rule.

IM-R: claim windows refer to the product description, with evidence-dependent treatment of listed issues. Keep this in an Instamart branch.

IN-EC: rules 4(5) and 6(4)(b) concern acknowledgement within 48 hours and redress within one month; 5(3)(b) concerns complaint tracking; 6(3) concerns seller remedies for specified defective/nonconforming/late supplies, with a force-majeure exception for lateness. Rules 4(8), 4(10), 4(11)(b) address cancellation-charge reciprocity, accepted-refund timing and arbitrary consumer classification. These do not prescribe a ₹500 agent limit.

IN-DP: core provisions listed in paragraph (c) commence eighteen months after publication. Do not label the prototype's exact restaurant-report field exclusions as a statutory field list.

## Supporting sources in the old ZIP, not operational authority

Business Standard's July 2025 report on customer tiers, May 2025 cancellation reporting and MediaNama's restaurant/refund reporting explain concerns, not enforceable thresholds. SHIELD marketing describes abuse signals, not a demonstrated food-refund SOP. Zomato karma reporting is a fairness comparator. Zendesk informs layout, not refund eligibility. Literature on automation bias informs interaction choices, not claim windows. The simulated interview synthesizes these materials and cannot independently validate them. The single external-domain expert call does not establish Swiggy policy. These sources were traced locally; this audit did not reverify every news claim or academic statistic.
