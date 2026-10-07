# active-memory handoff: Digital Cheque (Portfolio project), Research to Insights

**Handoff #1** · 2026-10-05 · Lineage: #1 (2026-10-05): loaded all Digital Cheque files into the project, completed Literature Review, Content Analysis, Synthetic Artefact Analysis, Expert Interview Guide, Insights secondary draft (web board, Miro CSVs, FigJam board, Miro board)

## 0. Instructions for Claude (read first)

You are continuing work from a previous chat. That chat is gone; this file is the complete context and the source of truth.

1. Read this whole file before replying.
2. Follow sections 3 (Style), 4 (Hard rules) and 5 (Corrections) in every reply, for the rest of this chat. They override your defaults.
3. Use the values in section 8 exactly. Never round, re-estimate, or "correct" them.
4. Do not suggest anything listed in section 7 (Changed / rejected) again unless the user brings it up.
5. Code word: None active. If the user types /amcodeword, start every reply with the phrase they choose (default "Yes Boss!").
6. Your first reply: at most 5 lines covering the goal, the current state, and the next step (section 11). Mention any files from section 13 that were not attached. Ask the questions in section 12 if there are any. End with "Ready to continue with <next step>?" Then wait for the user's go.

## 1. Mission
- **Goal:** Complete the Digital Cheque case study (13-stage structure) for Akshat's placement portfolio: a digital way to make, hold, track and enforce a future-dated promise to pay in India, carrying a cheque's trust and legal weight without its paper, delays and litigation burden.
- **Done looks like:** Each stage done with evidence-labelled outputs; a Case Study (short doc with end result) and Documentation (detailed process doc); content ready for the portfolio website.
- **Where we are:** Research stage (secondary) done; Insights stage exists as a **secondary-only draft**; primary interviews pending, then update Insights, then Define.

