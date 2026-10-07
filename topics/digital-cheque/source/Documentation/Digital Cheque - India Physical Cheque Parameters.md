# India — Physical Cheque: Current Parameters, Factors & Constraints
*Digital Cheque project · compiled 30 Sep 2026, from the Foundation Analysis (23 Sep 2026) and Design Factors doc (27 Sep 2026). Updated 1 Oct 2026 with confirmed current/savings account eligibility. This is a reorganisation of existing research into a single reference structure. Evidence labels carried over: Statutory / Regulatory / Industry practice / Secondary finding / Hypothesis.*

---

## 1. Legal framework

### 1.1 Governing statutes
- Negotiable Instruments Act, 1881 (NI Act) — primary statute [Statutory]
- Payment and Settlement Systems Act, 2007 (PSS Act), s.25 — parallel offence for failed electronic funds transfers [Statutory]
- IT Act, 2000 — governs electronic/digital signatures; First Schedule excludes negotiable instruments "other than a cheque," so cheques are covered [Statutory]

### 1.2 Instrument definition (NI Act s.6)
- A cheque is a bill of exchange, drawn on a specified banker, payable on demand [Statutory]
- Includes the electronic image of a truncated cheque and a "cheque in the electronic form" since the 2002 amendment [Statutory]
- Electronic cheque requires signing in a secure system with digital/electronic signature (IT Act standards) [Statutory]
- **Unresolved tension**: "payable on demand" vs. post-dating — how a future-dated instrument squares with this wording is an open legal question [Hypothesis / open item]

### 1.3 Roles and structure
- Drawer, drawee, payee defined (s.7) [Statutory]
- Crossing ("A/c payee" etc.) and collecting-bank protection (s.123–131) [Statutory]

### 1.4 Account-type eligibility — confirmed, resolves a prior open item
- **Unlike Singapore, Indian banks issue chequebooks, including for post-dated cheques, on both current and savings accounts.** [Industry practice — confirmed by project lead, 1 Oct 2026]
- **Implication for the Singapore comparison:** Singapore's EDP/EDP+ story includes a genuine access-expansion angle — savings-account holders there never had physical cheque access, so EDP/EDP+ is a new capability for them. **That expansion argument does not transfer to India.** Indian savings-account holders already have physical cheque and PDC access today, so a digital instrument here isn't "opening up" anything by account type — the access problem, to the extent one exists, lies elsewhere (e.g. informal/unbanked payers, not account type).
- This removes Scenario 3 (savings-account holder gains new capability) from the set of transferable Singapore lessons for India — it was already flagged as conditional pending this confirmation.

### 1.5 Dishonour and criminal liability
- Dishonour for insufficient funds is a criminal offence: up to 2 years' imprisonment, fine up to twice the cheque amount, or both (s.138) [Statutory]
- Presumption of debt in the payee's favour unless the drawer disproves it (s.139) [Statutory]
- Jurisdiction at the payee's bank branch (s.142, 2015 amendment) [Statutory]
- Interim compensation up to 20% during trial (s.143A); appellate deposit of at least 20% of the fine or compensation (s.148) [Statutory]
- Offences are compoundable / settleable (s.147) [Statutory]

### 1.6 Statutory timers (the "s.138 clock")
- Presentation window: within 6 months of the cheque date, or its validity period, whichever is earlier (s.138 proviso a) [Statutory]
- Cheque validity: 3 months from date (RBI, effective 1 Apr 2012) [Regulatory]
- Demand notice: must be sent within 30 days of learning of dishonour (s.138 proviso b) [Statutory]
- Grace period: drawer has 15 days from notice to pay before a complaint can be filed (s.138 proviso c) [Statutory]

### 1.7 Legal gaps (unresolved by the 2002 amendment)
- Electronic endorsement not defined [Statutory gap]
- Electronic "holder in due course" protection not defined [Statutory gap]
- Electronic crossing not defined [Statutory gap]
- These gaps mean a pure electronic instrument may only be a "quasi" negotiable instrument until addressed [Secondary finding / legal commentary]

