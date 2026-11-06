"""Local face/hand signals. No facial category establishes felt emotion or CMA."""
from pathlib import Path
import hashlib
import time
import cv2
import numpy as np
from checkpoint.cues import Cue
from checkpoint.face_detail import mouth_polygon,hand_mouth,visible_teeth


def neutral_movement():
    return dict(smile=0.,brow=0.,eyes=1.,eye_left=1.,eye_right=1.,brow_skew=0.,jaw=0.,tension=0.,laugh=0.,
                cheek=0.,mouth_wide=0.,pressed=0.,pucker=0.,snarl=0.,asymmetry=0.,teeth=0.,hand=0.,hand_side=1.,mouth_visible=1.)


def movement_parameters(scores,baseline=None,gain=1.5):
    baseline=baseline or {}
    def value(name):return max(0.,float(scores.get(name,0))-float(baseline.get(name,0)))
    def average(prefix):return (value(prefix+'Left')+value(prefix+'Right'))/2
    clip=lambda x,lo=0.,hi=1.:max(lo,min(hi,float(x)))
    floor=lambda x:max(0.,x-(.025 if baseline else .045))
    deadband=lambda x:0. if abs(x)<.12 else x
    smile=average('mouthSmile');frown=average('mouthFrown');stretch=average('mouthStretch');press=average('mouthPress')
    down=.65*average('browDown')+.35*max(value('browDownLeft'),value('browDownRight'))
    squint=max(average('eyeSquint'),average('cheekSquint'));cheek=average('cheekSquint')
    snarl=average('noseSneer')
    # Horizontal pulling/pressed lips with drawn brows is counter-evidence to a smile.
    conflict=clip((down-.06)*5)*clip((max(press,stretch,snarl)-.06)*4)*(1-clip(cheek*2))
    positive=clip(floor(smile-.35*frown)*gain*2.8)*(1-.95*conflict)
    negative=clip(floor(frown-.65*smile)*gain*2.5)
    brow=clip((floor(down)-.28*floor(value('browInnerUp')))*gain*3.,-1.,1.)
    brow-=clip(floor(max(value('browOuterUpLeft'),value('browOuterUpRight')))*gain*.7)
    jaw=clip(floor(value('jawOpen'))*gain*1.9)
    eyes=[]
    for side in ('Left','Right'):
        eyes.append(clip((1-value('eyeBlink'+side))*(1-.45*value('eyeSquint'+side))+value('eyeWide'+side)*.6,.08,1.5))
    laughing=clip((positive-.2)/.65)*clip((jaw-.12)/.5)
    result=neutral_movement();result.update(smile=deadband(positive-negative),brow=deadband(brow),eyes=sum(eyes)/2,
        eye_left=eyes[0],eye_right=eyes[1],jaw=deadband(jaw),tension=clip(down*gain+press*gain*.35,0,.7),laugh=laughing,
        cheek=clip(floor(cheek)*gain*2.8),mouth_wide=clip(floor(stretch)*gain*2.5),pressed=clip(floor(press)*gain*2.8),pucker=clip(max(value('mouthPucker'),value('mouthFunnel'))*gain),
        snarl=clip(floor(snarl)*gain*3),asymmetry=clip((value('mouthSmileLeft')-value('mouthSmileRight'))*gain*2,-1,1),
        brow_skew=clip((value('browOuterUpLeft')-value('browOuterUpRight'))*gain*2,-1,1))
    return result


