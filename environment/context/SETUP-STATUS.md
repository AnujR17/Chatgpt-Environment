# Context setup handoff

Prepared on 9 October 2026 (Asia/Kolkata). Branch: `task/environment/topic-context`.

## User requirements

- `ENV_ALL` is the Mem0 token variable, shared across tasks using this environment.
- Mem0 context must be separate per topic.
- Restore context at the start of a conversation/task, not on every message.
- Support Figma and add other tools when future tasks require them.
- Implement these workflows as reusable skills.

## Implemented

- Topic context skill with a single scoped retrieval per task and local-file fallback.
- Figma skill with scoped, cached REST reads only when needed; editing needs a separate native connector.
- Standard-library helper with no SDK pings, telemetry, polling or automatic retries.
- Per-topic Mem0 entity filters, task-scoped retrieval caching and cross-session identical-summary deduplication.
- Credential/header protection and rejection of redirects.
- Repeatable installer that preserves unrelated instructions and locally edited managed files.
- Workspace instructions pointing to installed skills independently of topic branches.

## Validation

14 offline tests passed. They exercise request budgets, scope, credentials, errors, deduplication, read targets and installation preservation. Mem0 endpoints/filters and Figma headers/paths were checked against their official maintained client/specification.

## Remaining setup

Neither `ENV_ALL` nor `FIGMA_ACCESS_TOKEN` was present in the actual runtime or configured secret bindings during inspection. Secure values must be supplied in environment settings. `MEM0_USER_ID` must be stable; the draft suggests `chatgpt-environment-owner`, or use the exact ID for an existing Mem0 namespace.

After configuration applies, use one topic-scoped Mem0 search to validate access and one requested Figma file/node read when Figma is needed. No live authenticated API success is claimed. Environment publication and fresh-task activation must be verified separately. The setup applies to tasks using this configured environment, not globally to unrelated chats.

Update this record after live validation. Do not upload the Digital Cheque archive, full transcripts or missing research outputs as part of the credential check.