---

## 2. Regulatory and clearing infrastructure

### 2.1 Clearing system
- Cheque Truncation System (CTS): banks exchange the cheque's image, not the paper, since introduction in 2008 [Regulatory]
- CTS-2010 standard cheque design, though banks add their own extra security features on top, causing variation across the system [Regulatory]
- Continuous clearing Phase 1 live since 4 Oct 2025: presentation 10am to 4pm, confirmation till 7pm, unconfirmed items deemed approved; hours revised 24 Dec 2025 to presentation 9am to 3pm, confirmation 9am to 7pm [Regulatory]
- Phase 2 (settlement within ~3 hours) deferred "until further notice," Dec 2025 [Regulatory]

### 2.2 Fraud and verification controls
- Positive Pay System (PPS): banks must enable it for cheques ≥₹50,000; many banks made it mandatory at ₹5 lakh+ from Aug 2022; only PPS-compliant cheques get CTS dispute-resolution protection [Regulatory]
- PPS requires the payer to separately confirm payee/amount details before presentation — a second, disconnected step from issuing the cheque [Industry practice / friction point]

### 2.3 Volume and value trends
- CY2024: 62.59 crore cheques processed via CTS, worth ₹71.80 lakh crore [Secondary finding]
- Cheque transaction volume fell from 72 crore (2021) to 57 crore (2025) [Secondary finding]
- Cheque values held up / rose slightly even as volume fell — cheques concentrating into larger-value transactions [Secondary finding]
- Paper instruments held ~2.3% of total transaction value in H1 2025, against 99.7–99.8% digital share of volume [Secondary finding]

---

## 3. Court and dishonour-enforcement burden

### 3.1 Case volume
- Nationally: **43 lakh pending s.138 cases** as of Dec 2024 [Secondary finding, confirmed via GSTV]. Earlier figure: **35.16 lakh** as of 31 Dec 2019, cited by the Supreme Court in In Re Expeditious Trial (16 Apr 2021). Use both, dated; the rise is itself a finding [corrected 1 Oct 2026]
- Delhi district courts: 6,50,283 pending cases as of Sep 2025; s.138 cases are 49.45% of total trial-court pendency in Delhi [Secondary finding]
- Mumbai: 1,17,190 pending; Kolkata: 2,65,985 pending [Secondary finding]

### 3.2 Trial process and duration
- Typical process: cheque return memo → legal notice (30 days) → 15-day grace period → court filing (30 days) → summons → trial → judgment [Statutory, sequenced]
- Duration estimates vary widely by source: 6 months (summary-trial target) to 1.5–3 years (reported practice) [Secondary finding, wide range — needs an advocate to confirm which applies to your target courts]
- Most cases now tried as summary trials (s.143 read with s.262 CrPC); sentence under summary trial capped at 1 year, but cases >₹5 lakh may go to regular summons trial [Statutory]

### 3.3 Recent court-driven digitisation
- *Sanjabij Tari v. Kishore S. Borcar* (25 Sep 2025): summons by email/WhatsApp; QR/UPI links in district courts to pay the cheque amount online; standard complaint synopsis; graded settlement costs [Secondary finding — case law]
- A referenced 2026 source mentions a "2025 Amendment" introducing Mandatory Mediation and a new Section 138A. **Re-checked 1 Oct 2026: no supporting source found.** A Supreme Court guidelines article covering the same ground discusses settlement/compounding under the *existing* framework, not a new mandatory-mediation mechanism. **Now treat this claim as more likely wrong than merely unverified — do not design around it without a primary source.**

---

## 4. Stakeholders and their needs

