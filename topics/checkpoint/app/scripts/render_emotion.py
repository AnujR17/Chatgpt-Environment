"""Reproducible native screenshots, reference atlas and actual procedural MP4."""
import argparse,json,math,subprocess
from pathlib import Path
from PySide6.QtCore import Qt,QEvent,QPointF
from PySide6.QtGui import QImage,QPainter,QFont,QColor
from PySide6.QtWidgets import QWidget,QHBoxLayout
from checkpoint.app import create_application,MainWindow,CheckinDialog
from checkpoint.affect import ANCHORS,contours,svg_path,dimension_words
from checkpoint.motion import AffectWidget
from checkpoint.theme import PALETTES

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts'
app=create_application([])

def render(widget,path):
    app.processEvents();im=QImage(widget.size(),QImage.Format.Format_ARGB32);im.fill(0);widget.render(im);im.save(str(path));return im


def cleanup(widget):
    widget.close();widget.deleteLater();app.sendPostedEvents(None,QEvent.Type.DeferredDelete);app.processEvents()


def screenshots():
    w=MainWindow(no_setup=True,data_dir=OUT/'preview-no-history');w.show();w.timer.stop();w.session.check_in('excited');w.refresh()
    for e in w.emblems:e.timer.stop();e.value=e.target;e.phase=2.1
    render(w,OUT/'emotion-ui-light.png')
    d=CheckinDialog(w);d.select('frustrated');d.show();d.preview.timer.stop();d.preview.value=d.preview.target;render(d,OUT/'emotion-checkin.png');cleanup(d)
    w.toggle_theme()
    for e in w.emblems:e.timer.stop();e.value=e.target;e.phase=2.1
    render(w,OUT/'emotion-ui-dark.png')
    w.toggle_theme();w.session.check_in('angry');w.change_view(1)
    for e in w.emblems:e.timer.stop();e.value=e.target;e.phase=2.1
    render(w,OUT/'emotion-ui-lines.png')
    w.session.check_in('calm');w.change_view(2)
    for e in w.emblems:e.timer.stop();e.value=e.target;e.phase=2.1
    render(w,OUT/'emotion-ui-dots.png')
    w.session.check_in('mixed');w.refresh();render(w,OUT/'emotion-ui-unknown.png');cleanup(w)


def font(p,size,bold=False):
    f=QFont('DM Sans');f.setPixelSize(size);f.setBold(bold);p.setFont(f)


def atlas():
    im=QImage(1440,1320,QImage.Format.Format_ARGB32);im.fill(QColor('#F4F2EC'));p=QPainter(im);p.setRenderHint(QPainter.RenderHint.Antialiasing);p.setPen(QColor('#252D29'));font(p,34,True);p.drawText(40,56,'Twelve words. A continuous emotional space.');font(p,16);p.drawText(40,88,'CMA reference points · Adjustable design defaults · Similar feelings can share a form')
    glyph=AffectWidget(240);glyph.show();glyph.timer.stop()
    data=[]
    for i,(key,(title,v,a,desc)) in enumerate(ANCHORS.items()):
        x=40+i%4*350;y=120+i//4*380
        p.setPen(Qt.PenStyle.NoPen);p.setBrush(QColor('#FFFEFA'));p.drawRoundedRect(x,y,330,360,18,18)
        glyph.set_state(key,v,a);glyph.timer.stop();glyph.value=(v,a);glyph.phase=2.1
        g=QImage(glyph.size(),QImage.Format.Format_ARGB32);g.fill(0);glyph.render(g);p.drawImage(x+45,y+3,g)
        p.setPen(QColor('#252D29'));font(p,23,True);p.drawText(x+22,y+268,title);font(p,13);p.setPen(QColor('#626B65'));d1,d2=dimension_words(v,a);p.drawText(x+22,y+297,d1+' · '+d2);p.drawText(x+22,y+323,f'Valence {v:+.2f}  /  Activation {a:+.2f}')
        data.append({'key':key,'label':title,'valence':v,'arousal':a,'description':desc,'dimensions':[d1,d2],'paths':[svg_path(path,360) for path in contours(v,a,2.1)]})
    font(p,14);p.drawText(40,1300,'Shapes encode reported dimensions, not unique emotion identities. Unknown / mixed stays unassigned.');p.end();im.save(str(OUT/'emotion-atlas.png'));cleanup(glyph)
    (ROOT/'design/emotion-geometry.json').write_text(json.dumps(data))


def video():
    stage=QWidget();stage.resize(1280,720);stage.setStyleSheet('background:#F4F2EC;');stage.show()
    glyphs=[]
    for i in range(3):
        g=AffectWidget(360,mode=i);g.setParent(stage);g.move(26+i*414,145);g.show();glyphs.append(g)
    sequence=['calm','excited','tense','frustrated','sad','happy'];fps=30;seconds=18
    ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','bgra','-s','1280x720','-r',str(fps),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT/'emotion-motion.mp4')],stdin=subprocess.PIPE)
    phase=0.
    for frame in range(seconds*fps):
        t=frame/fps;index=min(len(sequence)-1,int(t/3));key=sequence[index];title,v,a,_=ANCHORS[key]
        previous=ANCHORS[sequence[max(0,index-1)]][1:3];u=min(1.,(t-index*3)/.8);e=u*u*(3-2*u);value=tuple(x+(y-x)*e for x,y in zip(previous,(v,a)))
        phase+=2*math.pi*(.07+.19*(value[1]+1)/2)/fps
        for g in glyphs:g.set_state(key,v,a);g.timer.stop();g.value=value;g.phase=phase
        app.processEvents();im=QImage(stage.size(),QImage.Format.Format_ARGB32);im.fill(QColor('#F4F2EC'));stage.render(im)
        p=QPainter(im);p.setPen(QColor('#252D29'));font(p,34,True);p.drawText(40,62,'A feeling, in motion.');font(p,16);p.setPen(QColor('#626B65'));p.drawText(40,98,'One continuous CMA mapping. Three ways to read the same reported moment.')
        for i,name in enumerate(['01  Form','02  Lines','03  Dots']):font(p,16);p.drawText(50+i*414,158,name)
        p.setPen(QColor('#252D29'));font(p,36,True);p.drawText(40,572,title);font(p,20);p.setPen(QColor('#626B65'));p.drawText(40,612,'  ·  '.join(dimension_words(*value)));font(p,14);p.drawText(40,676,'Illustrative check-ins · 800ms transitions · Native Qt rendering · No facial inference')
        p.end();ff.stdin.write(bytes(im.bits()))
        if frame in [0,105,195,285,375,465]:im.save(str(OUT/f'emotion-motion-{frame:03}.png'))
    ff.stdin.close();code=ff.wait();assert code==0;cleanup(stage)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--video',action='store_true');args=parser.parse_args();screenshots();atlas()
    if args.video:video()
