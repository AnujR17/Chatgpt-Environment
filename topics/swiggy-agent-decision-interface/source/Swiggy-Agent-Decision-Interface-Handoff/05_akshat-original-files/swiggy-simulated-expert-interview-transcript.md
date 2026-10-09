---
name: swiggy-simulated-expert-interview-transcript
description: Transcript of the Simulated Expert Interview (source-grounded) for the Swiggy Support Agent Decision Interface case study. Expert S1 is a simulated composite persona, not a real person. Every claim is tagged by its basis. Verified against sources on 2026-10-01; see the Verification Log at the end.
conducted: 2026-10-01
status: verified by an independent agent; 2 citation errors found and corrected, 0 fabricated claims
---

**Expert:** Expert S1 (simulated composite persona: card-dispute operations design, Amex-style, plus marketplace trust-and-safety practice). **Not a real person, not a real interview.**
**Interviewer:** Claude, acting as interviewer, questions fixed in advance per `swiggy-simulated-expert-profile.md`.
**Method note:** an attempt to run this as two separate sub-agents (one playing the expert, one interviewing) was abandoned after Q1, because the sub-agent hand-off mechanism only returns a *summary* of what the expert said, not the verbatim answer. A summary cannot carry the per-claim source tags this interview needs, so the interview was conducted directly, in one pass, holding to the same locked profile, knowledge boundaries and three-part answer format.

---

## Part 1. How dispute review works

### Q1. Walk through a disputed case from claim to decision, first for a card dispute, then for a food-delivery refund. Where do reviewers lose time?

**Answer:** On the card side, a cardmember raises a dispute, it lands on the merchant's case list with a status, amount, reason code and a reply-by date. The merchant opens the case, reads what that specific reason code requires as evidence, and either agrees or submits evidence before the deadline. On the food-delivery side, a customer reports an issue, the platform sorts it into an issue type, works out a refund amount and who pays, and either resolves it on the spot or sends it to a review team when a trigger fires, such as a high-value order or a late report. Time gets lost in the same place on both sides: hunting for the one piece of information that settles the case, whether that's which reason code actually applies or whether this specific order had a photo taken at delivery.

**Basis:**
- Card case view and fields: [Source: Amex merchant dispute case view, Official]
- Reason-code structure and evidence requirements: [Source: Amex chargeback reason codes, Official]
- Food-delivery issue sorting, cost split, escalation triggers: [Source: Uber Eats order errors, Official] [Source: DoorDash missing items, Official]
- What actually slows Swiggy's own agents down: [Not known publicly] (gap A1, A9 in the gap analysis)

**Design note:** [Inferred] A fixed reason-code-style checklist is a real, working pattern for card disputes. For Swiggy food orders, no such published checklist exists, so the panel must not invent one that looks equally authoritative. Where Swiggy is silent, say so on the screen rather than filling the gap with a plausible-looking rule.

---

### Q2. How is policy shown to a reviewer: as free text, a decision tree, or named conditions? What works under queue pressure?

**Answer:** The strongest published pattern is named conditions, each with its own time window and required evidence, the way Amex lays out a reason code. That beats free text because a reviewer under time pressure cannot be expected to parse a paragraph correctly every time. A decision tree is close, but it hides the conditions a reviewer didn't travel through, so if the tree routes wrong, nobody sees why. Named conditions, shown together, let a reviewer check them in parallel rather than being led by the hand.

**Basis:**
- Named-condition structure (reason code + window + evidence): [Source: Amex chargeback reason codes, Official]
- People follow a decision aid's path even when it's wrong, and this isn't fixed by instructions: [Source: Parasuraman & Manzey 2010, Literature]
- Trust should be calibrated to a specific, visible component rather than to "the system" as a whole: [Source: Lee & See 2004, Literature]
- Which exact format Swiggy agents currently see: [Not known publicly]

**Design note:** [Inferred] Named conditions, each labelled with its data source, is the format this project has already chosen (the "checklist" idea from the refund research file). This interview supports that choice rather than a decision-tree or free-text alternative.

---