| Stakeholder | Role | Core need | Hypothesised pain |
| --- | --- | --- | --- |
| Payer (drawer) | Writes, signs, owns the account | Control over *when* money leaves; formal record | Can't track pending cheques; criminal exposure if funds fall short |
| Payee (holder) | Receives, holds, presents | Assurance of future payment; legal leverage | Waiting, bank trips, bounce risk, slow litigation |
| Drawee bank | Pays or returns the cheque | Fraud prevention, clear mandate | Signature disputes, altered cheques, PPS gaps |
| Collecting bank | Collects for payee | Good-faith collection protection (s.131) | Handling physical instruments and returns |
| NPCI | Runs CTS grid and UPI | Standardised, secure image/data | Two parallel worlds (CTS, UPI) with little overlap |
| RBI | Sets clearing/PPS/validity rules | Payment-system safety and efficiency | Large residual paper-instrument value |
| Courts | Hear s.138 complaints | Clear evidence of debt, dishonour, notice | Heavy backlog (Section 3, above) |
| Landlords, lenders, vendors | Demand cheques as security/payment | Enforceable commitment | Chasing payers, storing PDC bundles |
| Lawyers/notaries | Draft notices, file complaints | Proof of dates and delivery | Manual timeline reconstruction |
| Mediators | Hear cases referred under mediation (if 2025 amendment confirmed) | Faster settlement track | **Likely not real** — the claim underlying this row wasn't corroborated on re-check; keep the row but treat it as low-confidence |
| Credit bureaus (CIBIL/Experian) | Hold payer credit/repayment history | Accurate, queryable risk data | Not currently integrated into cheque-acceptance decisions |
| Guarantors / co-signatories | Back SME PDCs in some lending arrangements | Visibility into the instrument they've guaranteed | Currently invisible to the instrument's design |
| Issuing platform (bank/fintech) | Builds and operates the digital instrument | Regulatory compliance, fraud liability | Currently unaddressed — the instrument doesn't build itself |
| MSME trade associations | Shape community trust and norms | Credible, adopted standard | Untested whether they'd endorse a new instrument |

**Design implication carried over**: courts and banks are *invisible users* — records need to be legible to a judge or bank officer, not just the two app users.

---

## 5. Current cheque lifecycle (physical instrument)

1. **Drawing** — payer fills date, payee, amount (words + figures), signs. Friction: errors, overwriting, signature is the only authentication. [Statutory: s.6, s.7]
2. **Delivery** — handed over in person, by courier, or left with landlord/lender, often post-dated. Friction: theft, loss, no receipt of handover. [Industry practice]
3. **Holding** — payee waits for the date or a condition. Friction: payer can't see or stop a pending cheque; payee has no funds guarantee. [Industry practice]
4. **Presentation** — must occur within 3 months of the cheque date. Friction: missed windows, branch/drop-box trips. [Regulatory + Statutory]
5. **Clearing** — image-based via CTS. Friction: Phase 2 (fast settlement) still deferred. [Regulatory]
6. **Verification** — signature, funds, and PPS check (if submitted). Friction: PPS is a separate, easily-forgotten step. [Regulatory]
7. **Settlement** — payee credited, usually notified only by SMS, with no link back to the underlying agreement. [Regulatory]
8. **Dishonour** — returned with a reason memo; starts the legal clock. [Regulatory / bank practice]

---

## 6. Underlying user needs a cheque currently serves

| Need | How a physical cheque meets it | Do current digital rails meet it? | Confidence |
| --- | --- | --- | --- |
| Enforceable promise | s.138 criminal offence + s.139 presumption of debt | Partly (PSS Act s.25 exists but little-known, narrow scope) | High |
| Future-dated payment | Post-dating locks amount + date | Partly (NACH/UPI AutoPay cover recurring merchant debits only) | High |
| Payer control of debit timing | Money leaves only on presentation | Partly (scheduled NEFT is payer-controlled but gives payee no commitment) | Medium |
| Security/collateral | Undated/post-dated cheques held as s.138 threat | Weak (e-mandates carry less perceived legal "bite") | Medium |
| Formal documentation | Physical artefact with name, amount, signature, number | Partly (UTR numbers prove transfer but carry no purpose/agreement/signature) | Medium |
| Large-value P2P | No per-instrument cap | Partly (UPI capped at ₹1 lakh/day P2P; NEFT/RTGS uncapped but no future-dating) | High |
| Institutional habit/compliance | Some institutions specify cheque/DD | Varies | Low — needs field check |
| Ritual and formality | Signing feels deliberate | Unknown — UPI feels casual by design | Low |
| Unfamiliarity with digital | Assumed for older/rural users | Probably overstated for business users | Low — treat with caution |