def movement_label(m):
    if m.get('hand',0)>.5:return 'neutral','Hand near mouth'
    if m['brow']>.2 and max(m.get('pressed',0),m.get('mouth_wide',0),m.get('snarl',0))>.22 and m['smile']<.45:return 'anger','Drawn brows and tense mouth'
    if m.get('snarl',0)>.3 and m['smile']<.3:return 'disgust','Nose and upper lip raised'
    if abs(m.get('asymmetry',0))>.4 and m['smile']<.45:return 'contempt','One-sided mouth lift'
    if m['smile']>=.16:return ('happiness','Open smile') if m.get('laugh',0)>.08 else ('happiness','Smile movement')
    if m['brow']>.15:return 'anger','Brows drawn'
    if m.get('eyes',1)>1.12 and m['brow']<-.12 and m.get('mouth_wide',0)>.15 and m['jaw']<.35:return 'fear','Wide eyes and tense mouth'
    if m['smile']<-.15:return 'sadness','Mouth corners lowered'
    if m['jaw']>.2:return 'surprise','Mouth open'
    if m.get('mouth_wide',0)>.2:return 'neutral','Mouth widened'
    if m.get('pucker',0)>.25:return 'neutral','Lips rounded'
    if m.get('teeth',0)>.15:return 'neutral','Teeth visible'
    return 'neutral','Neutral appearance'


