# Shared context and integrations

Current setup: Mem0 using `MEM0_API_KEY`, entities named for this environment, strict topic isolation, and connected Mem0/Figma plugins when their tools are exposed. No separate memory user-ID or Figma token setting is required.

## Request policy

| Event | Default remote requests |
| --- | --- |
| Local configuration check | 0 |
| New task with known topic and authenticated Mem0 | 1 scoped lookup |
| Ordinary follow-up or delegation | 0 extra context lookups |
| Useful changed decision/correction/handoff | 1 curated write, deduplicated when unchanged |
| One-time environment entity registration | 1 setup-record write |
| Task needs Figma | Minimal plugin calls for the requested file/node |
| Error or rate limit | 0 automatic retries |

Prefer connected MCP/plugin tools and their existing authentication. Do not call both MCP and the direct-API fallback for the same operation. The fallback uses Python's standard library with no SDK pings or telemetry, preserves proxy and verified TLS settings, and rejects redirects.

## Authentication and entities

The only new credential is `MEM0_API_KEY`, securely entered in environment settings and routed only to `api.mem0.ai` for the direct-API fallback. MCP authentication is controlled by its connection; this environment cannot silently install or reconfigure a connector in another app.

Entity names are derived locally from the known workspace environment name:

| Mem0 field | Value |
| --- | --- |
| user entity | `Chatgpt-Environment` |
| topic agent entity | `Chatgpt-Environment/topic/<topic-slug>` |
| metadata environment | `Chatgpt-Environment` |

The fallback does not read or require a separately configured user ID. The API still needs entity fields in requests; they are supplied automatically from these names. Different topic entities stay isolated. Existing memories under other IDs are not automatically migrated.

After authentication becomes available, add the short `bootstrap.txt` record under the environment and `environment-setup` entities once. Use connected MCP or the fallback `mem0-save` command from the topic-context skill. Remote registration remains pending until that write succeeds. Do not upload entire source archives or transcripts to initialize memory.

## Install and activate

```sh
python environment/context/install.py
python /workspace/shared/environment-context/bin/context_tools.py status
```

The installer retains skills and the helper at `/workspace/shared/environment-context`, independently of topic branches, and maintains a managed block in `/workspace/AGENTS.md`. It preserves unrelated instructions and rejects overwriting locally edited managed files. Saved install instructions must pin the corrected commit; otherwise an older installer can restore obsolete requirements.

The startup instructions load context only for the user's selected topic. This setup applies to tasks using the configured cloud environment, not automatically to unrelated chats. A skill file does not install an MCP server or expose host-side tools.

## Fixing the saved settings

The settings API supports additive credential requirements and cannot delete old requirements. Remove the obsolete Figma-token and old Mem0-token rows and the separate memory user-ID row in the environment settings editor. Keep only `MEM0_API_KEY` for this context integration, save and publish. The corrected helper, skills and startup instructions do not use those obsolete settings even before their rows are removed.

API routes are hostnames, not MCP server URLs. The draft can save `api.mem0.ai` as an HTTP destination; that is not a registered MCP URL. A user-entered MCP URL needs the product's supported connector settings, which this configuration tool does not expose. Do not invent a server URL or treat a key rename as proof of a repaired MCP connection.

## Validation

Offline tests verify key-only authentication, environment/topic filters, per-task caching, account changes, error caching, deduplicated writes, credential redaction, one-time setup payload and installer preservation. Live Mem0 access and entity creation remain unverified until authentication is available. Verify with the useful setup write and one topic search, not redundant ping or account probes.

Official interface references: [Mem0 client](https://github.com/mem0ai/mem0/blob/main/mem0/client/main.py) and [typed options](https://github.com/mem0ai/mem0/blob/main/mem0/client/types.py). The fallback uses their current v3 search/add paths and filters. If the exposed MCP differs, use its documented schema.