---

## 7. Constraints specific to India's primary and secondary research segments

### 7.1 MSME supplier–buyer (primary segment)
- Post-dated cheques used for 30/60/90-day credit terms, advance and security cheques [Industry practice]
- Core need: enforceable future payment, cash-flow control [Hypothesis]
- Independent data (non-cheque-specific): ₹10.7 lakh crore in MSME working capital locked in delayed payments annually; 80% owed to micro/small enterprises; median debtor days for micro-enterprises 195, against a legal 45-day window [Secondary finding — MSME Samadhaan / GAME research]
- Formal redress is weak: under 1% of registered MSMEs ever file on Samadhaan; only ~22–26% of filed cases resolve/settle [Secondary finding]

### 7.2 Tenants and landlords (secondary segment)
- Rent PDC bundles, security deposit cheques [Industry practice]
- Core need: assurance of rent for landlord, control for tenant [Hypothesis]

### 7.3 Access-for-research constraint
- MSME/vendor segment: good research access (local traders, Gandhinagar/Ahmedabad markets)
- Tenant/landlord segment: good access (students, local owners, brokers)
- Lenders/NBFCs: medium access (guarded)
- Priority ranking is itself a **Hypothesis**, to be revisited after early interviews

---

## 8. Instrument-design constraints (from the Design Factors doc, filtered to what's relevant to the *current* physical instrument, not the future digital one)

- **Mandatory fields**: payer, payee, drawee bank, amount in words and figures, date, instrument number, signature [Statutory/Design]
- **Mutability**: stop-payment is possible but only by explicit request; no easy in-flight edit [Industry practice]
- **Transferability**: endorsement exists on paper but has no defined electronic equivalent [Statutory gap]
- **Funds certainty**: none — a cheque can always bounce; there is no reservation-at-issue mechanism in the current paper system [Industry practice]
- **Uniqueness**: physical scarcity (one signed original) is the only duplicate-prevention mechanism [Industry practice]
- **Batch/business workflows**: maker-checker approval chains for business cheques are informal, paper-based [Industry practice]
- **Account-type eligibility**: both current and savings accounts get chequebooks, including for PDCs [Industry practice — confirmed 1 Oct 2026]

---

## 9. What this file deliberately excludes
- Anything from the Global Precedents doc (Hong Kong, Singapore) — that's comparative, not India's *current* state
- Anything about the proposed digital concept (A/B/C or the hybrid) — that belongs to Ideation/Design stages
- Unverified [V]-tagged items from the Design Factors doc that need a legal/regulatory source check before being treated as current fact

## Open items carried forward
- [x] ~~Confirm whether Indian savings accounts can issue physical cheques~~ — **Resolved 1 Oct 2026**: both current and savings accounts get chequebooks, including PDCs. Singapore's "EDP/EDP+ expands access to savings accounts" argument does not transfer to India.
- [x] ~~Reconcile the two conflicting national court-pendency figures~~ — **Resolved 1 Oct 2026, corrected same day**: both figures are sourced. 35.16 lakh (Dec 2019, Supreme Court 2021) and 43 lakh (Dec 2024, GSTV). Cite both with dates.
- [x] ~~Verify the 2025 Mandatory Mediation / Section 138A claim against the bare amended Act~~ — **Re-checked 1 Oct 2026**: no supporting source found; now flagged as likely wrong, not just unverified.
- [ ] Confirm which duration estimate (6 months vs 1.5–3 years) applies to Gujarat courts specifically, via an advocate
