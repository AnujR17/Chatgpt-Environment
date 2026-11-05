# Video sources, trained elements and pretrained facial models

The seven-source list is in design/gameplay-video-shortlist.csv and .json. Six YouTube candidates cover full runs, techniques, an obstacle, a setback and an ending. Search/creator metadata is not visual review. A direct download attempt was rejected by the workspace proxy with HTTP 403; no YouTube video was downloaded, labelled or used for training, and no access-control workaround was used.

The publisher-hosted official Steam trailer was accessible. Its 43.3 seconds were downloaded as video-only data, hashed and inspected through a contact sheet. No raw video is redistributed. We manually labelled visible opening-lake, rock-slope, grey-rock/pipe and title/non-game views, excluding transition boundaries. Code: ml/train_game_scenes.py. Annotations: design/game-scene-annotations.json. Features: spatial colour summaries and HSV histogram, with most subtitles excluded. A logistic scene classifier was fitted on 50 training frames, selected by 20 validation frames, then evaluated on 47 held-out frames from different time blocks of the same trailer.

Validation balanced accuracy was 100%; held-out frame accuracy was 78.7%, balanced accuracy 75%. It confused every held-out opening-lake frame with rock slope. This is one short edited source with correlated frames, not independent-video, full-map or event-recognition validation. The resulting game-scene-model.json is an exploratory research artifact and is NOT used to issue live location cues or nudges. Actual game-event training still needs accessible, usable, labelled unedited gameplay with independent videos for evaluation. No player-emotion labels were invented from streamer appearance or titles.

## Existing face models — no personal emotion-photo set

Google MediaPipe Face Landmarker is now the default physical-face mapping engine. The bundled task model is provider-trained and maps visible eye, brow and mouth movement. It is not a felt-emotion or CMA model. Model version/URL/SHA-256 are in face-landmarker-provenance.json; model bytes are unchanged. Optional neutral calibration subtracts observed relaxed offsets in memory, rather than training on a collection of posed personal photos.

The existing HSEmotion enet_b0_8_best_afew ONNX model was also obtained from its provider and tested against our earlier classifier using the matched frozen protocol: 208 RAVDESS actor 01–04 acted speech clips, ten frames in each clip's middle 60%, identical YuNet face/quality gating, and mean probabilities. Calm is excluded, and errors into contempt still count. No weights or confidence threshold were trained/tuned on those clips.

| Model | Clip accuracy | Macro-F1 on supported truth classes |
| --- | ---: | ---: |
| Earlier in-project classifier | 29.8% | 0.251 |
| Provider-trained HSEmotion | 62.5% | 0.603 |

The HSEmotion pipeline median was 28.4 ms per sampled frame, p95 36.4 ms on this CPU environment; this excludes decoding, UI, sampling delay and game frame-time impact. Its anger recall was 56.3%; neutral recall 50%. The new classifier is better on this exploratory comparison, not universally accurate. Four acted actors and unknown overlap with provider training data do not establish gamer, Indian-context, personal webcam or felt-emotion accuracy. A fresh target-context test is still needed. The default movement mapper avoids requiring the category classifier to call a face angry before Pip can draw lowered brows. Original weights/metrics are retained for reproducibility.

Details and clip records: artifacts/pretrained-comparison.json. Adapter preprocessing follows the provider's RGB/ImageNet normalization and reorders its eight outputs into the existing project label contract. HSEmotion display abstention at .7 is a conservative presentation threshold, not calibrated probability of a person's emotion. Neither engine sets player CMA or diagnoses mood/frustration.

Sources: https://github.com/av-savchenko/hsemotion-onnx ; https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker/python ; https://store.steampowered.com/app/240720/Getting_Over_It_with_Bennett_Foddy/ ; https://zenodo.org/records/1188976 . Provider code licences are preserved under third_party; underlying datasets and publisher content retain their own terms.
