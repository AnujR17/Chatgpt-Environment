# Job search agent handoff

Updated 24 October 2026. Continue in the existing checkout on branch `topic/job-search-agent`.

## Live deployment

- URL: https://chatgpt-environment.vercel.app
- Existing GitHub repository: AnujR17/Chatgpt-Environment. Do not create another repository.
- Vercel project: chatgpt-environment, ID prj_o1CANE3Uj8jY3AWgGku9nV0qjqPg.
- Owner accountId verified: team_wbMCzPWEpuswtIa2AekWJJLh.
- Production deployment dpl_JCoWzatBVkPpPXTFt1YRgbn6qTPm is READY, source commit 1b56d21f6adf2702771646b3ccb82e2cdaf74229 on topic/job-search-agent.
- Root directory topics/job-search-agent/app; Vite; npm ci; npm run build; output dist; Node24.
- User initially imported main, which contains workspace docs and not the app. The existing Vercel project was corrected and the topic branch was deployed directly to production. Main was not modified or merged.
- The Vercel connection works using the exact project ID and default connection scope. Explicit teamId calls returned403; do not repeat team-scope probes or ask the user to reinstall/reconnect.
- HTTPS verification returned200 for the application shell and /data/jobs.json with13 researched leads. Deployment Protection was preserved.

## Product state

UX/interaction/product design internships. Prioritise remote India, then Gujarat/Maharashtra/Goa/southern India. Gujarat minimum INR20k/month; elsewhere INR30k+, INR25k conditional. Remote30k provisional. Initial13 leads include3 employer-stated stipend matches. No applications submitted. No portfolio/resume inspected; do not infer applicant experience.

Private application stages/profile/notes are browser-local with JSON backup/restore, not cloud synced and not readable by the daily task. Public feed contains only job research. Collector initial run:15 sources,10 fetched,5 blocked. Nested GitHub cron is a prepared optional workflow and is not active on this topic branch.

## Scheduled search

Connected daily task remains enabled (ID6adb815b657c81919e216feb90a11041). Its prompt now includes deploying exact new listing-data commits to the existing production Vercel project and verifying READY plus the live feed. A topic-branch push alone is not proof production refreshed because Git production tracking was originally main. Do not merge main or create new projects/repos. Task cannot read browser-local application progress.

## Validation and limits

Local production build, model tests, collector tests and desktop/mobile browser smoke test passed. Public deployed HTML and JSON verified directly with trusted HTTPS. Chromium initially could not trust the session proxy CA; further live browser QA routes first-party requests through Python verified HTTPS rather than disabling TLS checks.

Prior portfolio-scoped Mem0 lookup returned no records. Previous Mem0 handoff save returned HTTP400 and was not retried. This GitHub handoff is the durable record.
