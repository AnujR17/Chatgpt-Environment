# Countries with India-like Cheque Factors — Who Cracked the Transition (and Who Didn't)
*Digital Cheque project · compiled 30 Sep 2026. "Similar factors" is read here as: criminal or quasi-criminal liability for a dishonoured cheque, and/or a large SME trade-credit culture built on post-dated cheques — the two features that make India's problem distinctive from a purely developed-market payments story. Hong Kong and Singapore (already researched in the Global Precedents doc) do NOT share the criminal-liability factor, so they are cross-referenced only, not re-analysed here. Evidence labelled per project convention; nothing below is verified against primary regulator sources unless stated.*

---

## Why Hong Kong and Singapore aren't full matches on "similar factors"

- Hong Kong's e-Cheque still permits dishonour without criminal consequence — a bounced e-Cheque is a civil/banking matter with a bank fee (HK$150 at HSBC), not a prosecutable offence. [Secondary finding, from Global Precedents doc]
- Singapore's EDP is deliberately *not* a cheque in law specifically to avoid the Bills of Exchange Ordinance and any criminal exposure. [Secondary finding, from Global Precedents doc]
- Neither country has India's scale of informal SME trade credit built on post-dated cheques as collateral.
- **They remain the two strongest precedents for the *mechanics* of a digital instrument** (see Global Precedents doc) — this doc adds two countries closer to India on the *legal and economic* factors, to test whether the mechanics precedent still holds when criminal liability and SME credit culture are in play.

---

## 1. Turkey — closest legal/economic match, partial digitisation

### Why it matches India
- Post-dated cheques ("vadeli çek") are a core SME trade-credit instrument, much like India's PDCs for 30/60/90-day terms. [Secondary finding]
- Turkey criminalised cheque dishonour, decriminalised it in 2003, then reintroduced imprisonment for wilful non-payment for repeat offenders via a 2016 amendment — so criminal exposure is live again, similar in spirit to India's s.138. [Secondary finding — needs verification against the current Turkish Cheque Law text]
- Turkey has a well-documented history of high cheque-bounce and default rates tracking economic stress, comparable to India's court-backlog dynamic. [Secondary finding]

### What Turkey actually digitised (and what it didn't)
- **Did NOT create a bank-issued electronic cheque.** The paper cheque remains the legal instrument.
- **Did digitise the trust/verification layer**: a national "Karekodlu Çek" (QR-coded cheque) system, run through Turkey's credit bureau (Findeks/KKB) in partnership with banks (Garanti BBVA, Halkbank, and others each offer their own front end onto the same registry). A QR code printed on the physical cheque lets the *payee* query the drawer's payment risk and the cheque's status in real time before accepting it. [Secondary finding — verify against kkb.com.tr / tcmb.gov.tr before citing]
- This is functionally closest to India's Positive Pay, but flipped: Positive Pay verifies for the *bank* at presentation; Turkey's system lets the *payee* verify at the moment of acceptance, before the cheque is even taken.
- A parallel centralised "Çek Raporlama" (cheque reporting) registry tracks a drawer's cheque history nationally, which a payee or bank can query — addressing India's H4 (payers/payees losing track of issued cheques) at the ecosystem level, not just per-transaction.

### Design implication for the project
- This directly strengthens Opportunity Area O6 (built-in Positive Pay) and suggests a variant: a **payee-facing, pre-acceptance risk check**, not just a payer-facing confirmation step. Worth testing in interviews as its own concept, independent of the A/B/hybrid legal-route decision.
- Turkey's result is a caution against assuming "digitise the cheque" must mean "replace the cheque." A verification-layer-only digitisation reduced fraud and information asymmetry without touching the legal instrument or the criminal-liability regime at all.

### Open gaps
- No usage/adoption data found for the Karekodlu Çek system's actual uptake.
- Current criminal-liability text not verified against the primary Turkish statute.
- Whether Turkey's court backlog for bounced cheques improved after the QR system launched is unknown — not found in this pass.

---

## 2. Philippines — same legal shape, no comparable digitisation (a negative case)

### Why it matches India
- Batas Pambansa Blg. 22 ("BP 22," the Bouncing Checks Law) criminalises issuing a cheque that bounces for insufficient funds — a near-identical statutory shape to NI Act s.138, including its role as a very heavily litigated offence in Philippine courts. [Secondary finding]
- The Philippines has a large informal and SME trade-credit economy that relies on post-dated cheques (PDCs) for supplier payments, similarly to India. [Secondary finding]

### What the Philippines has and hasn't done
- Cheque clearing runs through the Philippine Clearing House Corporation (PCHC) with check-image clearing, comparable to India's CTS — a back-end digitisation only. [Secondary finding — not independently verified this pass]
- No evidence found of a bank-issued electronic cheque instrument, a QR-verification layer like Turkey's, or a funds-reserved digital variant like Singapore's.
- Digital payment growth (PESONet, InstaPay) has followed the same pattern as India's UPI/NEFT — solving instant transfer, not the future-dated, payee-held commitment function.