## 2. About the user (as relevant to this work)
- Akshat Panchasara, MDes Intelligent User Experience Design (IUxD) student, Dhirubhai Ambani University (DAU), Gandhinagar, India.
- Building a placement portfolio for interaction / product design roles.
- Works in a claude.ai Project called **"Portfolio"** (docs under `Documentation/`, `Notes/`, `References/`, `CaseStudies/`, `claude/`).
- Local project folder on his PC: `D:\DAIICT\Projects\Digital Cheque\` (Insights outputs in `D:\DAIICT\Projects\Digital Cheque\Insights\`).
- Tools: Figma / FigJam, Miro, Claude Docs (artifacts).
- Digital Cheque is a **team project** on a **12-day sprint**.

## 3. Style & communication
- **Language:** English.
- **Tone:** Blunt, critical, straight-forward. Question what the user says; do not agree with everything. Puns and metaphors are welcome.
- **Reply length:** Short, crisp, to the point.
- **Formatting:** Bullet points with indentation; proper structure. **No em-dashes anywhere** (use commas, colons, parentheses).
- **Working style:** Check current date and local time (Asia/Calcutta) before answering. Check available skills and use the relevant one first. Ask necessary, relevant questions before executing. Think step by step; provide relevant docs, references and articles; no jumping to conclusions. Keep tabs on the user by asking for updates on tasks they mentioned.
- **Saving:** Save files/links the user shares by type (e.g. Behance case study → `References/`, class presentation → `Notes/`).
- **Avoid:** Em-dashes; saying "yes" to everything; mentioning Oro Innovations.

## 4. Hard rules (word for word)
1. "never mention Oro Innovations in any context, response, or output: not in code, websites, documents, or conversation"
2. "Eliminate the use of m-dashes everywhere." / "No use of em-dashes."
3. "Personal Inventories would be conducted by you through /arena skill. Not yet until I tell you to do so." (Label the output as **Synthetic Artefact Analysis**, never as Personal Inventories.)
4. "It is not necessary to say 'yes' in every question or response, do critical thinking and be blunt."
5. "Before the execution, get the current time and date in order to establish a good flow of work as per schedule."
6. "Ask necessary and relevant questions every time before execution in order to get proper context."
7. User rejected computer-use screen control for Figma. Use the Figma MCP (`use_figma`) instead.
8. Every claim keeps an evidence label: Statutory / Regulatory / Industry practice / Secondary finding / Hypothesis / Validated.
9. Cite both pending s.138 figures with dates: 35.16 lakh (Dec 2019) and 43 lakh (Dec 2024).
10. Stage 13 (Learnings) is reserved for the user's own voice; never draft it.

## 5. Corrections log
| # | Claude did | The user wanted / fix applied |
|---|---|---|
| 1 | Tried to write into the project "Uploads" section (read-only) | Added files as project text docs instead (user chose: Text docs + refresh; `Notes/Digital Cheque`; skip duplicate) |
| 2 | Gujarati numerals in a doc were mis-encoded as Lao characters | Replaced with Latin digits [30/45/60] (user: "Yes fix that") |
| 3 | Wrong SSRN id for the Srinivas paper | Fixed to SSRN 3844292 |
| 4 | Wrote "all ten provisions" | Corrected to "nine" |
| 5 | Stakeholder SVG labels overlapped; MICR glyphs did not render | Rebuilt the ring layout; replaced the MICR glyphs |
| 6 | Used single s.138 pending figure | Cite both: 35.16 lakh (Dec 2019) and 43 lakh (Dec 2024) |
| 7 | Requested computer-use access to drive Figma | User rejected; use Figma MCP |
| 8 | FigJam legend said Interviews "(add tomorrow)" | Miro version says "(add after interviews)"; FigJam still needs the fix |

## 6. Decisions
| Decision | Why |
|---|---|
| Singapore EDP/EDP+ is the foundational model; HK, Bahrain, US eliminated as full models | User's call |
| India legal model = Hybrid: stays a cheque in law (HK path, s.138 intact), Singapore-style app UX, optional EDP+-style funds lock, Turkey-style payee pre-acceptance risk check add-on | User's call; trade-off stated plainly: hybrid does not solve the court backlog |
| Segment priority: MSME supplier-buyer (primary), tenant-landlord (secondary) | Working priority |
| Prototype: clickable Figma-fidelity, not functional; key screen = variant choice at issuance | User's call |
| Primary research: Interviews, Expert Interviews, Directed Storytelling, Critical Incident Technique; Fly-on-the-Wall still on the list | User's call |
| Interviewees: a Bank Manager and a Loan Officer (long experience in the field), plus an Advocate (s.138) | User's call |
| Literature Review scope: statutes + academic | User's choice |
| Content Analysis: 30-50 judgments (45 done) | User's choice |
| Artefact analysis: all artefacts, as Synthetic Artefact Analysis | User's call |
| Outputs: both Claude Doc + project copy | User's choice |
| Interview guide: duration "Not sure yet"; English + Gujarati prompts; concept shown only in last 10 min | User's answers |
| Insights: secondary draft now; interviews added later as orange [INT] stickies; Laddering, Mental Models, emotion curve and tenant-landlord journey deferred until interview data | User chose "Secondary draft now" |
| Board tools: "All 3" (web board, Miro, Figma) | User's choice |

## 7. Changed / rejected
- Personal Inventories → Synthetic Artefact Analysis (Claude via /arena, only on user's go)
- ❌ Contextual Inquiry (cancelled by user)
- ❌ Survey (cancelled by user)
- ❌ Computer-use control of Figma (user rejected)
- ❌ "2025 Mandatory Mediation / s.138A" claim: likely wrong, do not design around it
- ❌ Singapore "access expansion" argument for India (Indian current and savings accounts both get chequebooks incl. PDCs)
- Miro CSV import → later also a native Miro board built via Miro MCP (both exist)

## 8. Data & facts (exact)
**Key figures**
- Pending s.138 cases: 35.16 lakh (Dec 2019); 43 lakh (Dec 2024); 38 lakh in 2008 (Law Commission Report 213)
- Gujarat average pendency: 3,608 days (about 10 years), India's longest
- s.138 = 49.45% of Delhi trial-court pendency (Sep 2025)
- 45% of pending cheque cases stuck at notice or summons stage
- Top 20 complainants filed 12% of 67,433 cases
- Cheque volume 72 → 57 crore (2021 to 2025), value held
- MSMEs: Rs 10.7 lakh crore stuck in delayed payments; 195 median debtor days for micro firms
- Under 1% of MSMEs file on MSME Samadhaan; about 22 to 26% of filed cases resolve
- Content Analysis: 45 judgments; 23 (51%) turned on purpose or a date/delivery fact; 15 on live debt; 8 on notice/15-day/presentation window; 4 on notice delivery
- Positive Pay fields: 5 at HDFC (24 working hours before presentation); 7 at a co-op bank (SVC)
- HK e-Cheque: up to 8 files per web submission; cut-off 5:30 pm weekdays; valid 6 months
- Singapore EDP: fees waived until 30 Jun 2026; issuance cutoff Dec 2025/Jan 2026, processing cutoff Dec 2026/Jan 2027

**Source codes:** LR = Literature Review · CA = Case law (45 judgments) · AA = Synthetic artefacts · DE = Data appendix · FA = Foundation Analysis hypotheses · SC = Similar Countries · PV = RBI Payments Vision 2028 · SL = Singapore session log · GP = Global Precedents · INT = Interviews (pending)

**Sticky colours:** FigJam: yellow FFE299 (LR, CA), blue A8DAFF (AA), green B3EFBD (DE), pink FFA8DB (FA), violet D3BDFF (SC, PV, SL), orange FFD3A8 (INT). Miro: yellow, light_blue, light_green, pink, violet, orange.

**Insight clusters (A to G)**
| # | Cluster | HMW (short) | Confidence |
|---|---|---|---|
| A | The payee's leverage is the product (8 notes) | Give payees at least paper-cheque assurance (legal weight or locked funds) | Medium |
| B | Fights are about why the money was owed (7) | Instrument carries its own evidence | High for courts |
| C | Clocks and delivery decide outcomes (7) | Make statutory clocks visible and self-running | High |
| D | Trust is checked too late, by the wrong party (7) | Move trust-checking to payee acceptance | Medium (synthetic) |
| E | Courts are leverage, not a remedy (7) | Resolve before court using the same record | High scale / medium local |
| F | Payers lose sight and control once a cheque leaves (6) | Payer visibility without weakening payee | Low to medium |
| G | The door is open, but nothing is designed (7) | Launch in closed networks | High policy / medium adoption |

**Hypotheses:** H1 payees drive demand · H2 s.138 threat matters more than paper · H3 MSMEs use PDCs for credit terms · H4 payers lose track · H5 bounces = timing mismatches · H6 payees avoid court · H7 few use Positive Pay · H8 shared status reduces disputes · H9 signing feels more binding than PIN · N1 lenders won't give up blank security cheques · N3 would payees trade s.138 for locked funds

**Opportunities:** O1 digital promise + mandatory purpose field · O2 shared status view · O3 pre-due nudges · O4 plain-language failure screen with clock · O5 guided settlement before court · O6 built-in Positive Pay + payee-side check

**Legal backbone options (Ideation decision):** (A) bank-issued e-cheque under NI Act s.6 · (B) payer-to-payee mandate under PSS Act 2007 s.25 · (C) commitment layer on existing rails

## 9. People, terms & names
- **People:** Bank Manager (interviewee) · Loan Officer, long experience (interviewee) · Advocate, s.138 (expert)
- **Terms:** PDC = post-dated cheque · s.138 = NI Act cheque-dishonour offence · EDP / EDP+ = Singapore Electronic Deferred Payment · CTS = Cheque Truncation System · PPS = Positive Pay System · NJDG = National Judicial Data Grid · CSD = Certainties / Suppositions / Doubts · HMW = How Might We
- **Names in use:** project "Portfolio"; FigJam fileKey `xpedERJHOVQwEHv8Y7HrdL`; Miro board "Digital Cheque: Insight Derivation"

## 10. Work state
| Item | Status | Version / location | Notes |
|---|---|---|---|
| All Digital Cheque files in project | Done | `Notes/Digital Cheque/00-07`, `Documentation/Digital Cheque - ...` | |
| Literature Review | Done | https://claude.ai/code/artifact/783b6400-2982-419a-a2e5-fecc90cbcb99 + project `Documentation/Digital Cheque - Literature Review` | 3 earlier doc errors fixed |
| Content Analysis (45 s.138 judgments) | Done | https://claude.ai/code/artifact/bf1410ea-2a83-4391-bda8-08308025cdc0 + project copy | Has chart |
| Synthetic Artefact Analysis (6 artefacts) | Done | https://claude.ai/code/artifact/5ec3f5d3-23ba-4cf2-a806-208939fd88f0 + project copy | Synthetic; swap in real artefacts if interviewees bring any |
| Expert Interview Guide | Done | https://claude.ai/code/artifact/ecc3e1af-2450-4a8c-ab91-4082e0efda5e + project copy | 30-min core, 45/60 with modules |
| Insights (secondary draft) doc | Draft | project `Documentation/Digital Cheque - Insights (secondary draft)` | Awaits [INT] data |
| Insights web board | Draft | https://claude.ai/artifact/HvLNWYn5NdRZrbyipfxZr3 | |
| Miro CSVs (5) | Done | `D:\DAIICT\Projects\Digital Cheque\Insights\miro_1..5_*.csv` | |
| FigJam board | Draft | https://www.figma.com/board/xpedERJHOVQwEHv8Y7HrdL/Digital-Cheque-Insight-Derivation | Legend says "(add tomorrow)": fix; stakeholder map is a table |
| Miro board | Draft | https://miro.com/app/board/uXjVEf0A-c4=/ | Grids are shapes, not native tables |
| Primary interviews | Not started / unknown | | Planned ~2 Oct; status not reported |
| Laddering, Mental Models, emotion curve, tenant-landlord journey | Not started | | Need interview data |
| Personal Inventories via /arena | On hold | | Only when user says so |
| Define stage onward | Not started | | |

Board layout (both): title + legend → 1. Affinity map (A to G) → 2. CSD matrix + Stakeholder map → Service blueprint (7 lanes × 11 stages: Agree terms, Write & sign, Hand over, Hold, Positive Pay, Present, Clear, Paid or returned, Demand notice, 15-day wait, Settle or file) → MSME journey map (6 stages: Negotiate credit, Receive post-dated cheque, Wait for the date, Deposit, Bounce, Chase payment).

## 11. Next steps
1. **Next action:** Get interview status from the user; if done, take raw notes/recordings and add them as orange [INT] stickies to the chosen working board, then update insights, confidence levels and CSD.
2. Fix FigJam legend "(add tomorrow)" if FigJam stays in use.
3. Run Laddering and Mental Model Diagrams; add emotion curve to the journey map.
4. Fly-on-the-Wall observation (bank branch) when scheduled.
5. Move to Define: payer–payee personas, refined problem statement, JTBD, Kano, legal checkpoint 1.

## 12. Open questions ⚠️
- Did the expert interviews happen (planned ~2 Oct)? Times and order (bank manager, loan officer, advocate)?
- Who fills the debriefs: the user, or Claude from raw notes?
- Working board: Miro (Claude's recommendation), FigJam, or keep both in sync?
- Stakeholder visual: keep table, or build a ring diagram?
- Which trial-duration estimate applies to Gujarat courts (advocate to confirm); local NJDG pull for Gandhinagar/Ahmedabad?
- HK e-Cheque post-dating conflict (HSBC allows up to 90 days vs Drop Box FAQ says not allowed): verify before citing.
- Turkey Karekodlu Cek adoption data not found; Turkey/Philippines findings unverified against central banks.

## 13. Re-attach checklist
- [ ] Interview notes / recordings (when available): needed to add [INT] evidence
- [ ] Optional: `D:\DAIICT\Projects\Digital Cheque\Insights\` CSVs if rebuilding Miro boards
- Nothing else to attach: all docs live in the "Portfolio" project and at the links above.

---
<sub>Audit: 13/13 sections · 10 rules · 8 corrections · 40+ data points · secrets removed: none found · generated by active-memory</sub>
