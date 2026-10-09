# MyAlumnus

Environment repository: `AnujR17/Chatgpt-Environment`

Working branch: `topic/myalumnus`

## Goal

Maintain project understanding, research, planning, and future work in a dedicated topic branch. The initial request was to understand the existing project; no application changes or deployment have been requested.

## Product

MyAlumnus is a university campus-gate visitor-verification tool. A guard console and an admin console share one database. Alumni are records searched by the guard; they do not have a self-service app or account.

- Guard: name search, record/photo comparison, approve/deny, holds, expected visits, inside/exit tracking, student-family visits, and offline search with queued decisions.
- Admin: escalation decisions, people/photos and bulk uploads, expected visits, history/CSV export, staff/devices, campus settings, and weekly reports.
- Current escalation flow: guard calls the host first; unresolved holds pass to an admin. Earlier admin-first descriptions are historical.
- Desktop and iPad; English/Hindi guard interface and light/dark themes.
- Stack: Next.js 16, React, TypeScript, Supabase, and Vercel.

## Current state and evidence

Reviewed on 9 October 2026:

- [Application repository](https://github.com/sukhman0402/myalumnus): default branch `main`, inspected commit `5955e1e1d16564f6374467b8384c12e577108116`.
- [Live demo](https://myalumnus.vercel.app): returned HTTP 200 and redirected to `/sign-in`, offering guard-device and admin access. Authenticated workflows were not exercised.
- Three uploaded handoff archives: inventory, key planning/testing documents, application source, and representative guard/admin final screenshots reviewed. This was an overview, not an exhaustive audit of every file.
- Source comparison: 191 files were byte-identical to GitHub at the inspected commit; `README.md` and `env.example` differed. Eleven GitHub paths were absent from the snapshot, mostly migration files. The handoff also contains a separate applied-migration export.
- Historical handoff names live commit `0e354e0`; the inspected GitHub branch is newer. Neither deployment commit nor current database state was independently established.

The supplied report describes one real-guard think-aloud session and expert/model-based evaluations. Its simulations are not field-measured impact. It reports an unresolved silent approval failure and other issues; these were not reproduced during the overview.

## Navigation

- [TASKS.md](TASKS.md): authorized work and open items.
- [DECISIONS.md](DECISIONS.md): current session decisions and evidence boundaries.
- [HANDOFF.md](HANDOFF.md): continuation instructions and local source locations.
- [source/README.md](source/README.md): source inventory and provenance.

## Next task

Await the user's next project objective. Possible work includes a case study, deeper implementation review, or a specified application fix; none is authorized by this branch setup alone.
