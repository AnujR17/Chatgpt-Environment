# Reference comparison and integration

Reviewed 10 November 2026. Reference:
[ai-job-search-dev/ai-job-search](https://github.com/ai-job-search-dev/ai-job-search)
at `e9ab29dcc20b3d802356077b02898cd97db0d312`. Existing board baseline:
`f235c4d` on `topic/job-search-agent`. The reference README, license, agent
entry point and application command were inspected. Its tests and reported
hiring outcomes were not independently reproduced.

## What the reference does

It is an agent workflow that runs around local files, primarily in Claude Code.
Setup builds a career profile; search finds roles; rank evaluates and shortlists;
apply evaluates fit, drafts a CV/letter, runs a separate reviewer, revises,
compiles PDFs and checks their layout and extracted text. Interview/outcome
commands use the submitted materials and feedback. It also documents learning
plans, extensible templates and portals, an offline report, and optional Gmail
and Notion workflows. Core criteria are market independent. Its four Danish
portal examples are joined by multi-market LinkedIn and Freehire adapters;
it is inaccurate to describe the whole reference as Denmark-only.

## Current differences

| Area | Existing board before this integration | Reference workflow | Integrated change / remaining gap |
| --- | --- | --- | --- |
| Personal UX/design discovery | India/remote research, role feed, company directory, source coverage, pay caveats, local clipper | Portable portal search and custom adapters | Preserve the existing market-specific discovery and evidence. No search refresh was performed by this change. |
| Application preparation | Generic email built from the profile; draft edits were lost when the drawer closed | Tailored CV and letter with factual review | Added a private role-specific Codex request/result round trip, persisted email drafts and an application document workspace. The chat does AI writing; no model service is installed in the board. |
| Evidence | Source-backed role requirements and browser-local Met/Partly/Gap checklists | Profile-grounded factual and fit evaluation | Export candidate-confirmed fact IDs and full posting; validate returned quotes and IDs. Validation cannot establish truth or exhaustive coverage. |
| Continuity | Stable researched IDs and private localStorage overrides/backups | Local tracker and application archives | Requests/results retain the existing board role ID. Drafts and frozen submitted copies use the existing overrides and JSON backup; no parallel tracker or cloud private-data store. |
| Review | No application-specific review record | Separate drafter/reviewer with revision | A reviewed result contract checks role/request/source identity and cited facts. Draft edits invalidate its review. Actual review quality still needs a real application pilot. |
| Interview prep | Interview date/notes | Role-specific packs and mock interviews based on submitted documents | Workspace stores an imported prep pack and submitted documents; chat skill handles preparation. No interview is booked or conducted by the static page. |
| Final files | Editable email text | Compiled, visually checked PDF plus text-layer/keyword review | Markdown document export added. PDF/DOCX generation, layout inspection and text-layer checks remain gaps. |
| Follow-up and feedback | User-entered next action and due date | Outcome history, silence follow-up drafts and calibration | Existing dates and stages preserved. Structured feedback-driven recalibration and automated follow-up suggestions remain future work. |
| Integrations | Browser clipper, backups, public research updates | Documented optional Gmail/Notion workflows | No email/Notion connection or permissions added. Sending and submission remain manual. |

The smaller `topic/ai-job-search` starter remains a historical prototype. Its
source/profile snapshots and evidence-review ideas are now adapted to the
existing board's data model. The board is the canonical product. No upstream
source code was copied; retain the reference's MIT notice if copying code later.

## How to use the integration

1. On the board, open a role and choose **Prepare with Codex**. Existing profile
   information stays in the same browser; no new account or onboarding store.
2. Paste the complete job description, review your saved facts, confirm them and
   download the request. It includes contact links and confirmed experience,
   but excludes notes, blacklists, assessment judgments and other applications.
3. Attach the request in Codex and ask it to prepare the application. Alternatively,
   copy the request from the board. The repository skill specifies evaluation,
   tailoring, interview prep and the factual-review response format.
4. Import the returned JSON in the same role. Wrong-role, obsolete or malformed
   results are rejected before any update. Source/profile changes require a new
   request. Imported text is editable; editing removes the previous review.
5. Download documents or the application kit. After submitting externally, save
   the exact submitted copy. Later working edits leave it unchanged. Change the
   application stage yourself after the real event. JSON backup includes it all.

The page makes no model call or employer submission. This is a working handoff
through a chosen chat, not automatic synchronization with a cloud agent. The
agent cannot read your existing browser-local state until you explicitly share
an export. Public research files stay unchanged by this integration.

## What would establish better results

Current verification establishes software behavior, not better hiring outcomes.
For a fair writing/ranking comparison, use the same candidate-confirmed profile
and five real postings, including a strong fit, adjacent fit, mandatory-eligibility
gap, unknown pay and an older listing. Compare unsupported factual claims,
missed mandatory requirements, whether unknowns remain visible, useful tailoring,
source/date fidelity and time needed for candidate review. These are proposed
measures; no baseline, uplift or hiring-probability claim has been established.

The next useful extensions are verified PDF/text extraction, outcome and
follow-up calibration, and source adapters chosen for real coverage gaps.
Prioritize them after a real request-to-reviewed-application pilot, rather than
adding another scraper or a numerical fit score without evidence.
