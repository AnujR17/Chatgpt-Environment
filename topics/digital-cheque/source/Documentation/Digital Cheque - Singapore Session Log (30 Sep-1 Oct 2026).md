# Digital Cheque — Session Context Log
*Compiled 1 Oct 2026, 01:01 IST. Covers the Singapore EDP/EDP+ research thread, the India hybrid-model decision, the stakeholder and scenario work, and every visual produced in this session. Evidence labels follow project convention: Statutory / Regulatory / Industry practice / Secondary finding / Hypothesis — with "unverified" flagged wherever a primary source (MAS, RBI, the bare Act) hasn't confirmed it yet.*

---

## 1. What this session covered

Starting point: the team had already finalized **Singapore's EDP/EDP+** as the core foundational model for the Digital Cheque case study, having eliminated Hong Kong, Bahrain, and the US as full models (Hong Kong remains a cross-reference for legal-continuity mechanics). This session:

1. Answered what happens to existing post-dated cheques (PDCs) under Singapore's sunset of corporate cheques.
2. Clarified EDP vs EDP+ mechanics, specifically how each treats post-dating and fund locking.
3. Clarified Singapore's current/savings account eligibility for EDP/EDP+ and what that means relative to physical cheque access.
4. Confirmed paper cheques are NOT fully sunsetting in Singapore — only the corporate track is, retail/personal cheques continue.
5. Researched whether any concrete India-specific digital cheque model already exists (RBI, NPCI, industry) — found none beyond a two-sentence "explore" commitment.
6. Locked four sprint-planning decisions via a structured question (see Section 3).
7. Built a full stakeholder map (13 stakeholders, expanded from the original 9).
8. Built a legal-model implications comparison (Pure Singapore vs Hybrid) and recommended the **Hybrid model** for India.
9. Built 9 detailed user scenarios for Singapore's EDP/EDP+, then mapped India equivalents under the hybrid model.
10. Produced three rounds of visuals: a 3-diagram inline widget set, one combined full-detail flowchart (matplotlib), and 9 individual per-scenario flowcharts (matplotlib).

---

## 2. Singapore EDP/EDP+ — mechanics established this session