### Design implication for the project
- This is the useful **negative case**: a country with essentially the same legal architecture as India (criminal liability, heavy court litigation, SME PDC culture) that has *not* cracked the transition. It suggests criminal liability and litigation pressure alone are not sufficient triggers for digitisation — something else has to move first (a regulatory mandate, as in Singapore's phase-out; a new legal category, as in Hong Kong's e-Cheque; or a verification-layer product, as in Turkey).
- Strengthens the case that **India's RBI Payments Vision 2028 "exploration" commitment is the actual gating factor**, not the underlying legal or economic conditions — those have existed in multiple countries without producing a digital cheque on their own.

### Open gaps
- Whether the Philippines has any digital-cheque pilot or proposal in progress was not found in this pass — worth a follow-up search if time allows.

---

## 3. Cross-reference: what Hong Kong and Singapore still contribute

Per the existing Global Precedents doc: Hong Kong shows the *legal-continuity* path (still a cheque, still enforceable, no criminal bounce risk); Singapore shows the *funds-certainty* path (not a cheque, no bounce risk at all under EDP+). Neither operates under criminal-liability pressure, which is why Turkey and Philippines were researched here — they test whether the same digitisation logic holds when a criminal statute like s.138 is actually in the room. Turkey suggests yes, but via a narrower verification-only route; Philippines suggests the pressure alone changes nothing without a deliberate regulatory push.

---

## 4. Summary table

| Country | Criminal liability on bounce | SME PDC-style trade credit | What got digitised | Outcome for India's project |
| --- | --- | --- | --- | --- |
| Hong Kong | No (civil/bank fee only) | Limited | Full e-Cheque, still legally a cheque | Strongest mechanics precedent (see Global Precedents doc); weak on criminal-liability parallel |
| Singapore | No (not a cheque in law) | Limited | Funds-reserved deferred payment (EDP+) | Strongest funds-certainty precedent; weak on criminal-liability parallel |
| **Turkey** | **Yes** (reintroduced 2016) | **Yes** (vadeli çek) | Verification/registry layer only (QR risk check), not the instrument itself | Best legal/economic match; suggests a payee-facing pre-acceptance risk-check concept, separate from the A/B/hybrid decision |
| **Philippines** | **Yes** (BP 22) | **Yes** (PDCs) | Clearing only (image-based, like India's CTS) — no front-end digitisation found | Negative case: same conditions as India, no digital cheque produced; confirms regulatory will is the actual bottleneck, not legal/economic pressure |

---

## 5. What this means for the 12-day sprint

- The Turkey finding is strong enough to justify one additional "how might we" candidate at Ideation: a payee-facing pre-acceptance risk/status check, independent of which legal route (A/B/hybrid) the team picks for the core instrument.
- The Philippines finding is useful primarily as a rebuttal-ready data point if anyone on the team or a reviewer asks "why hasn't this happened already, given other countries have the same law?" — the answer is now evidenced, not assumed.
- Neither new country changes the core Hong Kong/Singapore concept-decision analysis already documented; they sit alongside it as supporting evidence, not replacements.

## Sources
- [Findeks Karekodlu Çek Sistemi](https://www.kkb.com.tr/urunler/findeks-karekodlu-cek-sistemi)
- [Halkbank Karekodlu Çek](https://www.halkbankkobi.com.tr/tr/kobi/urun-ve-hizmetler/Nakit-Yonetimi/Halkbank-Karekodlu-Cek.html)
- [Garanti BBVA Karekodlu Çek](https://www.garantibbva.com.tr/isim-icin/diger-urunler/karekodlu-cek)
- [New QR Code Era for Cheques in Turkey (Mondaq)](https://www.mondaq.com/turkey/financial-services/408392/new-qr-code-era-for-cheques-in-turkey)
- [Criminal Consequences of Bounced Cheques in Turkey (Lexology)](https://www.lexology.com/library/detail.aspx?g=b142aafc-0472-4bff-876c-c37a19b74c08)
- [Turkey's bounced cheques, loan and card defaults soar (AGBI, 2023)](https://www.agbi.com/analysis/economy/2023/10/turkeys-bounced-cheques-loan-and-card-defaults-soar/)
- [What is BP22 Bouncing Checks Law in the Philippines (Respicio & Co.)](https://www.lawyer-philippines.com/articles/what-is-bp22-bouncing-checks-law-in-philippines)
- [Bounced Check Laws in the Philippines (Respicio & Co.)](https://www.lawyer-philippines.com/articles/bounced-check-laws-in-the-philippines)
- [Philippine Check Clearing Process Overview (Scribd)](https://www.scribd.com/document/441851250/Philippine-Check-Clearing-Process)

**Not independently verified in this pass** — check against Türkiye Cumhuriyet Merkez Bankası (tcmb.gov.tr) and Bangko Sentral ng Pilipinas (bsp.gov.ph) before these findings go into the final case study.
