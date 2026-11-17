"""Feature-policy and game-vision regressions, not emotion accuracy measurements."""
import cv2
import numpy as np
from checkpoint.cues import Cue
from checkpoint.face_mapping import movement_parameters, neutral_movement
from checkpoint.reflection import ReflectionEngine
from checkpoint.session import Session
from checkpoint.gameplay import GettingOverItAnalyzer


def pose(engine, **features):
    m=neutral_movement();m.update(features)
    return engine.classify(Cue('accepted','neutral',movement=m), 100.)[0]


def test_confusion_requires_a_combination_and_stays_tentative():
    features=dict(brow_furrow=.6,brow_inner_raise=.5,eye_squint=.4,brow=.2)
    assert pose(ReflectionEngine(),**features)=='confusion'
    for key in ('brow_furrow','brow_inner_raise','eye_squint'):
        partial={**features,key:0.}
        assert pose(ReflectionEngine(),**partial)!='confusion'
    for change in ({'smile':.8,'cheek':.5},{'pressed':.8},{'jaw':.7},{'blink':.8},{'snarl':.5}):
        assert pose(ReflectionEngine(),**{**features,**change})!='confusion'


def test_separate_brow_and_lid_features_survive_mapping():
    scores={'browDownLeft':.25,'browDownRight':.25,'browInnerUp':.25,
            'eyeSquintLeft':.25,'eyeSquintRight':.25}
    m=movement_parameters(scores)
    assert m['brow_furrow']>.4 and m['brow_inner_raise']>.4 and m['eye_squint']>.4
    assert pose(ReflectionEngine(),**m)=='confusion'


def test_confusion_dwell_unknown_and_checkin_separation():
    s=Session();s.experimental_analysis=True;s.start_capture('camera');s.check_in('happy',.7,.4)
    e=ReflectionEngine()
    for i in range(8):
        now=100+i/8;m=neutral_movement();m.update(brow_furrow=.6,brow_inner_raise=.5,eye_squint=.4)
        s.cue=Cue('accepted','neutral',movement=m);s.cue_received_at=now
        d=e.display(s,now)
        if i<3:assert d.artwork is None
    assert d.title=='Confused?' and d.artwork=='confused'
    assert (s.report,s.valence,s.arousal)==('happy',.7,.4)
    s.cue=Cue('unavailable',reason='No face detected');s.cue_received_at=101.
    assert e.display(s,101.).artwork is None


def test_surprise_needs_eyes_and_brows_not_just_an_open_mouth():
    assert pose(ReflectionEngine(),jaw=.8) is None
    assert pose(ReflectionEngine(),jaw=.8,brow=-.5,eye_wide=.8)=='surprise'


def scene(seed=1):
    return cv2.GaussianBlur(np.random.default_rng(seed).integers(0,256,(360,640,3),dtype=np.uint8),(3,3),0)


def test_vision_exposes_structured_movement_and_counts_one_run():
    a=GettingOverItAnalyzer();base=scene()
    for i in range(8):
        frame=cv2.warpAffine(base,np.float32([[1,0,0],[0,1,-9*i]]),(640,360),borderMode=cv2.BORDER_REFLECT)
        a.observe(frame)
    assert a.state['kind']=='falling' and a.state['possible_falls']==1
    a.observe(None)
    assert a.state['kind']=='unavailable' and a.state['section'] is None


def test_zoom_is_not_a_fall_and_named_views_need_actual_matches():
    a=GettingOverItAnalyzer();base=scene()
    assert a.mark_start(base,'Chimney practice')
    a.observe(base)
    assert a.state['kind']=='marked_view' and a.state['section']=='Chimney practice'
    a.observe(scene(99))
    assert a.state['section'] is None
    a.clear();a.observe(base)
    for scale in (1.05,1.1,1.15,1.2):
        frame=cv2.warpAffine(base,cv2.getRotationMatrix2D((320,180),0,scale),(640,360))
        a.observe(frame)
        assert a.state['kind'] not in ('climbing','falling')
