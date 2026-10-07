# Digital Cheque — Data & Evidence Appendix
*Supplements the Foundation Analysis (23 Sep 2026) with real numbers, live datasets, and one legal development the original doc missed. Same evidence-label system: Statutory / Regulatory / Industry practice / Secondary finding / Hypothesis / Validated. Nothing here is a validated finding — validation only comes from your primary research. Updated 1 Oct 2026: pendency figures and mediation claim re-checked.*

*Compiled 30 Sep 2026.*

---

## 1. Payments-system time series (fills the "why cheques persist" gap with real numbers)

| Metric | Value | Period | Source type |
| --- | --- | --- | --- |
| Cheques processed via CTS | 62.59 crore cheques, worth ₹71.80 lakh crore | CY2024 | Secondary finding (RBI Payment System Report, Dec 2024) |
| Cheque transaction volume trend | Fell from 72 crore (2021) to 57 crore (2025) | 2021→2025 | Secondary finding (RBI PSR H2 2025, via CIOL) |
| Cheque value trend | Values held up / rose slightly even as volume fell — cheques concentrating in larger-value transactions | 2021→2025 | Secondary finding — **directly supports your H-segment priority (large-value, relationship-bound payments)** |
| Digital payments share | 99.7% of volume, 97.5% of value (CY2024); 99.8%/97.7% in H1 2025 | CY2024–H1 2025 | Secondary finding (RBI PSR) |
| Paper instruments (cheques) share of value | 2.3% of total transaction value | H1 2025 | Secondary finding |
| UPI share of volume | 85.5% of all payment volume, but only ~9% of value | H2 2025 | Secondary finding — small-ticket dominance, confirms UPI ≠ cheque substitute for high-stakes payment |
| RTGS share of value | 69% of value, ~0.1% of volume | H2 2025 | Secondary finding |
| Total payment volume/value growth | Volume CAGR 45.0% (2019→2024); Value CAGR 9.8% | 2019–2024 | Secondary finding |

**Why this matters for the case study:** you now have a *time series*, not a single-year snapshot. You can chart "cheque volume declining while cheque value holds" as visual evidence that cheques are retreating into exactly the high-stakes niche your Problem statement claims. That's a stronger opening chart than anything in the current Foundation Analysis.

**Live source (queryable, update it yourself before final submission):**
- RBI Payment System Reports (half-yearly): rbi.org.in → Publications → Reports → Payment System Report
- dataful.in RBI-sourced dataset — month/operator/location-wise CTS, NACH, NEFT, RTGS, IMPS, UPI volumes since 2020: https://dataful.in/datasets/136/

---

## 2. Court and dishonour-litigation data (fills the s.138 backlog claim with sources you can cite properly)

