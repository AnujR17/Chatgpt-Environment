# Design search clipper

A small companion to the existing design search board. Log in normally on your own device, open a job detail, click the extension and review the captured fields. Save for review, export the capture file, then use **Export → Import captured jobs** in the board. Imports remain in that browser; they are never uploaded into the public research feed.

## Install

1. Download `design-search-clipper.zip` using the board's Export menu and unzip it.
2. In Chrome, Edge or Brave, open `chrome://extensions`, enable Developer mode and choose **Load unpacked**. Select the extracted folder containing `manifest.json`.
3. Pin the extension and open a job detail page. Read the captured company, role, location, pay text and description before choosing **Save for review**. Missing text can be pasted into the popup.
4. Choose **Export captures**. On the board in your usual browser, choose **Export → Import captured jobs** and select the JSON file.

An embedded in-app browser may not support installing extensions. Use a supported desktop Chromium browser. Installing this extension does not give the cloud chat access to your browser session.

## Behaviour and privacy

- The only permissions are `activeTab`, `scripting` and `storage`. No standing website permissions, background crawler, cookies permission, server, analytics or external AI request.
- A page is read only after you open the popup or press Read page again. Captures stay in extension-local storage until you explicitly export them. The JSON includes only the displayed capture fields and source/date metadata; inspect it before sharing it elsewhere.
- Captures include job-description text rather than a whole-page/account snapshot. No résumé, inbox, applicant profile or application answers are collected. A job page can still contain employer contact information in its description.
- Site-specific readers cover Naukri, LinkedIn and Indeed; employer JobPosting JSON-LD is a fallback. Site layouts change. Missing or incorrect fields must be corrected manually. A readable page is not proof of current intake or eligibility.
- The board imports captures as `on_hold`, with pay unverified and no invented original posting date, location eligibility or internship classification. Raw pay wording is retained without salary-to-stipend conversion. Review type, seniority, dates and units before shortlisting.
- Exact URL/platform-ID duplicates already in the feed, local records or additional sources are skipped at import. Cross-posts without a shared ID/URL are separate until reviewed; no fuzzy merging. A public feed role added after a private capture may still need duplicate review. Existing public records and private notes/stages are never overwritten by a capture import.
- The current browser's company blacklist is checked before importing; existing application history is retained. Explicitly unpaid captured pay text is skipped. Ambiguous compensation remains unverified.
- Saving a capture never marks it Applied. There is no form filling, submission, employer messaging, login automation, access-challenge solving or unattended collection.
- Exported captures retain their local copies; clearing the extension does not clear the board. Back up each browser's data before changing browsers or removing the extension.

## Open-source attribution

`capture.js` adapts the page-reader function from [PrafulAggarwal1234/job-application-tracker](https://github.com/PrafulAggarwal1234/job-application-tracker), `popup.js` at upstream commit `46dc8319dc6ec8d7b7a6852ac4f4abcc4583cfee` (file blob `89d156d73ca532a3b842f24f2721cefc323d5578`). Copyright ©2026 Praful Aggarwal. The complete MIT licence is retained in `LICENSE` and included in the download.

Changes include scoped description/location/raw-compensation capture, structured employer metadata, review before saving, local capture export and conservative board intake. The original extension's automatic Applied status is not used. Other reviewed projects are architectural references only; no code from an unverified licence was copied.

## Build and checks

From `app`, run `python scripts/package_clipper.py` to create a deterministic ZIP in `public/downloads`. No dependencies or build tools are needed to load the extension itself. App tests cover capture-file validation, exact source deduplication, unverified compensation, blacklist handling and private-state preservation. Browser checks use controlled fixtures; those checks are not a certification of live logged-in platform support.