### Q3. What types of evidence exist, and how should a reviewer know where each piece came from and when it was captured?

**Answer:** Evidence splits cleanly into two kinds: evidence captured automatically at the moment of the event, like a delivery photo or a barcode scan, and evidence supplied afterward by one of the parties, like a customer's own photo of a cracked egg. A reviewer needs to know which kind they're looking at, because the two carry very different weight, and needs to know exactly when it was captured, not just that it exists.

**Basis:**
- Evidence types and capture timing (signature, barcode, picture, ID, pincode; automatic only for leave-at-door): [Source: Uber Direct proof of delivery, Official]
- Swiggy's own evidence rule for food orders: [Not known publicly] (gap A4)
- A real instance of after-the-fact evidence being gamed (AI-edited cracked-egg photo, Instamart): [Source: deep research report, citing Business Today and The Logical Indian, Reported]

**Design note:** [Inferred] Every evidence item on the panel should carry two tags: type (photo, signature, OTP, text) and origin (captured at event vs submitted afterward). Never a "verified" or "suspicious" badge, since that's a verdict dressed as a fact.

---

### Q4. How should deadlines be shown: the claim window, the time left to respond, a regulatory clock?

**Answer:** All three, but kept separate, because they answer different questions. A claim window tells the reviewer whether a complaint was even raised in time. A reply-by date tells them their own clock. A regulatory clock, like India's 48-hour acknowledgement and one-month resolution rule, tells them what a regulator is watching. Collapsing these into one countdown would hide which deadline actually matters for this case.

**Basis:**
- Reply-by date on the card side: [Source: Amex merchant dispute case view, Official]
- 96-hour error-reporting cutoff on the food-delivery side: [Source: Uber Eats order errors, Official]
- 48-hour acknowledgement, one-month resolution: [Source: Consumer Protection (E-Commerce) Rules 2020, Law]
- Swiggy's own food claim window: [Not known publicly] (gap A3)

**Design note:** [Inferred] Three separate, labelled clocks, not one merged timer. Where Swiggy's own window is unpublished, show the regulatory clock and the reply-deadline only, and mark the claim-window row "No published rule" rather than guessing a number.

---

## Part 2. Three parties and history

### Q5. A refund moves cost between customer, restaurant, courier and platform. Should the reviewer see who pays, and how?

**Answer:** Yes, as a plain fact, not as a hint toward a particular outcome. Uber Eats already shows this directly: the refund amount, what the merchant is charged, and what the platform covers, as three separate figures. A reviewer who can't see where the cost lands is working blind on exactly the part of the decision that creates the most downstream conflict, since restaurants and couriers both complain when money is taken from them without a visible reason.

**Basis:**
- Three-way cost breakdown shown to the merchant: [Source: Uber Eats order errors, Official]
- Restaurants report deductions "even without customer proof, with no way to dispute": [Source: refund and blocking rules research file, citing MediaNama, Reported]

**Design note:** [Inferred] Show the split as three plain amounts, labelled by party, the same way Uber Eats does it for merchants. Do not colour-code or rank the parties by how much they lose.

---

### Q6. How do you show a party's past claims or complaints without turning them into a label or score?

**Answer:** Dated, individual events, nothing aggregated. "3 refunds in 90 days: 12 Jan missing item, refunded; 2 Feb wrong item, refunded; 9 Feb cancelled, no refund" tells a reviewer the pattern without telling them what to conclude from it. A single number, like a count or a percentage, always ends up read as a verdict, even when nobody intended that.

**Basis:**
- "History as plain counts with dates", explicitly avoiding a single score: [Source: refund and blocking rules research file, Inferred within that file]
- Zomato's karma score is the real-world example of exactly this turning into a score, and the fairness objection it attracted: [Source: cross-party evidence research file, citing Outlook Business and India News Network, Reported]
- Explanations and summaries make people accept a conclusion whether or not it's right, which is why a derived "pattern" line is riskier than raw dated events: [Source: Bansal et al. 2021, Literature]

