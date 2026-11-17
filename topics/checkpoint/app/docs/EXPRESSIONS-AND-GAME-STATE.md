# Checkpoint 0.6: expressions, character and game state

17 November 2026. User-authorised implementation and OTA publication on `topic/checkpoint`. The separate session-study branch is preserved.

## What changed

The default **Expressions** view uses short names rather than a running description: Neutral, Happy, Laughing, Angry, Sad, Surprised, Disgusted, Fearful, Smirk, Tense and tentative **Confused?**. The main caption is hidden; the small source label says Expression estimate. Movement test and Inspect face signals retain technical details. Nothing writes camera labels into the player's CMA check-ins.

Nori uses an original rounded contour with a shallow two-foot base, no heavy body outline, navy facial features, curved quadratic brows, an offset questioning brow, refreshed mint/ochre/coral/periwinkle colours, and a small mitten without finger stripes. These are design choices inspired by the supplied reference's softness, not copied character artwork. The same geometry and face treatment run in Qt and the phone canvas. Fixed-topology contours and time-based interpolation keep state changes smooth. Face loss flattens the expression immediately while body colour returns gently. Reduced motion skips decorative easing.

## Facial movement research and implementation

| Signal | Why retain it separately | What this build does |
| --- | --- | --- |
| Brow lowering / furrow | Can occur with anger, effort and confusion | Keep the pretrained category where supported; brows alone do not assert anger |
| Inner-brow raise with furrow and lid tightening | Reported in confusion research, but overlaps with other states | Require a sustained combination and low smile/mouth-pressure/blink counter-evidence for Confused? |
| Outer brow asymmetry | Useful for rendering an authored questioning look | Curve and offset the two brows rather than drawing identical straight lines |
| Eye widening, brow raise and jaw opening | Multiple regions give more evidence than mouth opening alone | Add a surprise-like fallback only for the combination |
| Smile, cheeks, jaw, stretch, press and snarl | Speaking or stretching the mouth need not indicate happiness | Preserve smile counter-evidence and the separate open-smile/laugh configuration |
| Hand over mouth / face loss | Hidden features cannot be reliably recovered | Withhold the expression; retain a flat unknown appearance |

MediaPipe blendshapes approximate visible facial actions; they are not FACS ground truth. `brow_furrow`, `brow_inner_raise`, `eye_squint`, `eye_wide` and blink now remain separate through inference instead of disappearing into one signed brow value. Existing neutral calibration covers outer brows and squint as well. The new confusion rule is a transparent, unvalidated heuristic, not a newly trained ninth class. Its thresholds are engineering choices. The existing eight-class model is unchanged and retains its documented limitations.

Voluntary and spontaneous expressions both occur. Brow raising, smiling and even an eye-constricted smile can be deliberately produced; timing and muscle combinations do not let this app certify whether an expression is involuntary or whether a person truly feels that emotion. The app makes no authenticity, deception or microexpression claim. It can run on the camera or a local facial video without a game running.

Sources consulted:

