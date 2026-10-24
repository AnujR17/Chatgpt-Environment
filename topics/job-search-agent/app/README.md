# Design internship tracker

Live board: https://chatgpt-environment.vercel.app

Production is READY from the board branch in the existing Vercel project `chatgpt-environment`.

Personal internship discovery and application Kanban for Anuj. Primary GitHub owner: **AnujR17**. Deployment target: **Vercel**.

## Included

- 20 researched roles, including internships and clearly marked junior/fresher alternatives, updated24 October2026. Four Indeed detail listings, one employer-linked Naukri route, employer careers and two X cross-post enrichments complement earlier sources.
- Separate employer-confirmed pay, conditional pay and unconfirmed stipend labels. Uses the **minimum** advertised stipend, not the maximum.
- Remote India first; Gujarat, Maharashtra, Goa and southern India considered. Gujarat minimum ₹20,000/month; elsewhere ₹30,000, with ₹25,000 considered individually. A ₹30,000 remote minimum is provisional.
- Discover card/list views with platform, role type, location and pay-evidence filters; a separate application Kanban; on-hold review; notes, deadlines and interviews. New roles appear first by default.
- Separate company watchlist with17 researched targets grouped into editable Dream, Workable and Possible suggestions. Following/categories stay browser-local and are included in JSON backups.
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
