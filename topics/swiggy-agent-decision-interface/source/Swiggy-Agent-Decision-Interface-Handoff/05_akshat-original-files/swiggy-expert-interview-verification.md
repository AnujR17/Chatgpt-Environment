# Verification of Swiggy Simulated Expert Interview Transcript

Independent adversarial check of every `[Source: ...]` tagged claim in
`swiggy-simulated-expert-interview-transcript.md` against the six source
files listed in the task (literature review, artifact analysis, gap
analysis, and the three uploaded research files). This check does **not**
accept the transcript's own internal "Verification Log" at face value:
it re-derives verdicts independently.

| Question | Claim (short) | Tag claimed | Verdict | Note |
|---|---|---|---|---|
| Q1 | Card case fields: status, amount, reason code, reply-by date | Amex merchant dispute case view, Official | SUPPORTED | Artifact analysis A1 lists exactly these fields. |
| Q1 | Reason code requires specific evidence before deadline | Amex chargeback reason codes, Official | SUPPORTED | A2 structure (code, reason, time limits, required evidence) matches. |
| Q1 | Food-delivery sorts issue type, splits cost, escalates on trigger | Uber Eats order errors / DoorDash missing items, Official | SUPPORTED | A5 (cost split, escalation triggers) and A6 (issue refund flow) both back this. |
| Q1 | What slows Swiggy agents | [Not known publicly] | CORRECT GAP | Gap A9 in gap-analysis; no source addresses Swiggy agent time-loss causes. |
| Q2 | Named conditions = reason code + window + evidence | Amex chargeback reason codes, Official | SUPPORTED | Matches A2 exactly. |
| Q2 | People follow a decision aid even when wrong, not fixed by instructions | Parasuraman & Manzey 2010, Literature | SUPPORTED | L1: "cannot be prevented by training or instructions," occurs with "imperfect" decision aids. |
| Q2 | Trust should be calibrated to a specific component, not "the system" | Lee & See 2004, Literature | SUPPORTED | L2 "functional specificity" quote matches directly. |
| Q2 | Swiggy's exact screen format | [Not known publicly] | CORRECT GAP | No source describes Swiggy's current agent screen (confirmed absence, gap A1). |
| Q3 | Evidence types: signature, barcode, picture, ID, pincode; photo automatic only for leave-at-door | Uber Direct proof of delivery, Official | SUPPORTED | Matches A8 wording almost verbatim, including "pincode," which some other project files had dropped (gap-analysis D6 flags a *different* file for missing it; this transcript has it right). |
| Q3 | Swiggy's own evidence rule for food | [Not known publicly] | CORRECT GAP | Gap A4; refund research file confirms no written evidence rule for food orders. |
| Q3 | AI-edited cracked-egg Instamart photo, full refund issued | deep research report, **citing Business Standard**, Reported | **PARTLY SUPPORTED** | The event is real and documented in `swiggy_evidence-based_research.md` section 3.1, but that section cites it to **Business Today (26 Nov 2025)** and **The Logical Indian**, not Business Standard. Business Standard is cited elsewhere in the same doc for a *different* claim (cancellation-charge/CCPA reporting, section 3.1 and the parameters table). This is a source misattribution, not a fabricated event. |
| Q4 | Reply-by date on card side | Amex merchant dispute case view, Official | SUPPORTED | A1. |
| Q4 | 96-hour error-reporting cutoff | Uber Eats order errors, Official | SUPPORTED | A5: "more than 96 hours after order was placed" not charged to restaurant. |
| Q4 | 48-hour acknowledgement / one-month resolution | Consumer Protection (E-Commerce) Rules 2020, Law | SUPPORTED | Refund research file section 8, matches. |
| Q4 | Swiggy's own food claim window | [Not known publicly] | CORRECT GAP | Gap A3. |
| Q5 | Three-way cost breakdown (customer refund / restaurant charge / platform cover) | Uber Eats order errors, Official | SUPPORTED | A5 CSV fields match exactly. |
| Q5 | Restaurants report deductions without proof, no dispute path | refund and blocking rules research file, citing MediaNama, Reported | SUPPORTED | Verbatim match to refund research file section 7. |
| Q6 | "History as plain counts with dates," no single score | refund and blocking rules research file, tagged Inferred-within-file | SUPPORTED (tag is honest) | Source file itself labels this [Inferred] (section 11); transcript correctly represents it as the project's own inference, not an external finding. |
| Q6 | Zomato karma score = real example of history-to-score, drew a fairness objection | cross-party evidence research file, citing Outlook Business and India News Network, Reported | SUPPORTED | Matches cross-party doc 2b (karma score) and 2c (Telangana association fairness objection, India News Network link). |
| Q6 | Explanations/summaries make a conclusion persuasive regardless of correctness | Bansal et al. 2021, Literature | SUPPORTED | L4 exact quote. |
| Q7 | Automation bias occurs in experts too, resists training | Parasuraman & Manzey 2010, Literature | SUPPORTED | L1 exact quote. |
| Q7 | Explanations increase acceptance "regardless of correctness" | Bansal et al. 2021, Literature | SUPPORTED | Exact quote, L4. |
| Q7 | Cognitive forcing cuts over-reliance 64%→48% | Buçinca et al. 2021, Literature | SUPPORTED | Matches L3 exactly. |
| Q7 | Reply-suggestion tool: +34% novice RPH, minimal effect on experienced, 38% adherence | Brynjolfsson, Li & Raymond 2023, Literature | SUPPORTED | Exact figures, L5. Transcript's own text correctly flags this is a reply-suggestion tool, not an adjudication tool; matches literature review's caveat. |
| Q8 | Uber Eats escalation triggers named (late filing, high-value, alcohol, first-time) | Uber Eats order errors, Official | SUPPORTED | A5 exact wording. |
| Q8 | Payout-threshold guardrail with escalation | Fini refund audit log, Vendor | SUPPORTED | A7: "maximum autonomous payout threshold before escalation." |
| Q8 | Swiggy's own escalation thresholds | [Not known publicly] | CORRECT GAP | Gap A7. |
| Q9 | Audit log fields: policy version, data points, amount, action, timestamp | Fini refund audit log, Vendor | SUPPORTED | A7 exact quote. |
| Q9 | Forcing a reason/decision reduces over-reliance, costs preference | Buçinca et al. 2021, Literature | SUPPORTED | L3. |
| Q10 | Novice agents +34%, experienced "minimal impact" | Brynjolfsson, Li & Raymond 2023, Literature | SUPPORTED | Exact quote, L5. |
| Q10 | Whether Swiggy differentiates tooling by tenure | [Not known publicly] | CORRECT GAP | No source states this either way. |
| Q11 | Market Intelligence Dashboard tracks restaurant cancellations/complaints, but restaurant-facing | cross-party evidence research file, citing Swiggy Catalyst blog, Official | SUPPORTED | Matches cross-party doc 1a. |
| Q11 | No public source describes a delivery-partner history view | cross-party evidence research file, confirmed gap | SUPPORTED | Matches 2a: "confirmed gap." |
| Q11 | Whether either reaches an agent's screen | [Not known publicly] | CORRECT GAP | Matches doc's own "flagged as an open question, not assumed." |
| Q12 | Zomato karma score covers customers and riders, CEO quoted: "can never be fully right" | cross-party evidence research file, citing Outlook Business and India News Network, Reported | **PARTLY SUPPORTED** | The "can never be fully right" quote is correct, but it is **not** in the cross-party-evidence-research file (which instead carries a different, disputed quote, "sometimes cannot definitively assign responsibility," flagged in the gap analysis as not traceable to any source and slated for replacement). The "can never be fully right" wording is actually in `swiggy_evidence-based_research.md` section 6, citing **Exchange4media**, not India News Network. The transcript picked the *correct* quote but attributed it to the *wrong* file and the *wrong* outlet. |
| Q12 | Swiggy's own weighing logic | [Not known publicly] | CORRECT GAP | No source states this. |
| Q13 | Swiggy: "case to case" / "sole discretion," no number given | refund and blocking rules research file, citing Swiggy Refund Policy, Official | SUPPORTED | Matches section 2. ("Sole discretion" is sourced to Instamart specifically, not the general food policy, but the transcript doesn't over-specify, so this is a fair compression.) |
| Q13 | DoorDash 20-min/7-day thresholds, Uber Eats value-based escalation as comparable published examples | DoorDash missing items / Uber Eats order errors, Official | SUPPORTED | A6, A5. |
| Q13 | Swiggy's actual approval-without-escalation number | [Not known publicly] | CORRECT GAP | Gap A7. |
| Q14 | Confirmed absence of food claim window / evidence rule in Swiggy policy | refund and blocking rules research file, Official policy, absence confirmed | SUPPORTED | Matches section 3b/10. |
| Q14 | Amex publishes every window, no equivalent gap | Amex chargeback reason codes, Official | SUPPORTED (slight generalization) | A2 shows a consistent per-code structure (time to raise, time to challenge) for the codes documented; "every window" is a reasonable but not literally verified extrapolation across all Amex codes, since only two example codes are detailed in the artifact analysis. |
| Q15 | Project rule against value-tier / fraud-user flags | project rules, as given | SUPPORTED (as a design rule, not a [Source] claim against the 6 files) | Matches refund research file section 11's own stated rule ("Do NOT surface 'value tier' or a 'fraud user' flag"). Correctly not framed as an external citation. |
| Q15 | Zomato karma score as real precedent for this risk | cross-party evidence research file, citing Outlook Business, Reported | SUPPORTED | 2b. |
| Q15 | Explanations make a conclusion more persuasive regardless of correctness | Bansal et al. 2021, Literature | SUPPORTED | L4. |
| Q16 | Literature shows failures appear under load / on wrong-data cases, not easy ones | Parasuraman & Manzey 2010 / Buçinca et al. 2021, Literature | SUPPORTED | L1 (multiple-task load), L3 (no-AI group more accurate than AI groups when AI was wrong). |
| Q16 | Testing metrics (time to decision, lookups, consistency, override rate) named earlier in project | deep research report | SUPPORTED | Matches `swiggy_evidence-based_research.md` section (d) "Metrics for the prototype test" almost verbatim. |

## Verdict on "[Not known publicly]" tags

Every "[Not known publicly]" tag in the transcript was checked against all
six source files. In every case (Q1 agent time-loss causes, Q2 Swiggy's
screen format, Q3 Swiggy's evidence rule, Q4 Swiggy's claim window, Q8
Swiggy's escalation threshold, Q10 Swiggy's tenure-based tooling, Q11
whether restaurant/courier history reaches an agent screen, Q12 Swiggy's
weighing logic, Q13 Swiggy's approval-without-escalation number), none of
the six source files states the fact. The transcript does not dodge
anything it could have answered: each of these is a genuine, confirmed
gap (most map directly onto named gaps A1, A3, A4, A7, A9 in the gap
analysis). No instance was found where a "[Not known publicly]" tag was
used to avoid a claim a source file actually supports.

## Verdict on smuggled verdicts/scores/predictions

Every "[Inferred]" design note was checked for a disguised verdict, score,
or label about a customer, restaurant, or courier. None was found. The
design notes stay at the level of interface design guidance ("show X as a
dated fact, never a badge," "use an illustrative ceiling," "apply the same
format to all three parties") and never predict an outcome for, or attach
a label to, any specific party. The transcript is internally consistent
with the project's no-verdict rule throughout.

## Discrepancies this check found that the transcript's own Verification Log missed

The transcript's internal "Verification Log" claims 46 supported / 2
partly supported / 0 unsupported, and names only two partly-supported
items (the L5 adherence/improvement figures' task mismatch, already
flagged in-line, and the Q6 "Inferred within that file" tag correction).
This independent check found **two additional attribution errors** the
internal log did not catch:

1. **Q3**: the Instamart cracked-egg incident is tagged "citing Business
   Standard," but the source file (`swiggy_evidence-based_research.md`)
   actually cites **Business Today** (26 Nov 2025) and The Logical Indian
   for that specific event. Business Standard is a real outlet used
   elsewhere in that file for a different claim (the CCPA/cancellation
   story), so this looks like a citation mix-up rather than fabrication,
   but it is still a wrong attribution a reader could not verify by
   checking the named outlet.
2. **Q12**: the Zomato CEO quote "can never be fully right" is accurate,
   but it is sourced in the transcript to "cross-party evidence research
   file...India News Network." The cross-party file does not contain this
   quote (it carries a different, gap-analysis-flagged-as-unverifiable
   quote instead); the actual "can never be fully right" quote lives in
   `swiggy_evidence-based_research.md`, citing Exchange4media. The
   underlying fact is right; the citation trail is wrong.

Neither of these is a fabricated claim; both describe real, documented
events/quotes, but both would send a reader checking citations to the
wrong document and the wrong outlet name.

## Summary count

| Category | Count |
|---|---|
| Supported | 39 |
| Partly supported | 2 (Q3 source-outlet misattribution, Q12 source-file/outlet misattribution) |
| Unsupported (fabricated) | 0 |
| Correctly tagged "Not known publicly" gaps | 9 |

## Overall verdict

No claim in this transcript invents a fact, a Swiggy-specific number, or a
quote that doesn't exist in the source material. All substantive content
checks out against the artifact analysis, literature review, and the
three uploaded research files, and every declared gap is a genuine gap,
not a dodge. The two issues found here are narrower than fabrication:
both are **citation/attribution slips**, a real claim pointing to the
wrong named outlet or the wrong research file, rather than invented
content. Given that, the transcript is **safe to cite for its
substantive claims**, but a student case study should not reproduce the
two flagged citations (Business Standard for the egg photo; India News
Network for the "can never be fully right" quote) without correcting them
to the outlets/files actually responsible (Business Today/The Logical
Indian; Exchange4media), since a reader or examiner checking those named
sources directly would not find the quote there.
