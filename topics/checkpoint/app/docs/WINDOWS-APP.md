# Checkpoint Windows preview 2

[Download the Windows ZIP](https://github.com/AnujR17/Chatgpt-Environment/releases/download/checkpoint-v0.1.0-preview.2/Checkpoint-Windows-Preview.zip). Extract the entire archive, open the Checkpoint-Windows folder and run **Start Checkpoint.cmd**. Windows 10/11 x64 is the target; Python and Qt are bundled. Use **Check setup.cmd** for diagnostics.

## Face expressions

Tick **Track expressions (experimental)** beside the camera, then **Start camera**. The main card switches to **Live expression** and follows stable accepted expression estimates automatically. A local face video can be used instead. The card clears on uncertainty, a lost face, stale results or pause. Switch the card-source dropdown to **Your check-in** to view your own chosen word; your reported pleasantness and energy remain independent in both views.

The model predicts eight expression categories, not all 43 feeling words. It is unchanged and remains experimental: 77.1% held-out image accuracy and 29.8% external acted-video clip accuracy. Neither number measures gamer feelings or real-time webcam accuracy. Production release gates remain failed.

## Getting Over It

In **Settings**, enable **Observe the Getting Over It game window** and save. Return to the game. The app identifies its Windows foreground process and samples only its client area, twice per second. The context line can show **Possible climb**, **Possible fall**, uncertain movement, or a match to a player-marked start view. Use **Mark start view**, then switch to the desired game location to capture that in-memory reference. **Stop game tracking** clears it and stops observation.

These are optical-flow and reference-matching heuristics, not a trained game-event classifier. They have not been evaluated on actual Getting Over It recordings. They do not establish progress, death, restart, frustration or CMA. Borderless/windowed mode may be needed if fullscreen capture produces a blank frame. CS2/Valorant process identity is supported; their gameplay analysis is not.

## Privacy and verification

Camera and screen sampling are separate opt-in choices. Normal use does not save or upload camera/screen frames or use a microphone. The game view is not substituted for the face preview. Screen observation targets only the supported foreground game and stops on break, end or close. Optional local history stores derived player reports and session information; it is off by default.

34 checks passed in Linux, including actual recorded-video face inference, automatic native-card updates, report preservation, uncertainty clearing and synthetic scene-motion tests. The [Windows build](https://github.com/AnujR17/Chatgpt-Environment/actions/runs/41974006878) passed native launch plus live-card and GDI capture checks against its own Qt-window fixture. This is not evidence of physical webcam or actual game-event accuracy. The published ZIP was downloaded and checksum-verified. See [release verification](../../RELEASE-VERIFICATION.json).

Read [tracking controls and limitations](LIVE-TRACKING.md) for the required real-game validation. Earlier persona interviews remain synthetic. The current editable Figma file documents the earlier card design; the new live-tracking controls are implemented in the native app. No new primary research or model retraining was performed for this update.
