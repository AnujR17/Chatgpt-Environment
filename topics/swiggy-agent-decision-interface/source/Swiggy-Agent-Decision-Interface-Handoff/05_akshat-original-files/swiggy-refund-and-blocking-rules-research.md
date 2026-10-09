---
name: swiggy-refund-and-blocking-rules-research
description: Secondary research on how Swiggy decides refunds and account blocks: official rules, reported practice, law, and gaps. Research-stage source for the case study.
researched: 2026-09-25
---

# How Swiggy Decides Refunds and Account Blocks: Research Notes

## 0. How to read this
Every point carries one evidence tag. Trust decreases down the list.

| Tag | Meaning |
|---|---|
| **[Official]** | Swiggy's own published terms or policy (fetched 25 Sep 2026) |
| **[Law]** | Indian law, regulation or court order |
| **[Reported]** | News with a named or anonymised source; not confirmed by Swiggy |
| **[Anecdotal]** | Customer forums and Reddit. Shows patterns, proves nothing alone |
| **[Inferred]** | My reasoning, not a source |

**Headline:** Swiggy publishes the conditions for a refund but not the thresholds, percentages or scoring behind the decision. The one inside account (a Swiggy chat support executive speaking anonymously to Business Standard) says customer history and "value tier" shape the outcome. Swiggy did not respond to that report.

---

## 1. The decision in one picture [Inferred, built from the sources below]

```
WHAT HAPPENED            WHO CAUSED IT              WHEN / EVIDENCE                  WHO THE CUSTOMER IS
(issue type)        ->   (customer, restaurant, ->  (before or after acceptance,  -> (order history, past refunds,
                          delivery partner, Swiggy)  OTP, "delivered"; photos)        value tier, fraud flag)
                                        |
                                        v
                       Restaurant permission (required for resolution)
                                        |
                                        v
            OUTCOME: full / partial / coupon / none   and/or   account restricted or blocked
```

The **single most important variable is fault attribution**. Almost every official rule is written as "if the cause is attributable to X".

---

## 2. Who decides [Official]
- "Our decision on refunds shall be final and binding." (Refund Policy, D.3)
- Refunds for non-delivery "will be assessed on a case to case basis by Swiggy." (D.2)
- "No replacement / refund / or any other resolution will be provided without Merchant's permission." (D.4)
- Instamart: refunds and cancellations happen "if Instamart is satisfied that the request fulfills the aforesaid conditions" and "at its sole discretion".
- Terms of Use: "Swiggy does not offer any refunds against goods or services already purchased... unless an error that is directly attributable to Swiggy has occurred." (This conflicts with the Refund Policy, which allows refunds for merchant and delivery-partner faults.)
- Quality complaints (taste, efficacy) are the **restaurant's** liability; Swiggy "shall notify the same to Merchant and may also redirect the Buyer to the consumer call center of the Merchant."

**Takeaway:** the policy names conditions, then gives Swiggy full discretion over whether they are met.

---

## 3. Refund rules by situation [Official unless tagged]

### 3a. Cancellations
| Situation | Rule |
|---|---|
| Customer cancels after placing order | Swiggy may charge **up to 100%** of order value; prepaid: not refunded; COD: recovered from the next order. Stated purpose: "to compensate the Merchants and Delivery Partners." |
| Swiggy, restaurant or delivery partner caused the cancellation | **No penalty** to customer. |
| Some items unavailable | Swiggy calls the customer; customer may cancel the whole order for up to 100% refund. |
| Wrong address or outside delivery zone | Penalty may be charged. |
| Customer unreachable by phone or email at delivery | Penalty may be charged. |
| Customer gave no directions or authorisation at delivery | Penalty may be charged. |
| Customer changes address after ordering | Order cancelled, **no refund**. |
| Delivery address is a public place | Swiggy may cancel immediately, **no refund**. |
| Non-delivery caused by the customer | Order "deemed to have been delivered", no refund. |
| Platform fee | "Non-refundable". |

