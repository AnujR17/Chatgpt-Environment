"""Live derived state, conservative nudges, and a CMA report without sensor logs."""
import time
from checkpoint.blob import parameters,movement_visual
from checkpoint.character import CHARACTER_NAME
from checkpoint.cma_report import cma_summary
from checkpoint.expression_view import category_estimate


class CompanionState:
    def __init__(self):
        self.nudge='';self.nudge_at=0.;self.last_prompt=-1000.;self.last_fall=-1000.;self.fall_pending=False
        self.activity_sums={};self.activity_count=0;self.last_activity=-100.

    def update(self,session,display,game,*,input_stats=None,nudges=False,motion_enabled=True,reflection_summary=None,now=None):
        now=time.monotonic() if now is None else now;elapsed=round(session.elapsed(),1)
        title=display.title if display else session.affect[0];artwork=display.artwork if display else session.report
        source=display.source if display else 'player_report' if session.report else 'unassigned'
        cue=game.cue if game else '';game_status=game.status if game else 'Game observation off'
        if input_stats and now-self.last_activity>=5:
            for key in ('mouse_motion_per_second','clicks_per_second','key_presses_per_second'):
                value=input_stats.get(key)
                if isinstance(value,(int,float)):self.activity_sums[key]=self.activity_sums.get(key,0)+value
            self.activity_count+=1;self.last_activity=now
        if cue.startswith('Possible fall'):self.last_fall=now;self.fall_pending=True
        idle=(input_stats or {}).get('idle_seconds')
        if (nudges and self.fall_pending and 3<now-self.last_fall<25 and idle is not None and idle>=3
                and now-self.last_prompt>=120 and session.active and session.break_deadline is None):
            self.nudge='A setback? Take a moment if you want.';self.nudge_at=now;self.last_prompt=now;self.fall_pending=False
        if now-self.nudge_at>=10:self.nudge=''
        if not nudges or not session.active or session.break_deadline is not None:self.nudge=''
        activity={k:round(v/self.activity_count,2) for k,v in self.activity_sums.items()} if self.activity_count else None
        report=cma_summary(session,activity)
        if reflection_summary:report['observations']=reflection_summary
        visual=parameters(artwork) if display and display.source!='player_report' else parameters(artwork,session.valence,session.arousal)
        if display and display.movement:
            if display.source=='visual_pattern':visual.update(display.movement)
            else:visual=movement_visual(display.movement)
        state={'version':2,'character':CHARACTER_NAME,'updated_at':time.time(),'elapsed_seconds':elapsed,
            'animate':bool(motion_enabled and session.active and session.break_deadline is None),'active':session.active,'paused':session.break_deadline is not None,'game':session.game,
            'detail':display.detail if display else '', 'title':title,'source':source,'artwork':artwork,'blob':visual,'unknown':artwork is None,
            'camera_active':session.camera_active,'capture_source':session.source_kind,'game_status':game_status,'game_cue':cue,
            'checkin':{'title':session.affect[0],'pleasantness':session.affect[1],'activation':session.affect[2]},
            'model_estimate':category_estimate(session.cue) if display and display.source in ('face_movement','expression_estimate','visual_pattern') else None,
            'input':input_stats or {'status':'Input observation off'},'nudge':self.nudge,
            'cma_report':{k:report['cma'][k] for k in ('count','trend','insight','next_step','latest')}}
        return state,report