class LandmarkPipeline:
    def __init__(self,directory=None,*,hands=True,categories=True):
        import os
        os.environ.setdefault('MPLBACKEND','Agg')
        import mediapipe as mp
        from mediapipe.tasks import python
        from mediapipe.tasks.python import vision
        self.mp=mp;self.directory=Path(directory or Path(__file__).resolve().parents[1]/'artifacts')
        model=self.directory/'face_landmarker.task'
        if hashlib.sha256(model.read_bytes()).hexdigest()!='64184e229b263107bc2b804c6625db1341ff2bb731874b0bcc2fe6544e0bc9ff':raise ValueError('Face mapping model checksum mismatch')
        options=vision.FaceLandmarkerOptions(base_options=python.BaseOptions(model_asset_buffer=model.read_bytes(),delegate=python.BaseOptions.Delegate.CPU),
            running_mode=vision.RunningMode.VIDEO,num_faces=2,min_face_detection_confidence=.6,min_face_presence_confidence=.6,
            min_tracking_confidence=.6,output_face_blendshapes=True)
        self.detector=vision.FaceLandmarker.create_from_options(options);self.hand_detector=None;self.hand_error='';self.category_model=None;self.category_error=''
        try:
            if hands:
                hand=Path(__file__).with_name('assets')/'hand_landmarker.task'
                if hashlib.sha256(hand.read_bytes()).hexdigest()!='fbc2a30080c3c557093b5ddfc334698132eb341044ccee322ccf8bcf3607cde1':raise ValueError('Hand model checksum mismatch')
                self.hand_detector=vision.HandLandmarker.create_from_options(vision.HandLandmarkerOptions(
                    base_options=python.BaseOptions(model_asset_buffer=hand.read_bytes(),delegate=python.BaseOptions.Delegate.CPU),
                    running_mode=vision.RunningMode.VIDEO,num_hands=2,min_hand_detection_confidence=.55,min_hand_presence_confidence=.55,min_tracking_confidence=.5))
        except Exception as ex:self.hand_error=str(ex)
        try:
            if categories:
                from checkpoint.runtime import FacePipeline
                self.category_model=FacePipeline(pretrained=True)
        except Exception as ex:self.category_error=str(ex)
        self.last_timestamp=-1;self.baseline={};self.calibration=[];self.calibrating=False;self.gain=1.5
        self.last_mouth=None;self.last_face_at=0.;self.last_category_at=-100.;self.category=None

    def start_neutral(self):self.calibration=[];self.calibrating=True

    def infer(self,frame):
        start=time.monotonic()
        if frame is None or not frame.size:return Cue('unavailable',reason='No camera frame')
        h,w=frame.shape[:2];small=cv2.resize(frame,(min(640,w),max(1,round(h*min(640,w)/w))))
        if float(small.std())<5:return Cue('unavailable',reason='No usable camera image')
        rgb=cv2.cvtColor(small,cv2.COLOR_BGR2RGB)
        image=self.mp.Image(image_format=self.mp.ImageFormat.SRGB,data=rgb)
        timestamp=max(self.last_timestamp+1,int(start*1000));self.last_timestamp=timestamp
        result=self.detector.detect_for_video(image,timestamp)
        hands=[]
        if self.hand_detector is not None:
            try:hands=self.hand_detector.detect_for_video(image,timestamp).hand_landmarks
            except Exception as ex:self.hand_error=str(ex)
        if len(result.face_landmarks)!=1:
            gesture=hand_mouth(hands,self.last_mouth if start-self.last_face_at<.8 else None)
            if not result.face_landmarks and gesture['near']:
                movement=neutral_movement();movement.update(hand=1.,hand_side=gesture['side'],mouth_visible=0.)
                return Cue('unavailable',reason='Face partly hidden. Mouth movement is not estimated.',movement=movement,mapping_label='Hand near mouth',gesture=gesture)
            return Cue('unavailable',reason='No face detected' if not result.face_landmarks else 'Multiple faces detected')
        points=result.face_landmarks[0];xs=[p.x for p in points];ys=[p.y for p in points]
        if min((max(xs)-min(xs))*small.shape[1],(max(ys)-min(ys))*small.shape[0])<65:return Cue('unavailable',reason='Move closer to the camera')
        mouth=mouth_polygon(points);gesture=hand_mouth(hands,mouth);self.last_mouth=mouth;self.last_face_at=start
        if self.hand_error:gesture.update(status='unavailable',reason=self.hand_error)
        scores={c.category_name:float(c.score) for c in result.face_blendshapes[0]}
        if self.calibrating and not gesture['occluded']:
            self.calibration.append(scores);movement=neutral_movement();key='neutral';label=f'Hold a relaxed face · {len(self.calibration)}/8'
            if len(self.calibration)>=8:
                names=['mouthSmileLeft','mouthSmileRight','mouthFrownLeft','mouthFrownRight','browDownLeft','browDownRight','browInnerUp','jawOpen']
                self.baseline={name:min(.12 if name=='jawOpen' else .18,float(np.median([x.get(name,0) for x in self.calibration]))) for name in names}
                self.calibrating=False;label='Neutral face calibrated'
        else:
            movement=movement_parameters(scores,self.baseline,self.gain)
            movement['teeth']=visible_teeth(small,points,gesture['occluded'])
            movement.update(hand=float(gesture['near']),hand_side=gesture['side'],mouth_visible=0. if gesture['occluded'] else 1.)
            if gesture['occluded']:
                for name in ('smile','jaw','laugh','mouth_wide','pressed','pucker','snarl','asymmetry','teeth'):movement[name]=0.
            key,label=movement_label(movement)
            if label=='Neutral appearance':movement.update(smile=0.,brow=0.,jaw=0.,laugh=0.)
        if gesture['occluded']:
            category={'status':'occluded','label':None,'scores':{},'reason':'Mouth hidden; category estimate withheld'}
        elif self.category_model is not None:
            if start-self.last_category_at>=.35:
                try:
                    from checkpoint.runtime import LABELS
                    cue=self.category_model.infer(small)
                    self.category={'status':cue.status,'label':cue.expression,'score':cue.confidence,'scores':dict(zip(LABELS,cue.probabilities)),'reason':cue.reason}
                except Exception as ex:self.category={'status':'unavailable','reason':str(ex),'scores':{}}
                self.last_category_at=start
                self.category['observed_at']=start
            category=self.category
        else:category={'status':'unavailable','reason':self.category_error or 'Category model off','scores':{}}
        return Cue('accepted',key,reason='Visible movements; not a mood/CMA measurement',elapsed_ms=(time.monotonic()-start)*1000,
            movement=movement,mapping_label=label,gesture=gesture,model_estimate=category)

    def close(self):
        try:self.detector.close()
        finally:
            if self.hand_detector is not None:self.hand_detector.close()
