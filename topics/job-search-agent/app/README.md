# Design internship tracker

Live board: https://chatgpt-environment.vercel.app

Production is READY from the board branch in the existing Vercel project `chatgpt-environment`.

Personal internship discovery and application Kanban for Anuj. Primary GitHub owner: **AnujR17**. Deployment target: **Vercel**.

## Included

- 61 retained role records (59 active,2 archived), updated27 October2026. Seven new internships and one junior alternative stay on hold for compensation/intake details. Sources include employer careers, Indeed, an employer-linked Naukri route and caveated public cross-posts.
- Separate employer-confirmed pay, conditional pay and unconfirmed stipend labels. Uses the **minimum** advertised stipend, not the maximum.
- Remote India first; Gujarat, Maharashtra, Goa and southern India considered. Gujarat minimum ₹20,000/month; elsewhere ₹30,000, with ₹25,000 considered individually. A ₹30,000 remote minimum is provisional.
- Discover card/list views with platform, role type, location and pay-evidence filters; a separate application Kanban; on-hold review; notes, deadlines and interviews. New roles appear first by default.
- Separate company directory with153 researched targets grouped into editable Dream, Workable and Possible suggestions. Following/categories stay browser-local and are included in JSON backups.
- Historical company pay reports include original units, sources and limitations. They never count as a current role’s confirmed stipend. Undisclosed-pay roles stay on hold.
- Local application profile and editable factual email draft. No automatic submission or email sending.
- Current-board CSV export (opens in Excel), a researched-listings `.xlsx`, and JSON backup/restore for personal updates.
- Source evidence, exclusions, freshness caveats and a collection report.

## Run and check

```sh
npm ci
npm run dev
npm run build
npm test
python -m unittest discover -s tests -p 'test_*.py'
```

Python 3.12+ and `openpyxl==3.1.5` are used for collection/export. `collect.py` uses only the Python standard library.

```sh
python scripts/collect.py
python scripts/export_excel.py
```

`scripts/seed.py` recreates the initial researched snapshot. **Do not run it as a refresh**, because it resets collected source state.

## Collection and daily updates

An optional standalone-repository GitHub workflow is included at `.github/workflows/collect-jobs.yml`, with a **03:30 UTC / 09:00 IST daily** schedule. It is **not active** in this monorepo subdirectory/topic branch; GitHub scheduled workflows must live on the default branch. No main-branch changes were made. The connected daily search task is enabled and separate from this optional workflow. It checks configured public source pages, respects robots policy, records blocks/errors, detects visible content changes, and discovers relevant JobPosting JSON-LD and Lever API candidates. GitHub schedules can be delayed. It does not scrape every job board or social feed.

New supported candidates enter `public/data/review-queue.json` and appear on the board with pay unconfirmed. Previously known jobs are deduplicated by employer/title. Personal application progress is never overwritten by feed refreshes.

The initial research used company careers, employer LinkedIn listings/posts and public job boards. X was searched, but no qualifying original post was independently verified. A connected **daily search task is enabled**, including public LinkedIn/X search and job-board/company research. It can update this branch’s public feed through the connected GitHub integration. Broad coverage still depends on accessible sources; restricted pages are flagged for manual review. No CAPTCHA bypass is implemented.

A page fetch confirms only that content could be fetched. It does not reconfirm pay, employment terms or current recruiting. `checkedAt` is the manual research date; `lastPageFetched` is the collector observation. Original posting dates and discovery dates are distinct. Changed pages need review; personal application stages are never automatically closed.

Each run produces `public/data/collection-report.md` and an updated Excel workbook. Once the Vercel Git integration is connected to this production branch, public data commits can trigger deployment. The optional workflow summary is a source-health digest; the enabled daily task returns a job-search digest. Email/WhatsApp delivery is not configured.

## Deploy to Vercel

Import **AnujR17/Chatgpt-Environment**, use branch **topic/job-search-agent**, set root directory **topics/job-search-agent/app**, framework **Vite**, build command `npm run build`, output directory `dist`. Set the project production branch to `topic/job-search-agent`. No runtime secrets are needed for this version. `vercel.json` includes the configuration.

The existing source repository is public. Only public listing research and application source are committed; personal profile and progress stay browser-local. The Vercel deployment exposes only the researched job feed and application shell. If deployed without Vercel protection, anyone with its URL can read these public job leads. `noindex` is a search-engine hint, not authentication.

## Privacy and persistence

