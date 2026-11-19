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


def test_surprise_requires_both_brows_and_a_slightly_open_mouth():
    features=dict(brow_raise_left=.6,brow_raise_right=.5,jaw=.2,brow=-.4)
    assert pose(ReflectionEngine(),**features)=='surprise'
    for key in ('brow_raise_left','brow_raise_right','jaw'):
        assert pose(ReflectionEngine(),**{**features,key:0.})!='surprise'
    for change in ({'smile':.8,'cheek':.5},{'pressed':.8},{'blink':.8},{'snarl':.5},{'mouth_visible':0.}):
        assert pose(ReflectionEngine(),**{**features,**change})!='surprise'


def test_left_and_right_brow_features_survive_mapping_independently():
    scores={'browOuterUpLeft':.25,'browOuterUpRight':.25,'browInnerUp':.2,'jawOpen':.11}
    m=movement_parameters(scores)
    assert m['brow_raise_left']>.4 and m['brow_raise_right']>.4
    assert pose(ReflectionEngine(),**m)=='surprise'
    m=movement_parameters({**scores,'browOuterUpRight':0.,'browInnerUp':.7})
    assert pose(ReflectionEngine(),**m)!='surprise'


def test_surprise_dwell_unknown_and_checkin_separation():
    s=Session();s.experimental_analysis=True;s.start_capture('camera');s.check_in('happy',.7,.4)
    e=ReflectionEngine()
    for i in range(8):
        now=100+i/8;m=neutral_movement();m.update(brow_raise_left=.6,brow_raise_right=.5,jaw=.2)
        s.cue=Cue('accepted','surprise',movement=m);s.cue_received_at=now;d=e.display(s,now)
        if i<3:assert d.artwork is None
    assert d.title=='Surprised' and d.artwork=='surprised'
    assert (s.report,s.valence,s.arousal)==('happy',.7,.4)
    s.cue=Cue('unavailable',reason='No face detected');s.cue_received_at=101.
    assert e.display(s,101.).artwork is None


def test_mouth_open_or_single_raised_brow_does_not_claim_surprise():
    assert pose(ReflectionEngine(),jaw=.8) is None
    assert pose(ReflectionEngine(),jaw=.2,brow_raise_left=.8) is None


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
