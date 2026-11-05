# Current face engines — Pip preview

Default: provider-trained Google MediaPipe Face Landmarker, task version float16/1. It supplies physical brow/eye/mouth movements and does not estimate felt emotion or CMA. We did not train its weights. URL/hash: face-landmarker-provenance.json. Neutral calibration is optional, local and in memory; no personal photo collection or model fine-tuning is required.

Alternative: provider-trained HSEmotion enet_b0_8_best_afew ONNX. On the matched exploratory 208 RAVDESS acted-video clips, accuracy is 62.5%, macro-F1 .603, versus the archived original classifier's 29.8%/.251. Anger recall 56.3%, neutral recall 50%; do not claim individual reliability. No weights/thresholds were tuned on these clips. See pretrained-comparison.json and ../docs/VIDEO-AND-MODEL-RESEARCH.md for protocol, selection limits, provider overlap uncertainty and source links. No gamer, Indian-context or felt-emotion accuracy is established. Automatic player CMA remains unavailable.

The game-scene classifier is a separate single-trailer research trial, not a facial model or validated event detector, and is not used for live scene/cue decisions. Production affect-detection readiness is not claimed for any engine.

## Archived original classifier and benchmark

# Checkpoint expression model / research model card

Status: experimental; not production ready. Automatic CMA and frustration prediction are unavailable.

## Intended use

Local, opt-in testing of eight crowd-annotated facial-expression categories in an academic gaming-companion prototype. The app's CMA values come from player check-ins. Expression cues cannot overwrite them, change games, or trigger automatic interventions.

This model is not a mood, frustration, stress, mental-health, identity, protected-attribute or continuous valence/arousal estimator. Benchmark category labels are not observations of an internal emotional state.

## Model and data

Selected candidate: **transfer**, chosen using validation macro-F1 only. No test set was used for selection or calibration. Model SHA256: `b0e28051075f6f9ed200bbd9e510c451d2e05ceb3fab0d548cb5e9b3942da466`. Calibration SHA256: `c0662dc619d9ce2f55d6742c4e49b77dd4b3bf47a10b7ce80a75de89697ab66b`.

FER2013 images with FER+ ten-tagger vote distributions: 25,275 training, 3,329 validation, 3,360 eligible held-out images. Split/eligibility rules, rejected counts and hashes are in data/manifest.json. Exact pixel and coarse quantized-signature duplicates were removed across splits; identities were unavailable, so this does not prove subject independence. Original dataset rights remain a deployment/redistribution review item.

Compact CNN: trained from scratch, stopped after 23 completed epochs and preserved as a baseline. Transfer candidate: MobileNetV3-Small with ImageNet-1k object pretraining, fine-tuned on the same facial dataset. No pretrained facial-expression weights were used. Both use 48x48 grayscale input; the transfer graph includes its own 96x96 RGB expansion and ImageNet normalization.

Training uses soft crowd vote targets. Temperature scaling uses hard plurality-label NLL on validation only. Temperature 0.6945; confidence acceptance threshold 0.490. Threshold selection maximises validation coverage with a 95% Wilson precision lower bound of at least .80 and at least 50 examples. These are project choices, not a universal standard.

## Held-out image evaluation

Accuracy: **77.1%**, nominal image-level 95% Wilson CI 75.6% to 78.4%. Macro-F1: **0.621**; balanced accuracy 63.6%. Majority-class training baseline: 34.7%. ECE (15 bins): 0.013.

After confidence abstention: 81.7% accuracy on 88.1% of eligible images (2959 accepted, 401 abstained). Coverage is part of the result, not a hidden filter. This does not include excluded non-face/ambiguous source rows or all possible real-world inputs. Image-level confidence intervals do not establish participant-independent performance.

| Expression category | Test support | Precision | Recall | F1 |
| --- | ---: | ---: | ---: | ---: |
| neutral | 1166 | 0.806 | 0.774 | 0.789 |
| happiness | 907 | 0.883 | 0.877 | 0.880 |
| surprise | 414 | 0.810 | 0.812 | 0.811 |
| sadness | 422 | 0.583 | 0.642 | 0.611 |
| anger | 312 | 0.720 | 0.718 | 0.719 |
| disgust | 22 | 0.294 | 0.455 | 0.357 |
| fear | 91 | 0.477 | 0.462 | 0.469 |
| contempt | 26 | 0.321 | 0.346 | 0.333 |