Application profile, notes, stages and interview information live in **localStorage on the current browser/origin**, not in GitHub or a cloud database. They will not automatically sync across devices, deployment domains or browsers, and can be lost if browser storage is cleared. Use JSON backup before switching domains/devices. CSV exports reflect current browser state; the static Excel workbook reflects the research feed only.

Do not commit résumé files, personal profile data, credentials or browser backups. A cloud database with authentication can be added later if cross-device progress is needed. There is no public write endpoint.

## Application readiness

- ShramikSathi and BThree publish an application email, so drafts can be prepared without browser form automation.
- Hevo's public Lever form appears suitable for assisted filling once accurate profile/résumé information is supplied. Submission rules and CAPTCHA remain unverified.
- LinkedIn applications need a signed-in user session. Google/third-party forms need inspection of their actual requirements.
- No applications have been submitted. No employer has been contacted. No application is marked applied until the user records submission.

## Current top pay matches

| Employer | Role | Arrangement | Employer-stated stipend |
| --- | --- | --- | --- |
| ShramikSathi | UI/UX Design Intern | Remote India | ₹30,000/month |
| Menstrupedia | UX Design Intern | Ahmedabad | ₹25,000–₹30,000/month |
| More Retail | Product Design Intern | Bengaluru | ₹35,000/month |

Open each board card for the original source and requirements. No portfolio, degree, availability or prior work has been assumed. The topic-scoped Mem0 lookup for portfolio context returned no records.

## Access limitations

The GitHub identity is AnujR17, but repository creation was denied by the integration. The app therefore uses a dedicated branch in the existing repository. Vercel is now connected and the existing project is deployed at https://chatgpt-environment.vercel.app. The explicit teamId selector returned403, while operations on the verified project through the default connection scope succeeded.

Production was deployed directly from topic/job-search-agent without merging main. The daily search task is configured to deploy exact future listing-data commits to this same project and verify the live feed. A branch push alone should not be reported as a production refresh.

## 24 October redesign and broader research

Discover → review/save a role → Applications → next action is the main workflow. Company targets remain separate from vacancies and user-received offers. Suggested categories are editable and are not hiring probabilities.

The source filters include Indeed, Naukri and X. Indeed supplied four accessible job-detail pages. Keyideas’s employer page links an older Naukri application route; Naukri itself blocks automated inspection, so current route activity is unconfirmed. Wint and BThree X originals returned403; mirrors supplied content, with original URLs, access caveats and derived-date limits recorded as additionalSources. Cross-posts are deduplicated rather than counted as new jobs. Known expired/unpaid/removed listings remain in exclusions.

Company salary reports include Glassdoor evidence for Tekion, Scaler, Lenskart, Rapido, Techolution, F1studioz and other targets. Weak or geographically ambiguous evidence stays qualitative. F1studioz historical reports are below the target; it is a Possible target, not a confirmed stipend match. Current role pay and payBenchmark values are separate. Annual reports remain annual. No senior pay was extrapolated to internship stipends.

The Excel workbook contains a separate Company watchlist sheet. Company CSV and JSON backup/restore are available in the app. The collector defaults new undisclosed-pay candidates to on_hold. Do not run seed.py to refresh: it recreates the older initial snapshot.


## Expanded company directory and blacklist

The24 October expansion contains92 employer/studio targets (58 product companies) and28 role leads. Forty directory role records include senior team evidence and internship programs as well as real vacancies; inspect the explicit seniority, access and intake labels. Likely role families are inferred, not postings. Each company retains careers/public contact routes; contacts carry their actual purpose. Eight new early-career leads have unknown pay and remain on hold.

Companies now sorts product companies first, with search, company-type and role-evidence filters, editable categories/following and expandable role/source details. Each role has source-backed requirements and a private Met/Partly met/Gap/Unassessed checklist with evidence notes. The meter counts listed criteria, bonus items and application steps equally; it does not measure hiring odds or certify mandatory eligibility. No resume/portfolio was assessed, so initial personal fit is Unassessed.

Use Companies → Blacklist to exclude any employer, including a company absent from the feed. Blacklisting hides matching Discover/directory recommendations and future matching feed items in this browser. Saved applications, notes/history and next actions remain accessible. Exclusions are reversible and may include private reasons. Names match by normalised spelling or explicitly researched aliases, not fuzzy guessing.

Preferences, blacklist and evidence use the existing company override localStorage key and version1 JSON backup, with old backups still supported. They stay browser-local, cannot be read by the daily task, and never enter public research exports. Export filtered list creates a local CSV including current private evidence; download it only where intended. The static workbook includes Company directory and Role requirements sheets; public/data/company-directory.csv is regenerated with the workbook by python scripts/export_excel.py.