- [Google's blendshape model card](https://storage.googleapis.com/mediapipe-assets/Model%20Card%20Blendshape%20V2.pdf): avatar-oriented coefficients, landmark noise, occlusion and lighting limitations. The model card was read directly.
- [MediaPipe Face Landmarker documentation](https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker): 52 blendshape outputs and independent facial signals.
- [D'Mello, Confusion chapter](https://home.cs.colorado.edu/~mozer/Teaching/syllabi/TopicsInCognitiveScienceSpring2016/DMelloConfusion-Reprint.pdf): facial action combinations and verbal-report context. Indexed excerpts were available; direct PDF access timed out. This is not validation on gamers.
- [Schmidt et al., deliberate and spontaneous facial movement](https://pmc.ncbi.nlm.nih.gov/articles/PMC2843933/): deliberate smiles can include eye constriction. The indexed paper text was available; the direct page presented a browser challenge.
- [Barrett et al., Emotional Expressions Reconsidered](https://pmc.ncbi.nlm.nih.gov/articles/PMC6640856/): facial movements do not uniquely reveal inner emotion.

## Game state that is actually connected

**Track game** now enables foreground process detection and screen observation together. Previously the button enabled only process detection. The Windows capture checks the actual foreground game window before and after copying its client area. Other applications are rejected. Sampling remains twice per second, with frames kept locally in memory.

The tracker publishes a structured state to the desktop and paired phone: climbing/falling estimates, steady/no clear vertical movement, uncertain, changed view, unavailable, out of focus, or a matched marked view. Forward/backward optical flow plus a robust background transform reject incoherent changes, zoom and rotation. Counters describe possible sustained camera-motion runs, not deaths or confirmed player failures.

**Mark section** asks for a name and samples the next foreground game frame. ORB descriptors and a checked homography recognise that view again; up to eight references exist in RAM for the same game process. No frames or descriptors are sent to the phone or persisted. Matching a view does not establish a restart or whole-map location. Resizing substantially can require marking again. Ending tracking clears references. The old single-trailer colour classifier is not promoted into a full-route detector.

Limits: camera motion cannot see every jump when the camera is stationary. This is not a death, menu, completion or exact-height detector. Exclusive fullscreen/protected surfaces may block GDI capture. Input activity and game state cannot establish CMA. No game memory reading, injection, save editing or input automation was added.

## Verification

- Six new policy/vision regressions cover confusion counter-evidence, temporal qualification, missing faces, CMA separation, surprise counter-evidence, named views, sustained motion counts and zoom rejection.
- The local full suite passed 100 tests with 5 skips. Native UI checks exercise all six displayed examples, hide commentary, retain flat unknown, and export independent game state to the phone payload. Native renders use labelled synthetic signals.
- Actual Chromium phone checks cover live state updates, the character, hand masking/teeth, reduced motion, CMA PDF download, no overflow and no JavaScript errors. These are loopback browser checks, not a physical phone/Wi-Fi trial.
- The actual official Steam trailer was downloaded as a local video-only research copy, inspected as a contact sheet, and replayed at 2 Hz: 87 samples. It yielded unavailable/uncertain/steady/view-changed states, with no sustained climb/fall output. This edited trailer does not measure continuous-play event accuracy. See `artifacts/game-state-trailer-replay.json`.
- Windows release checks must pass native launch, real face/hand model loading, a public provider portrait inference, new expression/game-state checks, game-window capture, overlay focus/transparent behaviour, and updater successful restart/failed-start rollback before publication. A provider portrait is not emotional ground truth.

No new target-player accuracy, 43-class recognition, involuntary-expression detection, game-event accuracy, power saving or benefit claim is made. Actual webcam/gameplay/phone-device testing remains necessary. No raw research video, provider image or user photo is bundled.

## Update and use

Use **Settings > Check for updates > Update and restart**. The compatible app-only payload keeps the existing runtime and model weights. Camera and screen observation start off after restart. Choose **Start face tracking** for expressions; choose **Track game** while playing Getting Over It for game vision. Use **Mark section** if you want a specific view recognised on return. Phone pairing works as before on a trusted private LAN.

## Publication verified

Release `checkpoint-v0.6.0-preview.1` targets code commit `c223b27b127f2d0c52834067843bcc97f26a08fc`. [Windows run 44067117607](https://github.com/AnujR17/Chatgpt-Environment/actions/runs/44067117607) passed all release checks, including actual model inference on Google's public portrait, new native expression/game-state cases, game-window capture and actual Windows updater restart/rollback fixtures.

The public previous-version updater discovery and actual download/staging passed for the 6,148,689-byte app-only payload: all 83 declared file hashes match; runtime/model compatibility chooses the small package; the disposable old installation is preserved. No downloaded code was executed during staging. The full public ZIP returns HTTP 200 with a ZIP signature, and its checksum agrees across the manifest, sums and GitHub asset digest; this public check did not download the entire full ZIP. See [the release verification record](../../RELEASE-VERIFICATION.json). Additional native-to-Chromium checks show Confused? and a named game section together without commentary or JavaScript errors. These remain software fixtures, not a user-device or real-play validation.
