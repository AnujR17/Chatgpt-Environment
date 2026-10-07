# Digital Cheque — Design Factors and Parameters (under RBI constraints)
*Digital Cheque project · written 2026-09-27*

All factors, grouped under **12 headings**. Each heading splits into sub-headings, then categories, then the factors themselves. Each factor is tagged so you can sort by where the requirement comes from:

- **[S]** Statute: an Act of Parliament
- **[R]** RBI or NPCI rule
- **[C]** Court-directed or case law
- **[P]** Industry practice
- **[D]** Design consideration
- **[V]** A rule believed to exist but not yet verified in this project; check it before citing

The most important grouping: a small set of **non-negotiable constraints** (headings 1–2) limits what a large set of **design choices** (headings 3–12) can do. Deciding the instrument's legal identity first (1.1) settles many factors further down.

---

## 1. Legal and regulatory

### 1.1 The instrument's legal identity (decide this first)
- **Legal route:** NI Act s.6 "cheque in the electronic form" [S] vs PSS Act 2007 s.25 electronic funds transfer [S] vs a contract or mandate only [D]
- **Definition requirements:** "drawn on a specified banker", "payable on demand" (a conflict with post-dating) [S]; "account payee only" and "non-transferable" as defaults [D]
- **Signature standard:** digital signature or electronic signature as defined in the IT Act (s.6 Explanation I and III) [S]; which one to use: Aadhaar eSign, DSC or bank PIN [V]

### 1.2 NI Act provisions to respect
- **Roles:** drawer, drawee, payee (s.7) [S]
- **Crossing and collecting-bank protection** (s.123–131) [S]
- **Presentation window:** 6 months or the validity period, whichever is earlier (s.138a) [S]; 3-month validity [R]
- **Dishonour timers:** demand notice within 30 days, then 15 days to pay (s.138 b, c) [S]
- **Presumption of debt** (s.139) [S]
- **Jurisdiction:** at the payee's bank branch (s.142) [S]
- **Interim compensation** of up to 20% (s.143A) and **appeal deposit** of at least 20% of the fine or compensation (s.148) [S]
- **Compounding (settling out of court)** (s.147) [S]
- **Gaps:** electronic endorsement, holder in due course, electronic crossing [S, gap]

### 1.3 RBI and NPCI rules
- **Cheque Truncation System (CTS):** image clearing, CTS-2010 standard [R]
- **Continuous clearing:** Phase 1 live; Phase 2 postponed [R]
- **Positive Pay:** enabled at ₹50k+, may be mandatory at ₹5L+; only compliant cheques get CTS dispute resolution [R]
- **Payments Vision 2028:**
  - 3.10: review cheque design and security; explore e-cheques [R]
  - 3.1: on/off switch for payment modes [R]
  - 3.5: shared liability between banks [R]
  - 3.13: payments switching service [R]
  - 3.15: domestic LEI (business identifier) [R]
- **UPI limits:** ₹1L/day person-to-person; up to ₹5L per transaction for some merchant categories [R]
- **Other rules to verify:**
  - Digital payment security controls [V]
  - Limiting customer liability for fraud [V]
  - Turnaround time for failed transactions [V]
  - Payment data stored in India [V]
  - KYC Master Direction [V]
  - Beneficiary name look-up [V]

### 1.4 Adjacent laws
- **IT Act 2000:** e-signatures; First Schedule excludes negotiable instruments "other than a cheque" [S]
- **Bharatiya Sakshya Adhiniyam 2023:** admissibility of electronic records [V]
- **DPDP Act 2023:** consent and data rights [V]
- **Consumer Protection Act:** dark-patterns guidelines 2023 [V]
- **RPwD Act 2016:** accessibility obligations [V]

### 1.5 Court-driven
- **Supreme Court 2025 (Sanjabij Tari):**
  - Summons by email or WhatsApp [C]
  - QR or UPI payment of the cheque amount in court [C]
  - Standard complaint synopsis [C]
  - Graded costs for late settlement [C]
- **Post-dated cheques for an existing debt attract s.138** [C]

---

## 2. The instrument (what a digital cheque *is*)

### 2.1 Mandatory fields
- **Core fields:** payer, payee, drawee bank, amount in words and figures (or just one?), date, instrument number, signature [S/D]
- **Optional fields:** purpose, invoice or agreement reference, notes [D]

