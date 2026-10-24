# Job search agent handoff

Updated 24 October 2026. Continue in the existing checkout on branch `topic/job-search-agent`.

## Live deployment

- URL: https://chatgpt-environment.vercel.app
- Existing GitHub repository: AnujR17/Chatgpt-Environment. Do not create another repository.
- Vercel project: chatgpt-environment, ID prj_o1CANE3Uj8jY3AWgGku9nV0qjqPg.
- Owner accountId verified: team_wbMCzPWEpuswtIa2AekWJJLh.
- Production deployment dpl_4Rc3WD6hypRNJrTVYTA2F3TPuJbL is READY, source commit 0c777b27d5d945266a3ed97eba5f2e8843f9adb5 on topic/job-search-agent.
- Root directory topics/job-search-agent/app; Vite; npm ci; npm run build; output dist; Node24.
- User initially imported main, which contains workspace docs and not the app. The existing Vercel project was corrected and the topic branch was deployed directly to production. Main was not modified or merged.
- The Vercel connection works using the exact project ID and default connection scope. Explicit teamId calls returned403; do not repeat team-scope probes or ask the user to reinstall/reconnect.
- HTTPS verification returned200 for the application shell and /data/jobs.json with13 researched leads. Deployment Protection was preserved.

## Product state

UX/interaction/product design internships. Prioritise remote India, then Gujarat/Maharashtra/Goa/southern India. Gujarat minimum INR20k/month; elsewhere INR30k+, INR25k conditional. Remote30k provisional. Research expanded to20 roles, including4 Indeed details,1 employer-linked Naukri route,2 X cross-post enrichments and company career sources. Seventeen company targets are in public/data/companies.json. Sixteen unknown-pay/detail-uncertain roles start on hold. Three roles retain employer-stated stipend matches. No applications submitted. No portfolio/resume inspected; do not infer applicant experience.

Private application stages/profile/notes are browser-local with JSON backup/restore, not cloud synced and not readable by the daily task. Public feed contains only job research. Collector initial run:15 sources,10 fetched,5 blocked. Nested GitHub cron is a prepared optional workflow and is not active on this topic branch.

## Scheduled search

Connected daily task remains enabled (ID6adb815b657c81919e216feb90a11041). Its prompt now includes deploying exact new listing-data commits to the existing production Vercel project and verifying READY plus the live feed. A topic-branch push alone is not proof production refreshed because Git production tracking was originally main. Do not merge main or create new projects/repos. Task cannot read browser-local application progress.

## Validation and limits

Local production build, model tests, collector tests and desktop/mobile browser smoke test passed. Public deployed HTML and JSON verified directly with trusted HTTPS. Chromium initially could not trust the session proxy CA; further live browser QA routes first-party requests through Python verified HTTPS rather than disabling TLS checks.

Prior portfolio-scoped Mem0 lookup returned no records. Previous Mem0 handoff save returned HTTP400 and was not retried. This GitHub handoff is the durable record.


## Redesigned app and research rules

- Discover is the default, with recent roles first, readable cards and source/location/pay/type filters. Applications holds the saved-role Kanban; Companies is a separate watchlist. Next actions and the profile remain available.
- Company categories Dream / Workable / Possible are editable suggestions, not hiring odds. Following and categories persist in browser localStorage and JSON backups. Existing progress keys and job IDs are preserved.
- payMin/payMax are current listing pay only. payBenchmark is separate historical/model context with original units, source and limitations. New undisclosed-pay roles use on_hold; reported below-target pay is disclosed rather than hidden.
- Techolution, F1studioz and Keyideas roles now have reported pay context, none treated as current stipend confirmation. F1studioz historical intern reports are below target; Possible tier. Dream company evidence is mostly weak/ambiguous and stays qualitative. No current vacancy is inferred from the watchlist.
- Naukri originals block automated checking; Keyideas employer page corroborates and links the application, whose slug is historical. X originals403; Wint/BThree mirrors enrich existing roles without duplicate cards and carry date/access caveats. Indeed gave4 accessible job-detail pages; additional official Zunderdog intern and fresher roles are included.
- Excel has20 role rows and17 company-watchlist rows. The daily task prompt now explicitly searches Indeed/Naukri/X, retains unknown-pay roles on hold, maintains companies.json and deploys updated feeds to the same project. No employer messages/applications sent.
- Local production build, model/collector tests, and expanded desktop/mobile browser workflow QA passed before deployment. Live deployment is READY; live browser verification follows the existing verified-HTTPS transport approach to respect session CA trust.


## Product-first directory and blacklist expansion, 24 October 2026

User requested a long company/studio list with product companies prioritised, careers/public contacts, published role requirements, personal criteria fit and a reversible company blacklist.

