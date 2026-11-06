"""Responsive expression reflection; reported feelings remain independent CMA data."""
from collections import Counter,deque
import time
from checkpoint.expression_view import ExpressionDisplay,EXPRESSIONS,category_estimate
from checkpoint.signal_filter import OneEuro

TITLES={'neutral':'Neutral expression','happiness':'Smile-like expression','laugh':'Laugh-like expression',
        'anger':'Tense expression','sadness':'Downturned expression','surprise':'Surprised-looking expression',
        'disgust':'Disgust-like expression','fear':'Fear-like expression','contempt':'One-sided expression','tension':'Mouth and brows tense'}
ARTWORK={key:value[1] for key,value in EXPRESSIONS.items()};ARTWORK['laugh']='happy';ARTWORK['tension']='frustrated'


class ReflectionEngine:
    # Engineering defaults, not validated emotion-duration thresholds.
    DWELL=.45
    NEUTRAL_DWELL=.65
    MAX_GAP=1.
    TREND_SECONDS=4.

    def __init__(self):
        self.token=None;self.generation=None;self.pattern=None;self.pending=None;self.pending_at=0.;self.pending_count=0
        self.changed=0.;self.filters={};self.smoothed={};self.samples=deque(maxlen=160)
        self.valid_seconds=0.;self.hidden_seconds=0.;self.pattern_counts=Counter();self.video_test=False
        self.last_valid=-1000.;self.last_sample=None;self.last_hidden=False;self.last_usable=False;self.trend=None
        self.uncertain_since=None;self.reason='Waiting for usable tracking.'

    def reset_tracking(self):
        self.pattern=None;self.pending=None;self.pending_count=0;self.filters.clear();self.smoothed={};self.samples.clear();self.trend=None;self.uncertain_since=None

    def classify(self,cue,now):
        m=cue.movement or {}
        self.smoothed={k:self.filters.setdefault(k,OneEuro()).update(v,now) for k,v in m.items()}
        m=self.smoothed
        estimate=category_estimate(cue) or {}
        scores=estimate.get('scores') or {}
        ordered=sorted(scores.items(),key=lambda item:-item[1])
        # Scores are model scores, not calibrated probabilities of an inner feeling.
        label=ordered[0][0] if ordered else estimate.get('label')
        score=ordered[0][1] if ordered else estimate.get('score',0) or 0
        margin=score-(ordered[1][1] if len(ordered)>1 else 0)
        trusted=estimate.get('status')=='accepted' and score>=.7 and margin>=.15 and now-estimate.get('observed_at',now)<=1.
        if not m:
            if trusted and label in ARTWORK:return label,'Model estimate with a clear leading score.'
            if cue.status=='accepted' and cue.confidence is not None and cue.confidence>=.7 and cue.expression in ARTWORK:
                return cue.expression,'Model estimate.'
            return None,'The expression model is unsure.'
        smile=m.get('smile',0);brow=m.get('brow',0);jaw=m.get('jaw',0)
        tense=brow>.25 and max(m.get('pressed',0),m.get('mouth_wide',0),m.get('snarl',0))>.22 and smile<.25
        # Learned classes are primary. Unvalidated hand rules must not redefine them.
        if trusted and label in ARTWORK:
            positive=smile>.28 and m.get('cheek',0)>.25
            if label=='happiness' and tense or label in ('anger','disgust','fear','sadness','contempt') and positive:
                return None,'The model and facial movements disagree.'
            if label=='neutral' and (abs(smile)>.25 or abs(brow)>.35 or jaw>.3 or m.get('snarl',0)>.3):
                return None,'The neutral estimate conflicts with visible movement.'
            if label=='happiness' and m.get('laugh',0)>.2 and jaw>.22:
                return 'laugh','Pretrained smile estimate with an open-mouth configuration.'
            return label,'Pretrained expression estimate; your feeling remains your check-in.'
        # With no confident category, reflect only clearly supported visual configurations.
        if smile>.28 and not tense and m.get('cheek',0)>.25:
            return ('laugh' if m.get('laugh',0)>.2 and jaw>.22 else 'happiness'),'Smile and cheek evidence.'
        if tense:return 'tension','Tension is visible; anger, effort and focus remain ambiguous.'
        resting=abs(smile)<.16 and abs(brow)<.2 and jaw<.18 and m.get('mouth_wide',0)<.2 and m.get('snarl',0)<.15
        if resting:return 'neutral','A relaxed-looking facial configuration, not a claim of calm.'
        return None,'No clear agreement yet. Nori stays neutral-looking.'

    def observe(self,session,now):
        if self.generation!=session.generation:
            self.reset_tracking();self.generation=session.generation;self.token=None;self.last_sample=None;self.last_valid=-1000.
        cue=session.cue;token=(session.generation,session.cue_received_at)
        if not cue or token==self.token or now-session.cue_received_at>self.MAX_GAP:return
        self.token=token;m=cue.movement or {};hidden=m.get('mouth_visible',1)<.5
        usable=cue.status=='accepted' and not hidden
        dt=now-self.last_sample if self.last_sample is not None and 0<now-self.last_sample<=self.MAX_GAP else 0.
        if usable and self.last_usable:self.valid_seconds+=dt
        if hidden and self.last_hidden:self.hidden_seconds+=dt
        if self.last_sample is not None and now-self.last_sample>self.MAX_GAP:self.reset_tracking()
        self.last_sample=now;self.last_hidden=hidden;self.last_usable=usable
        self.video_test|=session.source_kind=='video'
        if not usable:
            self.reset_tracking();self.reason='Mouth hidden; expression withheld.' if hidden else cue.reason or 'No usable face.'
            return
        self.last_valid=now
        candidate,self.reason=self.classify(cue,now)
        if candidate is None:
            self.pending=None;self.pending_count=0;self.trend=None
            if self.uncertain_since is None:self.uncertain_since=now
            if now-self.uncertain_since>=.35:self.pattern=None
            self.samples.append((now,None))
            return
        self.uncertain_since=None
        if candidate!=self.pending:
            self.pending=candidate;self.pending_at=now;self.pending_count=1
        else:self.pending_count+=1
        dwell=self.NEUTRAL_DWELL if candidate=='neutral' else self.DWELL
        if candidate!=self.pattern and self.pending_count>=3 and now-self.pending_at>=dwell:
            self.pattern=candidate;self.changed=now;self.pattern_counts[candidate]+=1
        self.samples.append((now,candidate))
        while self.samples and now-self.samples[0][0]>self.TREND_SECONDS:self.samples.popleft()
        self.trend=None
        if self.samples and now-self.samples[0][0]>=self.TREND_SECONDS-.5:
            durations=Counter();coverage=0.
            for (t,a),(u,b) in zip(self.samples,list(self.samples)[1:]):
                if u-t<=self.MAX_GAP:
                    coverage+=u-t
                    if a==b:durations[a]+=u-t
            if coverage>=self.TREND_SECONDS-.5 and durations:
                key,span=durations.most_common(1)[0]
                if span/coverage>=.75:self.trend=key

    def display(self,session,now=None):
        now=time.monotonic() if now is None else now;self.observe(session,now)
        if not session.experimental_analysis or not session.camera_active:
            self.reset_tracking()
            return ExpressionDisplay('Ready when you are',None,'Start face tracking to see a live reflection. Choose a feeling whenever you want to check in.',source='visual_pattern')
        if now-self.last_valid>self.MAX_GAP or self.pattern is None:
            detail=self.reason if session.cue else 'Starting the tracker. Your preview can appear before the models are ready.'
            return ExpressionDisplay('Expression unclear' if session.cue else 'Looking for your face',None,detail,source='visual_pattern')
        title=TITLES[self.pattern];detail='A smoothed visual signal. Your check-in records how you feel.'
        if self.trend:detail=f'Recent trend: {TITLES[self.trend].lower()}. Your check-in records how you feel.'
        movement=None
        if self.pattern=='laugh':
            # Authored companion pose, not a copy of every camera movement.
            movement={'smile':.75,'jaw':.4,'laugh':.45,'eyes':.8,'eye_left':.8,'eye_right':.8,
                      'teeth':min(.7,self.smoothed.get('teeth',0)),'brow':0.,'mouth_visible':1.}
        if self.pattern in ('happiness','laugh','anger','tension') and self.smoothed.get('teeth',0)>.25:
            movement=movement or {}
            movement.update(teeth=min(.7,self.smoothed['teeth']),jaw=.35 if self.pattern in ('happiness','laugh') else .2)
        return ExpressionDisplay(title,ARTWORK[self.pattern],detail,movement,source='visual_pattern')

    def summary(self):
        return {'usable_face_seconds':round(self.valid_seconds,1),'mouth_hidden_seconds':round(self.hidden_seconds,1),
                'expression_transitions':dict(self.pattern_counts),'video_test':self.video_test,
                'recent_visual_trend':self.trend,'basis':'Smoothed expression transitions, not emotion durations; no facial event log retained'}
