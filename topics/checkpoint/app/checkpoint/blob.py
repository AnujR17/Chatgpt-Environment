"""Nori: one continuous native body, reused by the app and transparent companion.
Animation parameters are presentation choices, never automatic CMA measurements.
"""
import math
import time
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen
from checkpoint.motion import AffectWidget, painter_path
from checkpoint.character import CHARACTER_NAME,FEELING_LOOKS,COLOURS
from checkpoint.vocabulary import CARDS


BASE = dict(red=151., green=190., blue=175., stretch=0., tension=0., smile=0., eyes=1., brow=0., energy=.2,jaw=0.,laugh=0.,eye_left=1.,eye_right=1.,brow_skew=0.,mouth_wide=0.,pressed=0.,pucker=0.,snarl=0.,asymmetry=0.,teeth=0.,hand=0.,hand_side=1.,mouth_visible=1.,tears=0.,lean=0.)
LOOKS = {
    'happy': dict(red=235,green=188,blue=102,smile=.9,eyes=.65,energy=.55,stretch=.06),
    'excited': dict(red=235,green=178,blue=103,smile=1.,eyes=1.15,energy=.8,stretch=.12),
    'angry': dict(red=226,green=135,blue=116,smile=-.65,eyes=.65,brow=.75,tension=.5,energy=.65),
    'frustrated': dict(red=219,green=151,blue=126,smile=-.45,eyes=.7,brow=.55,tension=.35,energy=.5),
    'annoyed': dict(red=192,green=166,blue=159,smile=-.25,eyes=.45,brow=.35,tension=.2),
    'sad': dict(red=154,green=174,blue=199,smile=-.75,eyes=.6,brow=-.55,stretch=-.08,energy=.12),
    'afraid': dict(red=194,green=185,blue=167,smile=-.35,eyes=1.4,brow=-.7,tension=.35,energy=.6),
    'surprised': dict(red=183,green=175,blue=207,smile=0.,eyes=1.45,brow=-.5,stretch=.12,energy=.6),
    'confused': dict(red=198,green=187,blue=156,smile=-.1,eyes=1.1,brow=-.3,tension=.12),
    'disgust': dict(red=168,green=185,blue=158,smile=-.4,eyes=.5,brow=.4,tension=.25),
    'exhausted': dict(red=174,green=181,blue=176,smile=-.1,eyes=.3,stretch=-.14,energy=.05),
}
ALIASES = {'happiness':'happy','neutral':'composed','anger':'angry','sadness':'sad','fear':'afraid','surprise':'surprised','contempt':'annoyed',
           'delighted':'happy','contented':'happy','grateful':'happy','exhilarated':'excited','bewildered':'confused','miserable':'sad','weepy':'sad','withdrawn':'sad','bored':'exhausted',
           'amused':'happy','appalled':'surprised','astonished':'surprised','awe':'surprised','brooding':'sad','combative':'angry','curious':'confused',
           'disappointed':'sad','hate':'angry','hysterical':'excited','hopeful':'happy','indignant':'angry','loathing':'disgust','modest':'composed',
           'satisfied':'happy','serene':'composed','shy':'confused','sneaky':'annoyed','silly':'happy','wonder':'surprised','determined':'composed'}


def parameters(key,valence=None,arousal=None):
    result=dict(BASE)
    if key in FEELING_LOOKS:
        result.update(zip(('red','green','blue'),COLOURS[CARDS[key]['colour']]))
        result.update(FEELING_LOOKS[key])
    else:result.update(LOOKS.get(ALIASES.get(key,key),{}))
    result['eye_left']=result['eyes'];result['eye_right']=result['eyes']
    # Only self-report coordinates modulate the body. Camera movements pass no CMA.
    if valence is not None and arousal is not None:
        v=max(-1.,min(1.,valence));a=max(-1.,min(1.,arousal))
        result['energy']=.6*result['energy']+.4*(a+1)/2
        result['stretch']+=a*.065
        target=(207,195,142) if v>=0 else (170,175,197)
        for channel,value in zip(('red','green','blue'),target):result[channel]+=(value-result[channel])*abs(v)*.22
    return result


def movement_visual(movement):
    result=parameters(None);result.update(movement)
    positive=max(0.,result['smile']);drawn=max(0.,result['brow'])*(1-positive);low=max(0.,-result['smile'])
    for channel,happy,angry,sad in [('red',235,226,154),('green',188,135,174),('blue',102,116,199)]:
        value=BASE[channel];result[channel]=value+(happy-value)*positive*.6+(angry-value)*drawn*.55+(sad-value)*low*.5
    result['smile']-=drawn*.3
    result['brow']*=1-positive*.85
    result['eyes']*=1-.22*drawn-.18*positive
    result['eye_left']=movement.get('eye_left',movement.get('eyes',1.))*(1-.22*drawn-.18*positive)
    result['eye_right']=movement.get('eye_right',movement.get('eyes',1.))*(1-.22*drawn-.18*positive)
    result['stretch']=result['jaw']*.065+positive*.035-drawn*.07
    result['lean']=movement.get('lean',result['asymmetry']*.07)
    result['energy']=.2+result['laugh']*.25
    return result