### 3b. Order problems
| Situation | Rule |
|---|---|
| Packaging tampered or damaged, customer refuses at the door | Proportionate refund. |
| Delivery partner fails to deliver (partner's or Swiggy's fault) | Up to 100%, case by case. |
| COD order: tampered, wrong, or missing items | Customer need not pay, **only if reported to Customer Care before the order is marked delivered.** |
| Food quality or taste | Restaurant's liability; may be redirected to the restaurant. |
| Prepaid food: missing or wrong items after delivery | **No explicit written rule found** in the food policy. It falls under "case to case" discretion. |

### 3c. Instamart (groceries), Swiggy Instamart Pvt Ltd
- Cancellable only if: (1) not yet packed; (2) Instamart or the store cancels for reasons not caused by the buyer; (3) not delivered within the ETA shown at order time. Otherwise, a charge of up to 100%.
- Refund or replacement of up to 100% for **tampered packaging, incomplete order, or incorrect items**, only if:
  - reported **within the claim window shown on each product page** (varies by product, not one fixed number);
  - "subject to the required evidences provided by the Buyer" (evidence type not specified);
  - with merchant permission.

### 3d. Alcohol and Genie (niche, but show the pattern)
- **Alcohol:** giving the OTP to the delivery partner = "accepted delivery"; no cancellation or refund after that. Refund possible if not delivered within **2 hours**, or if the store cancels.
- **Genie (pick-up and drop; shut down May 2025 per Wikipedia):** ₹40–75 fee if cancelled after the partner arrives; full service fee if cancelled after pickup.

### 3e. Swiggy One membership
- Cannot be cancelled by the member.
- If Swiggy cancels it: prorated refund, **except** when Swiggy decides the conduct "involves fraud or misuse", in which case there is no refund.
- Usable on **2 devices at a time**.

---

## 4. The parameters behind a decision
Official parameters are rules the policy names. Reported parameters come from news and customers.

