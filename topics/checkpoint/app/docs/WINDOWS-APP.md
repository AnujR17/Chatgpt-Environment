# Checkpoint for Windows — current build

The current application uses the supplied emotions poster as a reference for an outlined, five-colour card family. It includes the poster's 39 words plus Calm, Frustrated, Excited and Bewildered from the project vocabulary. This is a selectable vocabulary, not an emotion taxonomy or a set of new facial-model classes.

## Download

[Download the portable Windows ZIP](https://github.com/AnujR17/Chatgpt-Environment/releases/download/checkpoint-v0.1.0-preview.1/Checkpoint-Windows-Preview.zip). Extract the whole archive before launching.

## Launch

Extract the entire `Checkpoint-Windows-Preview.zip` archive, open the `Checkpoint-Windows` folder and double-click **Start Checkpoint.cmd**. Keep its folders together. Python, Qt and the numerical runtime are bundled; no Python installation or package download is required at launch. The target is Windows 10/11 x64.

Choose a game and intention. Camera starts off. **Choose a feeling** opens eight common cards. **All feelings** and search expose all 43 cards. Clicking any part of a card opens its check-in; adjust pleasantness and energy, then save. Cancel leaves the existing report unchanged. Not sure records an unassigned state without CMA coordinates.

**Start camera** and **Open video** are explicit source actions. They show your own preview rather than gameplay. The expression model is experimental, off by default and cannot select a feeling, either CMA dimension or an intervention. Breaks stop capture; returning keeps it off.

The Check-ins view includes reports from the active session and any opted-in saved summaries. Settings offers reduced animation, optional derived history and experimental analysis. Settings apply to the current app launch. Saving settings pauses capture. Game and intention can be edited during the session without resetting the report.

## Review files

- `artifacts/cards-app-session.png`: actual native session UI
- `artifacts/cards-app-empty.png`: first-use state
- `artifacts/cards-app-library.png`: common card selection
- `artifacts/cards-app-all-feelings.png`: full searchable vocabulary
- `artifacts/cards-app-search.png`: a search result
- `artifacts/cards-app-checkin.png`: independent CMA inputs
- `artifacts/cards-app-settings.png`: bounded, scrollable settings
- `artifacts/cards-app-compact.png`: 1000×680 layout with the main action visible
- `artifacts/cards-app-setup.png`: session onboarding
- `artifacts/cards-app-break.png` and `cards-app-summary.png`: follow-up states
- `artifacts/cards-vocabulary.png`: full reference-derived character sheet

Editable Figma: page **11 Windows app / Reference cards**. Session: https://www.figma.com/design/Rj3WAO6IpUb48OFUerY7aW?node-id=108-127

The Figma views use exported native widget geometry, original vector scenes, imported shared buttons and a reusable feeling-card component with text/artwork properties. Continuous sliders, real source access, persistent session state and complete search run in the native app. The Figma prototype illustrates common paths.

## Verification and limits

27 automated checks pass in the Linux workspace. These cover actual card clicks and search, saving independent dimensions, cancellation, onboarding, capture failures, real recorded-video input, expression isolation, motion controls, local history and clean snapshot exit. A pixel-level check also verifies that card body colours and outlines render separately.

The Windows distribution was assembled with official embedded Python 3.13.17 and matching Windows x64 wheels. PE architecture, required Qt platform plugin, bundled C runtime, trained-model hash and ZIP integrity were checked. **Windows execution, physical-camera permission handling and target-device performance could not be verified in this Linux workspace.** Run `Check setup.cmd` for diagnostics; startup errors are written under `%LOCALAPPDATA%\CheckpointResearch\Checkpoint\startup-error.log`.

No training images or third-party reference downloads are bundled. The user's reference image is redrawn as scalable assets, not presented as a training dataset. Numeric slider defaults remain adjustable design suggestions; they are not population norms. Recognition with players, Indian-context validation and frustration reduction remain untested. Previous synthetic persona interviews are still synthetic. Model weights, benchmark accuracy and failed production release gates are unchanged.

The normal runtime does not record/upload camera frames or use a microphone. Derived history is off by default. App-scoped shortcuts are Ctrl+Shift+C (check-in), Ctrl+Shift+B (break) and Ctrl+Shift+P (pause capture); these are not global game hotkeys. No automatic game detection, game-event CV, OS startup service or automatic intervention is claimed.

## Reproduce source assets

`python -m checkpoint.app --no-setup` runs the source app. `python -m scripts.render_cards_app` recreates the current screenshots and scene catalogue. `python -m scripts.export_qt_design` exports geometry for Figma. The Windows assembly scripts are under `scripts/`; downloaded vendor runtime files stay under `build/`. Source and vendor provenance are included in the portable folder.
