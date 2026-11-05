# Open-source parts adapted for the existing board

Reviewed 5 November 2026. Keep the current Vite/React app, public research schema and browser-local progress. Reuse small parts where they address a real gap.

| Upstream | Specific part | Fit with our implementation | Status |
| --- | --- | --- | --- |
| [Praful Aggarwal / Job Application Tracker](https://github.com/PrafulAggarwal1234/job-application-tracker/blob/46dc8319dc6ec8d7b7a6852ac4f4abcc4583cfee/popup.js), MIT | `scrapeJobPage()` and its user-click/activeTab approach | `extension/capture.js` adapts the reader; a new popup lets the user review description/location/raw pay and export captures. `app/src/captures.js` validates local intake. | Implemented; full MIT notice retained in the package. No upstream Applied-on-save behaviour reused. |
| [Muatasim-Aswad / Job Tracker](https://github.com/Muatasim-Aswad/job-tracker/blob/main/apps/extension/src/adapters/builtin/linkedin/identity.ts), MIT | Platform identity across bare/slugged job URLs; adapter boundaries; multiple listing sources per opportunity | Our capture importer independently uses exact platform IDs/URLs to skip known listings and additional sources. Existing stable public IDs and private stages are preserved. | Architectural reference; no source copied. Future cross-post merges require review; no fuzzy automatic merge. |
| [JobNavigator Greenhouse handler](https://github.com/vesaias/JobNavigator/blob/main/backend/scraper/ats/greenhouse.py), MIT | Public board JSON API, company slug/office/department filters and job detail text | Our collector already handles JobPosting JSON-LD and Lever. A focused Greenhouse payload adapter would fill an actual discovery gap. | Inspected, not integrated. Adapt only the useful payload handling; do not import the whole suite or infer India eligibility from a company location. |
| [JobNavigator Ashby handler](https://github.com/vesaias/JobNavigator/blob/main/backend/scraper/ats/ashby.py), MIT | Public board JSON API and board-specific location/team handling | A separate Ashby adapter could produce the existing `on_hold` candidate schema and retain original dates/URLs. | Inspected, not integrated. Requires source-specific robots/access and eligibility checks before live collection. |
| [JobSpy](https://github.com/speedyapply/JobSpy), MIT | Multi-board search/discovery adapters | Possible optional worker feeding review candidates, not the browser's private progress. Current platform access must be tested separately. | Not installed. No bypass-oriented transport/proxy recommendations adopted. |
| [changedetection.io](https://github.com/dgtlmoon/changedetection.io), Apache-2.0 | Filtered careers-page change watches and notifications | `app/scripts/collect.py` already hashes visible text and records changes. Selected section/keyword watches could improve signal without adding another application stack. | Reference only; not installed or copied. |

## Implemented capture flow

User opens a job detail in their own supported browser → opens the clipper → reviews fields → saves/exports a capture file → imports it through the existing board's Export menu. No authenticated session is sent to the cloud task. The clipper cannot be assumed installable in an embedded in-app browser.

Only `activeTab`, `scripting` and `storage` permissions are requested. There are no standing host permissions, background crawler, external AI calls, form filling or submission. Captures and imported records remain local until the user explicitly exports/shares a file. They are not published into the researched jobs feed.

Imports keep pay, dates, work arrangement, seniority and role classification unverified. Annual/foreign/ambiguous pay is retained as raw text, never turned into a monthly INR stipend. Exact known source identities, current browser-blacklisted employers and explicit unpaid pay text are skipped. Malformed capture files are rejected before state changes; applicant/profile/notes/stage fields embedded in a capture file are ignored.

The capture importer adds local custom records without overwriting any feed ID, existing note, application stage, company preference or evidence checklist. A later public-feed role that matches an earlier private capture can still require duplicate review; this release does not promise global or fuzzy duplicate merging.

## Validation and limits

Eighteen capture/model tests, five existing collector tests and the production build pass. Controlled Naukri/LinkedIn/Indeed/employer metadata fixtures verify field extraction and absence of whole-page/profile capture. Popup save/deduplication/export is exercised with mocked Chrome APIs; desktop/mobile board tests import that actual exported file, check hostile extra fields, duplicate/unpaid/blacklist handling, invalid-file rejection, retained private state and reload. No runtime errors in those checks. Packaged ZIP contents match the six reviewed source/licence files exactly; public research JSON/CSV/workbook/report bytes are unchanged.

This does not verify a real Chrome toolbar permission grant or current logged-in job-board DOM. The browser owner must install the extension and check their job page; missing descriptions can be pasted into the review popup. No live account, application submission, CAPTCHA bypass or employer contact occurred. The existing unrelated Gravity data-test expectation remains documented in the research handoff; no claim that the full data suite passes.
