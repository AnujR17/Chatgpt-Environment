"""Pretrained physical face mapping. Blendshape values do not measure felt emotion."""
from pathlib import Path
import hashlib
import time
import cv2
import numpy as np
from checkpoint.runtime import Cue


def movement_parameters(scores,baseline=None,gain=1.5):
    baseline=baseline or {}
    def value(name):return max(0.,float(scores.get(name,0))-float(baseline.get(name,0)))
    smile=(value('mouthSmileLeft')+value('mouthSmileRight'))/2
    frown=(value('mouthFrownLeft')+value('mouthFrownRight'))/2
    down=(value('browDownLeft')+value('browDownRight'))/2
    up=value('browInnerUp');blink=(float(scores.get('eyeBlinkLeft',0))+float(scores.get('eyeBlinkRight',0)))/2
    clip=lambda x,lo,hi:max(lo,min(hi,float(x)))
    deadband=lambda x:0. if abs(x)<.1 else x
    return {'smile':deadband(clip((smile-frown)*gain*2,-1,1)),'brow':deadband(clip((down-up)*gain*2,-1,1)),
            'eyes':clip(1-blink, .08,1.3),'jaw':deadband(clip(value('jawOpen')*gain,0,1)),
            'tension':clip(down*gain,0,.6)}


class LandmarkPipeline:
    def __init__(self,directory=None):
        import os
        os.environ.setdefault('MPLBACKEND','Agg')
        import mediapipe as mp
        from mediapipe.tasks import python
        from mediapipe.tasks.python import vision
        self.mp=mp
        model=Path(directory or Path(__file__).resolve().parents[1]/'artifacts')/'face_landmarker.task'
        if hashlib.sha256(model.read_bytes()).hexdigest()!='64184e229b263107bc2b804c6625db1341ff2bb731874b0bcc2fe6544e0bc9ff':raise ValueError('Face mapping model checksum mismatch')
        options=vision.FaceLandmarkerOptions(base_options=python.BaseOptions(model_asset_buffer=model.read_bytes(),delegate=python.BaseOptions.Delegate.CPU),
            running_mode=vision.RunningMode.VIDEO,num_faces=2,min_face_detection_confidence=.6,min_face_presence_confidence=.6,
            min_tracking_confidence=.6,output_face_blendshapes=True)
        self.detector=vision.FaceLandmarker.create_from_options(options);self.last_timestamp=-1;self.baseline={};self.calibration=[];self.calibrating=False;self.gain=1.5

    def start_neutral(self):self.calibration=[];self.calibrating=True

    def infer(self,frame):
        start=time.monotonic()
        if frame is None or not frame.size:return Cue('unavailable',reason='No camera frame')
        h,w=frame.shape[:2];small=cv2.resize(frame,(min(640,w),max(1,round(h*min(640,w)/w))))
        if float(small.std())<5:return Cue('unavailable',reason='No usable camera image')
        rgb=cv2.cvtColor(small,cv2.COLOR_BGR2RGB)
        timestamp=max(self.last_timestamp+1,int(time.monotonic()*1000));self.last_timestamp=timestamp
        result=self.detector.detect_for_video(self.mp.Image(image_format=self.mp.ImageFormat.SRGB,data=rgb),timestamp)
        if len(result.face_landmarks)!=1:return Cue('unavailable',reason='No face detected' if not result.face_landmarks else 'Multiple faces detected')
        points=result.face_landmarks[0];xs=[p.x for p in points];ys=[p.y for p in points]
        if min((max(xs)-min(xs))*small.shape[1],(max(ys)-min(ys))*small.shape[0])<65:return Cue('unavailable',reason='Move closer to the camera')
        scores={c.category_name:float(c.score) for c in result.face_blendshapes[0]}
        label='Neutral appearance';key='neutral'
        if self.calibrating:
            self.calibration.append(scores)
            if len(self.calibration)>=8:
                names=['mouthSmileLeft','mouthSmileRight','mouthFrownLeft','mouthFrownRight','browDownLeft','browDownRight','browInnerUp','jawOpen']
                self.baseline={name:float(np.median([x.get(name,0) for x in self.calibration])) for name in names};self.calibrating=False;label='Neutral face calibrated'
            else:label=f'Hold a relaxed face · {len(self.calibration)}/8'
            movement={'smile':0.,'brow':0.,'eyes':1.,'jaw':0.,'tension':0.}
        else:
            movement=movement_parameters(scores,self.baseline,self.gain)
            if movement['brow']>.22:key='anger';label='Brows drawn'
            elif movement['smile']>.3:key='happiness';label='Smile movement'
            elif movement['jaw']>.35:key='surprise';label='Mouth open'
            elif movement['smile']<-.2:key='sadness';label='Mouth corners lowered'
            if key=='neutral':movement.update(smile=0.,brow=0.,jaw=0.)
        return Cue('accepted',key,reason='Physical face mapping · not a mood estimate',elapsed_ms=(time.monotonic()-start)*1000,
                   movement=movement,mapping_label=label)

    def close(self):self.detector.close()
