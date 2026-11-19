"""Timing and safety checks with scripted events, not game detection accuracy."""
from checkpoint.play_support import PlaySupport
from checkpoint.gameplay import GameObservation
from checkpoint.blob import eyebrow_curve


def observation(kind, count=1):
    return GameObservation('Getting Over It','Fixture',state={'kind':kind,'possible_falls':count})


def tick(policy, kind, now, count=1, **kwargs):
    return policy.update(observation(kind,count),now,enabled=True,active=True,paused=False,**kwargs)


def test_setback_responds_after_settling_without_camera_or_input_tracking():
    p=PlaySupport()
    for t in (100,101,102,103):assert not tick(p,'falling',t)
    assert p.pending_at==100  # Repeated frames do not restart the delay.
    assert not tick(p,'steady',104)
    assert not tick(p,'steady',105)
    assert tick(p,'steady',106)=='Possible fall. One secure hold. Then try the next reach.'
    assert p.basis=='Experimental game-window motion estimate'
    assert not tick(p,'steady',116)
    tick(p,'falling',117,count=2)
    tick(p,'steady',120,count=2)
    assert not tick(p,'steady',122,count=2)  # Two-minute automatic cooldown.
    tick(p,'falling',230,count=3)
    tick(p,'steady',234,count=3)
    assert tick(p,'steady',236,count=3,mode='Encouragement').endswith('Your next try starts here.')


def test_old_event_focus_loss_stale_stream_and_motion_do_not_prompt():
    for bad in ('climbing','view_changed','uncertain','out_of_focus','unavailable'):
        p=PlaySupport();tick(p,'falling',100)
        assert not tick(p,bad,104)
        assert not tick(p,bad,106)
    p=PlaySupport();tick(p,'falling',100)
    stale=observation('steady')
    p.update(stale,101,enabled=True,active=True,paused=False)
    assert not p.update(stale,105,enabled=True,active=True,paused=False)
    assert p.pending_at is None
    p=PlaySupport();tick(p,'falling',100);tick(p,'steady',126)
    assert not tick(p,'steady',128)


def test_disabled_paused_ended_clear_and_manual_support_never_sets_cma():
    p=PlaySupport()
    assert p.manual(100,'Quiet pause')=='A breath before the next try, if you want.'
    assert p.basis=='Player marked a setback'
    assert p.update(None,101,enabled=False,active=True,paused=False)
    for enabled,active,paused in ((True,False,False),(True,True,True)):
        p.manual(101)
        assert not p.update(None,102,enabled=enabled,active=active,paused=paused)
        assert p.pending_at is None


def test_brows_stay_short_and_above_even_amplified_or_asymmetric_eyes():
    for brow in (-3,-1,0,1,3):
        for skew in (-3,-1,0,1,3):
            for side in (-1,1):
                a,c,b=eyebrow_curve(brow,skew,side)
                assert b[0]-a[0]==.11
                # Largest eyes extend .098 scale above centre. Brows remain clear.
                assert max(a[1],b[1],c[1])<=-.14
                assert abs(a[1]-b[1])<=.051


def test_cma_changes_offer_only_from_recent_player_report_with_override():
    from checkpoint.session import Session
    from checkpoint.play_support import response_mode
    s=Session()
    assert response_mode(s,'Match my check-in')=='Next move'

    s.check_in('frustrated',-.7,.8)
    assert response_mode(s,'Match my check-in')=='Quiet pause'
    assert response_mode(s,'Next move')=='Next move'
    s.reports[-1]['elapsed_seconds']-=121
    assert response_mode(s,'Match my check-in')=='Next move'
    s.check_in('happy',.7,.4)
    assert response_mode(s,'Match my check-in')=='Encouragement'
    s.check_in('mixed')
    assert response_mode(s,'Match my check-in')=='Next move'


def test_immediate_rounded_checkin_does_not_drop_its_guidance():
    from checkpoint.session import Session
    from checkpoint.attempts import guidance_mode
    s=Session();s.elapsed=lambda:10.
    s.reports=[{'valence':-.7,'arousal':.8,'elapsed_seconds':10.005}]
    assert guidance_mode(s)[0]=='brief'
    s.reports[-1]['elapsed_seconds']=11
    assert guidance_mode(s)[0]=='choice'


def test_setback_support_never_implicitly_enables_break_reminders():
    p=PlaySupport()
    for now in range(301):assert not tick(p,'steady',now)


def test_clock_pauses_outside_game_and_does_not_count_stale_or_suspended_time():
    p=PlaySupport()
    for now in range(100):tick(p,'steady',now)
    before=p.play_seconds
    for now in range(100,300):
        p.update(GameObservation(None,'Other app',state={'kind':'out_of_focus'}),now,enabled=True,active=True,paused=False)
    assert p.play_seconds==before
    assert not tick(p,'steady',300)
    stale=observation('steady')
    p.update(stale,301,enabled=True,active=True,paused=False)
    p.update(stale,900,enabled=True,active=True,paused=False)
    assert p.play_seconds<105


def test_timer_respects_mute_pause_and_camera_independence():
    p=PlaySupport()
    for now in range(100):tick(p,'steady',now)
    assert not p.update(observation('steady'),100,enabled=False,active=True,paused=False)
    assert p.play_seconds==0
    for now in range(101,201):tick(p,'steady',now)
    p.update(observation('steady'),201,enabled=True,active=True,paused=True)
    assert p.play_seconds==0
    for now in range(202,350):assert not tick(p,'steady',now)


def test_timer_and_fall_share_cooldown_and_wait_for_motion_to_settle():
    p=PlaySupport()
    for now in range(149):tick(p,'steady',now,count=0)
    assert not tick(p,'falling',149)
    assert not tick(p,'falling',150)
    assert not tick(p,'falling',151)
    tick(p,'steady',152)
    assert tick(p,'steady',154).startswith('Possible fall.')
    assert p.play_seconds==0
    assert p.basis=='Experimental game-window motion estimate'


def test_process_observation_does_not_enable_break_reminders():
    p=PlaySupport()
    for now in range(151):
        assert not p.update(GameObservation('Valorant','Foreground process detected',state={'kind':'unsupported'}),now,enabled=True,active=True,paused=False)