| Metric | Value | Date | Source type |
| --- | --- | --- | --- |
| Nationally pending s.138 cases | **43,05,932** (government figure to Lok Sabha). Earlier figure: **35.16 lakh as of 31 Dec 2019**, cited by the Supreme Court in [In Re Expeditious Trial, 16 Apr 2021](https://api.sci.gov.in/supremecourt/2020/9631/9631_2020_31_501_27616_Judgement_16-Apr-2021.pdf). Use both, dated; the rise is itself a finding (corrected 1 Oct 2026). | Dec 2024 | Secondary finding, confirmed against [GSTV](https://www.gstv.in/news/magazines/43-lakh-cases-of-cheque-bouncing-pending-in-the-countrys-courts) |
| Delhi district courts pendency | 6,50,283 cases; 49.45% of total trial-court pendency in Delhi | Sep 2025 | Secondary finding, confirmed via [Maheshwari & Co.](https://www.maheshwariandco.com/blog/section-138-ni-act-new-guidelines-by-sc/) |
| Mumbai pendency | 1,17,190 cases | Sep 2025 | Secondary finding |
| Calcutta pendency | 2,65,985 cases | Sep 2025 | Secondary finding |
| Typical case duration | Estimates range 6 months (summary trial target) to 1.5–3 years (in practice) depending on source | 2025–2026 | Secondary finding — **wide range, don't cite a single number without an advocate confirming which applies to your target courts** |
| Filing window | ~75 days total from dishonour (30-day notice + 15-day grace + 30-day filing window) | Statutory | Statutory |

**Legal development flagged in the Foundation Analysis — re-checked 1 Oct 2026, likely not real:**
A 2026 source references a "2025 Amendment" introducing Mandatory Mediation and a new Section 138A. On re-checking against a Supreme Court guidelines source covering the same period, **no supporting mention of a new mandatory-mediation mechanism or Section 138A was found** — that source discusses settlement/compounding under the *existing* framework only. Treat this claim as **more likely wrong than merely unverified**, and do not build a design assumption (e.g. Opportunity Area O5, guided dishonour path) on it without a primary legal source confirming it.

**Reusable methodology, not just a citation:** The Leap Blog built its own litigant-type dataset by pulling from the e-courts database for Mumbai (417,437 cases: 317,225 disposed, 99,712 pending) and a rural comparison region. This is a template your team could replicate at smaller scale for Gandhinagar/Ahmedabad district courts if you want local, not just national, numbers — but that's a stretch goal, not core to a 12-day sprint.

**Live source (queryable):**
- National Judicial Data Grid — filterable by court, case stage, pendency: https://njdg.ecourts.gov.in/njdg_v3/

---

## 3. MSME delayed-payment data (your primary segment — this is the strongest addition)

| Metric | Value | Date | Source type |
| --- | --- | --- | --- |
| MSME Samadhaan cases filed nationally | 87,713 cases; ₹26,227.38 crore amount payable; 46,302 disposed | Live (pulled 30 Sep 2026) | Regulatory portal data |
| Annual working capital lost to delayed payments | ₹10.7 lakh crore; ~5.9–7.8% of GDP/GVA depending on source year | 2023–2024 reports | Secondary finding |
| Share owed to micro/small enterprises specifically | 80% | Secondary finding | Secondary finding |
| Median debtor days (micro-enterprises) | 195 days — vs the legally mandated 45-day window | 2021 data | Secondary finding — **this is a strong, concrete stat for your Problem stage** |
| MSME Samadhaan effectiveness | Under 1% of registered MSMEs ever file; only ~22–26% of filed cases get resolved/settled | Recent reports | Secondary finding — **supports H6 (payees avoid formal legal routes because they're slow/ineffective)** |
| Statutory interest on delayed MSME payment | 3x RBI bank rate, compounded monthly (~20.25% p.a. at 6.75% bank rate) | MSMED Act s.16 | Statutory |
| Filing route change | All new delayed-payment references must go through the MSME ODR portal (odr.msme.gov.in) since 15 Oct 2025, not the old Samadhaan filing flow | Oct 2025 | Regulatory — **another development after your Foundation Analysis's research window, worth a one-line note in Problem/Research** |

**Direct hypothesis support:** this data is a strong, independent (non-cheque) confirmation that MSME payment delay is systemic and under-addressed by existing formal remedies — which strengthens your core premise even before you run a single interview.

**Dataset for pattern analysis (not a live portal, a downloadable file):**
- Hugging Face `Bhupathe/msme-payment-dispute-dataset` — ~4,600 structured MSME payment dispute cases with claim amount, delay days, buyer type (govt/private), contract presence, outcome (win/settlement/escalation): https://huggingface.co/datasets/Bhupathe/msme-payment-dispute-dataset
  - Useful for: sizing typical delay lengths and outcome patterns *before* you interview, so your interview guide can probe against real distributions instead of guessing.

**Live source (queryable):**
- MSME Samadhaan portal, live case counts: https://samadhaan.msme.gov.in

---

## 4. What this data still can't tell you (why the interviews aren't optional)

- None of this explains **why** a payer or payee chooses a cheque over UPI/NEFT/NACH in a specific relationship — that's H1 through H10, and only interviews test it.
- Court and Samadhaan data show the *scale* of the delayed-payment and dishonour problem, not the *lived experience* of holding a PDC bundle or waiting on a bounced cheque.
- None of it is Gujarat/Gandhinagar-specific. If you want local grounding, the NJDG filter lets you pull that, but treat it as a stretch goal given the timeline.

---

## 5. Open items carried over

- [x] ~~Reconcile the two conflicting national pendency figures (43 lakh vs "over 35 lakh")~~ — **Resolved 1 Oct 2026, corrected same day**: both are sourced. 35.16 lakh (Dec 2019, Supreme Court 2021) and 43 lakh (Dec 2024). Cite both with dates.
- [x] ~~Verify the 2025 Mandatory Mediation / Section 138A claim~~ — **Re-checked 1 Oct 2026**: no supporting source found; treat as likely wrong.
- [ ] Decide whether to attempt a local NJDG pull for Gandhinagar/Ahmedabad or stay with national figures, given the 12-day timeline.
