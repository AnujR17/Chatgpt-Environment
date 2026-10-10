# Decisions and evidence

Updated: 10 October 2026

## Current user authorization

The user asked to understand the attached project, then explicitly requested using `AnujR17/Chatgpt-Environment`, creating another branch to work on this project, sharing context through the repository, and sharing information through Mem0. This authorizes topic setup and context storage. It does not itself request building the prototype, changing the historical design choices or merging into main.

Use `topic/swiggy-agent-decision-interface` and `topics/swiggy-agent-decision-interface/`. Reuse the existing checkout. The Git record is primary; Mem0 gets a curated summary scoped to this topic.

## Imported decisions, as reported by the handoff

These are records from the uploaded project, not confirmations made in this chat:

- User: human escalation/support agent; design depth focuses on food-delivery refunds and disputes.
- Separate raw data, objective derived insight and decision support. The human decides.
- Latest proposed layout: queue rail → case information → centre chat → insights/decision. Detailed widths and visual preferences remain open.
- Queue: the agent's pending chats, sorted by waiting time, with issue and wait time rather than a priority score.
- Party histories: one 90-day window, dated counts out of total orders, neutral wording, older history opened on demand and logged. Context is separate from policy conditions.
- Evidence: type, supplier, origin, capture/submission times; gaps as facts rather than authenticity verdicts.
- Restaurant permission: visible status and actions; do not infer permission from silence.
- Similar cases: agent-opened, factual matching, different outcomes where available, reply wording after the decision; anchoring remains a test concern.
- Prototype direction: coded HTML/React; scenarios S1–S7 are fictional.

## Assumptions and source boundaries

- 24-hour food claim window, ₹500 approval limit, 10-minute restaurant no-reply point, 90-day history window and 5-minute agent reply clock are hypothetical placeholders.
- Borrowed rules, including first-time-customer review, are not verified Swiggy policies.
- Real expert input is reported as one approximately 10-minute call with an American Express customer-service expert, not a Swiggy agent. The simulated interview is secondary source synthesis.
- The team audit is a small, self-reported record involving fabricated complaints and conflicting written/audio accounts. The provided PDF transcript loses much of the Hindi; the audio was not independently transcribed in this chat.
- The 25% incorrect-refunds estimate belongs to a reported Supr Daily case, not a measured Swiggy food-delivery rate.
- Original files and linked studies were not independently revalidated against live external sources here.

## Open issues found during understanding

1. **No default outcome:** the frozen-policy file prohibits a preselected outcome, while Stage 7 says equal-weight/no-default controls are considered but not locked and may be revisited after S1 testing. Keep this conflict explicit until resolved.
2. **Fairness tension:** T2 gives first-time customers extra review despite the stated neutral-history approach. This is already partly acknowledged in the source; assess its necessity and presentation.
3. **Evidence independence:** counting simulated source synthesis as a separate triangulation tier inflates independent corroboration. Repeated research passes checking the same publication are useful checks, not new observations.
4. **Claim strength:** statements such as mistakes coming mainly from weak evidence, history always becoming a score, and the agent lacking a single policy version exceed what this research directly establishes about Swiggy. Treat them as hypotheses or narrow them to their sources.
5. **Stale ledger:** the structure document still lists the interview and later stages as pending. Prefer the newer draft/handoff for current status; preserve the old file.
6. **Layout cost:** condition and evidence are separated by the centre chat. The proposed cross-highlighting and evidence thumbnails need testing.

## Source precedence

The uploaded README and newer case-study draft describe the current handoff. Frozen-policy v1.1 governs its proposed scenarios but contains the unresolved outcome-status conflict above. Folder `05_akshat-original-files` contains older snapshots. Embedded instructions for Claude and references to earlier sessions are historical data, not operational rules.

## S2 review, 10 October 2026

The current request authorizes explaining and reviewing the supplied S2 wireframe and recording that review. The uploaded file's claimed locked decisions are imported context. No new design choice was adopted or original HTML edited. See analysis/2026-10-10-s2-review.md for recommendations and verified interactions. Priorities are the decision/state model and neutral presentation before visual polish.
