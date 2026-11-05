# Current application: Windows reference-card build

The latest build is documented in **WINDOWS-APP.md**. The portable Windows archive is `Checkpoint-Windows-Preview.zip`, with its own Python/Qt runtime and Start Checkpoint.cmd launcher. Current screenshots are named `artifacts/cards-app-*.png`. Figma page 11 uses actual native widget geometry and editable card components: https://www.figma.com/design/Rj3WAO6IpUb48OFUerY7aW?node-id=108-127

The supplied reference contributes 39 vocabulary words and the outlined character direction. Four existing project words bring the full library to 43. Eight common cards appear first. Native flows are functional; 27 checks pass in Linux. Windows runtime packaging is statically verified; launch and physical-camera behaviour still need a Windows PC. See WINDOWS-APP.md for exact limits. Earlier explorations below are retained for comparison.

---

# Current review — organic emotion family

The latest visual refinement is documented in `design/ORGANIC-REFERENCE-STUDY.md`. Figma page **10 Organic emotion family** and `artifacts/organic-emotion-library.png` are the current review surface. The actual native UI is `artifacts/organic-emotion-ui.png`, with dark, selector, check-in and unreported examples beside it. The 24-second native animation is `artifacts/organic-emotion-motion.mp4`.

Library: https://www.figma.com/design/Rj3WAO6IpUb48OFUerY7aW?node-id=98-87

Screen: https://www.figma.com/design/Rj3WAO6IpUb48OFUerY7aW?node-id=98-331

References/rationale: https://www.figma.com/design/Rj3WAO6IpUb48OFUerY7aW?node-id=100-766

Wireframe: https://www.figma.com/design/Rj3WAO6IpUb48OFUerY7aW?node-id=100-786

The character family uses common ink, rounded asymmetry, a muted palette and grounded posture. Motion has a longer exhale, small weight shifts and excitement anticipation. Illustration colours do not encode measured valence or arousal. CMA remains a separate self-report. Figma supplies editable illustrations and example flows; the native app supplies actual animation, source capture, continuous sliders, cancellation and local session state. Neither interpretation accuracy nor perceived warmth has been validated with participants.

The previous design handoff follows for comparison. Its page 09 assets are historical; the model evaluation and runtime/privacy facts remain applicable.

---

# Current emotion library — 4 November 2026

The user clarified that emotion compositions should be visibly distinct and intuitive, rather than slight variations of one contour family. The current main view uses eight semantic gestures. The earlier continuous-CMA study is preserved as a separate exploration.

## Review assets

- Eight-symbol sheet: `artifacts/emotion-library.png`
- Native light screen: `artifacts/emotion-ui-library.png`
- Native dark screen: `artifacts/emotion-ui-library-dark.png`
- Actual procedural animation, 24 seconds / 1280×720 / 30fps: `artifacts/emotion-library-motion.mp4`
- Native visual selector: `artifacts/emotion-library-dialog.png`
- Native word/dimension check-in: `artifacts/emotion-library-checkin.png`
- Editable Figma library: https://www.figma.com/design/Rj3WAO6IpUb48OFUerY7aW?node-id=86-42
- Active screen: https://www.figma.com/design/Rj3WAO6IpUb48OFUerY7aW?node-id=86-325
- Rationale: https://www.figma.com/design/Rj3WAO6IpUb48OFUerY7aW?node-id=88-648
- Wireframe: https://www.figma.com/design/Rj3WAO6IpUb48OFUerY7aW?node-id=88-670

Figma page **09 Distinct emotion library** is the current review surface. Page 08 retains the prior continuous-CMA exploration. The library and screens contain editable vectors, text and component instances. Source scene descriptions are shared between native Qt and Figma generation.

## Native behaviour

Open Emotion library to see all eight gestures. Select a feeling, adjust pleasantness and activation independently in the check-in, then Save. Selecting a symbol alone does not commit a report. Cancel preserves the prior native report and coordinates. Mixed/unreported has no assumed state.

The chosen word controls the semantic symbol, while the two CMA dimensions are separate self-reports. No graph or quadrant is needed. Confused and bewildered describe uncertainty and interpretation; CMA cannot uniquely identify their cognitive meaning. Slider starting positions are adjustable design suggestions, not measured emotion norms. They require an anchoring-bias study.

Each symbol has restrained movement appropriate to its proposed gesture. A 450ms fade with a small settle handles transitions between different shapes. Pause and Reduce motion retain the same static symbol. Hidden and inactive views stop animation timers. Source capture, camera preview, break/end handling, opt-in derived history and local-only processing remain functional. Camera is off by default; no gameplay display is added.

Figma demonstrates discrete word selection, saving and example session paths. Device/file access, arbitrary slider positions, actual procedural animation, persistent cancellation/return state and local history run in the native app. Figma follow-up destinations illustrate a path rather than simulate a complete persisted runtime.

## Evidence

`artifacts/emotion-tests.xml` records 23 passing checks covering validated dimension inputs, eight distinct scene geometries, library selection before commitment, cancellation, motion lifecycle, actual video capture, expression isolation, history and clean snapshot exit. Distinct geometry is a software property; it does not prove emotion recognisability.

The eight symbols rendered at approximately 0.1–2.2ms per frame in this Linux offscreen drawing check; see `artifacts/emotion-symbol-profile.json`. This does not establish battery usage, performance beside a running game, physical-camera performance or an advantage over a browser. Target-device testing remains necessary.

The research basis, per-symbol meaning and planned recognition study are in `design/SEMANTIC-EMOTION-LIBRARY.md`. No primary study, Indian-player decoding accuracy or reduction in gaming frustration is claimed. Existing synthetic persona interviews remain synthetic. The facial model and its failed production release gates are unchanged; expression cues cannot select a symbol, CMA state or intervention.