**Design note:** [Inferred] Apply the same dated-events format to all three parties equally, customer, restaurant and delivery partner, so no one party is shown with more judgement attached than another.

---

### Q7. Scores, flags and "approve" suggestions: shown or hidden from reviewers? What goes wrong either way?

**Answer:** Hidden, as a design choice, not because they're technically hard to build. Showing a flag or a suggested action gets followed even when wrong, and that doesn't go away with training. Hiding it protects decision quality but gives up a real, measured speed benefit for new agents on other kinds of tasks, like drafting a reply. The honest answer is that this is a trade, not a free win, and the trade is worth stating plainly rather than claiming the safer design has no cost.

**Basis:**
- Automation bias happens in experts too and resists training: [Source: Parasuraman & Manzey 2010, Literature]
- Explanations increase acceptance of a recommendation "regardless of its correctness": [Source: Bansal et al. 2021, Literature]
- Forcing a person to decide before seeing a suggestion cuts over-reliance (64% to 48% on wrong answers) but is rated less preferred: [Source: Buçinca et al. 2021, Literature]
- A reply-suggestion tool raised novice agents' resolutions per hour by 34%, with minimal effect on experienced agents, and was adhered to only 38% of the time: [Source: Brynjolfsson, Li & Raymond 2023, Literature]

**Design note:** [Inferred] This is the clearest point where the case study should state its cost openly: hiding verdicts protects against automation bias, and may give up part of the speed gain a suggestion-based tool could offer novice agents. Say this in Limitations rather than claiming the safe design is strictly better in every way.

---

## Part 3. Guardrails and accountability

### Q8. Value ceilings and escalation rules: how should a reviewer see why a case was routed to approval?

**Answer:** As the specific rule that fired, not as a status label. "Routed to approval: order value above ceiling" tells the reviewer something they can act on. "Escalated" alone tells them nothing. Uber Eats already states its triggers this way in its own documentation, which is useful, because it means the pattern is provable rather than invented for this project.

**Basis:**
- Escalation triggers named explicitly ("not filed in a reasonable time frame", "high-value orders", "alcohol items", "first-time customers"): [Source: Uber Eats order errors, Official]
- A payout-threshold guardrail with escalation on breach: [Source: Fini refund audit log, Vendor]
- Swiggy's own escalation thresholds: [Not known publicly] (gap A7)

**Design note:** [Inferred] Use an illustrative, clearly-labelled ceiling since Swiggy's real number isn't public, and always show the rule name next to the routing decision, never just a flag.

---

### Q9. What should the audit record of a human decision contain? Should the reviewer give a reason before acting?

**Answer:** At minimum: which conditions were shown to the reviewer, what data version they were looking at, what the reviewer chose, and why, if they went against what the facts seemed to point toward. Requiring a short reason before the final action is a genuinely useful piece of friction. It's the one intervention in the research that's actually been tested and shown to reduce blind agreement, even though people don't enjoy it.

**Basis:**
- Audit log fields (policy version, data points, amount, action, timestamp): [Source: Fini refund audit log, Vendor]
- Making a person decide, or justify, before seeing or acting on a suggestion reduces over-reliance, at a cost to how much they like the process: [Source: Buçinca et al. 2021, Literature]

**Design note:** [Inferred] A short mandatory reason field on any deviation or final confirmation is supported by the one controlled experiment that actually measured this kind of friction. Expect agents to rate it as annoying; measure decision quality and consistency anyway, not just satisfaction.

---

### Q10. How should the screen differ for a new BPO agent compared with an experienced one?

**Answer:** The honest answer is that the research doesn't tell you to build two different screens. What it shows is that a help tool's benefit is concentrated in new agents, close to a third more resolutions per hour for novices, almost nothing for experienced agents. That argues for one screen that's genuinely easy to learn, rather than a stripped-down "beginner mode" and a separate "expert mode". If the facts and conditions are laid out clearly enough for a novice to use well, an experienced agent loses nothing by using the same screen faster.

