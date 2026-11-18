# Classroom brief and case-study coverage

Transcribed from the clearer classroom-board image supplied by the user on 18 November 2026. This records the project requirements; it is not participant research.

| Board requirement | Checkpoint application | Evidence in this case study |
| --- | --- | --- |
| Individual Design Project | One bounded interaction and service design project for an individual player. | Scope, decision record and working prototype. AI assistance is disclosed below. |
| Subject: Human Computer Interaction Design | The player understands sources, chooses help, corrects their own report and controls sensing. | Information architecture, layout plan and native task flow. |
| Theme: AI for Society / Social Cause | Intended benefit: agency and more considered responses during difficult play. | Problem definition and usefulness questions. Reduced anger/wellbeing benefit is not demonstrated. |
| Framework: Circumplex Model of Affect (CMA) | Adjustable self-reported pleasantness and activation shape optional help density and target size. | CMA decision table, implementation parameters and report. |
| Technology: cameras and sensors built into mobile phones, laptops, computers and devices | Laptop webcam; optional Windows game-window capture and aggregate input timing. Phone is a paired display, not another sensor in this implementation. | Local architecture and tested/untested capability table. |
| Tools: any AI tools + editing software | Codex for assisted research, code and writing; existing MediaPipe/HSE expression inference; Python/PySide6/QPainter for UI and vector editing; Playwright/Chromium for browser checks; Git/GitHub for branch and Windows CI. | Native source, original graphics, review scripts and verification. No claim that Figma or a new training pipeline was used in this revision. |
| Core concepts: design, AI/computer, input, system/service/product, output for society/human | Design the support interaction; process optional visual inputs locally; deliver a companion service; let the player choose, try and reflect. | Core-concept mapping below. |
| Design process: Empathize, Define, Ideate, Prototype | Four explicit stages, each with work, artifacts and limitations. | Process evidence below. Validation is a next step, not an invented completed fifth stage. |

## Core-concept mapping

| Concept on the board | Concrete implementation |
| --- | --- |
| Design | Make the player’s next choice understandable and voluntary. |
| AI / computer | Local face/hand features and category estimates; game-window vision estimates. Authored decision rules adapt guidance. |
| Input | Explicit CMA report, selected practice problem and optional camera/game/input-timing signals. Each has its own source and uncertainty. |
| System | Windows application coordinates local analysis, session state, overlay and paired phone. |
| Service | Choose a cue, try it, give a verdict and recall a useful adjustment. |
| Product | Working PySide6 app with Nori and a CMA session report. |
| Human / societal output | Intended player agency and less intrusive support during difficult play. The demonstrable outputs are a selected cue, the player’s feedback and their own report; wider benefits remain hypotheses. |

The board is a conceptual path, not an instruction to treat uncertain AI estimates as facts. The prototype preserves a clear boundary between camera-derived expression and player-reported affect.

## Design-process evidence

| Stage | Work actually completed | Artifact | What remains unknown |
| --- | --- | --- | --- |
| Empathize | Reviewed published work and public gaming accounts in the existing evidence pack; rehearsed five fictional scenarios, three in Indian contexts. | Research report, evidence register, interview guide, simulated answers. | No genuine primary interviews, observation study or verified demand. |
| Define | Scoped the player problem: being stuck while still wanting the challenge; needing one useful choice without losing control over play. | Target audience, job statement, intended benefit and exclusions. | Which benefit the target player values most. |
| Ideate | Compared a personal companion, full launcher, venue service and automated emotional coach; considered desktop and phone delivery. | Alternatives table, information architecture and reconstructed layout plan. | Preferred delivery surface and whether sensing earns its cost. |
| Prototype | Implemented task navigation, original gaming visuals and icons, CMA-adjusted practice, feedback/recall and report delivery. | Actual native screens, source, browser bridge, PDF and successful Windows CI. | Physical device/game compatibility, expression accuracy in play and real-world usefulness. |

## Authorship and scope

This is an individual design project with AI assistance used for research synthesis, implementation and draft documentation. Secondary sources, fictional persona exercises and software checks are identified separately. No primary interviews, new model training, clinical benefit, performance improvement or usability-success result is claimed.
