---
name: swiggy-gap-analysis
description: Stage 4 Gap Analysis (#57) for the Swiggy Support Agent Decision Interface. Every known gap across the research files in one place, sorted by type, with its effect on the design and how it is handled.
researched: 2026-10-01
status: complete as of stage 4; update after the Customer Experience Audit and the simulated expert interview
---

# Gap Analysis

## 0. How to read this
Sources merged: `swiggy-refund-and-blocking-rules-research.md`, `swiggy-cross-party-evidence-research.md`, `swiggy_evidence-based_research.md`, `swiggy-case-study-context.md`, `swiggy-literature-review.md`, `swiggy-artifact-analysis.md`.

Five gap types. The type decides what we do about it.

| Type | Meaning | What we do |
|---|---|---|
| **A. Not public** | Searched and confirmed absent from public sources | Design around it and label it as an assumption. More searching will not help. |
| **B. Not yet searched** | Not reached within the research budget | Search if it can change the design; otherwise list as a limitation. |
| **C. Contradiction** | Two sources disagree | Pick a stance, cite both, explain the choice. |
| **D. Weak evidence in use** | A claim we rely on rests on one, low-tier or unverified source | Downgrade, re-verify, or drop. |
| **E. Method gap** | A research method planned but not done | Fill or declare in Limitations. |

Priority: **High** = changes what the panel shows; **Medium** = changes how a claim is worded; **Low** = background only.

**Headline:** the biggest gaps are not fixable by searching. Swiggy publishes no agent screen, no refund thresholds, no food claim window and no rule for weighing restaurant and delivery-partner history. These are type A, so the design must treat them as labelled assumptions. The gaps we can still close are a handful of type B searches, the teammate file corrections, and the two missing methods (audit and expert input).

---

## 1. Type A: Not public (design around)

| # | Gap | Effect on design | Handling | Priority |
|---|---|---|---|---|
| A1 | What the Swiggy Agent Workbench screen shows | No baseline to compare against | Concept framed as hypothetical; every element labelled data, insight or decision support | High |
| A2 | Refund thresholds, percentages and partial-refund rules ("up to 100%", "case to case") | Checklist cannot state an amount rule | Condition rows show **"No published rule"** where Swiggy is silent (pattern from Amex codes, artifact A2) | High |
| A3 | Food-order claim window | Timeline cannot draw a Swiggy cutoff for food | Use the one published cutoff ("before marked delivered", COD) and mark others as illustrative | High |
| A4 | Evidence rule for food claims (what counts, who supplies it) | Evidence panel cannot say what is "required" | Tag evidence by type and origin only (artifact A8); never "sufficient / insufficient" | High |
| A5 | How customer, restaurant and delivery-partner history are weighed together | The core of the problem statement has no reference | Show each party's dated raw events side by side; no weighting, no score | High |
| A6 | Whether agents see restaurant and delivery-partner history today | Unknown if the panel adds new data or regroups existing data | Keep as `[Assumed]` in stage 3; ask in the simulated expert interview as "not known publicly" | High |
| A7 | Refund value agents can approve without escalation | Value-ceiling rule needs a number | Use a clearly illustrative ceiling, labelled as such | Medium |
| A8 | How restaurant permission is requested and recorded | Hidden dependency on a third party | Show "restaurant response: pending / given / refused, time" as a fact | Medium |
| A9 | Human agent handling time for refund disputes | No baseline for "faster" | Measure relative time in testing (with vs without panel); do not claim a Swiggy baseline | Medium |
| A10 | Whether SHIELD device signals reach refund decisions | Unknown if device facts belong on the panel | Leave device signals off the panel; note as future scope | Low |
| A11 | OTP as delivery evidence for food (only alcohol is documented) | Cannot use OTP as a food evidence type | Use only for alcohol cases, or label as assumption | Low |
| A12 | Appeal process for blocked accounts | Outside the refund panel's decision | Out of scope; mention in Limitations | Low |

---

## 2. Type B: Not yet searched (close or declare)

| # | Gap | Could it change the design? | Handling | Priority |
|---|---|---|---|---|
| B1 | Full text of Swiggy's refund policy (page did not render) | Yes: may contain cutoffs we lack | Open the page in a browser during the audit and capture the text | High |
| B2 | Reddit r/swiggy and AmbitionBox, agent-side posts | Yes: only route to agent voices without an interview | 30-minute search for posts by support staff; tag Anecdotal | High |
| B3 | CCPA final outcome on cancellation and refund policy | Medium: changes the regulation section | One search; if none found, keep "pending" | Medium |
| B4 | Blinkit, Zepto detail, Amazon, Flipkart refund review practice | Low: Zepto and Uber Eats already cover the pattern | Declare as limitation | Low |
| B5 | Non-India rivals beyond Uber Eats and DoorDash | Low | Declare as limitation | Low |
| B6 | DPDP Act 2023 specifics on showing partner data to agents | Medium: supports role-limited fields | One check of purpose limitation wording before citing | Medium |
| B7 | State gig-worker laws on automated decisions | Low for the panel, medium for the ethics argument | Do not cite until verified | Low |
| B8 | Consumer commission orders beyond Amritsar | Low | Declare as limitation | Low |
| B9 | Parasuraman and Manzey full text (82% vs 33% figure) | No: argument already stands on the abstract | Do not cite the figure | Low |
| B10 | Management Science paper on two-sided platform disputes | Medium: only academic source on platform disputes | Read if time allows on Fri | Medium |
| B11 | Re-check: Swiggy Market Intelligence Dashboard, Uber Eats order accuracy, Zendesk context panel (now done, artifact A3) | Low | Market Intelligence and order accuracy pages still to open | Low |

---

## 3. Type C: Contradictions (pick a stance)

| # | Contradiction | Stance for the case study |
|---|---|---|
| C1 | Terms of Use: refunds only for Swiggy's own errors. Refund Policy: refunds for merchant and delivery-partner faults too. | Show both as a research finding. The panel follows the Refund Policy (the more specific document) and notes the conflict. |
| C2 | Policy and @SwiggyCares say 100% cancellation charge; MediaNama (citing Moneycontrol) reports charges up to 90%. | Cite 100% as the published policy and 90% as reported practice. Do not merge them. |
| C3 | Databricks post claims "100% of customer queries were fully automated" and also describes a human fallback. | Treat the 100% claim as vendor marketing; rely on the human-fallback description. |
| C4 | Teammate's file cites the Swiggy Market Intelligence Dashboard; the deep research report says it was not found. | Unresolved. Open the page (B11) before citing either way. |
| C5 | Literature: AI suggestions speed up novices (L5) vs suggestions cause errors when wrong (L1, L3, L4). | Panel chooses facts over suggestions and states the possible speed cost (literature review 3c). |

---

## 4. Type D: Weak evidence in use (fix before citing)

| # | Claim | Problem | Action |
|---|---|---|---|
| D1 | Agents see a "value tier", 3-month refund total and "fraud user" flag | One anonymised source (Business Standard); Swiggy did not respond | Cite as "reported by one anonymised agent"; use only to justify what the panel excludes |
| D2 | **Teammate file: Telangana association objection** | Misattributed; the article is about speed pressure, not the karma score | **Correct the file** before anyone cites it |
| D3 | **Teammate file: Uber Eats fraud rule** | Misread; the merchant is not charged, the customer's refund is not said to be withheld | **Correct the file** |
| D4 | **Teammate file: Uber Eats categories "disjoint"** | Wrong; the lists overlap and are a merchant cost rule, not a fault taxonomy | **Correct the file** |
| D5 | **Teammate file: "sometimes cannot definitively assign responsibility"** | Quote not found in any source | **Replace** with "We can never be fully right" (Exchange4media / India News Network) |
| D6 | Teammate file: Uber POD list | Misses pincode; ignores that options are configurable | **Correct the file** |
| D7 | Pathfinder blog: Swiggy AI decides refunds in 3 to 8 seconds | Low-tier, untraced | Drop |
| D8 | "vimo" chatbot name | No Swiggy primary source | Drop or tag secondary |
| D9 | Bot resolution about 75% (DEV repost) and 70% automation (PubNub) | Author's own figure and vendor marketing | Cite with the tag, never as fact |
| D10 | Medium repost: customers cancelling dozens of orders for 100% refunds | Not in the original Swiggy post | Tag low-tier or drop |
| D11 | Glassdoor agent reviews | Only 5 reviews | Quote as anecdote only |
| D12 | Zomato "50 to 70%" dispute figure | Reported three different ways from one podcast | Report as "roughly half to 70%, reported inconsistently" |

---

## 5. Type E: Method gaps

| # | Gap | Status | Handling |
|---|---|---|---|
| E1 | No real interview (expert cancelled) | Decided | Simulated expert interview, combined profile, labelled "source-grounded simulation"; Limitations line required |
| E2 | Customer Experience Audit not done (structure file wrongly says "done") | Open | Akshat runs it in the Swiggy app; kit to follow; fix the structure file wording |
| E3 | No agent participants for testing | Open | Heuristic evaluation and cognitive walkthrough only; peer Wizard of Oz only if time allows |
| E4 | No dispute-specific academic literature | Declared | Literature review section 4 |
| E5 | Artifact Analysis from documentation, not hands-on screens | Declared | Artifact analysis section 6 |

---

## 6. What to close before Define (Fri 2 Oct)
1. **D2 to D6:** correct the teammate's file (about 20 minutes). Needs your go-ahead, since it is not our file.
2. **E2 plus B1:** run the Customer Experience Audit and capture the full refund-policy text in the same session (about 2 hours, Akshat).
3. **B2:** 30-minute search of Reddit and AmbitionBox for agent-side posts.
4. **E1:** simulated expert interview, using A5, A6 and A7 as the questions the "expert" must answer as "not known publicly".
5. **B3:** one search for the CCPA outcome.

Everything else stays as a labelled assumption or a Limitations line.
