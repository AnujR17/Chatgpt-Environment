# Sources and licences

## Facial-expression training

FER2013 images: academic benchmark distributed via https://huggingface.co/datasets/chitradrishti/fer2013 at revision 4ad26b38d1dcc1c3891d841a48758653b6c67105. Original benchmark: https://www.kaggle.com/c/challenges-in-representation-learning-facial-expression-recognition-challenge/data . A mirror's MIT metadata does not independently establish rights in every source image. Images are excluded from the review bundle. Production and redistribution require rights review.

FER+ annotations: Microsoft FERPlus, https://github.com/microsoft/FERPlus . Emad Barsoum, Cha Zhang, Cristian Canton Ferrer and Zhengyou Zhang, “Training Deep Networks for Facial Expression Recognition with Crowd-Sourced Label Distribution,” ICMI 2016. https://arxiv.org/abs/1608.01041 . Annotation file SHA256 is pinned in ml/prepare.py. Microsoft repository code/annotations carry its MIT licence; this does not relicense FER2013 images.

## External video evaluation

RAVDESS: Steven R. Livingstone and Frank A. Russo (2018), “The Ryerson Audio-Visual Database of Emotional Speech and Song (RAVDESS).” https://zenodo.org/records/1188976 . Paper https://doi.org/10.1371/journal.pone.0196391 . CC BY-NC-SA 4.0: https://creativecommons.org/licenses/by-nc-sa/4.0/ . Actors 01–04, video-only emotional speech. Original archive MD5 and derived clip SHA256 are checked/stored in data/video-manifest.json.

The raw videos are not included in the source/model review bundle. Any annotated demonstration clip distributed separately is a modified excerpt with model overlays and no audio, shared under CC BY-NC-SA 4.0 with this attribution. It shows acted material, not a player's mood or a user webcam.

## Face localisation

YuNet 2023mar model from OpenCV Zoo, copyright Shiqi Yu (2020), MIT. See YUNET-LICENSE.txt. Model SHA256 8f2383e4dd3cfbb4553ea8718107fc0423210dc964f9f4280604804ed2552fa4. This is a pretrained detector only, not the expression classifier.

## Transfer backbone

Torchvision MobileNetV3-Small with ImageNet-1k V1 weights, https://pytorch.org/vision/stable/models/generated/torchvision.models.mobilenet_v3_small.html . Official weight URL https://download.pytorch.org/models/mobilenet_v3_small-047dcff4.pth . Torchvision code is BSD 3-Clause. Pretraining is general ImageNet object classification; no pretrained facial-expression weights are used. Final expression weights result from the documented FER+ fine-tuning run. Full local pretraining hash is recorded in artifacts/pretraining-provenance.json.

## UI assets

CMA vector emblems are exact native SVG exports of the user's Checkpoint Figma components 50:2, 50:9, 50:16, 50:23 and 50:30 in file Rj3WAO6IpUb48OFUerY7aW. No flattened UI image is used in the app. Camera/video imagery is supplied dynamically by the explicitly selected local source.

DM Sans is bundled under the SIL Open Font License 1.1; see DM-Sans-OFL.txt and checkpoint/assets/OFL.txt. No browser or embedded web engine is used by the native app.

## Pip preview providers and gameplay study

Google MediaPipe runtime 0.10.35 and Face Landmarker float16/1 are provider assets, not in-project training. Runtime licence: MEDIAPIPE-LICENSE.txt. Model URL and SHA-256: artifacts/face-landmarker-provenance.json. Documentation: https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker/python .

HSEmotion ONNX enet_b0_8_best_afew is provider-trained: https://github.com/av-savchenko/hsemotion-onnx . Provider licence: HSEMOTION-LICENSE.txt; model provenance/hash in artifacts/hsemotion-provenance.json. Provider code/weight licensing does not relicense underlying datasets. Outputs are expression-category estimates, not validated mood/CMA or clinical measurements.

The Getting Over It trailer is publisher-hosted media, movie 256696623, authored/published by Bennett Foddy/associated game publisher. Its raw video and thumbnails are excluded from this distribution. A hash, visual annotations, experimental feature model and results document a limited research trial; no general reuse/commercial-training licence is asserted. YouTube candidates are listed as metadata discovery only and were not downloaded or trained on.

QR generation uses qrcode 8.2; its distribution licence is retained in the bundled runtime metadata. Phone UI uses the same bundled OFL DM Sans and original Pip vector geometry as the native application.
