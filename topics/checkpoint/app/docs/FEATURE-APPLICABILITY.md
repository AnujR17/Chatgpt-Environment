# Planned features and implementation status

This maps the design brief to the native research build. “Implemented” means code exists; verification scope is stated separately.

| Planned feature | Status | Applied behaviour and evidence |
| --- | --- | --- |
| Native desktop companion | Implemented | Qt Widgets, local Python/ONNX runtime; no browser or embedded web engine. Portable Windows x64 folder assembled with embedded Python and matching native wheels. Linux rendering/flow tests and package integrity pass; Windows execution/camera permission still need a target PC. |
| Select game and intention | Implemented, manual | Setup supports game/intention and competitive context. No automatic game identification is claimed. |
| Camera or local video | Implemented | Explicit source action, bounded worker, local preview. Tested with actual RAVDESS video files; physical webcam and target-OS permission handling remain unverified. |
| Facial-expression model | Implemented, experimental | Actual FER+ training, validation-only calibration, model selection, untouched image test and separate external video evaluation. Results are generated in artifacts; this is not a mood/frustration classifier. |
| Automatic CMA or frustration recognition | Unavailable | FER+ does not contain continuous valence/arousal or gamer frustration labels. No categorical-expression-to-CMA conversion is used. Requires paired consented gamer video and player self-reports. |
| CMA visualisation | Implemented | 43 poster-referenced cards replace the graph, with eight common choices and a searchable full vocabulary. The selected word sets the gesture; separate player-reported pleasantness and activation remain visible as text. See docs/WINDOWS-APP.md. |
| Player correction and manual mode | Implemented | Eight common choices, all 43 cards through search, Not sure and two independent sliders. The library opens before the check-in; Save commits, Cancel preserves the previous report. Older vocabulary remains readable. Works with capture and analysis off. |
| Game-event CV / supported game telemetry | Deferred | Manual game context is available. No universal game understanding, score tracking, death detection or hidden screen capture is fabricated. |
| Light/dark theme and motion controls | Implemented | Warm light default, dark toggle, Pause motion and Reduce motion in Preferences. Hidden, unknown, paused, break and ended states stop animation timers. Render timing in artifacts/emotion-symbol-profile.json is cloud/offscreen only. |
| Emotion shapes empirically validated | Not yet | CMA supports two dimensions. Coordinates, geometry and colour are adjustable design hypotheses. A recognition and CMA study plan is in design/SEMANTIC-EMOTION-LIBRARY.md; no decoding or intervention-efficacy results are invented. |
| Optional microphone | Unavailable | No microphone capture or voice emotion analysis. No fake permission toggle is shown. |
| Quiet prompts / suitable moment | Applied conservatively | Support is user-requested. No automatic nudges are triggered by an expression or setback. Competitive mode does not interrupt gameplay. |
| Optional break | Implemented | Actual 30-second countdown, early exit, camera/video stops. Timer completion and return never resume capture. |
| Pause, source loss, end, exit | Implemented | Stops worker, clears frames and cues, rejects stale results. File EOF and capture failure recover to manual mode. Tested on video; hardware driver stalls remain a target-device check. |
| Retention and deletion | Implemented | Retention off by default. Explicit opt-in saves derived reports/duration/game only. Exact local summary file can be deleted; imported video files are never deleted. |
| Support suggestions | Implemented, user-controlled | Technical, communication, challenge and break options. No game input injection, automatic mute/report, OS privilege or difficulty changes. |
| Settings / frequency | Implemented | Experimental analysis opt-in, summary retention and bounded 0.25–5 Hz analysis. Applying changes pauses capture. |
| Tray / shortcuts | Implemented where supported | App-scoped keyboard shortcuts and a tray menu when Qt reports system-tray availability. Offscreen environment cannot verify a real OS tray or global hotkeys. |
| Startup service / automatic launch | Deferred | No privileged service or automatic startup installation. |
| Lower power than a browser | Not established | Local latency, memory and CPU measurements are reported with test conditions. No game frame-time, GPU, battery or same-hardware browser comparison has been performed. |
| Primary research / Indian-context validation | Not conducted | Earlier persona interviews remain synthetic. Benchmark demographic labels are inadequate for Indian-context performance claims. New participant research is required. |
| UI approval | Pending | Revised native light and dark screenshots, actual motion MP4, emotion atlas and editable Figma revision are supplied for review. No user approval is assumed. |

No public deployment, research-data upload, automatic camera access or production-readiness claim is part of this delivery.