**Basis:**
- Novice agents improved 34% with an assistive tool; experienced agents saw "minimal impact": [Source: Brynjolfsson, Li & Raymond 2023, Literature]
- Whether Swiggy differentiates its tooling by agent tenure today: [Not known publicly]

**Design note:** [Inferred] Design one screen for the novice case, since that's where the measured benefit concentrates, rather than building two tiers on a guess.

---

## Part 4. Swiggy specifics (held to the end)

### Q11. Do Swiggy agents see restaurant and delivery-partner history at decision time today?

**Answer:** Not known publicly. There's a real signal that the data exists somewhere inside Swiggy, since the Market Intelligence Dashboard tracks cancellation and complaint rates for restaurants, but that dashboard is explicitly a restaurant-facing growth tool, and nothing public says a support agent sees the same numbers, or any numbers, during a live refund decision. For delivery partners, there isn't even that much: no public source describes a delivery-partner history view at all. This is a confirmed gap, not something I can estimate around.

**Basis:**
- Market Intelligence Dashboard exists and tracks restaurant cancellations/complaints, but is restaurant-facing: [Source: cross-party evidence research file, citing Swiggy Catalyst blog, Official]
- No public source describes a delivery-partner history view: [Source: cross-party evidence research file, confirmed gap]
- Whether either reaches an agent's screen: [Not known publicly]

**Design note:** [Inferred] Stage 3's `[Assumed]` label on this exact point is the right call, and should stay. This interview does not resolve it; it confirms the gap is real and worth testing directly with agents in future work, not assuming either way.

---

### Q12. How does Swiggy weigh the three parties' histories in one decision?

**Answer:** Not known publicly, and I'd be cautious even to guess by analogy. Zomato is the only platform in this space that talks about weighing customer and rider history together at all, through its karma score, and even its own CEO is quoted saying the system "can never be fully right." That's a competitor's admission that this weighing is genuinely hard and contested, not a template to borrow for how Swiggy does it, since Swiggy's approach, if it has one, hasn't been described anywhere public.

**Basis:**
- Zomato's karma score covers both customers and riders, and its own CEO's quoted uncertainty about it ("can never be fully right"): [Source: deep research report, citing Exchange4media, Reported]
- Swiggy's own weighing logic: [Not known publicly]

**Design note:** [Inferred] The honest design response to this gap is exactly what the project already decided: show each party's history as separate dated facts, and let the reviewer do the weighing, rather than the interface claiming to know how Swiggy does it.

---

### Q13. What refund value can an agent approve without escalation?

**Answer:** Not known publicly. Swiggy's refund policy describes decisions as "case to case" and "at our sole discretion" without stating a number. DoorDash and Uber Eats both publish thresholds for their own merchant-side flows, which shows platforms in this exact industry are capable of publishing a number. Swiggy choosing not to doesn't tell us whether no threshold exists internally or whether it simply isn't public.

**Basis:**
- Swiggy's "case to case", "sole discretion" wording with no number: [Source: refund and blocking rules research file, citing Swiggy Refund Policy, Official]
- DoorDash's 20-minute/7-day thresholds and Uber Eats' value-based escalation, as comparable published examples: [Source: DoorDash missing items, Official] [Source: Uber Eats order errors, Official]
- Swiggy's actual number: [Not known publicly]

**Design note:** [Inferred] Use a clearly fictional, illustrative ceiling in any mockup or walkthrough, labelled as illustrative, never a number that could be mistaken for Swiggy's real policy.

---

### Q14. Where Swiggy's policy is silent (food claim window, evidence rule), what should the panel show?

**Answer:** Say so, directly, as its own row: "No published rule" or "Not specified by Swiggy policy." That's a fact about the policy, and it's one a human reviewer genuinely needs, since it tells them this is a point where their own judgement, not a rule, is doing the work. Hiding the gap, or quietly filling it with a number that looks official, would be worse than showing nothing.

**Basis:**
- Confirmed absence of a food-order claim window and evidence rule in Swiggy's published policy: [Source: refund and blocking rules research file, Official policy, absence confirmed by search]
- The Amex reason-code pattern this project is borrowing from has no equivalent gap, since Amex publishes every window: [Source: Amex chargeback reason codes, Official]

