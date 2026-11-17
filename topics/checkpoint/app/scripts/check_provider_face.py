"""Actual model inference on Google's public example; not emotion accuracy evidence."""
import hashlib
import json
from pathlib import Path
import urllib.request
import cv2
import numpy as np
from checkpoint.face_mapping import LandmarkPipeline

ROOT=Path(__file__).resolve().parents[1]
url='https://storage.googleapis.com/mediapipe-assets/portrait.jpg'
with urllib.request.urlopen(url,timeout=30) as response:
    data=response.read(4*1024*1024+1)
if len(data)>4*1024*1024:raise ValueError('Provider image too large')
frame=cv2.imdecode(np.frombuffer(data,np.uint8),cv2.IMREAD_COLOR)
assert frame is not None
mapper=LandmarkPipeline()
try:
    cue=mapper.infer(frame)
    assert cue.status=='accepted' and cue.movement is not None
    assert {'brow_furrow','brow_inner_raise','eye_squint','eye_wide','blink'}<=set(cue.movement)
    result={'source':url,'sha256':hashlib.sha256(data).hexdigest(),
            'fixture':'One public provider portrait, no labelled emotional ground truth',
            'face_detected':True,'separate_action_features':'passed',
            'category_model_available':mapper.category_model is not None,
            'emotion_accuracy':'not measured'}
    out=ROOT/'artifacts/expression-review';out.mkdir(parents=True,exist_ok=True)
    (out/'provider-face-check.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result))
finally:
    mapper.close()
