# Hiring posts and design studios

Search employer and recruiter posts as a separate source family on every research
pass. LinkedIn Jobs alone is insufficient: internships may be announced in company
Updates, founder/design-lead posts or recruiter roundups without a Jobs-tab advert.

Read `app/public/data/social-watchlist.json`. Generate the dated query links with:

```sh
python app/scripts/social_search_plan.py
```

This builds `app/public/data/social-search-plan.json`, a research checklist, not a
scraper or proof of live platform access. The connected research task must actually
run the queries and inspect evidence. It does not log in, fetch private feeds,
create alerts, send messages or change application state. The existing task owns
the schedule; do not start another scheduler or duplicate task.

## Every pass

1. Run broad LinkedIn **Posts** searches, including `/posts/` and `/feed/update/`,
   plus public X hiring-post searches. Search wording such as product design
   intern, UX intern, interaction-design internship, hiring interns, portfolio,
   joining the team and internship cohort. Search company Updates separately
   from Jobs, and inspect a dated public sample of founder/design-lead/recruiter
   posts. Do not count profile biographies or generic community membership as jobs.
2. Check every-pass targets Onething Design, HireDesigners and Devoq. Rotate deeper
   checks across existing product/studio targets. Keep recruitment agencies and
   communities distinct from actual employers. HireDesigners' client openings are
   not automatically vacancies at HireDesigners; never guess an unnamed client.
3. Follow the exact post permalink and employer application/careers destination
   where public and allowed. A credible post can be the primary vacancy evidence;
   it does not require a Jobs-tab duplicate. Record post/activity ID, named author,
   employer relationship if verified, wording of title/location/pay/cohort, and
   exact source URL. Unknown pay stays null/on_hold with a useful next action.
4. Distinguish original publication, visible relative labels, search crawl/repost,
   discovery and check dates. Do not call a post fresh from its index date. If a
   timestamp is derived, label its method and limitations; do not silently use it
   as an employer-confirmed date. Read closed/filled edits and application status.
5. Deduplicate employer roles, social posts, recruiter crossposts and job-board
   advertisements into one card when identity is established. Keep stable job,
   post and requirement IDs; put genuine corroboration in additionalSources.
   Similar titles alone do not prove the same requisition or allow pay transfer.
6. Update separate LinkedIn-post, X and recruitment-source coverage with actual
   query strings, targets, access method, checkedAt, findings and limitations.
   A generated query is **not searched**. Restricted, empty or unsearched feeds
   must not be reported as no vacancies. Retain useful negative and stale evidence.

Onething's current Gurugram internship is explicitly marked outside the usual
location set; this does not make all NCR vacancies eligible. The original role
states15kINR/month, six months and four office days plus Wednesday home working.
Company Updates mention final-semester students; cohort eligibility must be checked.
Public hiring advertisements are opportunities, not applicant-received offers.

## Access and captures

Use public pages/indexed evidence where allowed. Respect robots, rate limits,
login gates and CAPTCHA. Public X/Naukri search may be unavailable; say so and
try a permitted employer corroboration route. Do not claim a linked account from
an opened tab, request cookies/passwords or run a logged-in background scraper.

The browser clipper supports reviewed LinkedIn/Naukri/Indeed **job details**. It
currently has no dedicated LinkedIn-post or X-post reader. For post-only evidence,
use the board's Add role form, or manually complete the clipper's required role,
company and vacancy-text fields on the exact permalink before exporting/importing.
Imported captures are browser-local, unclassified/on_hold with pay unverified.
They are not shared with the background task or published public feed. No automatic
application or message is sent. Never promise complete social-feed coverage.
