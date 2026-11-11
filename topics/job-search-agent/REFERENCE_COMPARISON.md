# Reference comparison

Reference reviewed10November2026:
[ai-job-search-dev/ai-job-search](https://github.com/ai-job-search-dev/ai-job-search)
at `e9ab29dcc20b3d802356077b02898cd97db0d312`. Its README, license, agent
entry point and application command were inspected. Tests and hiring outcomes
were not independently reproduced. No upstream source was copied.

## Current status —11November2026

The user removed the application assistant. The dedicated page, application
workspace, model-generation API and Gateway dependency are gone. The existing
job board remains the canonical product: public design-role research, company
directory, source evidence, local tracking, profile, editable factual email
drafts, clipper import and backups. Old document fields are retained only for
backup compatibility; no assistant workflow is exposed.

The reference is a file-based agent workflow with profile setup, search,
ranking, tailored CV/letter drafting, separate review, PDF/layout/text checks,
interview preparation and outcomes. It has market-independent criteria plus
Danish and multi-market adapters. Those capabilities are reference context,
not claims that this board currently implements them.

| Area | Current board |
| --- | --- |
| Discovery | India/remote design-role research, company directory and source/pay/freshness caveats |
| Tracking | Stable IDs and browser-local stages, notes, follow-ups and assessments |
| Applications | Editable factual email template; manual sending and submission |
| Documents | No assistant generation, CV/letter workbench or PDF/ATS verification |
| Continuity | Existing browser storage and JSON backups; no cloud private-profile database |
| Integrations | Browser clipper and researched public-feed publication; no employer messaging |

The earlier `topic/ai-job-search` starter is a historical prototype, not a
second app to run or republish. Keep private applicant data out of public
research and preserve the existing board. Tests establish software behavior,
not better ranking, writing, ATS success or hiring probabilities.
