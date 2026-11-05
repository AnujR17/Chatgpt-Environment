# Pip — Windows, desktop companion and phone

Pip is one original soft blob. Its contour, colour, brows, eyes and mouth interpolate within the same body. It does not swap characters between expressions. Neutral has a straight mouth and relaxed brows; missing detection uses the same flat neutral appearance with an explicit unavailable/no-face status, not a measured neutral emotion.

## Start

Extract the whole Windows ZIP into a new folder and run Start Checkpoint.cmd. Tick **Track my face**, then **Start camera**. The default engine maps physical face movements through Google MediaPipe Face Landmarker. It runs locally with bundled weights; there is no startup model download or personal emotion-photo collection.

**Set my neutral face** optionally measures eight relaxed samples in memory. No images are saved. Settings offers **Pip facial movement strength** to adjust visible movement amplitude. It does not make a model more certain that you feel angry. Settings also offers **HSEmotion expression estimates**, a provider-trained eight-category classifier. The original research classifier is retained only for reproducibility.

## Frameless desktop Pip

**Show Pip** creates a transparent top-level desktop companion, with no panel, title bar, taskbar entry or game injection. During play it is click-through and does not take focus. Settings chooses a corner; **Move Pip on the desktop** enters a temporary drag mode and Done restores click-through. Leaving the app also restores click-through. The companion is about 132 logical pixels, inside a small transparent window; a brief optional nudge appears above it.

Borderless/windowed mode is recommended. Exclusive fullscreen, protected surfaces and game-specific anti-cheat restrictions can hide or reject ordinary desktop overlays. Actual game compatibility and frame-time impact still require a check on your PC. No universal compatibility or lower-power-than-browser claim is made.

## Phone dashboard

Click **Phone dashboard**, put both devices on the same trusted private Wi-Fi, choose the laptop's Wi-Fi address if several are listed, and scan the QR. The dashboard opens in your phone browser; no store installation or phone inference is required. It shows the same Pip, current movement/expression label, player-reported CMA, experimental game cues, recent session moments, and a report download.

A random per-sharing-session token protects the read-only data endpoints. The pairing link carries it in the URL fragment; the page removes the fragment and retains the token only for that browser session. No camera/game images, raw face landmarks, typed text or key identities are sent. This local preview uses HTTP, not encrypted transport; use a trusted private network and allow the Windows app on Private networks if prompted. It is not a public internet dashboard. Router client isolation, a VPN address or a firewall may block physical-phone pairing; loopback/browser verification is separate from that hardware/network check.

Closing the pairing dialog keeps sharing active. Reopen it and choose **Stop phone sharing** to revoke the link. Closing Checkpoint also stops sharing. A lost connection clears the phone's live appearance to neutral and displays Disconnected. Reports must be downloaded before closing the laptop app if you want to keep the derived timeline.

## Game, input and nudges

In Settings, enable **Observe the Getting Over It game window** for opt-in screen sampling. Windows process identity selects the supported foreground game; only Getting Over It receives screen analysis. The current live cues remain experimental optical-flow estimates of camera movement and a player-marked start reference. They do not establish a fall, restart, progress percentage, frustration or the full game route.

**Observe game-focused mouse and key timing** uses Windows Raw Input while a supported game has focus. It keeps bounded 100 ms aggregates of relative mouse movement, clicks, key counts and key-hold duration. No characters or key identities are exported; hold durations are capped at ten seconds. Other apps' events are discarded immediately. An ordinary keyboard/mouse does not measure key/click force. These aggregates are not an emotion score.

Optional quiet nudges require game observation and input timing. After a possible setback, Pip waits until input has been quiet for at least three seconds, with at least two minutes between invitations. It does not trigger from an anger label alone, pause the game or inject controls. Helpfulness and timing are not validated outcomes. Camera, game tracking and raw input stop on break, session completion or app exit; returning does not silently restart them.

## Report and evidence

The laptop's **Report** view and phone **Download session report** export JSON with player reports, source-labelled recent moments and optional numeric input aggregates. Live moments are capped at 240; input snapshots retain at most 360 five-second samples. These are observations/estimates, not a proven emotional history. Check-in retention remains opt-in and separate from explicitly exporting a full derived report. Normal use records no raw video or screenshots.

Local automated and mobile-browser checks are in artifacts/pip-tests.xml and artifacts/pip-phone-verification.json. Browser screenshots use synthetic UI cues, not a participant or accuracy test. Windows build checks cover native launch, own-window GDI, overlay focus/style, Raw Input registration, model loading/inference and the authenticated loopback API. Physical webcam performance, actual phone Wi-Fi, full-screen game behaviour and real Getting Over It event accuracy remain target-device checks.

Camera will not start, or the phone QR link will not load? See [camera and phone troubleshooting](CAMERA-AND-PHONE-TROUBLESHOOTING.md). The updated build tries DirectShow first and lets you choose another camera. The pairing dialog includes adapter names, a laptop link test and an explicit Windows Private-network firewall helper.
