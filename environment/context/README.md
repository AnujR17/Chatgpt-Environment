# Shared context and integrations

Requested setup: Mem0 using `ENV_ALL`, memory isolated per topic, Figma on demand, and additional tools as needed later.

## Request policy

| Event | Default remote requests |
| --- | --- |
| Local configuration check | 0 |
| Start a new task with a known topic and configured Mem0 | 1 cached topic search |
| Ordinary follow-up message or agent delegation | 0 extra context searches |
| Useful changed decision/correction/handoff | 1 curated write, deduplicated when unchanged |
| Task needs a Figma file/node | 1 scoped read, cached within the task |
| Error or rate limit | 0 automatic retries |

The helper calls the APIs directly with Python's standard library. It avoids SDK initialization pings, SDK telemetry and additional dependencies. TLS verification, session proxy settings and CA trust remain enabled. Credential headers are never sent through redirects.

## Configuration

| Setting | Purpose | Secure entry |
| --- | --- | --- |
| `ENV_ALL` | Mem0 token, bound only to `api.mem0.ai` | Environment secret settings |
| `MEM0_USER_ID` | Stable non-secret memory identity | Environment variable settings |
| `FIGMA_ACCESS_TOKEN` | Optional Figma REST read credential, bound only to `api.figma.com` | Environment secret settings |

The proposed new namespace is `chatgpt-environment-owner`. If an existing Mem0 identity should be reused, set `MEM0_USER_ID` to that exact existing ID. A different ID will not retrieve old memories. Topic isolation uses both this user ID and an agent ID of `chatgpt-environment/topic/<slug>`. No global cross-topic memory search is performed.

## Install and activate

From the existing checkout:

```sh
python environment/context/install.py
python /workspace/shared/environment-context/bin/context_tools.py status
```

Installation copies the skills and helper to `/workspace/shared/environment-context`, outside branch-specific content, and adds a managed instruction block to `/workspace/AGENTS.md`. It preserves other instructions and rejects overwriting locally edited managed files. No credential values are read or saved by the installer. Repeating installation with unchanged files is safe.

The environment startup instructions point to the retained skill files. They do not switch to Digital Cheque for unrelated tasks. Existing Digital Cheque sources and its branch remain unchanged. New branches inherit repository content from their base; the installed shared skills are available independently of the selected branch within this configured environment.

Publishing this environment retains the installed files. Processes and authentication must not be assumed to persist; credentials come from supported environment settings. Saved configuration and installed skills do not activate Figma MCP or make this setup apply to every ChatGPT chat globally.

## Extension contract

For another integration, add a skill only when its capabilities are known and needed. Specify trigger, supported operations, auth variable or native connection, HTTPS domains, minimal request scope, caching, and error behavior. Record whether it is configured, tested, or still awaiting credentials. Do not share a service token with unrelated tools.

## Validation and limitations

Offline tests verify request budgets, topic separation, deduplicated writes, error caching, credential redaction and Figma request scope. A local missing-credential check is not a successful API test. Live Mem0 and Figma access must be checked after the secure bindings and domain policy are applied. Test Mem0 with one topic search; test Figma against a file the user actually wants accessed, rather than adding account probes.

Interface references: [Mem0 official client](https://github.com/mem0ai/mem0/blob/main/mem0/client/main.py), [Mem0 typed options](https://github.com/mem0ai/mem0/blob/main/mem0/client/types.py), [Figma REST OpenAPI](https://github.com/figma/rest-api-spec/blob/main/openapi/openapi.yaml). Checked during setup on 9 October 2026. The helper uses the official client's current v3 memory search/add paths and entity filters. Live compatibility remains unverified until credentials are available.
