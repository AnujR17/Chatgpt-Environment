# Nori: live reflection, movement test and CMA

This build replaces the slow 20-second reflection window and 30-second hold. Nori remains a frameless, draggable desktop character, with the same local phone companion and check-in report. [Research, alternatives, model comparison and plan](REBUILD-RESEARCH-AND-PLAN.md).

## Start and choose a view

Select **Start face tracking**. That explicit action enables local analysis and opens the selected camera; capture remains off on launch. The preview appears while models initialize. If a model fails, the camera preview continues and the interface explains the failure. Camera selection, Windows DirectShow fallback, pause and restart remain available. **Open video** deliberately enables tracking for a local file and selects the movement tester.

- **Live reflection**, the default, shows a smoothed expression using authored Nori poses. The proposed evidence dwell is 0.45 seconds (0.65 for neutral), at least three observations, with adaptive feature filtering and no long lock. A separate four-second trend sentence reflects recent visual consistency. These are engineering choices, not psychological definitions of how long an emotion lasts.
- **Movement test** maps the visible facial/hand movements directly. Use **Inspect face signals** for individual features, tracking availability and eight-class scores. This is the diagnostic view; it does not set your CMA.
- **My check-in** shows your selected word and adjustable pleasantness/energy. A check-in updates the report and this view; it never freezes Live reflection. All 43 vocabulary words are selectable illustrations, not 43 trained camera classes.

Neutral is a flat mouth. An unavailable or hidden face also has a neutral appearance, with an explicit unclear/unavailable label rather than a claim of calm. A valid resting expression has a separate Neutral expression label. The camera/inference worker retains one latest frame and drops stale work rather than replaying an old queue.

## How recognition affects the character

The existing provider-trained HSEmotion B0 model supplies eight broad expression scores alongside MediaPipe face/hand geometry. The larger B2 candidate did not improve overall accuracy in the exploratory comparison and was slower; see the research record. Model scores are not probabilities of a person's inner feelings.

A smile needs compatible mouth/cheek evidence or model support. Mouth widening, talking, visible teeth and drawn brows alone are insufficient for a happy or angry label. A tense-looking mouth/brow configuration may be reflected as a visual pattern without claiming anger. Conflicting signals become unclear. The character changes an authored pose rather than copying every blink or small lip movement; a supported open-smile configuration has restrained laugh-like motion. Visible teeth can modify supported smile/tense poses without turning a tense mouth happy. Teeth remain a conservative image heuristic, not a validated teeth model.

The hand model estimates proximity/overlap with the mouth. A possible hidden mouth immediately withholds those cues. Hand-to-mouth is not proof of contact or anxiety. Inspect face signals exposes the tracker state; no hidden expression is invented. Optional neutral calibration stores only a short-lived in-memory baseline, not photos.

These gates trade coverage for fewer forced labels. Video smoke checks still show substantial uncertainty and missed acted expressions. This repair does not establish dependable eight-class recognition on the user's webcam, 43-emotion accuracy or frustration detection. No personal emotion-photo collection is required.

## CMA and report

The circumplex model describes reported pleasantness/valence and energy/activation. The report uses only player check-ins for coordinates, first/latest/most-activated moments, region sample counts and the journey. Counts are check-ins, not emotion durations. Unreported time stays unknown. Optional aggregate visual context is labelled separately; no per-frame facial log appears. Desktop and paired phone export a PDF.

## Desktop and phone

**Show Nori** enables the transparent, frameless, click-through companion. Hold **Ctrl+Alt and drag**, then release to lock it; the tray's **Move Nori** action offers a temporary move mode. Position is saved and clamped to an available screen. No game injection or text capture is used.

**Phone dashboard** pairs over the same trusted private Wi-Fi. The phone receives the same reflected pose, recent-trend text and reported CMA. It receives no camera/gameplay images. Open the app's pairing dialog for network/firewall recovery; see [camera and phone troubleshooting](CAMERA-AND-PHONE-TROUBLESHOOTING.md). Physical phone Wi-Fi and game/fullscreen compatibility still need target-device checking.

## Updating and evidence

Use **Settings → Check for updates → Update and restart**. This release preserves the pinned native runtime and existing face/hand weights, so compatible installs can use the small app package. Model/runtime mismatches use the full fallback automatically. Capture stays off after restart.

Evidence includes deterministic response traces, isolated spikes, uncertainty, model disagreement, no-face/hand occlusion, source changes, check-in separation, actual local-video processing, native renders, phone polling/PDF and Windows package/updater fixtures. Synthetic previews and software checks are labelled; none proves the companion reduces gaming frustration.
