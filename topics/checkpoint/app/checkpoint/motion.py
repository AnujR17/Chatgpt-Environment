"""Native, bounded CMA visual. Unknown states never animate or imply neutrality."""
import math
import time
from PySide6.QtCore import Qt, QTimer, QPointF
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QWidget
from checkpoint.affect import REFERENCES, contours
from checkpoint.symbols import scene
from checkpoint.theme import PALETTES


def painter_path(points, centre, scale):
    p=[QPointF(centre.x()+x*scale,centre.y()+y*scale) for x,y in points];n=len(p)
    path=QPainterPath(p[0])
    for i in range(n):
        p0,p1,p2,p3=p[(i-1)%n],p[i],p[(i+1)%n],p[(i+2)%n]
        path.cubicTo(p1+(p2-p0)/6,p2-(p3-p1)/6,p2)
    path.closeSubpath();return path


class AffectWidget(QWidget):
    def __init__(self,size=None,mode=0):
        super().__init__();self.setMinimumSize(220,300)
        if size:self.setFixedSize(size,size)
        self.mode=mode;self.current_state=None;self.target=None;self.start=(0.,0.);self.value=(0.,0.)
        self.transition_start=0.;self.phase=0.;self.reduced_motion=False;self.paused=False;self.enabled=True;self.theme='light'
        self.animation_time=0.;self.previous_state=None;self.fade_start=0.;self.fade_override=None
        self.clock=time.monotonic();self.timer=QTimer(self);self.timer.setTimerType(Qt.TimerType.PreciseTimer);self.timer.timeout.connect(self.tick)
        self.setAccessibleName('Feeling form: no check-in yet');self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def set_state(self,state,valence=None,arousal=None):
        target=(valence,arousal) if valence is not None and arousal is not None else REFERENCES[state][1:3] if state in REFERENCES else None
        if state==self.current_state and target==self.target:return
        self.previous_state=self.current_state;self.fade_start=time.monotonic();self.current_state=state;self.start=self.value;self.target=target;self.transition_start=time.monotonic()
        if target is not None and (self.reduced_motion or self.paused):self.value=target;self.start=target
        self.setAccessibleName('Feeling form: '+(REFERENCES[state][0] if state in REFERENCES else 'mixed or not reported'))
        self.sync_timer();self.update()

    def configure(self,*,theme=None,reduced_motion=None,paused=None,enabled=None):
        before=(self.theme,self.reduced_motion,self.paused,self.enabled)
        if theme is not None:self.theme=theme
        if reduced_motion is not None:self.reduced_motion=reduced_motion
        if paused is not None:self.paused=paused
        if enabled is not None:self.enabled=enabled
        if before==(self.theme,self.reduced_motion,self.paused,self.enabled):return
        if (self.reduced_motion or self.paused) and self.target is not None:self.value=self.target;self.start=self.target
        self.sync_timer();self.update()

    def sync_timer(self):
        run=self.isVisible() and self.enabled and self.target is not None and not self.reduced_motion and not self.paused
        if run and not self.timer.isActive():self.clock=time.monotonic();self.timer.start(33)
        elif not run:self.timer.stop()

    def tick(self):
        now=time.monotonic();dt=min(.1,now-self.clock);self.clock=now;self.animation_time+=dt
        if self.target is None:return
        t=min(1.,max(0.,(now-self.transition_start)/.8));e=t*t*(3-2*t)
        self.value=tuple(x+(y-x)*e for x,y in zip(self.start,self.target))
        self.phase+=dt*2*math.pi*(.07+.19*(self.value[1]+1)/2)
        self.update()

    def showEvent(self,event):super().showEvent(event);self.sync_timer()
    def hideEvent(self,event):self.timer.stop();super().hideEvent(event)

    def draw_symbol(self,p,key,centre,opacity,zoom):
        p.save();p.translate(centre);factor=min(self.width(),self.height())*1.30/360*zoom;p.scale(factor,factor);p.translate(-180,-180)
        colours=PALETTES[self.theme]
        for item in scene(key,self.animation_time):
            ink=QColor(colours[item['role']]);ink.setAlphaF(item['opacity']*opacity)
            if item['kind']=='dot':p.setPen(Qt.PenStyle.NoPen);p.setBrush(ink);p.drawEllipse(QPointF(item['x'],item['y']),item['r'],item['r']);continue
            path=QPainterPath()
            for c in item['commands']:
                if c[0]=='M':path.moveTo(c[1],c[2])
                elif c[0]=='L':path.lineTo(c[1],c[2])
                elif c[0]=='C':path.cubicTo(*c[1:])
                elif c[0]=='Q':path.quadTo(*c[1:])
                elif c[0]=='Z':path.closeSubpath()
            stroke=QColor(ink);stroke.setAlphaF(ink.alphaF()*item.get('stroke_opacity',1));pen=QPen(stroke,item['width']);pen.setCapStyle(Qt.PenCapStyle.RoundCap);pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin);p.setPen(pen if item['width'] else Qt.PenStyle.NoPen)
            fill=QColor(colours[item['fill']]) if item['fill'] else QColor(ink);fill.setAlphaF(item['opacity']*opacity*item.get('fill_opacity',1));p.setBrush(fill if item['fill'] else Qt.BrushStyle.NoBrush);p.drawPath(path)
        p.restore()

    def paintEvent(self,event):
        p=QPainter(self);p.setRenderHint(QPainter.RenderHint.Antialiasing)
        c=PALETTES[self.theme];centre=QPointF(self.width()/2,self.height()/2);scale=min(self.width(),self.height())*.53
        if self.target is None:
            if self.mode==0:
                # An empty, static body represents absence of a report, not neutral affect.
                self.draw_symbol(p,None,centre,1.,1.);p.end();return
            # Retained only for earlier CMA development views.
            pen=QPen(QColor(c['muted']),1.6,Qt.PenStyle.DotLine);p.setPen(pen);p.setBrush(Qt.BrushStyle.NoBrush)
            for r in (.60,.76):p.drawArc(int(centre.x()-r*scale),int(centre.y()-r*scale),int(2*r*scale),int(2*r*scale),25*16,295*16)
            p.end();return
        if self.mode==0:
            fade=1. if self.reduced_motion or self.paused else self.fade_override if self.fade_override is not None else min(1.,(time.monotonic()-self.fade_start)/.45)
            fade=fade*fade*(3-2*fade)
            if self.previous_state in REFERENCES and fade<1:self.draw_symbol(p,self.previous_state,centre,1-fade,1.)
            self.draw_symbol(p,self.current_state,centre,fade,.97+.03*fade);p.end();return
        v,a=self.value;blend=max(0.,min(1.,(v+1)/2));warm=QColor(c['unpleasant']);cool=QColor(c['pleasant'])
        col=QColor.fromRgbF(warm.redF()*(1-blend)+cool.redF()*blend,warm.greenF()*(1-blend)+cool.greenF()*blend,warm.blueF()*(1-blend)+cool.blueF()*blend)
        paths=contours(v,a,self.phase)
        if self.mode==0:
            fill=QColor(col);fill.setAlphaF(.075 if self.theme=='light' else .12)
            p.setPen(Qt.PenStyle.NoPen);p.setBrush(fill);p.drawPath(painter_path(paths[-1],centre,scale))
        if self.mode in (0,1):
            for j,points in enumerate(paths):
                ink=QColor(col);ink.setAlphaF(.38+j*.12);p.setPen(QPen(ink,1.4 if self.mode==0 else 1.65));p.setBrush(Qt.BrushStyle.NoBrush);p.drawPath(painter_path(points,centre,scale))
        # Dots travel along the same contours; activation increases speed, not distress severity.
        p.setPen(Qt.PenStyle.NoPen)
        for j,points in enumerate(paths):
            number=22 if self.mode==2 else 3
            for k in range(number):
                t=(k/number+self.phase/(2*math.pi)*(.11+j*.015))%1*len(points)
                idx=int(t);mix=t-idx;x1,y1=points[idx];x2,y2=points[(idx+1)%len(points)]
                pos=QPointF(centre.x()+(x1+(x2-x1)*mix)*scale,centre.y()+(y1+(y2-y1)*mix)*scale)
                ink=QColor(col);ink.setAlphaF(.35+.55*(k+1)/number);p.setBrush(ink)
                radius=(1.5+(a+1)*.35) if self.mode==2 else 2.4;p.drawEllipse(pos,radius,radius)
        p.end()
