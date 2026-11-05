# Checkpoint Windows preview 2 — live expression cards and game observation

Extract the whole ZIP and run Start Checkpoint.cmd. This update fixes the missing connection between expression results and the large card: enable Track expressions (experimental) and start the camera, or open a local face video. Stable accepted estimates now update Live expression automatically. Your manual feeling and CMA stay independent.

Settings also offers opt-in Getting Over It foreground-window observation. Sustained optical flow provides possible climb/fall cues; a player-marked start view can be matched. These are unvalidated heuristics, not a trained game-event or frustration detector. No raw screen/camera recording or upload occurs in normal use.

34 checks passed in Linux, including real recorded-video face inference and card updates. The Windows build additionally gates publication on native launch and card/GDI capture fixture checks. Physical webcam, real Getting Over It event accuracy and game-performance checks remain outstanding. The expression model is unchanged: 77.1% held-out image accuracy, 29.8% external acted-video clip accuracy, failed production gates. The app remains an unsigned research preview.

See topics/checkpoint/app/docs/LIVE-TRACKING.md for controls, limitations and the next validation steps. Vendor runtime hashes are verified during assembly; the published SHA256SUMS.txt verifies the package.