Dim-light, blur and lower-face-occlusion results are reported separately in image-evaluation.json. No model or threshold was retuned on these test transformations.

## External video evaluation

RAVDESS video-only emotional speech, actors 01–04: 208 supported-category clips attempted, 208 with quality-eligible predictions. 32 calm clips excluded because FER+ has no separate calm category. No calm-to-neutral relabelling was performed.

Protocol: ten evenly spaced frames in the middle 60% of each clip, then mean probabilities after face and image-quality checks. Recording-level acted labels are used. **This is clip classification, not live frame-level emotion ground truth.** Video recordings were not used for training, selection or thresholds.

Conditional clip accuracy: **29.8%**. Actor-bootstrap 95% interval: 22.1% to 40.4%. Only four actor groups make this interval unstable. Macro-F1 over seven supported truth classes: **0.251**; errors into the eighth contempt output remain errors. Operational accuracy including no-prediction failures: 29.8%. Operational clip coverage: 100.0%.

At the unchanged image-selected threshold: 32.5% selective clip accuracy with 72.6% coverage (151 accepted clips). These mean-pooled clip confidences have not been calibrated for video and can fail under domain shift.

The eight-output metrics are primary. A separately named seven-class renormalised diagnostic is not the deployed classifier. Per-class tables retain all eight outputs; the declared macro-F1 label indices specify the supported video classes. Image-calibrated confidence has not been retuned to video. Acted clips are not representative Indian gamers, natural frustration episodes or successful interventions.

Frame pipeline p95: **20.8 ms**, median 14.7 ms on the recorded CPU environment. This excludes source decoding, display, the 2 Hz sampling interval and three-frame stability delay; it does not measure game FPS, GPU or battery impact. App streaming applies stability gating separately from the mean-pooled clip evaluation.

## Project acceptance checks

| Check | Measured | Target | Result |
| --- | ---: | ---: | --- |
| image_top1_accuracy | 0.7705357142857143 | 0.75 | Pass |
| image_macro_f1 | 0.6212403634143167 | 0.65 | Fail |
| image_ece | 0.012592783814207439 | 0.08 | Pass |
| image_selective_accuracy | 0.8171679621493748 | 0.8 | Pass |
| image_selective_coverage | 0.8806547619047619 | 0.4 | Pass |
| external_video_macro_f1 | 0.2505582820132862 | 0.55 | Fail |
| frame_pipeline_latency | 20.838372299567702 | 250 | Pass |

Even passing quantitative checks would not approve production use. Mandatory open items are independent consented gamer videos, participant-disjoint target-context evaluation, paired participant-reported CMA/frustration, Indian-context evidence without inferring demographic attributes from faces, source-rights review, real target-OS camera and game-performance checks, and UI approval.

## Privacy and product behaviour

Camera and analysis are off by default. All runtime inference is local. Normal app use saves no raw frames, camera recordings or audio. User-requested command-line annotated output and screenshot flags are explicit research-output exceptions. Retaining derived summaries requires opt-in. Deleting app summaries does not delete imported media. Source loss, pause, break, end and close stop capture and clear expression cues. Mixed/unknown and manual-only use are supported.

## Reproduction and artifacts

See README.md, the two candidate folders, training-config.json, training-history.json, environment.json, model-selection.json, image-evaluation.json, video-evaluation.json, runtime-verification.json and release-gates.json. Source and data checksums are recorded. Third-party sources/licences are in ../third_party/NOTICES.md. Feature applicability is in ../docs/FEATURE-APPLICABILITY.md. Earlier persona interviews remain simulated and were never used as model training or validation data.

![Image confusion matrix](figures/image-confusion.png)
![External video confusion matrix](figures/video-confusion.png)
![Validation learning curves](figures/learning-curves.png)
![Test reliability](figures/classification-reliability.png)
