# Checkpoint — native Windows gaming companion

A native desktop app for checking in with your feelings during a game. Choose from 43 illustrated cards, adjust pleasantness and energy independently, and take a break when you want one.

## Download for Windows

**[Download Checkpoint for Windows x64](https://github.com/AnujR17/Chatgpt-Environment/releases/download/checkpoint-v0.1.0-preview.2/Checkpoint-Windows-Preview.zip)** · [Release and checksums](https://github.com/AnujR17/Chatgpt-Environment/releases/tag/checkpoint-v0.1.0-preview.2)

1. Download `Checkpoint-Windows-Preview.zip` and **extract the entire archive**.
2. Open the `Checkpoint-Windows` folder.
3. Double-click **Start Checkpoint.cmd**. Python and Qt are included.

Windows 10/11 x64 is the target. Keep the extracted folders together. Run **Check setup.cmd** for diagnostics. This is an unsigned research preview. The package was assembled on a Windows runner and passed a native launch/screenshot check. Its download and SHA-256 checksum have been verified. See [live tracking instructions and verification scope](docs/LIVE-TRACKING.md).

![Native Checkpoint application](artifacts/cards-app-session.png)

## What works

- Eight common feeling cards first; all 43 available through search and the full library.
- Check-ins with independent pleasantness and energy sliders; cancellation preserves your last report.
- Optional own-camera/video preview with **Track expressions (experimental)**. Stable estimates automatically change the **Live expression** card. The eight model classes are separate from the 43 self-report words.
- Windows foreground-process detection and opt-in Getting Over It window sampling. Optical flow gives possible climb/fall cues; a player-marked reference identifies a similar start view. These game-event cues are unvalidated heuristics.
- Breaks, session completion, light/dark appearance, reduced animation and optional local summary history.

![Feeling cards](artifacts/cards-app-library.png)

Feelings and CMA come from **your check-in**. Facial-expression inference is experimental, disabled by default and cannot assign your mood or trigger interventions. Microphone capture is not implemented. Getting Over It screen sampling is a separate opt-in control in Settings and only targets that supported foreground game. Normal use does not record or upload video. History is off by default.

## Source and verification

```sh
cd topics/checkpoint/app
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
python -m pip install -r requirements-runtime.txt
python -m pip install --no-deps -e .
python -m checkpoint.app
```

34 checks pass in Linux, including real recorded-video expression inference and automatic native card updates; the Windows-only GDI check is skipped locally. Synthetic game scenes test motion direction, temporal gating, scene cuts and start-view matching, not real-game recognition accuracy. See [tracking instructions and limits](docs/LIVE-TRACKING.md). Earlier evidence: 27 checks passed in the original Linux workspace. A [GitHub Actions Windows runner](https://github.com/AnujR17/Chatgpt-Environment/actions/runs/41971376058) also passed a native window launch and screenshot check. Physical-camera access, player recognition of the illustrations and performance on your computer remain unverified. The model failed its production release gates; this is a research preview.

[Windows instructions](docs/WINDOWS-APP.md) · [Feature applicability](docs/FEATURE-APPLICABILITY.md) · [Model card](artifacts/MODEL-CARD.md) · [Third-party notices](third_party/NOTICES.md) · [Editable Figma](https://www.figma.com/design/Rj3WAO6IpUb48OFUerY7aW?node-id=108-127)

To run software checks, install pytest and run `python -m pytest -q`. The external-video test requires the separately sourced research fixture and skips when it is absent. Raw training images, evaluation videos, downloaded visual references, caches and environments are excluded from this repository.

The exact Python embedded runtime and wheel hashes are recorded in `design/windows-runtime-sources.json`. The [branch workflow](../../../.github/workflows/checkpoint-windows.yml) fetches those exact vendor files, assembles the app, checks a native Windows launch and publishes the portable ZIP. The scripts in `scripts/` assemble and verify the bundle from vendor files under `build/`. They do not train or alter the model. SHA256SUMS.txt in the release verifies the downloadable ZIP.
