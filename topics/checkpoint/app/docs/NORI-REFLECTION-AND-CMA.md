# Nori: reflection, face preview and CMA

The character is now Nori. Its default job is to help a player notice a sustained pattern and choose a useful check-in, rather than copy every mouth movement. The alternative instant mirror remains valuable as a camera/model tester. Fully automatic labels for 43 felt emotions would not be supported by the available models or evidence; this implementation does not invent them.

## Three views

**Reflection** is the default. It observes a rolling 20-second window, requires at least 12 usable seconds across at least a 15-second span, and looks for consistent positive-looking or tense-looking visual cues. A qualifying pattern needs 70% support among usable intervals. It holds a display for at least 30 seconds before switching. These are proposed stability rules, not measured emotion accuracy. Mouth-hidden samples, dropouts and sparse tracking do not count as usable evidence. After a long loss of usable tracking, the visual reflection becomes unavailable/neutral-looking rather than asserting calm.

A short grin, grimace or hand gesture therefore does not immediately change the companion. A sustained suggestion is labelled as a visual pattern: focus, effort and frustration can look similar. Once the player checks in, that confirmed word/CMA takes priority and remains explicitly labelled as the last check-in, with its age. Camera cues never overwrite it. The smallest useful next evaluation is whether a player recognises the sustained suggestion as helpful and chooses a fitting check-in; software tests cannot establish that outcome.

**Face preview** shows individual movements for testing a webcam or someone else's local video. Opening a video selects this view; Reflection can also be selected during a long clip. Preview exposes independent eyes/blinks/widening, brow movement/asymmetry, smile, mouth widening, pressure, rounding, jaw opening, nose/upper-lip movement, visible-teeth cues and hand proximity. Face preview details lists all eight categorical model scores separately. Scores are not probabilities of a person's felt emotion. Sustained windows need regular tracking; the default is four samples per second.

**Your check-in** shows only the player's chosen word and adjustable CMA. All 43 vocabulary words now have distinct character profiles; they are illustrations for selection, not 43 trained camera classes. Similar feelings remain semantically close, so the word label is retained. The optional HSEmotion classifier still has eight broad classes and its previous limitations. Its weights and the earlier exploratory benchmark are unchanged.

## Teeth and hands

Smiling is separated from horizontal mouth stretch. Drawn brows with pressed/widened lips provide counter-evidence to a happy smile; cheeks and eye cues can support a genuine smile. Teeth are an independent appearance cue, not a happiness label. A conservative pixel heuristic looks for bright, low-chroma, horizontal regions strictly inside the lip aperture. It can still miss teeth or confuse highlights; it is not a separately validated teeth classifier.

The bundled provider-trained Google MediaPipe Hand Landmarker supplies 21 landmarks per hand. Hand-to-mouth is a 2D geometric proximity/overlap estimate, not proof of physical contact or anxiety. Possible mouth occlusion masks smile, jaw and teeth cues and withholds the categorical estimate. A briefly lost face may still show the hand gesture using a recent mouth region; it does not invent the hidden expression. Hand details appear in Face preview, not as copied gestures in Reflection.

The hand task is bundled under checkpoint/assets so compatible 0.3 installations can receive it in a normal small app update. No new Python/native runtime dependencies are needed. Its URL/hash are in artifacts/hand-landmarker-provenance.json. The provider's hand example produced two hands with 21 points each; this is a smoke check, not hand-to-mouth accuracy. Real occlusion/teeth performance on the user's webcam remains unvalidated.

## CMA and report

CMA here means the circumplex model of affect: pleasantness/valence and energy/activation. Vocabulary coordinates are adjustable design starting points, not universal empirical norms. User-confirmed coordinates modulate Nori's body colour, stretch and energy in check-in views. Automatic face/mouth cues do not establish either axis.

The report now shows the check-in journey on both axes, first/latest and most activated check-ins, region counts, a reflection and a next-session prompt. Counts describe samples, not time spent in an emotion. Dashed connections are visual guides; unreported time is unknown. Optional tracker context is aggregate visual-pattern information, not an emotion-duration chart. No per-frame facial event list or raw input timeline appears in the report. Both the native Report view and paired phone export a readable PDF. With no check-ins, the report explains what is missing instead of fabricating a mood history.

## Move Nori

Nori stays frameless, transparent and click-through during play. Hold **Ctrl+Alt**, then drag the character; release to lock it again. The tray's **Move Nori** action and Settings offer a temporary 30-second move mode. Position is clamped to an available screen and saved in the app's preferences. Only modifier states are checked for dragging; no character text, key identities, game hooks or injection are added. Physical dragging across the user's actual monitor/game setup remains a target-device check.

## Evidence and sources

Tests exercise sustained-window/hold rules, brief-expression rejection, check-in priority, hand occlusion, teeth-mask heuristics, 43 profile coverage, CMA modulation, dragging persistence, PDF generation and authenticated phone PDF download. Native render examples use labelled synthetic inputs. The hand example, recorded-face mapping, native Windows model loading and updater tests are separate evidence. None establishes 43-emotion accuracy, intervention effectiveness or a person's internal mood.

Sources: [Russell's circumplex model](https://doi.org/10.1037/h0077714), [MediaPipe hand landmarks](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker), [Face Landmarker](https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker), and [limits of inferring emotions from facial movements](https://pubmed.ncbi.nlm.nih.gov/31313636/).
