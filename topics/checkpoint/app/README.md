# Checkpoint · Session study

New branch: **topic/checkpoint-session-20261116**, based on the existing Windows build. The stable branch and OTA channel remain unchanged.

This version replaces the large rounded-card session screen with a flatter paper/ink workspace, compact Nori reflection, a separate camera column and visible session actions. Confirmed CMA check-ins can offer a short reset or one smaller practice goal. Keep going silences further suggestions for this session. Reports use actual choices and optional feedback rather than inferring benefit.

[What changed and how to try it](docs/SESSION-BRANCH.md) · [Windows review workflow](https://github.com/AnujR17/Chatgpt-Environment/actions/workflows/checkpoint-session-review.yml)

Download **checkpoint-session-study** from the successful branch workflow run. Extract it, then extract **Checkpoint-Session-Study.zip** into a separate folder and run **Start Checkpoint.cmd**. This is a review artifact, not a GitHub Release or OTA package.

Camera reflection and player-reported CMA remain separate. Existing recognition limitations are unchanged. The new support policy is a prototype, not a proven frustration intervention.

## Development and evidence

Source uses native PySide6/OpenCV/ONNXRuntime/MediaPipe, without a desktop browser engine. Runtime wheels and hashes are pinned in design/windows-runtime-sources.json. Create a venv, install requirements-runtime.txt and install this project with `python -m pip install --no-deps -e .`; run `python -m checkpoint.app`. Tests use pytest; separately sourced research videos and the provider hand example are not committed. Linux development can require system EGL/GLES libraries.

Model provenance, notices, software tests and browser checks are under artifacts/ and third_party/. [Release verification](../RELEASE-VERIFICATION.json) records downloaded package checks and native Windows fixtures. Rendered previews use labelled synthetic signals. The earlier eight-class comparison (62.5% vs 29.8% on 208 acted clips) does not establish personal webcam or 43-emotion accuracy. [Research](docs/VIDEO-AND-MODEL-RESEARCH.md) · [Model card](artifacts/MODEL-CARD.md).
