# E-Cheque in India — Predictive Scenarios to 2028
*Digital Cheque project · written 2026-09-26*

My forecast is that if e-cheques arrive, they will most likely be a **bank-issued digital twin of the paper cheque**. That means it's legally a cheque under NI Act s.6, it runs on the existing cheque-clearing system, and businesses get it first. The second strongest possibility is that the RBI's exploration **stalls** and nothing launches by December 2028. Everything below is judgement built on sourced facts; each line is labelled as evidence or forecast.

## 1. What the RBI's sentence tells us

| Phrase or placement | Evidence (from the document) | What I infer |
| --- | --- | --- |
| "unique benefits of paper-based instruments" | The RBI says cheques have benefits but doesn't name them | The RBI sees cheques as worth keeping, not something to phase out |
| Placed alongside a review of cheque *security* (3.10) | Paper cheques are being redesigned in the same section | Paper and electronic cheques will exist side by side; this is not a replacement |
| "speed and reliability of electronic payments" | — | The aim is faster clearing and less tampering, not new legal features |
| "new business use cases" | — | Businesses and MSMEs come first; individual customers later, or not at all |
| Listed under innovation goal 2.2(g), next to cards | Not listed under safety | Treated as a new product to try, not a fix for bouncing |
| "shall be explored" | The weakest verb used in the document | The next step is a study or discussion paper, not a launch |

## 2. Two real precedents that set the range
- **Hong Kong, 7 Dec 2015 (a true e-cheque).**
  - Legally a cheque under its Bills of Exchange Ordinance.
  - Issued through online banking as a digitally signed PDF and sent by email.
  - Deposited through online banking or a central "drop box".
  - Can be post-dated up to 90 days.
  - Must be "account payee only", so it can't be passed to someone else.
  - It can still bounce, and the bank charges a fee when it does.
- **Singapore (the opposite route).**
  - Banks stop issuing corporate cheque books after 31 Dec 2025. Corporate cheques stop being processed after 31 Dec 2026.
  - The replacement is Electronic Deferred Payment. Standard EDP debits the payer only when the payee presents it. EDP+ deducts the funds at issuance, so payment is certain.
  - EDP is deliberately *not* a cheque, so cheque law doesn't apply. If it isn't honoured, the payee's recourse is the original debt.
  - Retail cheques continue.

India's wording ("electronic cheques", while also upgrading paper cheques) is much closer to **Hong Kong** than to Singapore.

## 3. Four scenarios up to December 2028

| Scenario | What it would look like | Legal route | How likely (my judgement) | Why |
| --- | --- | --- | --- | --- |
| **A. Paper twin** (Hong Kong-style) | Bank app issues a signed e-cheque; payee deposits it; clears through the cheque system | NI Act s.6; a bounce falls under s.138 | **Most likely** | The law already exists; the clearing system and Positive Pay can be extended; it matches the RBI's word "cheque" |
| **B. Deferred payment, not a cheque** (Singapore-style) | Post-dated debit on NEFT or UPI; an optional version reserves the funds at issuance | Payment and Settlement Systems Act (s.25 for failures), or just the original debt | Less likely | It contradicts "electronic cheques" and the RBI's decision to keep paper cheques |
| **C. Cheque inside UPI** | NPCI builds an "e-cheque" object in UPI apps: post-dated, visible to the payee, clears on the due date | s.6 in form, UPI mandate in mechanics | Possible | NPCI's pattern is building on UPI, but mixing cheque law with UPI rules is legally messy |
| **D. Stall** | Only a study or discussion paper by 2028; no live system | — | **Real risk** | The legal definition has gone unused for 24 years; "explore" commits to nothing; Phase 2 of continuous cheque clearing is already postponed |

## 4. Six angles
- **Legal.**
  - Scenario A automatically brings in s.138, which makes a bounce a criminal offence. Easier issuing could therefore mean *more* bounce cases in courts already overloaded with them (forecast).
  - The RBI may add a variant that reserves funds at issuance, like EDP+, to reduce bounces (forecast).
  - The Act's missing rules for electronic endorsement and crossing push towards "account payee only, not transferable", as Hong Kong chose (inference).
- **Banks.**
  - They gain fees and less paper handling, and lose fraud from altered cheques.
  - Duplicate deposits of the same file become a new risk. Hong Kong handles this with a central deposit gateway (evidence).
- **MSMEs.** Their core need, a payee-held future commitment, is served. But an e-cheque with the date and amount filled in can't be an *undated blank security cheque*. That practice would either stay on paper or be forced to change (forecast).
- **Individuals.** Paper cheques continue, so there's no forced switch. Uptake depends on bank apps. This part is untested.
- **Fraud.** Likely new attacks include fake e-cheque PDFs sent by email or WhatsApp, and social engineering. So "is this e-cheque genuine?" becomes an important design moment (forecast).
- **Courts.** A digitally signed e-cheque with dated records could make it easier to prove a bounce case. That fits the Supreme Court's 2025 push to digitise these cases (inference).

## 5. What to watch for
- An RBI discussion paper or draft framework on e-cheques.
- An NPCI circular or pilot with a small group of banks.
- A bill amending the NI Act to cover electronic endorsement and crossing.
- Phase 2 of continuous cheque clearing being resumed.
- Positive Pay becoming mandatory at lower amounts.

## 6. What this means for our project
- **Don't bet on one scenario.** Design the layer that holds in A, B and C: a commitment the payee can hold, shared status, reminders before the due date, and records a court can use.
- **The A/B/C concept decision already in our plan maps onto these scenarios.** This analysis can serve as the evidence for that decision point in the case study.
- **Scenario D is an opportunity.** If the RBI stalls, the case study can present itself as input to the RBI's exploration.

## Sources
- [RBI Payments Vision 2028, official PDF](https://rbidocs.rbi.org.in/rdocs//PublicationReport/Pdfs/PAYMENTSVISION2028270326500316AFADEB47259CB970132BA01304.PDF)
- [Hong Kong e-Cheque launch, 23 Nov 2015 press release](https://www.info.gov.hk/gia/general/201511/23/P201511230374_print.htm)
- [HSBC Hong Kong e-Cheque FAQ](https://www.business.hsbc.com.hk/en-gb/regulations/e-cheque-faq)
- [Rajah & Tann on Singapore's EDP](https://www.rajahtannasia.com/viewpoints/mas-roadmap-to-cease-use-of-sgd-corporate-cheques-and-digital-payment-solutions-for-post-dated-payments/)
- [East & Partners on Singapore's corporate cheque timeline](https://eastandpartners.com/news/singapore-extends-timeline-for-phasing-out-corporate-cheques-to-2026/)

*Note: later research (Global Precedents doc) found the official ABS dates are: corporate cheque issuance stops 1 Jan 2026, processing stops 1 Jan 2027. MAS and HKMA pages could not be opened directly; confirm before citing.*