Run the new workflow check with PLAYWRIGHT_BROWSERS_PATH pointing at installed browser binaries: python tests/company_check.py. It exercises product filtering, source requirements, evidence meter, blacklist, saved application preservation, export, reload, backup/restore, custom exclusions and mobile layout. Existing browser_check.py covers the original workflow.


### Reviewed-fit imports

A version1 backup may contain assessment-only companyOverrides (no profile or application fields). Restore merges each company record and role criteria, retaining existing blacklist/reason/tier/following and unrelated criteria. The imported judgment wins for an identical criterion; export a backup first. Personal assessment files stay outside the public repository/feed and must be imported by the user in their own browser. Role details reuse the company requirement meter and support private criteria for employers absent from the public directory. Test this with python tests/fit_import_check.py.


## Broader source coverage

Public research now includes YC / Work at a Startup, Wellfound, Hacker News Who is hiring, Himalayas, We Work Remotely, Remote OK, Remotive, Remote.co, Working Nomads, India job boards and startup maps/directories. The feed has36 researched role leads and111 employer targets, including73 product companies. These counts include older on-hold leads, junior alternatives and watchlist-only company records; they are not a count of newly posted qualifying internships.

Discover has dedicated source-family filters and a Source coverage button. Sources & evidence displays21 checked sources with actual access limits, findings, examples excluded and dates. Individual source checks are expandable. A public directory/map listing is employer discovery, not a vacancy. Public research usually needs no linked account; applying/saving can require the platform's own login. No signed-in Indeed/Naukri connector or CAPTCHA bypass is configured.

Indeed links10 role records after4 new leads and cross-post enrichment; Naukri remains1 employer-linked route because original automated access is blocked. YC SuperKalam and Coulomb records originated in2024 and carry older-listing/on_hold warnings. HN October2026 research examined266 top-level posts with25 design-term matches but no verified India-eligible junior design vacancy. Several promising Wellfound originals are410 or below target; Chiblu gets a sourced cross-post rather than a duplicate card.

Annual/foreign junior salary stays in advertisedCompensation with original currency/period. The display supports annual INR/USD and labels it separately; it is never a confirmed monthly stipend match. SuperKalam pay metadata conflicts and remains unquantified. Matching Ungrammary Cutshort fellowship reports10–12k/month below target; a separate company page annual range is retained with limits. Salary and freshness caveats remain with source evidence.

The supported Excel export now includes Source coverage, and regenerates the public company CSV. The daily task prompt maintains this expanded coverage and source schema; browser-private state remains separate. Run python tests/source_coverage_check.py for source filters, cross-post dedupe, older listing labels, original salary units, coverage/access status and mobile layout.


##25 October research maintenance

The feed retains43 role records:42 active recommendations and1 archived removed listing. Four new on-hold entries are Atlabs and Revvity internships plus Moonfire and Enterprise Bot permanent fresher alternatives. No new qualifying monthly stipend is confirmed. Moonfire’s INR2.5–4lakh/year is annual pay. Glance links to its original Greenhouse application; the aggregator’s pay is unverified. Innovexis in295 is archived after original404/410, preserving saved application stages and history.

Directory123 companies;255 source records;24 source-coverage records. Source families actually checked carry25October dates; older dates remain where a check was not repeated. The39 existing primary URLs were attempted,34 fetched,4 blocked and1 removed. A fetched page alone does not confirm intake. Public research remains targeted best effort, with no signed-in Naukri/X session or CAPTCHA bypass. Source coverage documents zero suitable results and stale/misclassified/low-pay evidence.

The daily search now runs at exact07:00 Asia/Kolkata from26October2026; the prior flexible task is paused. The task updates and deploys public research. Private browser blacklist/profile/history remain in localStorage and cannot be read by the background search.


## Startup hiring follow-up

Search Startup in Discover to see10 curated startup leads:four new internships and six existing records. New companies are Propel, Kodin/Autometa Labs, FORMAS.AI and Daankart. All four are on hold for compensation/intake details; remote-global engagement still needs India contracting confirmation. No new guaranteed stipend match. This is a researched sample, not a list of every startup vacancy.

The full feed now retains47 records (46 active),136 company targets,272 source records and25 coverage rows. Company-only evidence distinguishes closed Figr/Grexa, experienced-only Coachingle, below-pay Cravv and Globalli’s absent current ATS designer. Closed or unsuitable search results are documented, not added to active roles. Application history and private exclusions remain browser-local.
