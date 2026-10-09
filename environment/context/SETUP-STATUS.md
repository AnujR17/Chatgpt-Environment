# Context setup repair handoff

Updated 9 October 2026 (Asia/Kolkata), branch `task/environment/topic-context`.

## Latest user requirements

- Replace the earlier Mem0 token name with `MEM0_API_KEY`.
- Remove the separately configured memory user ID.
- Use this environment name for Mem0 entities, keeping topics separate.
- Use the available Figma plugin; require no Figma token here.
- Prefer the connected Mem0 MCP when its tools are exposed.
- Retain the minimal-request policy and reusable skills.

## Diagnosis

The prior draft saved its API-domain and credential requirements, but no credentials were applied to the runtime. A key rename alone cannot establish authentication or fix a host-side MCP connection. No callable Mem0 or Figma MCP tools were exposed in this task's tool inventory during repair. Their presence in another app/chat remains distinct from availability here.

The configuration tool only adds secret/variable requirements; deleting obsolete rows needs the environment settings editor. The implementation removes those dependencies and supplies the environment entity automatically, so stale rows are not read by the helper.

## Corrected behavior

`MEM0_API_KEY` is the sole required fallback credential. Entity fields use `Chatgpt-Environment` and `Chatgpt-Environment/topic/<topic>`. Topic memory stays isolated. A different actual key gets a separate local cache scope. Proxy-placeholder credential rotation can still need an explicit refresh after diagnosis.

Figma REST code and its token requirement have been removed from the implementation. The Figma skill uses a connected plugin only when the task requires it. The Mem0 skill prefers exposed MCP tools and uses direct HTTP only as a fallback, never both for one operation.

A short bootstrap record is prepared to establish the environment and environment-setup entities once authentication is available. It contains configuration decisions only, without any keys or raw documents. No remote entity creation or live API success has been claimed.

## Remaining external actions

Remove obsolete credential/variable rows in environment settings, securely supply `MEM0_API_KEY`, save and publish the corrected configuration. Expose the Mem0/Figma connection to tasks that need it if its tools are not already callable. Then perform one useful setup write and a scoped lookup; update this status with observed results.