**Design note:** [Inferred] This single pattern, an explicit "No published rule" row, is probably the most defensible design decision in the whole panel, because it turns Swiggy's own ambiguity into a visible fact instead of papering over it.

---

## Part 5. Close

### Q15. What would you refuse to put on this screen?

**Answer:** Anything that predicts what the customer, the restaurant or the delivery partner intends, whether that's a fraud score, a value tier, a trust label, or a soft wording like "likely genuine." I'd also refuse a single merged "risk" number of any kind, since collapsing several facts into one score is exactly the move that turns a transparent screen into an opaque one, no matter how well-intentioned.

**Basis:**
- Project rule against value-tier and fraud-user flags: [Source: project rules, as given]
- Zomato's karma score as the real precedent for this exact risk: [Source: cross-party evidence research file, citing Outlook Business, Reported]
- Explanations and summaries make a conclusion more persuasive whether or not it's correct: [Source: Bansal et al. 2021, Literature]

**Design note:** [Inferred] This answer restates the project's own design rule rather than adding a new one, which is appropriate: the rule was already correct before this interview.

---

### Q16. If you had 20 minutes with five support agents, what would you test first?

**Answer:** Whether they can find the one fact that settles a case faster with this screen than with whatever they use today, on a handful of cases chosen specifically because the data conflicts, say the delivery partner's timestamp and the customer's complaint disagree. That's a sharper test than a smooth, typical case, because the typical case is exactly where any interface looks fine. I'd time it, count how many screens or lookups they need, and ask them to say out loud, before deciding, which single fact mattered most.

**Basis:**
- The literature consistently shows failures appear under load and on cases where a decision aid or the data itself is wrong, not on easy cases: [Source: Parasuraman & Manzey 2010, Literature] [Source: Buçinca et al. 2021, Literature]
- Testing metrics named earlier in this project (time to decision, lookups, consistency, override rate): [Source: deep research report]

**Design note:** [Inferred] Build at least one deliberately conflicting test case into the Testing stage's walkthrough, not only the clean illustrative cases used for the main demo.

---

## Verification Log

This transcript was checked twice: once inline while writing it, and once by an **independent agent** that had not seen the transcript being produced, working from the six source files directly (`swiggy-literature-review.md`, `swiggy-artifact-analysis.md`, `swiggy-gap-analysis.md`, and the three original research files). The independent check is the one that governs; it found two citation errors the inline check missed, both now corrected in the text above.

**Independent check results:** of 43 tagged `[Source: ...]` claims, 39 were SUPPORTED, 2 were PARTLY SUPPORTED, 0 were UNSUPPORTED (fabricated). All 9 `[Not known publicly]` tags were confirmed as genuine gaps, not dodges, each traceable to a named gap in the gap analysis (A1, A3, A4, A7, A9). No design note was found to smuggle in a verdict, score, or prediction about a customer, restaurant or delivery partner.

**The two citation errors found, now fixed:**
1. **Q3**, the Instamart AI-edited photo claim, was attributed to Business Standard. The deep research report actually cites it to **Business Today and The Logical Indian**. The fact itself was correct; only the named outlet was wrong. Corrected above.
2. **Q12**, the Zomato CEO quote "can never be fully right", was attributed to the cross-party evidence file citing India News Network. That file does not contain this quote (it has a different, untraceable quote the gap analysis already flags for replacement). The quote is correctly sourced to the **deep research report, citing Exchange4media**. Corrected above.

**No fabricated claims were found.** No answer invents a Swiggy-specific number, practice or quote. Every "Not known publicly" answer (Q1 Swiggy time-loss specifics, Q2 Swiggy's exact screen format, Q3 Swiggy's evidence rule, Q4 Swiggy's claim window, Q8 Swiggy's threshold, Q10 Swiggy's tenure practice, Q11-Q13 the three held-back Swiggy questions) correctly declines to guess.

**This transcript is cleared to cite.** The full verification table lives in `swiggy-expert-interview-verification.md`.
