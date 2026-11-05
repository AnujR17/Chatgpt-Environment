# Data needed before automatic gamer CMA

The current model's external-video result fails the project bar. More training on the same held-out clips would invalidate their role as an independent test. No benchmark result establishes a player's internal mood.

1. Recruit consenting adult players for the intended setting, including the Indian contexts in the design brief. The five previous personas are synthetic and are not participants or training examples.
2. Obtain separate consent for camera recording, game-context collection, research retention, model training and sharing. Ordinary app use remains unrecorded. Do not turn on research recording implicitly through the camera-preview action.
3. Collect timestamped player reports of pleasantness, activation and frustration at agreed natural pauses. Keep frustration separate from anger and from a difficult-but-enjoyable challenge. Record unknown/mixed and prompt dismissals.
4. Align labels to a defined preceding time window. Use frame-level expression/action annotations only when independently annotated; a recording-level acted label cannot serve as ground truth for every frame.
5. Assign participants to train, validation and blind test before extracting frames. Keep every session and adjacent frame from one person in one split. Reserve additional people/settings for external tests.
6. Calibrate uncertainty on target-domain validation data, then freeze the model and thresholds. Test the blind set once, including no-face, headset/occlusion, pose and lighting conditions. Report participant-level intervals, class coverage, false prompts and failures, not only accepted-case accuracy.
7. Assess context and demographic representation through voluntary participant-provided metadata if needed, never by guessing attributes from their face. Do not claim Indian-context validity from the public benchmarks used here.
8. Compare usefulness, correction effort and interruption burden against manual check-ins before enabling automatic support. The current native app supports manual CMA and optional support without requiring the classifier.

The current 208 RAVDESS test clips remain a frozen reported evaluation of model v0.1. If they are reused for adaptation, label that as a new experiment and obtain fresh independent test recordings. Avoid selecting a new temporal crop or confidence threshold after seeing this test's errors.
