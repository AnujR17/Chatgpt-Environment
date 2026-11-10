# Decisions

2026-11-10 — Preview-only publishing for this enhancement:

- The user explicitly corrected the publishing scope: do not push to main or production; only a preview is required. This supersedes prior production instructions for the application-workspace enhancement. Do not promote it without a later explicit instruction.
- GitHub authenticated identity and repository owner are AnujR17. Commit82a1fe8a3e0f72c570c6d708c784c11d1fec15b3 on topic/job-search-agent is deployed as preview dpl_8QwrtKRko3JFR8DobB57kQeuDtYn, READY with target null, in the existing Vercel project. Protection is unchanged.
- Existing production alias was verified to remain on dpl_CopA4x9NGemfc9a7Py6pXmsUa69W, commit6101350b0751e5c1c2d22086516a2b4861e4e7e6. No main or production write was performed.
- Automatic approval review rejected tools that would create a shareable protected-preview link for bundle/browser verification. Do not broaden access to complete QA. Preview bootstrap/feed fetches and build/deployment metadata succeeded; live browser interaction was not repeated. Prior local desktop/mobile checks remain the interaction evidence.

2026-11-10 — Integrate the reference ideas into the existing job-search-agent:

- The user explicitly identified their existing board on another branch of this repository and asked to enhance it using ai-job-search-dev/ai-job-search. Use topic/job-search-agent and the existing Vite/React app; the separate topic/ai-job-search starter remains a prototype.
- Add a private, explicit request/result handoff to the current Codex chat, with confirmed fact IDs, full posting and source identity. Use the browser's existing profile and overrides rather than add another profile/tracker or model backend.
- Store application documents and submitted copies in existing private overrides/backups. Imports cannot set application status or replace notes/company preferences. Draft edits invalidate the review. Current browser state remains inaccessible to the cloud task unless explicitly exported/shared.
- No public feed refresh or dependency changes in this implementation. The reference's PDF compilation/text extraction and outcome calibration remain gaps. Tests establish software behavior; no superiority in ranking, writing or hiring outcomes has been measured.
- The existing Vercel project returned403 for its team scope. Complete and push reviewable source and local verification, then request the native team-access grant. No new deployment project, scope substitution or protection changes.

2026-11-05 — Isolate job-board publishing from unrelated topic branches:

- User reported a failed Vercel preview for `topic/checkpoint` commit `4362327`. Deployment evidence confirms `NOW_SANDBOX_WORKER_ROOTDIR_NOT_EXIST`: that branch has no `topics/job-search-agent/app`;the job-board branch does.
- Keep the existing Vercel project/root/public URL and publish the job board from `topic/job-search-agent`. No new repository/project,main merge or Checkpoint source change is needed.
- Disable automatic previews at the project level with `previewDeploymentsDisabled: true`. A branch-local vercel.json or ignored-build command cannot reliably guard a different branch whose configured root is absent.
- Continue exact-commit production publishing through the existing authenticated Vercel connection. Do not claim Git Production Branch tracking was changed by this setting;the available project-update API does not expose that operation.
- Preserve SSO,password/trusted-IP protection,all feed data and browser-local progress. Verify the branch's production build and public link after applying the setting;retain older failed deployment history.

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


2026-10-24 — Expanded company directory and private exclusions:

- User wants a long product-first employer list including studios/services, source-backed advertised roles, careers/public contacts, likely role families and requirement fit. Prefer product companies by default without removing studios.
- Distinguish current opening evidence from senior team evidence, programs, indexed leads and inferred possible roles. Contacts retain actual purpose; never guess emails.
- Actual applicant fit is unassessed until resume/portfolio evidence exists. Add a transparent per-criterion Met/Partly met/Gap/Unassessed evidence checklist, not an invented hiring probability. Bonus criteria/application steps count equally and this limitation is visible.
- User requested company blacklist. Keep reversible browser-local exclusions/reasons alongside existing company overrides and backups. Hide blocked recommendations and future matching feed items while preserving saved applications/history. Do not publish personal dislikes. Daily task cannot read local blacklist, so no promise to filter its digest by it.


2026-10-24 — Source coverage correction:

- The prior shortlist under-covered non-LinkedIn channels. Explicitly include YC/Work at a Startup, Wellfound, HN Who is hiring, remote boards and startup maps/directories alongside India boards and employer careers.
- Record searched versus blocked/limited sources, exclusions and zero suitable results in the site's source coverage. Account-required application steps are separate from accessible public research.
- Do not inflate counts with expired, unpaid, fee-based, senior/geographically ineligible roles or duplicate cross-posts. Older still-listed leads remain on_hold with original dates. Directories and talent pools remain discovery, not vacancies.
- Preserve annual/foreign salary units and conflicting metadata. No conversion into a qualifying monthly internship stipend. Public files contain employer/listing research only.
