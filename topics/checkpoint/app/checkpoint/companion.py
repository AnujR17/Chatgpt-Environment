"""A bounded, source-labelled session report and conservative, optional nudge policy."""
from collections import deque
import time
from checkpoint.blob import parameters,movement_visual


class CompanionState:
    def __init__(self):
        self.started=time.monotonic();self.moments=deque(maxlen=240);self.last_key=None;self.last_moment=-100.
        self.nudge='';self.nudge_at=0.;self.last_prompt=-1000.;self.last_fall=-1000.;self.fall_pending=False
        self.activity_samples=deque(maxlen=360);self.last_activity=-100.

    def update(self,session,display,game,*,input_stats=None,nudges=False,now=None):
        now=time.monotonic() if now is None else now;elapsed=round(session.elapsed(),1)
        title=display.title if display else session.affect[0]
        artwork=display.artwork if display else session.report
        source=display.source if display else 'player_report' if session.report else 'unassigned'
        cue=game.cue if game else '';game_status=game.status if game else 'Game observation off'
        key=(title,source,cue,session.active)
        if (display or session.report or cue or not session.active) and key!=self.last_key and now-self.last_moment>=3:
            self.moments.append({'elapsed_seconds':elapsed,'label':title,'source':source,'game_cue':cue})
            self.last_key=key;self.last_moment=now
        if input_stats and now-self.last_activity>=5:
            self.activity_samples.append({'elapsed_seconds':elapsed,**input_stats});self.last_activity=now
        if cue.startswith('Possible fall'):
            self.last_fall=now;self.fall_pending=True
        # An opt-in invitation is held until input has actually been quiet, not triggered by a face class.
        idle=(input_stats or {}).get('idle_seconds')
        if (nudges and self.fall_pending and 3<now-self.last_fall<25 and idle is not None and idle>=3
                and now-self.last_prompt>=120 and session.active and session.break_deadline is None):
            self.nudge='A setback? Take a moment if you want.';self.nudge_at=now;self.last_prompt=now;self.fall_pending=False
        if now-self.nudge_at>=10:self.nudge=''
        if not nudges or not session.active or session.break_deadline is not None:self.nudge=''
        report=session.summary();report.update({'schema':2,'moments':list(self.moments),
            'input_activity':list(self.activity_samples),
            'limitations':['Expression estimates are not mood/CMA measurements','Game cues are experimental visual estimates','Input activity is not a frustration score']})
        visual=parameters(artwork)
        if display and display.movement:visual=movement_visual(display.movement)
        state={'version':1,'character':'Pip','updated_at':time.time(),'elapsed_seconds':elapsed,
            'active':session.active,'paused':session.break_deadline is not None,'game':session.game,
            'title':title,'source':source,'artwork':artwork,'blob':visual,
            'unknown':artwork is None,'camera_active':session.camera_active,'game_status':game_status,'game_cue':cue,
            'checkin':{'title':session.affect[0],'pleasantness':session.affect[1],'activation':session.affect[2]},
            'input':input_stats or {'status':'Input observation off'},'nudge':self.nudge,'moments':list(self.moments)[-6:]}
        return state,report