def follow_visual(current,target,dt):
    """Time-based low-pass response, which does not restart on each camera sample."""
    result={}
    for key in BASE:
        tau=.45 if key in ('red','green','blue') else .3 if key in ('stretch','tension','energy') else .14 if target[key]>current[key] else .24
        alpha=1-math.exp(-max(0.,dt)/tau)
        value=current[key]+(target[key]-current[key])*alpha
        result[key]=target[key] if abs(value-target[key])<.001 else value
    return result


def contour(params, phase=0.):
    points=[]
    for i in range(64):
        angle=2*math.pi*i/64
        radius=.76 + .045*math.sin(3*angle+.5) + .025*math.cos(2*angle-.8)
        radius += params['tension']*.02*math.cos(4*angle)
        radius += .012*math.sin(phase)*math.sin(angle)**2
        points.append((math.cos(angle)*radius*(1-params['stretch']*.35)+params.get('lean',0)*math.sin(angle), math.sin(angle)*radius*(1+params['stretch'])))
    return points


class NoriWidget(AffectWidget):
    def __init__(self, size=None, mode=0):
        self.pip_current=parameters(None);self.pip_to=dict(self.pip_current);self.pip_clock=time.monotonic()
        self.movement=None;self.profile_key=None;self.report_coords=(None,None);self.motion_phase=0.
        super().__init__(size,mode)

    def set_state(self,state,valence=None,arousal=None):
        if state is None:
            self.pip_current=parameters(None);self.pip_to=parameters(None);self.pip_clock=time.monotonic()
        elif (state,valence,arousal)!=self.profile_key:
            self.interpolated();self.pip_to=parameters(state,valence,arousal)
        self.profile_key=(state,valence,arousal);self.report_coords=(valence,arousal)
        super().set_state(state,valence,arousal)
        self.setAccessibleName(CHARACTER_NAME+' · '+(str(state) if state else 'no current estimate'))

    def set_movement(self,movement):
        if self.movement is not None and movement is None:
            self.interpolated();self.pip_to=parameters(self.current_state,*self.report_coords)
        self.movement=movement
        if movement:
            target=movement_visual({k:float(v) for k,v in movement.items() if k in BASE})
            if target!=self.pip_to:self.interpolated();self.pip_to=target
        if movement and movement.get('mouth_visible',1)<.5:
            for key in ('smile','jaw','teeth','laugh','mouth_wide'):self.pip_current[key]=0.
        # Live values must repaint even when decorative animation is paused/reduced.
        self.update()

    def interpolated(self):
        now=time.monotonic();dt=max(0.,now-self.pip_clock);self.pip_clock=now
        self.pip_current=dict(self.pip_to) if self.reduced_motion or self.paused else follow_visual(self.pip_current,self.pip_to,dt)
        return dict(self.pip_current)

    def tick(self):
        previous=self.animation_time;super().tick()
        self.motion_phase+=(self.animation_time-previous)*(.45+self.pip_current['energy']*.8)

    def paintEvent(self,event):
        p=QPainter(self);p.setRenderHint(QPainter.RenderHint.Antialiasing)
        v=self.interpolated();self.pip_current=v
        size=min(self.width(),self.height());centre=QPointF(self.width()/2,self.height()*.50);scale=size*.48
        phase=0. if self.reduced_motion or self.paused else self.motion_phase
        ink=QColor('#34453E')
        unknown=self.current_state is None or self.target is None
        if unknown:v=parameters(None);phase=0.
        # Less than 1% body-height movement: a small laugh, no screen shake.
        if not self.reduced_motion and not self.paused:
            centre.setY(centre.y()-scale*.016*v['laugh']*(.5+.5*math.sin(phase*6)))
        body=QColor(round(v['red']),round(v['green']),round(v['blue']))
        p.setPen(Qt.PenStyle.NoPen);shadow=QColor('#34453E');shadow.setAlpha(19);p.setBrush(shadow)
        p.drawEllipse(QPointF(centre.x(),centre.y()+scale*.83),scale*.64,scale*.07)
        pen=QPen(ink, max(1.5,size*.009));pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin);p.setPen(pen)
        if unknown:pen.setColor(QColor('#8B9D92'));p.setPen(pen)
        p.setBrush(body);p.drawPath(painter_path(contour(v,phase),centre,scale))
        centre.setX(centre.x()+v['lean']*scale*.25)
        eye_y=centre.y()-scale*.02;eye_x=scale*.23
        blink=.12 if not unknown and not self.reduced_motion and self.animation_time%7.8>7.63 else 1.
        eye_h=max(1.8,scale*.065*v['eyes']*blink)
        p.setBrush(ink);p.setPen(Qt.PenStyle.NoPen)
        for direction in (-1,1):
            x=centre.x()+direction*eye_x
            eye_value=v['eye_left'] if direction==-1 else v['eye_right']
            if (v['smile']>.28 and eye_value<.9) or v['laugh']>.15:
                eye=QPainterPath(QPointF(x-scale*.05,eye_y+scale*.018))
                eye.quadTo(x,eye_y-scale*.08,x+scale*.05,eye_y+scale*.018)
                p.setPen(QPen(ink,max(1.5,size*.009)));p.setBrush(Qt.BrushStyle.NoBrush);p.drawPath(eye)
            else:
                p.setPen(Qt.PenStyle.NoPen);p.setBrush(ink);p.drawEllipse(QPointF(x,eye_y),scale*.035,max(1.8,scale*.065*eye_value*blink))
        pen=QPen(ink,max(1.5,size*.009));pen.setCapStyle(Qt.PenCapStyle.RoundCap);p.setPen(pen);p.setBrush(Qt.BrushStyle.NoBrush)
        if max(abs(v['brow']),abs(v['brow_skew']))>.15:
            for direction in (-1,1):
                x=centre.x()+direction*eye_x;y=eye_y-scale*.18
                brow=v['brow']+direction*v['brow_skew']
                p.drawLine(QPointF(x-scale*.075,y+direction*brow*scale*.09),QPointF(x+scale*.075,y-direction*brow*scale*.09))
        if v['mouth_visible']>.5:
            width=scale*(.14+.065*v['mouth_wide']+.055*max(0.,v['smile'])-.055*v['pucker'])
            y=eye_y+scale*.21;left_y=y+v['asymmetry']*scale*.045;right_y=y-v['asymmetry']*scale*.045
            curve=y+scale*(v['smile']*.26-v['snarl']*.06)
            opening=scale*max(v['jaw']*.27*(1-.65*v['pressed']),v['teeth']*.075)
            mouth=QPainterPath(QPointF(centre.x()-width,left_y))
            mouth.quadTo(centre.x(),curve,centre.x()+width,right_y)
            if opening>scale*.015:
                mouth.quadTo(centre.x(),curve+opening,centre.x()-width,left_y);mouth.closeSubpath();p.setBrush(ink)
            p.drawPath(mouth)
            if v['teeth']>.15 and opening>scale*.025:
                p.save();p.setClipPath(mouth);p.setPen(Qt.PenStyle.NoPen);p.setBrush(QColor('#FFFCED'))
                teeth=QPainterPath(QPointF(centre.x()-width,left_y+1))
                teeth.quadTo(centre.x(),curve+1,centre.x()+width,right_y+1)
                teeth.quadTo(centre.x(),curve+opening*.5+1,centre.x()-width,left_y+opening*.5+1);teeth.closeSubpath();p.drawPath(teeth)
                p.setPen(QPen(QColor('#9DAB9E'),max(.6,size*.004)))
                for offset in (-.04,.04):p.drawLine(QPointF(centre.x()+scale*offset,y-scale*.1),QPointF(centre.x()+scale*offset,y+scale*.3))
                p.restore()
        if v['tears']>.05:
            p.setPen(Qt.PenStyle.NoPen);p.setBrush(QColor('#8CBAC5'))
            for d in (-1,1):p.drawEllipse(QPointF(centre.x()+d*eye_x,eye_y+scale*.18),scale*.027,scale*.065*v['tears'])
        if v['hand']>.025:
            side=1 if v['hand_side']>=0 else -1;reach=v['hand']
            start=QPointF(centre.x()+side*scale*.56,centre.y()+scale*.43)
            end=QPointF(start.x()+(centre.x()+side*scale*.06-start.x())*reach,start.y()+(eye_y+scale*.24-start.y())*reach)
            arm=QPainterPath(start);arm.quadTo(start.x(),end.y()+scale*.18,end.x(),end.y())
            p.setOpacity(reach);p.setPen(QPen(ink,scale*.145,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap));p.setBrush(Qt.BrushStyle.NoBrush);p.drawPath(arm)
            p.setPen(QPen(body,scale*.11,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap));p.drawPath(arm)
            p.setPen(QPen(ink,max(1.,size*.008)));p.setBrush(body);p.drawEllipse(end,scale*.12,scale*.095)
            for dy in (-.025,.025):p.drawLine(QPointF(end.x()-scale*.03,end.y()+scale*dy),QPointF(end.x()+scale*.055,end.y()+scale*dy))
        p.end()


# Keep old code imports compatible with earlier research scripts.
PipWidget=NoriWidget
