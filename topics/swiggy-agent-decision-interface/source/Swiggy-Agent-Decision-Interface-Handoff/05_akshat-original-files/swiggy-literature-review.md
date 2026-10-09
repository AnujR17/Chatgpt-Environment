---
name: swiggy-literature-review
description: Stage 4 Literature Review (#71) for the Swiggy Support Agent Decision Interface. Five HCI and economics papers on automation bias, overreliance, explanations, trust calibration and AI help in customer support, with citable findings and design implications.
researched: 2026-10-01
status: complete for 5 core papers; domain-specific dispute literature not covered
---

# Literature Review: Human Reliance on Decision Support

## 0. How to read this
- **Read depth** is stated per paper. "Full text (extracted)" means the paper PDF was opened and the relevant sections pulled with exact quotes. "Abstract only" means only the published abstract was read.
- Quotes are verbatim from the source. Everything tagged **[Inferred]** is our reasoning, not the paper's.
- Rule kept: nothing below is cited beyond what was actually read.

**Headline:** Five studies agree on one point: when a screen offers people an answer, they follow it even when it is wrong, and training, explanations and instructions do not reliably stop this. The one study of AI in real customer support shows big gains for new agents, but it measured reply suggestions, not decisions about who is at fault. This supports a panel that shows facts and conditions instead of verdicts, and it also names the cost of that choice.

---

## 1. Papers reviewed

| # | Paper | Read depth | Evidence type |
|---|---|---|---|
| L1 | Parasuraman, R. & Manzey, D. H. (2010). Complacency and bias in human use of automation: An attentional integration. *Human Factors*, 52(3), 381-410. | Abstract only | Literature review (many studies) |
| L2 | Lee, J. D. & See, K. A. (2004). Trust in automation: Designing for appropriate reliance. *Human Factors*, 46(1), 50-80. | Full text (extracted) | Literature review and conceptual model |
| L3 | Buçinca, Z., Malaya, M. B. & Gajos, K. Z. (2021). To trust or to think: Cognitive forcing functions can reduce overreliance on AI in AI-assisted decision-making. *Proc. ACM HCI (CSCW)*, 5(CSCW1). arXiv:2102.09692 | Full text (extracted) | Controlled experiment, N=199 |
| L4 | Bansal, G., Wu, T., Zhou, J., Fok, R., Nushi, B., Kamar, E., Ribeiro, M. T. & Weld, D. S. (2021). Does the whole exceed its parts? The effect of AI explanations on complementary team performance. *CHI '21*. arXiv:2006.14779 | Full text (extracted) | Controlled experiments, 3 tasks, 1,626 participants |
| L5 | Brynjolfsson, E., Li, D. & Raymond, L. R. (2023). Generative AI at work. NBER Working Paper 31161 (Apr 2023, rev. Nov 2023). | Full text (extracted), working-paper version | Field study, 5,179 support agents |

Note: L5 was later published in a journal (2025). Only the NBER working paper was read, so cite the working paper.

---

## 2. Findings by paper

### L1. Automation bias cannot be trained away
- "Automation complacency occurs under conditions of multiple-task load, when manual tasks compete with the automated task for the operator's attention."
- "Automation bias results in making both omission and commission errors when decision aids are imperfect."
- Automation bias "occurs in both naive and expert participants, cannot be prevented by training or instructions, and can affect decision making in individuals as well as in teams."
- Earlier note (deep research report, partial text): failure detection 82% with variable-reliability automation vs 33% with constant reliability. **Not re-read here; do not cite until the full paper is opened.**
- **[Inferred] For us:** support agents work under queue pressure, which is the multiple-task load the paper describes. A suggested "approve refund" will be followed when wrong (commission error). A missing flag will mean a problem goes unchecked (omission error). Agent training will not fix either.

### L2. Design for appropriate trust, not more trust
- Trust is "the attitude that an agent will help achieve an individual's goals in a situation characterized by uncertainty and vulnerability."
- **Calibration** is "the correspondence between a person's trust in the automation and the automation's capabilities." Overtrust leads to misuse; distrust leads to disuse.
- **Functional specificity**: trust is tied to "a particular component or aspect," not to the whole system.
- Design guidance (paraphrased from the paper's recommendations): show the automation's past performance; make its process and algorithms understandable; show what it can do in this specific situation; use concrete, clearly organised, consistent detail.
- **[Inferred] For us:** even a facts-only panel contains automation. The policy checklist computes "met / not met", the timeline places events against cutoffs, and data can be stale or wrong. Each row therefore needs its data source and timestamp so the agent can calibrate trust in that one row (functional specificity), not in "the system".

### L3. Making people think first reduces overreliance, but they dislike it
- Task: participants replaced the highest-carbohydrate ingredient in a meal photo, with AI help in some conditions.
- Three cognitive forcing designs:
  - **On demand:** the AI suggestion was hidden until the user clicked "See AI's suggestion".
  - **Update:** users decided first, then saw the AI's suggestion and could change their answer.
  - **Wait:** a 30-second delay before the suggestion appeared.
- Overreliance (agreement with the AI when the AI was wrong) on one measure: **48% with cognitive forcing vs 64% with simple explanations** (p = .003).
- "Cognitive forcing significantly reduced overreliance compared to the simple explainable AI approaches."
- Trade-off: "people assigned the least favorable subjective ratings to the designs that reduced the overreliance the most."
- When the AI was wrong, participants with **no AI help at all** were more accurate than either AI group.
- Benefits were larger for people higher in Need for Cognition.
- **[Inferred] For us:** two direct carry-overs:
  1. A **"reason required" step before deviating or confirming** is a cognitive forcing function and is supported.
  2. Agents will likely rate such friction lower. Testing must measure decision quality and time, not only preference, or the safer design will lose on "liking".

### L4. Explanations make people accept AI answers, right or wrong
- 1,626 participants across three tasks (beer review sentiment, Amazon book review sentiment, LSAT questions), with an AI about as accurate as the humans.
- "Explanations increased the chance that humans will accept the AI's recommendation, regardless of its correctness."
- Explaining the top prediction "lead to better accuracy when the AI recommendation was correct but worse when the AI was incorrect."
- Authors' guidance: "Explanations should be informative, instead of just convincing."
- **[Inferred] For us:** a refund verdict with a neat justification ("Approve: customer has good history, restaurant has complaints") is the riskiest pattern. It persuades whether or not it is right. Showing the underlying facts, with no verdict, is the "informative, not convincing" option.

### L5. AI help in real support work: big gains for new agents
- Setting: 5,179 support agents at a Fortune 500 enterprise software firm, mostly in the Philippines.
- The tool gave real-time reply suggestions and links to internal documentation.
- Resolutions per hour up 13.8% with full controls ("increases RPH by 0.30 chats or 13.8%").
- "A 34% improvement for novice and low-skilled workers but with minimal impact on experienced and highly skilled workers."
- Agents under 1 month tenure improved by about 46%. "Treated agents with two months of tenure perform just as well as untreated agents with more than six months of tenure."
- Customer requests to speak to a manager fell by almost 25%. Attrition among newer agents fell by about 40%.
- Top-skilled agents saw "small but statistically significant decreases in resolution rates and customer satisfaction."
- Agents ignored most suggestions: "The average adherence rate is 38%."
- **[Inferred] For us:**
  - Strongest real-world support for helping novice BPO agents, who are likely Swiggy's workforce.
  - The tool helped with **what to say** (replies, documents), not **who is at fault**. Its gains cannot be assumed for refund decisions.
  - Our panel deliberately gives up verdicts. We may therefore lose part of this novice speed gain. That is a trade-off to state openly, not hide.

---

## 3. Synthesis

### 3a. What the literature agrees on
| Theme | L1 | L2 | L3 | L4 | L5 | Strength |
|---|---|---|---|---|---|---|
| People follow suggestions even when wrong | Yes | Yes (misuse) | Yes (64%) | Yes | Partly (38% adherence) | Strong |
| Training and instructions do not fix it | Yes | n/a | n/a | n/a | n/a | One review, many studies |
| Explanations can make it worse | n/a | n/a | Yes | Yes | n/a | Two experiments |
| Forcing people to engage first helps | n/a | Implied (manual engagement) | Yes | n/a | n/a | One experiment |
| Trust should be calibrated per component | n/a | Yes | n/a | n/a | n/a | Conceptual |
| Assistance helps novices most | n/a | n/a | n/a | n/a | Yes | One large field study |

### 3b. Design implications (each traced to a paper)
1. **No verdicts, no "approve" badge** (L1, L4). A recommendation will be followed under load, and explaining it makes acceptance stronger.
2. **Every computed row shows its source and time** (L2). The checklist itself is automation; trust must be calibrated per row.
3. **Agent records a reason before final action** (L3). Cognitive forcing reduces overreliance.
4. **Fact retrieval, not reply writing or adjudication, is where assistance is safest** (L5 plus L1). Help agents find facts faster; leave the judgement to them.
5. **Test for accuracy on cases where the data is wrong**, not only on typical cases (L1, L3, L4). Include deliberately conflicting cases in the walkthrough.
6. **Expect friction to score low on preference** (L3). Report time and accuracy alongside satisfaction.

### 3c. Tensions to state in the case study
- **Speed vs safety.** L5 shows suggestions speed up novices; L1, L3 and L4 show suggestions cause errors when wrong. Our panel picks safety and may give up some speed.
- **Facts are not neutral either.** Choosing which facts to show, and in what order, still steers the agent (L2). "No verdict" reduces this bias but does not remove it.
- **Friction vs adoption.** The design that protects decisions best is the one people like least (L3).

---

## 4. Limits of this review
- None of the five papers studies refund disputes, chargebacks or three-party fault decisions. All findings are carried over from nearby tasks.
- L1 was read at abstract level only. The 82% vs 33% figure must not be cited until the full paper is opened.
- L3 and L4 use lab tasks with crowd workers, not trained support staff under real queues.
- L5 is the working-paper version, and its firm is enterprise software, not food delivery.
- Not covered (optional, if time allows): the Management Science paper on two-sided platform disputes ("Improving Dispute Resolution in Two-Sided Platforms: The Case of Review Blackmail", 2022), and Goddard et al. (2012) systematic review of automation bias.

---

## Sources
- L1 Parasuraman & Manzey (2010): https://journals.sagepub.com/doi/10.1177/0018720810376055
- L2 Lee & See (2004): https://scispace.com/pdf/trust-in-automation-designing-for-appropriate-reliance-2uiy4o89ga.pdf (journal record: https://www.researchgate.net/publication/8555432_Trust_in_Automation_Designing_for_Appropriate_Reliance)
- L3 Buçinca, Malaya & Gajos (2021): https://arxiv.org/abs/2102.09692
- L4 Bansal et al. (2021): https://arxiv.org/abs/2006.14779
- L5 Brynjolfsson, Li & Raymond (2023): https://www.nber.org/papers/w31161 (PDF: https://www.nber.org/system/files/working_papers/w31161/w31161.pdf)
