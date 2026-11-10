# Personal job-search assistant

Branch: `topic/ai-job-search`

A personal assistant for Codex/ChatGPT: build a confirmed career profile,
evaluate roles, draft tailored CVs and letters, prepare interviews, and track
outcomes. The agent supplies reasoning and writing; a Python helper stores
your records. No additional model API key or Python package is required.

Inspired by [AI Job Search](https://github.com/ai-job-search-dev/ai-job-search),
reviewed at commit `e9ab29dcc20b3d802356077b02898cd97db0d312` on 2026-11-10.
This is an original, smaller implementation built for Codex rather than a fork
of its Claude commands and Denmark-focused portal integrations. The reference
repository is MIT licensed; retain its license if copying its code later.

## Use it in this chat

Ask **“Set up my job search”**, then supply a CV or pasted career history and
your target roles and locations. The agent follows the repository's
`job-search` skill. Next, ask **“Evaluate this job”**, **“Draft an application
for this job”**, **“Prepare me for this interview”** or **“Show my pipeline”**.
These are natural-language requests, not installed slash commands.

You can import jobs before completing your profile. Drafting requires a
confirmed profile. No career facts have been entered on your behalf.

## Run the helper

Run these from the repository root with Python 3.10+:

```sh
python3 topics/ai-job-search/jobsearch.py init
python3 topics/ai-job-search/jobsearch.py profile-check
python3 topics/ai-job-search/jobsearch.py add --company 'Example Co' --role 'Engineer' --posting /path/to/posting.txt --url 'https://example.com/jobs/123'
python3 topics/ai-job-search/jobsearch.py list
python3 topics/ai-job-search/jobsearch.py prepare JOB_ID
python3 topics/ai-job-search/jobsearch.py check JOB_ID
python3 topics/ai-job-search/jobsearch.py status JOB_ID ready
python3 topics/ai-job-search/jobsearch.py status JOB_ID applied --note 'Candidate confirmed submission'
python3 topics/ai-job-search/jobsearch.py status JOB_ID interview --note 'Recruiter confirmed interview'
python3 topics/ai-job-search/jobsearch.py show JOB_ID
python3 topics/ai-job-search/jobsearch.py report
```

`JOB_ID` means the full 12-character ID returned by `add` or `list`. The example
company, URL and posting path are illustrative. `prepare` creates unfinished
templates for the agent to complete; it does not call an LLM. `check` and
`status ... ready` fail until the drafts and review are complete. Commands emit
JSON and errors return a nonzero exit code. `--data-dir /absolute/path` goes
**before** the command; custom directories need their own Git exclusions.

The helper accepts plain UTF-8 posting text and records a URL as provenance.
It does not fetch URLs. Identical source URLs with `utm_*`, `gclid`, `fbclid`
or fragment differences deduplicate; job-identifying query parameters remain.
A changed posting at an existing URL is rejected without overwriting the
original. There is no automatic board search or refresh yet.

## Profile and review

`init` creates a blank `private/profile.json` without overwriting existing data.
Fill it with your confirmed facts. For example, this **fictional schema example
is not a candidate profile**:

```json
{
  "name": "Example Candidate",
  "headline": "Software engineer",
  "target_roles": ["Backend engineer"],
  "locations": ["Remote"],
  "work_modes": ["remote"],
  "constraints": ["Work authorization needs clarification"],
  "facts": [
    {
      "id": "F001",
      "claim": "Built a Python reporting tool at Example Co in 2024.",
      "source": "Candidate confirmation, YYYY-MM-DD; source CV page 1",
      "confirmed": true
    }
  ]
}
```

Candidate confirmation is required before setting `confirmed` to true. The
agent records the exact factual wording, source and stable ID. `profile-check`
checks structure and required fields; it cannot establish factual truth.

Each packet contains the original posting, a profile snapshot, metadata, an
evaluation, CV, letter, interview template, and `review.json`. A completed
review looks like this (hashes below must be replaced with actual digests):

```json
{
  "approved": true,
  "checks": {
    "factual_accuracy": true,
    "requirements_coverage": true,
    "no_placeholders": true
  },
  "claims": [
    {
      "document": "cv.md",
      "quote": "Built a Python reporting tool at Example Co in 2024.",
      "fact_ids": ["F001"]
    }
  ],
  "notes": "Record the actual review findings here.",
  "sha256": {
    "evaluation.md": "actual SHA-256 digest",
    "cv.md": "actual SHA-256 digest",
    "cover-letter.md": "actual SHA-256 digest",
    "profile.json": "actual SHA-256 digest",
    "posting.txt": "actual SHA-256 digest"
  }
}
```

Add an entry for every candidate factual claim in the drafts, including the
letter. `quote` must appear in its named document. Fact IDs must refer to
confirmed facts in the packet's profile. Compute digests from exact file bytes
using Python's `hashlib.sha256`. Changing a reviewed file invalidates its
recorded hash. The posting must also match the original in the tracker.

The readiness gate validates review structure, cited IDs, unfinished template
markers and hashes. It does **not** prove truth, exhaustive claim coverage,
CV quality or ATS compatibility. The agent's review and your final check
remain necessary. Interview prep is optional and does not block readiness.

## Storage and privacy

```text
topics/ai-job-search/private/       # excluded from Git
  profile.json                    # master candidate facts
  tracker.sqlite3                 # jobs and dated status events (UTC)
  packets/JOB_ID/                  # working application and source snapshots
  submitted/JOB_ID/                # preserved copy when recorded as applied
  report.html                     # generated local pipeline view
```

The helper sends no network requests. New data files use restrictive local
permissions. Git exclusion is not encryption or a backup: Codex/ChatGPT may
process your inputs in the current service, and environment storage can be
discarded. Back up the entire private directory separately; keep candidate
material out of Git, Mem0 and hosted dashboards. Submitted copies are preserved
by the helper but ordinary filesystem edits are still possible.

`applied` records a user-confirmed action and snapshots the reviewed packet.
It does not send an application. Later status changes append history without
rewriting that snapshot. Email, calendar and job-board integrations, scheduled
alerts, and PDF/DOCX export are future extensions, not installed features.

## Validation and next step

```sh
python3 -m unittest discover -s topics/ai-job-search/tests -v
```

Tests use temporary directories and fictional data. `TASKS.md`, `DECISIONS.md`
and `HANDOFF.md` track project state without personal information.

The next step is to supply your CV or career history, target roles and locations,
then complete one real posting-to-reviewed-draft cycle together.
