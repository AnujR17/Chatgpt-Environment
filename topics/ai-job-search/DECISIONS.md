# Decisions

## 2026-11-10: Personal assistant with Codex/ChatGPT

The user linked `ai-job-search-dev/ai-job-search` and selected a personal
assistant using Codex/ChatGPT. Build in the existing topic repository and
checkout, with no new worktree or hosted site. Use the current agent for AI
work rather than adding a model service or another API key.

The reference README, license, agent pointer, application workflow and file
tree were inspected at commit `e9ab29dcc20b3d802356077b02898cd97db0d312`.
It provides a Claude-centered workflow and Denmark-focused search adapters.
Its reported hiring outcomes are author claims, not independent evidence.
The local implementation is original; no upstream code has been imported.

## 2026-11-10: Private records and explicit evidence

Use Python's standard library and SQLite. Keep the candidate profile,
source documents, generated packets, report and tracker in an ignored local
directory. Store stable fact IDs and candidate confirmation. Archive source
postings verbatim and freeze a profile per application.

Readiness requires completed drafts, a claim-to-fact review and hashes of
the reviewed sources and drafts. This is a structural gate, not proof of
truth or exhaustive grounding. Submissions remain manual; the tracker records
an application as sent only after the candidate confirms that action.

## Unknowns

No CV, target roles, country, authorization, compensation preferences or job
posting has been supplied. Do not infer them from username or timezone.
Choose market-specific search sources after onboarding. No additional app
connections, scheduled search, export service or hosting has been configured.