| # | Parameter | What it means | Evidence |
|---|---|---|---|
| 1 | **Fault attribution** | Customer vs restaurant vs delivery partner vs Swiggy | [Official] |
| 2 | **Order stage / timing** | Before or after restaurant acceptance, packing, pickup, OTP, "marked delivered"; within the claim window; beyond the ETA | [Official] |
| 3 | **Issue type** | Cancellation, non-delivery, damaged, missing, wrong, quality | [Official] |
| 4 | **Payment mode** | Prepaid (refund) vs COD (don't pay / recover from next order) | [Official] |
| 5 | **Order vertical** | Food, Instamart, alcohol, Genie, Dineout | [Official] |
| 6 | **Evidence** | "Required evidences" for Instamart; photos commonly asked for | [Official] for Instamart; [Anecdotal] for food |
| 7 | **Restaurant permission** | Needed for any resolution | [Official] |
| 8 | **Refund amount in the last 3 months** | Visible to the agent on the customer profile | [Reported], one anonymised source |
| 9 | **Customer value tier** | High / medium / low, mainly by order frequency; "high-value... receives better service in terms of refunds" | [Reported], one anonymised source |
| 10 | **Complaint frequency** | Complaints on many orders lead to scrutiny after "two or three such cases" | [Reported] |
| 11 | **Fraud flag** | Account categorised as a "fraud user" after email-team review | [Reported] |
| 12 | **Device signals** | Device fingerprinting (SHIELD) detects cloned or tampered apps, multiple accounts on one device, GPS spoofing | [Reported], vendor case study; framed as promo abuse, not refunds |

**Not found anywhere:** numeric thresholds (how many refunds is "too many"), a refund-percentage matrix by issue, or the food claim window.

---

## 5. How the decision flows in practice [Reported + Anecdotal]
1. **Bot first.** Customer picks an issue in the in-app Help chat. The bot may offer a **partial refund (20–30%)** or a **coupon**. [Anecdotal]
2. **Ask for a human.** Customer chooses "Talk to an agent". Swiggy's own engineering post says a customer who wants a human is not blocked, and the chat history carries over. [Official, engineering blog]
3. **Agent sees the profile.** Customer profile plus the total refund amount over the last 3 months. [Reported]
4. **Repeat complainers are moved to email.** "After two or three such cases, the customer is asked to email the complaint." [Reported]
5. **Email team reviews the pattern.** "If a pattern emerges, the account is categorised as fraudulent." [Reported]
6. **Outcome.** Refund, partial refund, coupon, or a templated denial ("we will not be able to refund"). [Anecdotal]
7. **Escalation outside the app.** A separate escalation email, @SwiggyCares on X, the Grievance Officer, the National Consumer Helpline (1915), then the consumer commission. Users report NCH complaints often lead to a call from an escalation team and a refund. [Anecdotal]

---

## 6. Account restriction and blocking

### 6a. Official grounds [Official]
Swiggy may suspend or terminate an account:
- for failing to comply with the Terms of Use or other policies ("at our sole discretion");
- if registration information is inaccurate, not current or incomplete;
- if "your actions may cause legal liability for you, other users or us";
- for multiple accounts ("only one Swiggy Account");
- for fraud (named explicitly for Dineout, Scenes and Swiggy One);
- if the user is under 18 without guardian consent.

Other official lines:
- Swiggy may suspend "temporarily or permanently at any time without notice" and "may any time at our sole discretion reinstate suspended users."
- Offers: Swiggy may limit how many times an offer is used, and may "deny honoring the Offer on the grounds of suspicion or abuse... without providing the Customer any explanation" (bank-partner offer terms).

### 6b. How it plays out [Reported + Anecdotal]
- **Restriction ladder** [Inferred from reports]:
  1. Refunds become smaller or turn into coupons.
  2. The complaint is moved from chat to email.
  3. The account is flagged as a "fraud user".
  4. The account is suspended.
- **What the customer sees:** "account is suspended... contact support via email", or "due to multiple violations", usually with **no specific reason**. [Anecdotal, DesiDime 2022–2025]
- **Suspected triggers mentioned by users:** sharing a Swiggy One account widely, logging in on many devices, frequent refunds or cancellations. [Anecdotal]
- **Reversals happen.** One user was reinstated after 4 days: "technical error". [Anecdotal]
- **Wallet balance risk.** Users report Swiggy Money stuck in blocked accounts. [Anecdotal]
- **Restaurants get blocked too.** One restaurant partner said it was disabled for "self order / coupon abuse" when customers used coupons at different locations. [Anecdotal]

### 6c. Detection tools [Reported]
- **SHIELD** device intelligence (announced May 2024, per SHIELD's press page), used by Swiggy's Trust & Safety team. It "exposed cases such as a single device linked to dozens of accounts", cloned apps and GPS spoofing. Its stated aim is **promo abuse** and delivery-partner incentive abuse. Whether it feeds refund decisions is not stated.

---

## 7. Who pays for a refund
- [Official] Customer-cancellation charges exist "to compensate the Merchants and Delivery Partners."
- [Official] Quality issues and spurious products are the restaurant's liability.
- [Reported] Restaurant operators say platforms **deduct refunds from their payouts, even without customer proof, with no way to dispute** (MediaNama, May 2025).
- [Reported] Both platforms told the government that cancellations after food is prepared are a problem because "they must still pay restaurants in full."
- [Anecdotal] A delivery partner was reportedly fined ₹850 over an undelivered order at a closed restaurant.

**Implication [Inferred]:** every refund decision has **three affected parties** (customer, restaurant, delivery partner), and the agent's call moves cost between them.

---

## 8. Law and regulation (the outer limits)
- **Consumer Protection (E-Commerce) Rules, 2020** [Law]:
  - A grievance officer must acknowledge a complaint within **48 hours** and resolve it within **1 month**.
  - **No cancellation charges on consumers unless the platform bears similar charges when it cancels.**
  - Accepted refunds must be paid "within a reasonable period of time."
- **CCPA suo motu probe** (started Oct 2024; reported May 2025) [Reported]:
  - Complaints on the National Consumer Helpline: **10,590 against Swiggy** (~912 refund-related) and 7,938 against Zomato.
  - Issue: charges of up to **90%** for cancelling after the restaurant accepts.
  - An official said orders delayed beyond the promised ETA should get full refunds.
  - The CCPA was "likely to direct" revisions. **Final outcome not found.**
- **Dark Patterns Guidelines 2023** (13 patterns) and a **June 2025 advisory** asking platforms to self-audit within 3 months [Law].
- **Checkout transparency:** screenshots reviewed by MediaNama show neither Swiggy nor Zomato displays cancellation or refund terms at checkout [Reported].
- **Amritsar District Consumer Commission, June 2026** [Law]: Swiggy was ordered to refund with interest and compensation after acknowledging a missing item and promising a refund that never came. Holding: an intermediary is liable for its own acts and omissions even if it is not the seller.
- **Tension [Inferred]:** "our decision is final and binding" cannot override statutory redress. Customers do win through the NCH and consumer commissions.

---

## 9. Comparison: Zomato (industry practice, not Swiggy) [Reported]
- **Karma score:** CEO Deepinder Goyal says Zomato "looks at past records and complaint history on both sides", for both customers and riders, to judge who is likely at fault. In 50–70% of disputed cases Zomato refunds the customer and lets the rider keep working. Where fault is unclear, Zomato absorbs the cost.
- **Fraud types named:** hair placed in food, and AI-edited photos (added flies, insects, nails; "smashed" cakes).
- Zomato removes about **5,000 delivery partners a month** for fraud.
- Zomato's terms allow blocking users who are abusive to support agents.

---

## 10. Contradictions and gaps (research value)
| Gap or contradiction | Why it matters for the agent |
|---|---|
| Terms of Use says refunds only for Swiggy's own errors; Refund Policy allows merchant and partner faults | The agent can't cite a single consistent rule |
| "Up to 100%" and "case to case" are never quantified | Every partial refund is a judgement call |
| No written food-order claim window or evidence rule | The agent decides what evidence is "enough" |
| Merchant permission is required, but there's no public process for obtaining it | Hidden dependency: the agent waits on a third party |
| Restaurants report no dispute path | Fairness gap on the other side of the decision |
| Value tiers and fraud flags are reported but unconfirmed | Possible unequal treatment of customers |
| Blocking reasons aren't told to customers | No transparency, and no audit trail visible outside |

**Open unknowns** (to test with the expert interview and a customer-side audit):
- actual thresholds;
- what the agent screen shows;
- the refund-amount limits agents can approve without escalation;
- the photo requirement for food;
- the appeal process for blocked accounts;
- the CCPA outcome.

---

## 11. What this means for our interface [Inferred, checked against project rules]
- **Decision supported:** "Is this customer's claim covered, and by how much?" The facts that feed it are fault, stage and timing, evidence, merchant permission, and history.
- **Policy as a condition checklist** (insight layer). Each condition sits next to the fact it's checked against. For example: "Reported before 'marked delivered'? Yes, 7:42 vs 7:49." The interface shows met or not met, never a verdict.
- **Order timeline strip** (insight layer). Order events (accepted, packed, picked, OTP, delivered, complaint raised) plotted against the policy cutoffs, so the timing condition is visible at a glance.
- **History as plain counts with dates** (data layer). For example, "3 refunds in 90 days: ₹120, ₹80, ₹240, each with its issue type." Show the counts, not a label.
- **Do NOT surface "value tier" or a "fraud user" flag.** These are customer-intent scores, so they break the no-prediction rule. They also raise fairness risk: new or infrequent customers get worse treatment. This tension should appear in the case study.
- **Show who the cost falls on** (restaurant, delivery partner or platform) as a neutral fact, so the agent sees that the decision affects three parties.
- **Edge cases:**
  - first-time user (no history, so the counts must read "no history", not zero risk);
  - conflicting signals (the delivery partner says delivered, the customer says missing);
  - merchant permission still pending.

---

## Sources
Official
- Swiggy Refund & Cancellation Policy: https://www.swiggy.com/refund-policy
- Swiggy Terms & Conditions: https://www.swiggy.com/terms-and-conditions
- Instamart Cancellation & Refund Policy: https://instamart.in/instamart-cancellation-refund-policy
- Instamart Terms of Use: https://instamart.in/instamart-terms-of-use
- Swiggy engineering post (repost), chat platform: https://dev.to/abeyalex/chatbots-at-swiggy-9bp

Law and regulation
- Consumer Protection (E-Commerce) Rules 2020: http://thc.nic.in/Central%20Governmental%20Rules/Consumer%20Protection%20%28E-Commerce%29%20Rules%2C%202020.pdf
- CCPA dark-patterns self-audit advisory (PIB, Jun 2025): https://consumeraffairs.gov.in/public/upload/admin/cmsfiles/pressRelease/Central_Consumer_Protection_Authority_issues_advisory_to_E-Commerce_Platforms_for_self-audit_within_3_months_to_detect_Dark_Patterns_and_ensure_its_resolutionpress_release.pdf
- Amritsar commission order (Indian Express, Jun 2026): https://indianexpress.com/article/legal-news/no-veg-mezze-platter-woman-swiggy-ordered-pay-rs-5000-compensation-10747310

Reported
- Business Standard, customer ranking at Swiggy/Blinkit/Zepto (Jul 2025): https://www.business-standard.com/industry/news/swiggy-blinkit-zepto-rate-users-and-delivery-workers-here-s-how-it-works-125071101503_1.html
- Business Standard, CCPA likely to direct revisions (May 2025): https://www.business-standard.com/industry/news/ccpa-zomato-swiggy-cancellation-refund-policy-update-directive-125052101628_1.html
- MediaNama, CCPA probe and restaurants absorbing refunds (May 2025): https://www.medianama.com/2025/05/223-ccpa-probes-zomato-swiggy-cancellation-refund-policies
- SHIELD x Swiggy case study (vendor): https://shield.com/case-studies/swiggy
- Outlook Business, Zomato karma score (Jan 2026): https://www.outlookbusiness.com/news/inside-zomatos-karma-score-what-deepinder-goyal-reveals-about-fraud-refunds
- NDTV, Zomato fraud types (Jan 2026): https://www.ndtv.com/food/deepinder-goyal-reveals-most-common-scams-customers-and-delivery-riders-try-on-zomato-10325357
- News18, fake-refund delivery scam (May 2025): https://www.news18.com/viral/new-scam-targets-swiggy-and-zomato-users-with-fake-refunds-and-qr-code-payments-9337429.html

Anecdotal
- DesiDime, Swiggy account blocked thread: https://www.desidime.com/discussions/swiggy-account-blocked-dbb83645-dd2b-4ae4-b33a-e16a14c92ff3
- DesiDime, missing-item refund denied: https://www.desidime.com/discussions/swiggy-not-refunding-money-even-after-having-missing-items
- Reddit r/swiggy threads (refund refused, bot 20–30% offer, coupons for missing items): https://www.reddit.com/r/swiggy/comments/1jy20ov/swiggy_refused_refund , https://www.reddit.com/r/swiggy/comments/1k24u99/horrible_experience_with_swiggy_customer_support , https://www.reddit.com/r/swiggy/comments/1rqq6vk/no_refund_for_missing_items
- The Emerging India, Instamart refund-scam Reddit story (low reliability, SEO blog): https://www.theemergingindia.com/reddit-users-jaw-dropping-expose-on-friends-unethical-hack-highly-unethical-and-risking-bans/

Could not access: Swiggy "Beware of phishing" page body, Swiggy Bytes originals, Quora, the X post on late-delivery compensation, and the CaseMine judgment (Deepak Kumar Dube v. Swiggy, Aug 2025).
