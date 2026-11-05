"""Bounded local facial-expression inference. Never converts expressions to CMA/mood."""
from checkpoint.cues import Cue
import json
import math
import time
from pathlib import Path
import cv2
import numpy as np
import onnxruntime as ort

ort.disable_telemetry_events()
cv2.setNumThreads(1)
ROOT = Path(__file__).resolve().parents[1]
LABELS = ("neutral", "happiness", "surprise", "sadness", "anger", "disgust", "fear", "contempt")


def preprocess(crop):
    if crop.ndim == 3: crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    image = cv2.resize(crop, (48,48), interpolation=cv2.INTER_AREA)
    return (image.astype(np.float32)/127.5-1)[None,None]


class ExpressionModel:
    def __init__(self, directory=ROOT/"artifacts"):
        directory=Path(directory)
        config=json.loads((directory/"calibration.json").read_text())
        self.temperature=float(config["temperature"])
        self.threshold=float(config["abstention_threshold"])
        options=ort.SessionOptions();options.intra_op_num_threads=1;options.inter_op_num_threads=1
        self.session=ort.InferenceSession(str(directory/"expression.onnx"),sess_options=options,providers=["CPUExecutionProvider"])

    def probabilities(self, faces):
        logits=self.session.run(["logits"],{"face":faces.astype(np.float32)})[0]/self.temperature
        exp=np.exp(logits-logits.max(1,keepdims=True));return exp/exp.sum(1,keepdims=True)

    def predict_crop(self, crop):
        probs=self.probabilities(preprocess(crop))[0]
        cls=int(probs.argmax());confidence=float(probs[cls]);accepted=confidence>=self.threshold
        return Cue("accepted" if accepted else "uncertain", LABELS[cls] if accepted else None, confidence,
                   tuple(float(p) for p in probs), "" if accepted else "Below validation-selected confidence threshold")


class FacePipeline:
    def __init__(self, directory=ROOT/"artifacts", min_face_pixels=80,pretrained=False):
        if pretrained:
            from checkpoint.pretrained_expression import HSEExpressionModel
            self.model=HSEExpressionModel(directory)
        else:self.model=ExpressionModel(directory)
        self.detector=cv2.FaceDetectorYN.create(str(Path(directory)/"yunet.onnx"),"",(320,320),.9,.3,5000)
        self.min_face_pixels=min_face_pixels

    def infer(self, frame):
        start=time.perf_counter()
        def stop(reason, box=None):
            return Cue("unavailable",reason=reason,face_box=box,elapsed_ms=(time.perf_counter()-start)*1000)
        if frame is None or frame.size==0: return stop("Empty video frame")
        h,w=frame.shape[:2]
        scale=min(1.,640/max(w,h));sw=max(32,int(w*scale)//32*32);sh=max(32,int(h*scale)//32*32)
        small=cv2.resize(frame,(sw,sh));self.detector.setInputSize((sw,sh))
        _,faces=self.detector.detect(small)
        if faces is None or len(faces)==0: return stop("No face in frame")
        if len(faces)!=1: return stop("Multiple faces; select a private single-person view")
        face=faces[0].copy();face[:14:2]*=w/sw;face[1:14:2]*=h/sh
        x,y,fw,fh=map(float,face[:4]);box=(int(x),int(y),int(fw),int(fh))
        if min(fw,fh)<self.min_face_pixels:return stop("Face is too small",box)
        eye_dx=face[6]-face[4];eye_dy=face[7]-face[5]
        angle=abs(math.degrees(math.atan2(eye_dy,eye_dx)))
        if angle>90:angle=180-angle
        if angle>25:return stop("Face is too rotated",box)
        margin=.05
        x0=max(0,int(x-fw*margin));y0=max(0,int(y-fh*margin));x1=min(w,int(x+fw*(1+margin)));y1=min(h,int(y+fh*(1+margin)))
        crop=frame[y0:y1,x0:x1]
        if not crop.size:return stop("Face crop unavailable",box)
        gray=cv2.cvtColor(crop,cv2.COLOR_BGR2GRAY)
        brightness=float(gray.mean())
        if brightness<30 or brightness>235:return stop("Lighting is unsuitable",box)
        # Fixed-size sharpness avoids favouring large-resolution videos.
        sharpness=float(cv2.Laplacian(cv2.resize(gray,(96,96)),cv2.CV_64F).var())
        if sharpness<15:return stop("Face is too blurred",box)
        prediction=self.model.predict_crop(crop)
        return Cue(prediction.status,prediction.expression,prediction.confidence,prediction.probabilities,prediction.reason,box,(time.perf_counter()-start)*1000)


class CueSmoother:
    """Three recent accepted frames must agree. An unavailable frame clears the buffer."""
    def __init__(self, size=3):
        self.size=size;self.items=[]

    def reset(self): self.items=[]

    def update(self, cue):
        if cue.status!="accepted":self.reset();return cue
        self.items=(self.items+[cue.expression])[-self.size:]
        if len(self.items)<self.size or len(set(self.items))!=1:
            return Cue("uncertain",confidence=cue.confidence,probabilities=cue.probabilities,reason="Waiting for a stable expression cue",face_box=cue.face_box,elapsed_ms=cue.elapsed_ms)
        return cue
