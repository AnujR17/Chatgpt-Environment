from checkpoint.reflection import ReflectionEngine
from checkpoint.session import Session
from checkpoint.cues import Cue
from checkpoint.face_mapping import neutral_movement
from checkpoint.cma_report import cma_summary


def feed(engine,session,start,seconds,*,smile=0,brow=0,pressed=0,hidden=False):
    result=None
    for step in range(int(seconds*4)):
        now=start+step*.25;movement=neutral_movement();movement.update(smile=smile,brow=brow,pressed=pressed,mouth_visible=0. if hidden else 1.)
        session.cue=Cue('accepted','neutral',movement=movement);session.cue_received_at=now
        result=engine.display(session,now=now)
    return result


def setup():
    session=Session();session.experimental_analysis=True;session.start_capture('camera');return session,ReflectionEngine()


def test_brief_smile_does_not_instantly_change_reflection_or_create_a_mood_report():
    session,engine=setup();display=feed(engine,session,1000,2,smile=.8)
    assert display.artwork is None and session.report is None and cma_summary(session)['cma']['count']==0


def test_sustained_pattern_is_stable_and_confirmed_checkin_takes_priority():
    session,engine=setup();display=feed(engine,session,1000,20,smile=.8)
    assert display.title=='A positive-looking stretch' and display.source=='visual_pattern'
    session.check_in('sad',-.6,-.4)
    display=feed(engine,session,1020,20,smile=.8)
    assert display.artwork=='sad' and display.source=='player_report'
    assert session.valence==-.6 and session.arousal==-.4


def test_sustained_reflection_holds_instead_of_mirroring_a_new_expression():
    session,engine=setup();feed(engine,session,1000,20,smile=.8)
    display=feed(engine,session,1020,20,brow=.8,pressed=.6)
    assert display.title=='A positive-looking stretch'
    display=feed(engine,session,1040,12,brow=.8,pressed=.6)
    assert display.title=='A tense-looking stretch'
    assert engine.summary()['sustained_patterns']=={'positive':1,'tense':1}


def test_hand_occlusion_excludes_mouth_evidence_and_clears_live_reflection():
    session,engine=setup();feed(engine,session,1000,20,smile=.8)
    display=feed(engine,session,1020,8,smile=.8,hidden=True)
    assert display.artwork is None and engine.summary()['mouth_hidden_seconds']>7
    assert session.report is None and engine.summary()['sustained_patterns'].get('tense',0)==0