### 2.1 What happens to existing PDCs under the cheque sunset
- **No grandfathering, no automatic migration.** EDP/EDP+ is designed to replace PDCs going forward, not absorb existing ones. [Regulatory]
- Issuance cutoff: **31 Dec 2025 / 1 Jan 2026** — all banks stop issuing new SGD corporate chequebooks, bulk cheque services, and cheque self-printing. [Regulatory, confirmed via [East & Partners](https://eastandpartners.com/news/singapore-extends-timeline-for-phasing-out-corporate-cheques-to-2026/) and [ABS FAQ](https://abs.org.sg/docs/library/faqs-edp-edp.pdf)]
- Processing cutoff: **31 Dec 2026 / 1 Jan 2027** — last day a corporate cheque clears. Any PDC presented after this is rejected outright regardless of original issue date.
- Responsibility sits with payer and payee directly: payee must deposit before the deadline, or both parties renegotiate (cancel, agree a new EDP/EDP+ arrangement, or switch instrument).

### 2.2 EDP vs EDP+ — the core mechanical difference
| | EDP | EDP+ |
|---|---|---|
| Replaces | Post-dated cheque (PDC) | Cashier's order / bank draft |
| Funds locked | At **presentment** (near/at due date) | At **issuance**, immediately |
| Bounce risk | Same as a paper PDC — can still fail | None once issued — funds are reserved |
| Cancellation | Supported (mechanics not fully public) | Supported (mechanics not fully public) |
| Unclaimed | N/A in same way | **6-month expiry** from effective date, auto-refund to payer, payer must manually re-issue |

### 2.3 Account eligibility
- Eligible accounts: **current and savings SGD accounts linked to mobile banking only** — no separate third account type. [Regulatory, confirmed via DBS/OCBC/StanChart product pages]
- This is a **superset**, not a narrower pool: current-account holders keep physical cheque access AND gain EDP/EDP+; savings-account holders, who never had physical cheque access, gain EDP/EDP+ as a wholly new capability.

### 2.4 Corporate vs retail cheque tracks
- **Corporate current accounts**: paper cheque issuance and processing sunset on the timeline above. EDP/EDP+ is the mandated replacement.
- **Personal/retail current accounts**: paper cheques **continue**, unaffected by the corporate sunset. MAS's roadmap only sunsets the corporate track.

### 2.5 Legal status
- Neither EDP nor EDP+ is a cheque in law (deliberately, to avoid Bills of Exchange Ordinance exposure and any criminal liability). Dispute recourse for both is **civil/contract only**, never criminal.

---

## 3. Sprint-planning decisions locked this session

| Question | Decision |
|---|---|
| Segment scope | **Deferred** — team wants to define all stakeholders first, then set segment scope off that (see Section 4) |
| Interview count | **Fewer than 5, secondary data is the primary evidence base**; interviews are a stretch goal, not a research pillar |
| Prototype fidelity | **Clickable (Figma-fidelity) prototype**, not functional |
| Legal model for India | **Open pending the implications review** — resolved to **Hybrid model** after the comparison in Section 5 |

---

## 4. Stakeholder map (13, expanded from the original 9 in the Data Evidence Appendix)

Original 9 (from `Documentation/Digital Cheque - Data Evidence Appendix.md`):
Payer (drawer), Payee (holder), Drawee bank, Collecting bank, NPCI, RBI, Courts, Landlords/lenders/vendors, Lawyers/notaries.

**4 added this session, flagged as missing from the original map:**
- **Mediators** — relevant if the "2025 Mandatory Mediation / s.138A" claim (still unverified) is real.
- **Credit bureaus (CIBIL/Experian India)** — relevant if a Turkey-style (Karekodlu Çek / Findeks) payee-facing risk-check feature is built.
- **Guarantors/co-signatories** — sometimes back SME PDCs, currently invisible in the map.
- **The issuing platform itself** (bank or fintech operating the app) — currently treated as if the instrument builds itself.
- **MSME trade associations** — informal but real influencers of community trust and adoption.

---

## 5. Legal model decision — Pure Singapore vs Hybrid

| | Pure Singapore (not a cheque, no s.138) | **Hybrid (chosen)** |
|---|---|---|
| Criminal deterrent | None, civil/contract only | Retains s.138 — the leverage MSME payees currently rely on |
| Regulatory lift | Lighter | Heavier — must resolve NI Act's electronic-endorsement / holder-in-due-course gaps |
| Funds certainty | Strong (EDP+-style lock possible) | Possible as an **optional premium variant**, not the default |
| Fit with MSME trade-credit culture | Risky — removes the mechanism payees depend on | Strong fit |
| Court-backlog problem | Sidestepped, not solved | Not solved — an honest, disclosed trade-off |
| Build complexity | Lower | Higher |

**Decision: Hybrid.** Legal base follows **Hong Kong's** path (stays a cheque in law, NI Act s.6 route, s.138 intact). Delivery/UX follows **Singapore's** path (app-based issuance). Funds mechanic offers an **optional** Singapore EDP+-style lock-at-issuance variant, not mandatory. Verification layer borrows **Turkey's** Karekodlu Çek idea (payee-facing pre-acceptance risk check) as an add-on.

**Explicit limitation carried forward:** this model does not solve India's court-backlog problem (Section 3 of the Data Evidence Appendix) — removing s.138 would, but at the cost of the leverage MSMEs need. This is flagged as a known trade-off to state plainly in the final case study, not a gap to hide.

**Open risk to test, not assume:** whether Indian payees will accept a "less threatening" instrument (the optional EDP+-style variant) in exchange for funds certainty — a real question for interviews/secondary data, not a design assumption.

---

## 6. No existing India-specific model found
- RBI's only public position: Payments Vision 2028, Section 3.10 (27 Mar 2026) — two sentences, "will explore" e-cheques, no mechanism, no legal changes, no timeline. Still pre-consultation as of this session.
- Secondary reporting restates the existing NI Act s.6 electronic-cheque provision (already in law since 2002) in plain language — not a new proposal.
- No NPCI proposal, bank-led pilot, fintech whitepaper, or academic blueprint found specific to India's cheque-to-digital transition.
- **Conclusion carried into the project:** there is no external India model to react to or validate against. The hybrid concept fills a genuine vacuum rather than competing with an existing proposal.

---

## 7. Nine Singapore EDP/EDP+ scenarios (with India-hybrid equivalents)

1. **SME supplier payment via EDP** — funds not locked, bounce risk unchanged from a paper PDC. *India: default instrument, same bounce risk, s.138 intact.*
2. **High-trust one-off payment via EDP+** — funds locked at issuance, certainty for payee. *India: optional funds-reserved variant.*
3. **Savings-account holder gains new capability** — genuine expansion, not replacement. *India: not applicable. Resolved this session — Indian current AND savings accounts have both had full physical cheque/PDC access since banking was introduced in India, longstanding practice, not a recent change. There is no India equivalent of this scenario; the "EDP/EDP+ widens eligibility" narrative does not transfer.*
4. **Payer attempts EDP+ without sufficient funds** — issuance likely fails upfront (unverified); paper PDC can always be written, fails only later. *India: same two-variant distinction needs to be surfaced to the user at issuance.*
5. **Payee never claims the EDP+** — 6-month expiry, auto-refund, manual re-issue. *India: adopt same pattern for the optional variant; default instrument already has its own 3-month cheque validity rule, no new mechanic needed.*
6. **Cancellation before maturity** — EDP uses existing stop-payment mechanism; EDP+ cancellation rules unconfirmed. *India: default instrument reuses existing stop-payment flow; funds-reserved variant needs its own cancellation logic, no Indian precedent to copy yet.*
7. **Business caught mid-transition near the cutoff** — no auto-migration, manual renegotiation required. *India: flagged as a place to actively improve on Singapore — a batch-import/conversion path for outstanding PDCs, given India's far larger PDC volume.*
8. **Two tracks running in parallel** — Singapore splits by account type (corporate vs retail). *India: resolved this session — the split is entirely by account type as well, not by use case (MSME trade-credit vs personal/informal). Reverses the earlier untested assumption in this doc.*
9. **Dispute after payment** — Singapore: civil/contract recourse only for both EDP and EDP+, neither is a cheque in law. *India: this is the hybrid model's core advantage — the default instrument keeps s.138 + civil recourse; the optional funds-reserved variant likely weakens toward civil-only, a tradeoff that must be surfaced to the user at the moment of choosing it.*

**Cross-cutting pattern noted:** in almost every scenario, the friction point is the same — the hybrid model forces a choice between two variants (default cheque-like vs. optional funds-reserved) at issuance, each with different bounce risk, legal recourse, and cancellation rules. That choice screen is flagged as the single most important interaction to prototype and test.

---

## 8. Visuals produced this session

### 8.1 Inline widget diagrams (mcp visualize tool, node-budget constrained)
- `singapore_edp_edp_plus_overview` — instrument choice split (EDP vs EDP+)
- `singapore_edp_outcomes` — EDP issue → present → paid/bounced
- `singapore_edp_plus_outcomes` — EDP+ issue (locked) → claimed/unclaimed/cancelled

### 8.2 Combined full-detail flowchart (matplotlib, via `/data:create-viz`)
- `singapore_edp_edpplus_full_flow.png` — every step from account-type check through instrument choice, both full lanes, to every terminal outcome, plus two context notes (legacy PDC migration, corporate/retail track split). Corrected during review: the EDP dispute outcome was initially mislabeled with India's s.138 language; fixed to civil/contract-only, matching EDP+, since neither instrument is a cheque under Singapore law.

### 8.3 Nine individual per-scenario flowcharts (matplotlib)
- `scenario_01_edp_supplier_payment.png`
- `scenario_02_edp_plus_high_trust_payment.png`
- `scenario_03_savings_account_new_capability.png`
- `scenario_04_edp_plus_insufficient_funds.png`
- `scenario_05_edp_plus_unclaimed.png`
- `scenario_06_cancellation_before_maturity.png`
- `scenario_07_legacy_pdc_transition.png`
- `scenario_08_parallel_account_tracks.png`
- `scenario_09_dispute_after_payment.png`

Color key used throughout: blue = EDP lane, teal = EDP+ lane, green = success outcome, red = failure/weaker recourse, amber = pending/expiry/new-capability, gray = cancellation/neutral.

---

## 9. Open items / unverified facts carried forward

- [x] **Singapore's corporate-cheque issuance cutoff date** — **Resolved, and it contradicts the team's "Dec 2026" answer.** Two independent sources agree: issuance of new SGD corporate chequebooks stops **31 Dec 2025 / 1 Jan 2026** ([East & Partners](https://eastandpartners.com/news/singapore-extends-timeline-for-phasing-out-corporate-cheques-to-2026/), [ABS FAQ](https://abs.org.sg/docs/library/faqs-edp-edp.pdf)). "Dec 2026" is the **processing** cutoff (31 Dec 2026 / 1 Jan 2027), already correctly stated in Section 2.1. The team's answer conflated the two — use **Dec 2025/Jan 2026 for issuance**, **Dec 2026/Jan 2027 for processing**, going forward.
- [x] **EDP+ cancellation mechanics** — **Resolved** via [DBS](https://www.dbs.com.sg/personal/support/bank-payment-cancel-reject-edp.html). EDP: sender can cancel unilaterally through the app, no recipient consent needed, only before expiry and before the recipient cashes it out; recipient sees the stated reason. EDP+: sender **cannot** cancel directly in-app — must either get the recipient to reject it via their own banking app, or file an indemnity form at a branch. No explicit grace window beyond "before expiry, before cashed out."
- [x] **Whether EDP+ issuance fails upfront on insufficient funds** — **Marked resolved (yes, it fails) on the team's own search**, not on a source I could independently confirm. Re-checked ABS FAQ, OCBC, and Maybank pages myself before and after this was raised: none of them explicitly say issuance is rejected upfront. The closest primary wording (OCBC) is "funds are deducted immediately from the payer's account once the EDP+ is issued" — which implies upfront failure on insufficient funds by logical necessity (funds can't be deducted if they aren't there), but no page states it outright. Recording this as resolved per the team's find; if there's a specific page with the explicit statement, worth adding here as a citation so this isn't resting on inference alone.
- [x] ~~Whether Indian savings accounts can issue physical cheques today~~ — Resolved: both current and savings accounts get full chequebook/PDC access, longstanding practice since banking was introduced in India, not a recent change. Kills the "EDP/EDP+ widens eligibility" argument for India. Also updated in `Documentation/Digital Cheque - India Physical Cheque Parameters.md`.
- [x] **Whether India's natural instrument-track split is by use case or account type** — Resolved this session: **account type**, not use case. Section 7, Scenario 8 updated to match (was previously an untested "likely by use case" assumption — reversed).
- [ ] **Whether Indian payees would accept the optional, less-legally-protected funds-reserved variant** — stays open, **to be settled by research** (interview/secondary data), not desk-researchable.
- [~] Carried over from earlier work — **partially resolved.** National **43 lakh** pending-cheque-bounce-case figure has a direct source ([GSTV](https://www.gstv.in/news/magazines/43-lakh-cases-of-cheque-bouncing-pending-in-the-countrys-courts)); **correction (1 Oct 2026, later):** the ~35 lakh figure is sourced after all: 35.16 lakh as of 31 Dec 2019, cited by the Supreme Court in In Re Expeditious Trial (16 Apr 2021). Cite both figures with their dates. Delhi alone: **6.5 lakh pending** as of Sep 2025 ([Maheshwari & Co.](https://www.maheshwariandco.com/blog/section-138-ni-act-new-guidelines-by-sc/)). The **"2025 Mandatory Mediation / Section 138A"** claim found **no supporting source** in this pass either — the same Supreme Court guidelines article discusses settlement/compounding under the *existing* framework, not a new mandatory-mediation mechanism — this claim is now more likely wrong than merely unverified, do not cite it without a primary source. **Turkey's Karekodlu Çek adoption/uptake numbers:** still not found — searches return only explainer/how-it-works pieces, no usage statistics.
- [x] Project memory file (`digital-cheque.md`) — updated this session with the hybrid-model decision and these resolutions.

---

## 10. Sources used this session

- [MAS and ABS media release — EDP launch and cessation deadline extension](https://www.sgpc.gov.sg/api/file/getfile/Media%20release%20-%20MAS%20and%20ABS%20Announce%20Launch%20of%20EDP%20Solutions%20in%20Mid-2025%20and%20Extension%20of%20Deadline%20for%20Cessation%20of%20Corporate%20Cheques.pdf)
- [Linklaters — MAS's latest update on SGD Corporate Cheque Phase-out, EDP/EDP+](https://financialregulation.linklaters.com/post/102kzr1/singapore-mas-says-cheque-please-mass-latest-update-in-the-sgd-corporate-cheq)
- [DBS — Say Goodbye to Corporate Cheques](https://www.dbs.com.sg/sme/day-to-day/payments/domestic-funds-transfers/cheque-less)
- [DBS — Electronic Deferred Payment Services in Singapore](https://www.dbs.com.sg/sme/day-to-day/payments/domestic-funds-transfers/electronic-deferred-payment)
- [Standard Chartered Singapore — EDP FAQ](https://www.sc.com/sg/important-information/bbedpfaq/)
- [Standard Chartered Singapore — Electronic Deferred Payment](https://www.sc.com/sg/bank-with-us/manage-your-payments/electronic-deferred-payment/)
- [Charltons Quantum — MAS and ABS Announce EDP Launch](https://charltonsquantum.com/mas-and-abs-announce-launch-of-electronic-deferred-payment-solutions-in-mid-2025/)
- [OCBC — Electronic Deferred Payment product/T&C page]
- [East & Partners — Singapore Extends Timeline for Phasing Out Corporate Cheques to 2026](https://eastandpartners.com/news/singapore-extends-timeline-for-phasing-out-corporate-cheques-to-2026/)
- [ABS — EDP and EDP+ FAQs](https://abs.org.sg/docs/library/faqs-edp-edp.pdf)
- [DBS — Cancel or Reject an EDP/EDP+](https://www.dbs.com.sg/personal/support/bank-payment-cancel-reject-edp.html)
- [GSTV — 43 lakh cases of cheque bouncing pending in the country's courts](https://www.gstv.in/news/magazines/43-lakh-cases-of-cheque-bouncing-pending-in-the-countrys-courts)
- [Maheshwari & Co. — Section 138 NI Act New Guidelines by SC (2025)](https://www.maheshwariandco.com/blog/section-138-ni-act-new-guidelines-by-sc/)
- [Business Standard — RBI explores e-cheques in Payments Vision 2028](https://www.business-standard.com/markets/capital-market-news/rbi-explores-e-cheques-tighter-oversight-for-digital-platforms-in-payments-vision-2028-126032800324_1.html)
- [India Herald — E-Cheques coming, RBI proposes introduction](https://www.indiaherald.com/Politics/Read/994885470/No-More-Paper-E-Cheques-Are-Coming-RBI-Proposes-Their-Introduction-in-Payments)
- [Tribune India — RBI same-day cheque credit system from Oct 2026](https://www.tribuneindia.com/news/business/rbi-to-introduce-same-day-cheque-credit-system-from-oct-4-within-3-hours-from-jan-3-2026)

**Project docs referenced (not re-fetched, already in the project):**
- `Documentation/Digital Cheque - Data Evidence Appendix.md` (stakeholder table, MSME data, court pendency data)
- `Documentation/Digital Cheque - India Physical Cheque Parameters.md` (legal framework, NI Act gaps)
- `Documentation/Digital Cheque - Similar Countries Transition Analysis.md` (Turkey, Philippines research)
- Global Precedents doc (Hong Kong e-Cheque vs Singapore EDP/EDP+, uploaded PDF, read earlier in the broader session)

---

## 11. Files delivered this session (not saved to the project automatically)

- `singapore_edp_edpplus_full_flow.png` — combined full-detail flowchart
- `scenario_01` through `scenario_09` — nine individual PNG flowcharts
- This file — `digital-cheque-session-log.md`

None of the PNGs are currently saved into the Portfolio Craft project's doc list. If they should be kept as permanent reference material for the case study, they need to be attached/uploaded there separately, this project's doc store only holds text docs via `project_write`, not binary images.