- Expanded companies.json to92 targets:58 product companies, plus studios/services. Forty role records include published openings, programs, indexed leads, senior team evidence and prior role research; these are not40 recommended internships. Dream23 / Workable47 / Possible22 are editable suggestions.
- jobs.json now28 roles, with8 new official-page internships/junior alternatives (project44, Juno, Gravity, Frappe, Ungrammary, Nonlinear, Octet UI and UIUX). All8 have undisclosed pay and start on_hold. Gravity explicitly permits remote India; Juno/project44/Nonlinear are office roles; Frappe/Ungrammary/Octet arrangements need confirmation. No new qualifying stipend was verified.
- Each directory company has a careers or public contact route. Published email addresses retain purpose and source. project44 email is accommodation-only, not an application inbox. Likely role families are inferred and labelled. Senior/program/index-only entries must not be promoted as confirmed internships.
- New CompanyDirectory.jsx has search, product/studio filter, role-evidence filter, category/follow controls, expandable careers/contact/source/role details, and per-role requirements checklist. Checklist states Met/Partly met/Gap/Unassessed plus private evidence; meter counts facts only and does not estimate hiring odds. Criteria include bonus/application steps as explicitly disclosed. No resume/portfolio reviewed; all initial personal fit is Unassessed.
- companyOverrides (existing design-jobs.companies.v1 key) now holds assessments, blacklisted boolean and optional private reason. Company aliases and normalised names match future roles. Blacklist hides Discover and active directory records; saved applications, history and next actions remain. Can add an exact company name before a feed entry exists, reverse any exclusion, and transfer all preferences in existing version1 JSON backups.
- Blacklist is browser-local. Scheduled task cannot read it or private evidence, so its digest cannot promise browser-specific filtering. No public blacklist/private criteria were seeded or committed.
- Added Company directory and Role requirements Excel sheets and static company-directory.csv. scripts/export_excel.py regenerates both workbook and CSV. Browser filtered CSV includes current private evidence/preferences only in that downloaded file. Public exports have Unassessed fit and no private data.
- sources.json now155 source entries. Naukri robots blocked; new X searches produced no verified new post. Existing2 X cross-post enrichments remain with prior caveats. Studio evidence includes official/employer social and Indeed; ProCreator reported5–15k stays below-target context; ZEUX initial training pay unclear.
- Daily task prompt expanded for directory schema, sourced requirements, contact-purpose preservation and blacklist/fit privacy limits; enabled schedule unchanged.
-12 model/data tests,5 collector tests and production build passed. Existing browser smoke and new company_check.py passed locally, including92/58 counts, evidence meter, source/CSV, blacklist persistence, preserved application, backup/restore, unblocking, custom exclusions and390px layout. Deployment verification follows after exact commit publication.


Deployment result: production dpl_5ViDw8AtKYnjakx5XSM3eug45Bkf READY from71b37226f50f5d9e87f301c54ab1102c4b78baf6. Live HTTPS returned200 for28 jobs,92 companies, CSV and Excel. Both original and company-specific browser workflows passed against the deployed site, including mobile, using93 verified HTTPS first-party requests through the session trusted-CA transport (TLS verification retained). No applications/employer messages sent. Resume/portfolio still not supplied. Existing repo/account/project preserved; main unchanged.


## Generic requirement-import support

Role details and company records share a requirement meter. Role details also support locally stored criteria for employers absent from the public directory. Backup restore merges company preferences and per-role criteria, preserving blacklist/reason, tier, following and unrelated criteria. A judgment for the identical criterion is replaced by the imported value. Application stages, notes and profile are unaffected by assessment-only imports.

Role lookup prefers stable job IDs, then exact titles, before a shared careers URL. This prevents two roles on one careers page from accidentally sharing a criterion record.

Production deployment dpl_C8uzR9mzmP47Jo1Y99Tyx4ycLW57 is READY from a21d8e0fc8e4bf0efe5426e935e8e114a1e7c57e. Thirteen model/data tests and production build passed. Local and live tests verify nested merge preservation, role/company shared meters, shared-URL role matching and mobile layout. Live checks retained TLS verification and recorded no browser errors. Test fixtures contain generic sample strings.

Public documentation records software behavior and public research only. Applicant documents, assessments and review metadata belong outside this repository. Browser-local records require the user to import a downloaded file using Export > Restore a backup; export a current backup first.


## Public source expansion

User requested broader use of remote/startup/YC/Who is hiring channels and asked why Indeed/Naukri coverage was small. Public research expanded to36 role leads,111 employer targets (73 product companies),224 individual source records and21 source-coverage records. Eight additional role leads include older YC/Indeed records explicitly held for current-intake verification, junior salary alternatives and public Indeed/company details. No new qualifying monthly internship stipend was verified. Applicant/private assessment data was not copied into this research update.

Source chips now distinguish YC / Work at a Startup, Wellfound, Remote boards, Hacker News and Cutshort. HN matching is tested before generic ycombinator-domain matching. Source coverage explains blocks, sampled/partial searches, zero suitable leads, expired originals and directory-only discovery. Individual source checks are collapsed by default. Indeed linked roles10 (including cross-posts); Naukri1 and still robots blocked. Startup maps/directories do not imply vacancies or employer health.

Annual USD/INR salary is displayed using advertisedCompensation, distinct from verified monthly INR payMin/payMax. SuperKalam metadata conflicts, so no numeric monthly stipend. The two YC roles retain2024 posting dates and older-listing warning. Ungrammary gets a below-target Cutshort report without changing primary verified pay or duplicating its card. Chiblu/project44/Zunderdog cross-posts enrich stable IDs.

Daily task prompt now covers the additional channels, source coverage records, original dates/units and truthful zero-result reporting, preserving its existing schedule and private context. Generic app/model/data tests, collector tests, build and local browser source/legacy/company/import flows passed. Production publication and live checks follow on this exact update.


Source-expansion production verification: dpl_4Rc3WD6hypRNJrTVYTA2F3TPuJbL READY from 0c777b27d5d945266a3ed97eba5f2e8843f9adb5. Live HTTPS returned200 with36 jobs,111 companies and21 coverage records. Live workbook verified36 internship/junior rows,224 source rows,21 coverage rows and111 company rows. Production source workflow passed desktop/mobile with26 verified HTTPS requests, including Indeed deduplication, older YC badges, annual USD/INR units, remote-board filters and access-limit reporting. Existing local application/company/import browser workflows,16 model/data tests,5 collector tests and production build passed. No applications/messages sent; private user data was not published.