### 2.2 Time rules
- **Timing type:** issue now vs post-dated; maximum post-dating period (Hong Kong allows 90 days) [D]
- **Expiry and validity:** 3 months [R]; reminders before expiry [D]

### 2.3 Value rules
- **Amount limits:** minimum and maximum; per day and per instrument [R/D]
- **Currency:** INR only [D]

### 2.4 Mutability
- **Changes:** edit before acceptance? edit after? [D]
- **Stopping it:** cancel, or stop payment (who can, and until when) [P/D]
- **Replacement:** reissue or replace [D]

### 2.5 Transferability
- **Transfer:** endorsement allowed or not; split or partial payment [S gap/D]

### 2.6 Funds certainty model
- **Debit timing:** debit when presented (like a cheque) vs reserve funds at issue (like Singapore's EDP+) vs a hybrid [D]

### 2.7 Uniqueness
- **One live copy:** a single instrument ID that can't be presented twice or duplicated [D]

---

## 3. Lifecycle and system states

### 3.1 States
- **Draft → issued → delivered → accepted/rejected → held → due → presented → cleared/settled | returned → notice → paid-after-notice | escalated → compounded/closed → archived** [D]

### 3.2 State rules
- **Transitions:** who can move it to each state, and the time limit for each [S/D]

### 3.3 Timers
- **Tracked clocks:** due date, validity, the 30-day and 15-day s.138 clocks, clearing cut-offs [S/R]

### 3.4 Edge states
- **Unusual cases:** payer's account closed or frozen; payer dies or becomes insolvent; bank merger or account switch (Vision 3.13); holiday on the due date [D/P]

---

## 4. Stakeholders and roles

### 4.1 Primary
- **Payer and payee:** individual, business, or institution [D]

### 4.2 Business roles
- **Internal approvals:** maker-checker (one person drafts, another approves), approval limits, authorised signatories [P]

### 4.3 Banks
- **Drawee bank and collecting bank:** each one's liability and turnaround time [S/R]

### 4.4 Infrastructure
- **NPCI and the clearing house:** the rail operator [R]

### 4.5 Governance
- **Rule-makers and adjudicators:** RBI, courts, ombudsman [R/C]

### 4.6 Intermediaries
- **Third parties:** fintechs or technology providers, and their regulatory status (Vision 3.6, 3.14) [R]

### 4.7 Support roles
- **Professionals:** lawyers, CAs, accountants, brokers [P]

---

## 5. Identity, authentication and authorisation

### 5.1 Know-your-customer
- **KYC status:** of payer and payee [V]

### 5.2 Recipient identification
- **How the payee is named:** account plus IFSC, UPI ID, phone number, or business identifier [D]
- **Name check:** name match before issuing [V]
- **Account details:** whether the payee needs to share account details at all (a Hong Kong benefit) [D]

### 5.3 Authentication
- **Login and approval:** two-factor authentication, device binding, biometrics [V]

### 5.4 Signing
- **Signature:** type, legal validity, non-repudiation (the signer can't later deny signing) [S]

### 5.5 Consent
- **Explicit consent:** to issue, accept and share data [V/D]

### 5.6 Delegation
- **Acting for others:** power to sign for a company or family member [P]

---

## 6. Security and fraud

### 6.1 Integrity
- **Tampering:** tamper-evident record; alteration can be detected [R/D]

### 6.2 Authenticity
- **Fakes:** a way to check "is this e-cheque real?"; defence against spoofed PDFs or links [D]

### 6.3 Duplicate risk
- **Double use:** double presentment; replay attacks [D]

### 6.4 Social engineering
- **Deception:** phishing, fake payee, pressure tactics [D]

### 6.5 Verification
- **Positive Pay:** built-in equivalent, confirmed at issue [R]

### 6.6 Monitoring
- **Detection:** anomaly detection, velocity limits, on/off switch (Vision 3.1) [R/D]

### 6.7 Liability
- **Who pays for fraud:** allocation, including shared-responsibility ideas (Vision 3.5) [R]

### 6.8 Cyber
- **Resilience:** cyber controls, data encryption [V]

---

## 7. Money movement and settlement

### 7.1 Rail
- **Which system clears it:** CTS extension vs NEFT/RTGS vs UPI vs a new one [R/D]

### 7.2 Timing
- **Cut-offs:** settlement time; working days vs 24×7 [R]

### 7.3 Funds
- **Balance handling:** reservation or lien, balance checks, partial funds [D]

### 7.4 Failures
- **When a payment fails:** return reason codes, reversal turnaround time, compensation [R/V]

### 7.5 Costs
- **Fees and charges:** issuance, return, stop-payment [P]

### 7.6 Limits
- **Caps:** per instrument, per day, per segment [R/D]

---

## 8. Records, evidence and data

### 8.1 Audit trail
- **Event log:** every event time-stamped and unchangeable [D]

### 8.2 Legal evidence
- **Court readiness:** admissible, court-ready record [V]; proof that the notice was delivered [S/C]

### 8.3 Proof of payment
- **For users:** receipts, downloadable statements [D]

### 8.4 Retention
- **Storage:** how long records are kept; where they're stored (India) [V]

### 8.5 Privacy
- **Personal data:** collect only what's needed, purpose limits, user rights [V]

### 8.6 Access
- **Who sees what:** payer, payee, bank, court [D]

---

## 9. Failure, dispute and recourse

### 9.1 Pre-failure
- **Prevention:** low-balance warnings before the due date; reschedule by mutual consent [D]

### 9.2 Failure communication
- **Telling people:** instant alert to both parties with a clear reason [D]

### 9.3 Statutory path
- **Legal notice:** notice generated within 30 days; 15-day payment tracker [S]

### 9.4 Settlement
- **Early resolution:** in-app settlement or compounding; court payment by UPI or QR [S/C]

### 9.5 Disputes
- **Banking disputes:** bank dispute process, grievance redressal, ombudsman [R/V]

### 9.6 Non-payment disputes
- **Other conflicts:** disputes about the underlying deal; the payment system should stay neutral [D]

---

## 10. UX and interaction

### 10.1 Mental models
- **How people think of it:** cheque vs UPI vs promise; the payee's "held security" model [D]

### 10.2 Formality
- **Seriousness:** trust signals, a deliberate signing moment, "formal, not frictional" [D]

### 10.3 Transparency
- **Visibility:** status always visible; the next step and deadlines shown to both sides [D]

### 10.4 Confirmation
- **Checks before commitment:** review screen, cooling-off period, re-authentication for high value [D]

### 10.5 Errors
- **When things go wrong:** error states, recovery paths, empty states [D]

### 10.6 Cognitive load
- **Mental effort:** number of fields, defaults, templates for repeat payments [D]

### 10.7 Notifications
- **Alerts:** channels (SMS, app, email, WhatsApp), timing, frequency [D]

### 10.8 Inclusion
- **Reaching everyone:** languages, literacy, older users [D]; accessibility [V]; assisted channels (branch, agent) [D]

### 10.9 Ethics
- **Dark patterns:** none, e.g. no forced consent, no hidden fees [V]

### 10.10 Coexistence
- **Side-by-side use:** the paper cheque stays available; clear choice between the two [R]

---

## 11. Business workflows

### 11.1 Bulk
- **Volume:** batch issuance (Hong Kong: up to 200 per CSV) [P]

### 11.2 Integration
- **Systems:** ERP and accounting links; GST invoice references [D]

### 11.3 Controls
- **Approvals:** approval chains, limits per role [P]

### 11.4 Reconciliation
- **Matching:** matching payments to invoices; statements [D]

### 11.5 Credit terms
- **Post-dated schedules:** 30/60/90 days; instalments; links to TReDS (Vision 3.8) [R/D]

### 11.6 Security arrangements
- **Replacing blank security cheques:** a bounded, conditional alternative [D]

---

## 12. Ecosystem and adoption

### 12.1 Channel
- **Where it lives:** bank app vs UPI app vs net banking vs fintech [D]

### 12.2 Interoperability
- **Cross-bank:** any bank issues, any bank accepts [R]

### 12.3 Incentives
- **Why each party would adopt:** banks (fees, fraud reduction), payees (assurance), payers (control) [D]

### 12.4 Rollout
- **Phasing:** business users first; pilot banks; move to scale [R/D]

### 12.5 Migration
- **Transition:** from paper-cheque habits; education [D]

### 12.6 Scenario sensitivity
- **Changes by scenario:** these factors differ under scenarios A, B and C from the forecast: legal route, rail, funds model [D]

### 12.7 Measurement
- **KPIs:** bounce rate, time to settle, disputes, adoption [D]

---

**Checked vs not checked:**
- **[S], [R] and [C] items are checked** against sources used earlier in this project.
- **[V] items are from general knowledge.** Check each against the source before it goes into the case study.
- **[P] and [D] are framing,** not rules.
