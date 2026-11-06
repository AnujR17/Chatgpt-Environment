from checkpoint.reflection import ReflectionEngine
from checkpoint.session import Session
from checkpoint.cues import Cue
from checkpoint.face_mapping import neutral_movement
from checkpoint.cma_report import cma_summary


def feed(engine,session,start,seconds,*,fps=8,smile=0,brow=0,pressed=0,hidden=False,label=None,**extra):
    result=None
    for step in range(round(seconds*fps)):
        now=start+step/fps;m=neutral_movement();m.update(cheek=.5 if smile>.3 else 0.,smile=smile,brow=brow,pressed=pressed,mouth_visible=0. if hidden else 1.);m.update(extra)
        model={'status':'accepted','label':label,'score':.9,'scores':{label:.9,'neutral' if label!='neutral' else 'happiness':.1}} if label else None
        session.cue=Cue('accepted','neutral',movement=m,model_estimate=model);session.cue_received_at=now
        result=engine.display(session,now=now)
    return result


def setup():
    s=Session();s.experimental_analysis=True;s.start_capture('camera');return s,ReflectionEngine()


def test_sustained_smile_is_responsive_but_one_frame_spike_is_ignored():
    s,e=setup();feed(e,s,1000,1)
    assert feed(e,s,1001,.125,smile=.9).artwork=='composed'
    assert feed(e,s,1001.125,1).artwork=='composed'
    assert feed(e,s,1002.125,1,smile=.9).artwork=='happy'
    assert cma_summary(s)['cma']['count']==0


def test_checkin_never_pins_live_reflection_and_cma_stays_reported():
    s,e=setup();feed(e,s,1000,2,smile=.8);s.check_in('sad',-.6,-.4)
    assert feed(e,s,1002,2,smile=.8).artwork=='happy'
    assert (s.report,s.valence,s.arousal)==('sad',-.6,-.4)


def test_brow_and_mouth_tension_without_model_do_not_claim_anger():
    s,e=setup()
    assert feed(e,s,1000,2,brow=.8).artwork is None
    assert feed(e,s,1002,2,brow=.8,pressed=.6).artwork=='frustrated'
    assert feed(e,s,1004,2,brow=.8,pressed=.6,label='anger').artwork=='angry'
    assert feed(e,s,1006,1).artwork=='composed'


def test_laugh_has_authored_open_mouth_and_subtle_animation():
    s,e=setup();d=feed(e,s,1000,1,smile=.8,jaw=.7,laugh=.7,teeth=.8)
    assert d.artwork=='happy' and d.movement['laugh']==.45 and d.movement['teeth']<=.7


def test_hand_occlusion_and_loss_clear_immediately_and_recovery_does_not_wait_30_seconds():
    s,e=setup();feed(e,s,1000,2,smile=.8)
    assert feed(e,s,1002,1,smile=.8,hidden=True).artwork is None
    assert e.summary()['mouth_hidden_seconds']>.7
    assert feed(e,s,1003,1,smile=.8).artwork=='happy'
    s.cue=Cue('unavailable',reason='No face detected');s.cue_received_at=1004
    assert e.display(s,1004).artwork is None
    assert feed(e,s,1004.125,1).artwork=='composed'
    assert e.display(s,1010).artwork is None


def test_model_disagreement_does_not_force_anger_or_smile():
    s,e=setup();assert feed(e,s,1000,2,smile=.8,label='anger').artwork is None


def test_trend_is_separate_from_quick_reflection_and_sparse_frames_do_not_qualify():
    s,e=setup();d=feed(e,s,1000,5,smile=.8)
    assert e.trend=='happiness' and 'Recent trend' in d.detail
    d=feed(e,s,1005,1,brow=.8,pressed=.6,label='anger')
    assert d.artwork=='angry' and e.trend=='happiness'
    d=feed(e,s,1006,4,brow=.8,pressed=.6,label='anger')
    assert e.trend=='anger'
    s,e=setup()
    for now in (1000,1002,1004):d=feed(e,s,now,.125,smile=.8)
    assert d.artwork is None


def test_category_only_model_supports_eight_classes_without_movement_mapping():
    from checkpoint.runtime import LABELS
    for label in LABELS:
        s,e=setup();s.face_mapping=False
        for i in range(8):
            s.cue=Cue('accepted',label,.9);s.cue_received_at=1000+i/8;d=e.display(s,1000+i/8)
        assert d.artwork is not None


def test_mouth_widening_and_speech_like_smile_without_cheek_or_model_do_not_become_happy():
    s,e=setup()
    assert feed(e,s,1000,2,smile=.8,cheek=0.,jaw=.5).artwork is None
    assert feed(e,s,1002,2,mouth_wide=.8,jaw=.4).artwork is None


def test_smile_can_use_model_support_and_anger_teeth_do_not_turn_into_happy():
    s,e=setup()
    d=feed(e,s,1000,2,smile=.7,cheek=0.,label='happiness')
    assert d.artwork=='happy'
    d=feed(e,s,1002,2,brow=.8,pressed=.6,teeth=.8,label='anger')
    assert d.artwork=='angry' and d.movement['teeth']>.5 and 'smile' not in d.movement


def test_irregular_timestamps_duplicate_refresh_and_source_change_are_safe():
    s,e=setup()
    for now in (1000,1000.11,1000.27,1000.4,1000.55,1000.7):
        d=feed(e,s,now,.125,smile=.8)
        before=e.pending_count
        for _ in range(10):e.display(s,now)
        assert e.pending_count==before, 'UI refreshes must not count as new camera observations'
    assert d.artwork=='happy'
    s.stop_capture();s.start_capture('camera')
    assert e.display(s,1001).artwork is None


def test_adaptive_filter_reduces_resting_jitter_and_follows_a_step_without_a_long_delay():
    from checkpoint.signal_filter import OneEuro
    import math
    filt=OneEuro();raw=[];out=[]
    for i in range(80):
        value=.1+.025*(-1 if i%2 else 1);raw.append(value);out.append(filt.update(value,i/8))
    assert max(out[-40:])-min(out[-40:])<max(raw)-min(raw)
    for i in range(8):value=filt.update(.9,10+i/8)
    assert value>.88 and math.isfinite(value)
    assert filt.update(.4,12)==.4, 'A long loss must reset stale filtering state'


def test_confident_model_does_not_require_an_unvalidated_anger_geometry_threshold():
    s,e=setup()
    assert feed(e,s,1000,1,label='anger').artwork=='angry'


def test_confident_happy_model_and_tense_geometry_are_unclear_not_frustrated():
    s,e=setup()
    assert feed(e,s,1000,2,brow=.8,pressed=.6,label='happiness').artwork is None
