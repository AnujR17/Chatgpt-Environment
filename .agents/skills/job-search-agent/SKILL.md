---
name: job-search-agent
description: Maintain the existing design job board and its public research feed, preserving browser-local progress and evidence.
---

# Existing design job board

Use `topics/job-search-agent/app` on `topic/job-search-agent` in
`AnujR17/Chatgpt-Environment`. Read the app README and topic HANDOFF first.
The live board is `https://chatgpt-environment.vercel.app`; keep the existing
Vercel project and deployment protection. Do not create another tracker,
repository or deployment project or merge main for this work.

## Assistant removed

The user removed the application assistant on11November2026. Its page,
navigation, application workspace, server/API generation, AI dependency and
Gateway checks are removed. Do not restore it or require Gateway activation
or approval of that removed feature to publish daily job research.
Old `/assistant` links redirect to the board. The existing factual email draft
remains a local editable template; it sends no model request or application.

The `applicationKit` data helper is retained only for compatibility with older
browser backups. Preserve existing saved document fields, application stages,
notes, profile, company overrides, blacklist and requirement assessments.
Do not delete or publish private records while removing a feature. Legacy
saved documents can remain in JSON backups; there is no document-generation UI.

## Research and publication

Follow the latest user instructions for roles, geography, stipend floors,
source coverage, exclusions and privacy. Current instructions take precedence
over earlier dated criteria. Read actual source evidence; never invent an open
role, pay period, posting date, current intake or applicant fit. Unknown-pay
roles may remain on hold with a useful next action. Keep salary benchmarks
separate from current advertised compensation and preserve original units.

Preserve role/company/requirement IDs, sources, exclusions and browser-local
state compatibility. Never run seed.py as a refresh. Regenerate supported
research workbook and directory exports when the feed changes. Do not commit
CVs, private profile, backups, contact details, assessments or secrets. Private
workspace files belong in the ignored `topics/job-search-agent/private/`.
No applications or employer messages without explicit user authorization.

The authorized daily maintenance workflow publishes exact researched commits
from `topic/job-search-agent` to production in existing Vercel project
`prj_o1CANE3Uj8jY3AWgGku9nV0qjqPg`, root `topics/job-search-agent/app`, Vite,
`npm ci`, `npm run build`, output `dist`, Node24. Use the default authenticated
connection scope; do not add teamId. Preserve preview isolation and protection.
A branch push is not publication: verify READY, exact commit/ref/project,
production alias and live feed/export bytes before claiming refresh. Do not
redeploy for documentation-only changes or unchanged feeds. If access fails,
finish authorized research/checks and report the specific failure honestly.

Read `topics/job-search-agent/REFERENCE_COMPARISON.md` for the earlier reference
review. Software tests do not establish better hiring outcomes or writing.
