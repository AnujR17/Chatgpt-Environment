# Handoff

Continue the personal `ai-job-search` topic on `topic/ai-job-search` in the
existing checkout. Read README.md, DECISIONS.md, TASKS.md and the repository's
`.agents/skills/job-search/SKILL.md` before using the workflow.

The user asked for an assistant of their own inspired by
`https://github.com/ai-job-search-dev/ai-job-search`, and explicitly selected a
personal Codex/ChatGPT assistant. An original local starter now supplies a
profile, job intake, tracker, draft templates, review validation, interview
workflow, preserved submission copies and a local HTML report. AI writing is
performed by the current chat, not the Python helper.

No CV or candidate facts have been supplied. Do not invent or assume them.
Start onboarding with the candidate's CV/history, target roles and locations.
Keep all personal information in the ignored private directory and outside
Git and Mem0. Record only nonpersonal workflow decisions in topic memory.

Validation: 15 fictional-data tests pass with Python 3.12, including the full
profile → saved job → packet → reviewed/ready → applied snapshot → interview
flow, source preservation, duplicate detection, rejected unconfirmed/unknown
fact IDs, stale review hashes, preserved drafts and HTML escaping. CLI startup
was checked from a different directory. `git diff --check` passed and
`git check-ignore` confirmed the actual private profile and SQLite tracker are
excluded. Initialization created a blank local profile; its expected validation
failure confirms onboarding is still required. No real application, live
job-board search, PDF export or recruiter interaction has been tested.
