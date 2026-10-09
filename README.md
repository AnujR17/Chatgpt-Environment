# Topic workspace

This repository keeps research, planning, and project discussions in reviewable Git branches. Each topic has a dedicated brief, task tracker, decisions, and handoff so a future conversation can continue from written context.

| Topic | Branch | Entry point |
| --- | --- | --- |
| Digital Cheque | `topic/digital-cheque` | [Topic overview](https://github.com/AnujR17/Chatgpt-Environment/blob/topic/digital-cheque/topics/digital-cheque/README.md) |

See [WORKFLOW.md](WORKFLOW.md) for adding topics and continuing discussions. Use [the topic template](templates/topic.md) for a new topic.

The [shared context setup](environment/context/README.md) provides topic-isolated Mem0 context using `ENV_ALL` and on-demand Figma reads. Its installer retains the skills outside branch-specific files; credentials are supplied through environment settings.

The repository currently contains documents and research assets. There is no application server, package installation, or application test suite.
