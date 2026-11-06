"""Deterministic signal replay: responsiveness/guards, never emotion accuracy."""
import json
import subprocess
from pathlib import Path
from checkpoint.reflection import ReflectionEngine
from checkpoint.face_mapping import neutral_movement
from checkpoint.cues import Cue
from checkpoint.session import Session

ROOT=Path(__file__).resolve().parents[1]
BASELINE='ab0c2541e717cdaf96e4d5217d804a71f5490657'


def replay(engine,fps):
    session=Session();session.experimental_analysis=True;session.start_capture('camera')
    scenarios=[('neutral',3,{}),('smile',20,{'smile':.8}),('tense',35,{'brow':.8,'pressed':.6}),('neutral_return',5,{}),('hidden',2,{'mouth_visible':0.}),('recover_smile',3,{'smile':.8})]
    expected={'neutral':'composed','smile':'happy','tense':'angry','neutral_return':'composed','hidden':None,'recover_smile':'happy'}
    output={};clock=1000.
    for name,seconds,values in scenarios:
        onset=None;transitions=[];previous=object()
        for i in range(int(seconds*fps)):
            now=clock+i/fps;m=neutral_movement();m.update(values)
            if values.get('smile',0)>.3:m['cheek']=.5
            model={'status':'accepted','label':'anger','score':.9,'scores':{'anger':.9,'neutral':.1}} if name=='tense' else None
            session.cue=Cue('accepted','neutral',movement=m,model_estimate=model);session.cue_received_at=now
            display=engine.display(session,now)
            target=expected[name]
            # Previous release used different illustration names for its two states.
            matches=display.artwork==target or (name in ('smile','recover_smile') and display.artwork=='contented') or (name=='tense' and display.artwork=='frustrated')
            if matches and onset is None:onset=round(i/fps,3)
            if display.artwork!=previous:transitions.append({'after_seconds':round(i/fps,3),'artwork':display.artwork});previous=display.artwork
        output[name]={'first_matching_pose_seconds':onset,'transitions':transitions};clock+=seconds
    return output


def main():
    ns={};source=subprocess.check_output(['git','show',f'{BASELINE}:topics/checkpoint/app/checkpoint/reflection.py'],text=True)
    exec(compile(source,'prior_reflection.py','exec'),ns)
    result={'fixture':'Synthetic time-stamped face signals, not camera latency or emotion accuracy','baseline_commit':BASELINE,
            'fps':{str(fps):{'previous':replay(ns['ReflectionEngine'](),fps),'rebuild':replay(ReflectionEngine(),fps)} for fps in (4,8,12)}}
    (ROOT/'artifacts/reflection-replay.json').write_text(json.dumps(result,indent=2))
    for fps,values in result['fps'].items():print(fps,{version:{k:v['first_matching_pose_seconds'] for k,v in scenarios.items()} for version,scenarios in values.items()})


if __name__=='__main__':main()
