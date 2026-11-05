"""Stable reflections of sustained visual patterns, never measured inner feelings."""
from collections import deque,Counter
import time
from checkpoint.expression_view import ExpressionDisplay


class ReflectionEngine:
    WINDOW=20.
    MIN_OBSERVED=12.
    MIN_SPAN=15.
    HOLD=30.
    def __init__(self):
        self.samples=deque(maxlen=180);self.token=None;self.generation=None;self.pattern=None;self.changed=-1000.
        self.valid_seconds=0.;self.hidden_seconds=0.;self.pattern_counts=Counter();self.video_test=False;self.last_valid=-1000.

    def observe(self,session,now):
        if self.generation!=session.generation:
            self.samples.clear();self.pattern=None;self.changed=-1000.;self.generation=session.generation;self.token=None
        cue=session.cue;token=(session.generation,session.cue_received_at)
        if not cue or token==self.token or now-session.cue_received_at>3:return
        self.token=token;movement=cue.movement or {}
        category_valid=not session.face_mapping and cue.status=='accepted'
        valid=bool(cue.status=='accepted' and ((movement and movement.get('mouth_visible',1)>.5) or category_valid))
        positive=valid and (movement.get('smile',0)>.3 or category_valid and cue.expression=='happiness')
        tense=valid and ((movement.get('brow',0)>.2 and max(movement.get('pressed',0),movement.get('mouth_wide',0),movement.get('snarl',0))>.15 and movement.get('smile',0)<.3) or category_valid and cue.expression=='anger')
        hidden=bool(movement.get('mouth_visible',1)<.5)
        previous=self.samples[-1] if self.samples else None
        dt=now-previous['time'] if previous and 0<now-previous['time']<=1 else 0.
        if valid and previous and previous['valid']:self.valid_seconds+=dt;self.last_valid=now
        elif valid:self.last_valid=now
        if hidden and previous and previous['hidden']:self.hidden_seconds+=dt
        self.video_test=self.video_test or session.source_kind=='video'
        self.samples.append({'time':now,'valid':valid,'positive':positive,'tense':tense,'hidden':hidden})
        while self.samples and now-self.samples[0]['time']>self.WINDOW:self.samples.popleft()
        coverage=positive_time=tense_time=0.
        for left,right in zip(self.samples,list(self.samples)[1:]):
            span=right['time']-left['time']
            if span<=1 and left['valid'] and right['valid']:
                coverage+=span;positive_time+=span*bool(left['positive'] and right['positive']);tense_time+=span*bool(left['tense'] and right['tense'])
        candidate=None
        if self.samples and now-self.samples[0]['time']>=self.MIN_SPAN and coverage>=self.MIN_OBSERVED:
            if tense_time/coverage>=.7:candidate='tense'
            elif positive_time/coverage>=.7:candidate='positive'
        if candidate!=self.pattern and now-self.changed>=self.HOLD:
            # Lack of clear evidence clears a suggestion only after its display hold.
            self.pattern=candidate;self.changed=now
            if candidate:self.pattern_counts[candidate]+=1

    def display(self,session,now=None):
        now=time.monotonic() if now is None else now;self.observe(session,now)
        if session.report is not None:
            title=session.affect[0];age=max(0,int(session.elapsed()-session.reports[-1]['elapsed_seconds']))
            detail=f'Your last check-in, {age//60:02d}:{age%60:02d} ago. This reflection stays until you choose another feeling.'
            return ExpressionDisplay(title,session.report,detail,source='player_report')
        if not session.experimental_analysis or not session.camera_active:
            return ExpressionDisplay('A moment to check in',None,'Choose how you feel. Optional tracking can reflect longer visual patterns; it cannot establish your feeling.',source='visual_pattern')
        if now-self.last_valid>3:
            return ExpressionDisplay('Waiting for a longer view',None,'A usable, visible face is needed. Hand-covered mouth cues are excluded. Face preview shows individual movements.',source='visual_pattern')
        if self.pattern=='tense':
            return ExpressionDisplay('A tense-looking stretch','frustrated','A pattern persisted across the recent observation window. Could it be effort, focus or frustration? Check in with the word that fits.',source='visual_pattern')
        if self.pattern=='positive':
            return ExpressionDisplay('A positive-looking stretch','contented','Smile-like cues persisted across the recent observation window. Confirm how it felt in a check-in.',source='visual_pattern')
        return ExpressionDisplay('Gathering a longer view',None,'Reflection uses a 20-second window and holds changes steadily. Use Face preview for instant movement tests.',source='visual_pattern')

    def summary(self):
        return {'usable_face_seconds':round(self.valid_seconds,1),'mouth_hidden_seconds':round(self.hidden_seconds,1),
                'sustained_patterns':dict(self.pattern_counts),'video_test':self.video_test,
                'basis':'Visual patterns, not emotion durations; no per-frame event log retained'}
