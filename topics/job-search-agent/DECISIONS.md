# Decisions

2026-10-23 — Current user instructions:

- Roles: UX designer, interaction designer and product designer internships. Include UI/UX only when responsibilities are relevant.
- Prioritise remote India. Consider Gujarat and places south of it, explicitly Pune, Hyderabad, Bengaluru, Chennai, Trivandrum, Goa, Mysore, Puducherry, Ooty, Visakhapatnam and Mumbai.
- Stipend: Gujarat ₹20k/month minimum; elsewhere ₹30k+, with ₹25k conditional by role. Remote ₹30k floor is an implementation assumption awaiting correction if needed.
- Search company careers, public job boards, LinkedIn, X and other accessible sources. Do not claim universal coverage.
- User will supply résumé and portfolio. No personal skills, degree, availability or prior employment inferred. Portfolio-scoped Mem0 lookup returned zero results.
- Build Kanban and Excel export; GitHub primary account AnujR17; deployment target Vercel. AnujR17 identity independently verified by GitHub API.

Implementation decisions:

- Initial version is static Vite/React with browser-local private progress and explicit JSON backups. Public feed contains job research only. Cross-device syncing requires a later authenticated datastore.
- Confirmed-pay labels use the original employer-stated lower bound. Aggregator salary claims and wide ranges reaching the threshold do not prove a match.
- New discoveries are not application history. All initial listings are Discovered; no fabricated applications or interviews.
- Daily GitHub workflow checks known public career sources and supported structured feeds. Broad social search remains a manual/API research step. Blocks and stale posts remain visible as limitations.
- No applications or recruiter messages sent. Drafting email is distinct from sending an application.

Access outcome: the verified AnujR17 integration denied createRepository. Reuse existing public AnujR17/Chatgpt-Environment on topic/job-search-agent, with Vercel root directory topics/job-search-agent/app. Main is unchanged. The nested optional GitHub cron workflow is prepared but inactive.


2026-10-24 — User correction and redesign:

- Explicitly shortlist from Indeed, Naukri and X as well as employer career pages and other sources; avoid a LinkedIn-only experience.
- Retain undisclosed-pay roles on hold. Salary reports and employer reputation can guide company research, but cannot be presented as current offer pay. Historical below-target pay signals must also be shown honestly.
- Separate company watchlist into editable suggested Dream / Workable / Possible categories. These are preference/fit suggestions, not hiring odds or confirmed vacancies.
- Include clearly marked junior/fresher alternatives alongside internships. Preserve monthly vs annual units.
- Default to Discover cards with newly researched roles first. Use Applications for saved/application stages and a separate Companies view; avoid an initial board dominated by empty columns.
- Preserve existing browser-local roles/profile/progress and old JSON backup compatibility. Company following/categories use an additional local storage key and travel in backups.

Research outcome:20 roles, including4 Indeed details and1 employer-linked Naukri route, plus2 X mirror-backed cross-posts attached to existing roles. Seven new roles,16 held for pay/details. Company watchlist17 entries. Naukri direct access is blocked and X originals403; both caveats remain visible. No applications were submitted. Daily task prompt updated to carry these rules and maintain/deploy the public role and company feeds.
