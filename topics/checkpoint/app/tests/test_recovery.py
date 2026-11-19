from checkpoint.session import Session
from checkpoint.cma_report import cma_summary,report_html


def test_camera_cannot_fill_recovery_or_invent_a_trigger():
    s=Session();s.cue=object();s.record_response('continue')
    r=cma_summary(s)
    assert not r['cma']['points'] and not r['recovery']['contexts']
    assert r['recovery']['choices'][0]['before'] is None
    assert r['recovery']['choices'][0]['after'] is None


def test_self_report_context_and_followup_describe_change_without_causality():
    s=Session();s.check_in('frustrated',-.7,.8,context='Repeated setback')
    s.reports[-1]['elapsed_seconds']=0
    choice=s.record_response('pause');choice['elapsed_seconds']=1
    s.check_in('calm',.3,-.2);s.reports[-1]['elapsed_seconds']=20
    assert s.rate_response('yes')
    r=cma_summary(s);row=r['recovery']['choices'][0]
    assert row['change']=={'pleasantness':1.,'activation':-1.}
    assert r['recovery']['contexts']=={'Repeated setback':1}
    assert r['recovery']['helpful']=={'Take a pause':1}
    assert 'not detected causes' in report_html(r)


def test_later_choice_prevents_attributing_the_next_report_to_an_earlier_one():
    s=Session();s.check_in('frustrated',-.7,.8);s.reports[-1]['elapsed_seconds']=0
    s.record_response('pause')['elapsed_seconds']=1
    s.record_response('smaller_goal','One hold')['elapsed_seconds']=5
    s.check_in('calm',.5,-.4);s.reports[-1]['elapsed_seconds']=10
    rows=cma_summary(s)['recovery']['choices']
    assert rows[0]['after'] is None and rows[1]['after']['feeling']=='Neutral'


def test_response_rating_bounds_debounce_and_history():
    s=Session();assert s.record_response('invented') is None
    assert s.record_response('continue')
    assert s.record_response('continue') is None
    assert not s.rate_response('maybe') and s.rate_response('unsure') and not s.rate_response('yes')
    assert len(s.summary()['responses'])==1
    s.end();assert s.record_response('continue') is None
    assert len(s.responses)==1, 'Ending must not invent another pause'


def test_recent_derived_game_context_survives_app_focus_but_expires_and_clears(tmp_path):
    import time
    from checkpoint.app import create_application,MainWindow
    from checkpoint.gameplay import GameObservation
    app=create_application([]);w=MainWindow(no_setup=True,data_dir=tmp_path);w.timer.stop();w.detect_games=True
    w.receive_game_observation(None,GameObservation('Getting Over It','Fixture',state={'kind':'falling','title':'Possible fall','basis':'Fixture'}))
    w.game_observation=GameObservation(None,'App focused',state={'kind':'out_of_focus','title':'Not sampled'})
    assert w.checkin_game_context()['title']=='Possible fall'
    w.last_game_context_at=time.monotonic()-61;assert w.checkin_game_context()=={}
    w.last_game_context_at=time.monotonic();w.detect_games=False;assert w.checkin_game_context()=={}
    w.close();w.deleteLater();app.processEvents()
