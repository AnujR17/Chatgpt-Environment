"""Export the semantic emotion library and its actual native motion."""
import argparse,json,subprocess
from pathlib import Path
from PySide6.QtCore import QEvent,Qt
from PySide6.QtGui import QImage,QPainter,QColor,QFont
from PySide6.QtWidgets import QWidget
from checkpoint.app import create_application,MainWindow,CheckinDialog,EmotionLibraryDialog
from checkpoint.symbols import CORE,MEANINGS,scene,svg_path
from checkpoint.affect import ANCHORS
from checkpoint.motion import AffectWidget

def render(widget,path):
    app.processEvents();im=QImage(widget.size(),QImage.Format.Format_ARGB32);im.fill(0);widget.render(im);im.save(str(path));return im

def cleanup(widget):
    widget.close();widget.deleteLater();app.sendPostedEvents(None,QEvent.Type.DeferredDelete);app.processEvents()

def font(p,size,bold=False):
    f=QFont('DM Sans');f.setPixelSize(size);f.setBold(bold);p.setFont(f)


OUT=Path(__file__).resolve().parents[1]/'artifacts';app=create_application([])

def shots():
    w=MainWindow(no_setup=True);w.show();w.timer.stop();w.session.check_in('frustrated');w.refresh()
    for g in w.emblems:g.timer.stop();g.fade_override=1.;g.animation_time=1.
    render(w,OUT/'emotion-ui-library.png');w.toggle_theme()
    for g in w.emblems:g.timer.stop()
    render(w,OUT/'emotion-ui-library-dark.png');w.toggle_theme()
    library=EmotionLibraryDialog(w);library.show()
    for g in library.findChildren(AffectWidget):g.timer.stop();g.animation_time=1.
    render(library,OUT/'emotion-library-dialog.png');cleanup(library)
    d=CheckinDialog(w);d.select('confused');d.show();d.preview.timer.stop();d.preview.fade_override=1.;render(d,OUT/'emotion-library-checkin.png');cleanup(d);cleanup(w)


def atlas():
    im=QImage(1440,1000,QImage.Format.Format_ARGB32);im.fill(QColor('#F4F2EC'));p=QPainter(im);p.setRenderHint(QPainter.RenderHint.Antialiasing);p.setPen(QColor('#252D29'));font(p,34,True);p.drawText(40,56,'Different feelings. Different gestures.');font(p,16);p.setPen(QColor('#626B65'));p.drawText(40,90,'A semantic emotion library · Each composition uses only what it needs · No quadrant to decode')
    glyph=AffectWidget(240);glyph.show()
    for i,key in enumerate(CORE):
        x=40+i%4*350;y=122+i//4*400
        p.setPen(Qt.PenStyle.NoPen);p.setBrush(QColor('#FFFEFA'));p.drawRoundedRect(x,y,330,378,20,20)
        glyph.set_state(key);glyph.timer.stop();glyph.fade_override=1.;glyph.animation_time=1.
        art=QImage(240,240,QImage.Format.Format_ARGB32);art.fill(0);glyph.render(art);p.drawImage(x+45,y+8,art)
        p.setPen(QColor('#252D29'));font(p,25,True);p.drawText(x+22,y+274,ANCHORS[key][0]);font(p,15);p.setPen(QColor('#626B65'));p.drawText(x+22,y+306,MEANINGS[key][0]);font(p,13);p.drawText(x+22,y+340,'Player-chosen feeling · CMA shown separately')
    font(p,14);p.setPen(QColor('#626B65'));p.drawText(40,966,'Proposed visual language. Recognisability still needs testing; CMA does not prescribe any of these shapes.');p.end();im.save(str(OUT/'emotion-library.png'));cleanup(glyph)
    data=[{'key':k,'label':ANCHORS[k][0],'gesture':MEANINGS[k][0],'meaning':MEANINGS[k][1],'items':[{**a,**({'path':svg_path(a['commands'])} if a['kind']=='path' else {})} for a in scene(k,1.)]} for k in CORE]
    Path('design/emotion-symbols.json').write_text(json.dumps(data,indent=2))


def video():
    stage=QWidget();stage.resize(1280,720);stage.setStyleSheet('background:#F4F2EC');stage.show();glyph=AffectWidget(480);glyph.setParent(stage);glyph.move(710,115);glyph.show()
    ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','bgra','-s','1280x720','-r','30','-i','-','-an','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT/'emotion-library-motion.mp4')],stdin=subprocess.PIPE)
    for frame in range(720):
        t=frame/30;i=int(t/3);key=CORE[i];local=t-i*3;glyph.set_state(key);glyph.previous_state=CORE[i-1] if i else None;glyph.timer.stop();glyph.animation_time=t;glyph.fade_override=min(1.,local/.45) if i else 1.
        app.processEvents();im=QImage(stage.size(),QImage.Format.Format_ARGB32);im.fill(QColor('#F4F2EC'));stage.render(im);p=QPainter(im);p.setPen(QColor('#626B65'));font(p,14);p.drawText(48,64,'CHECKPOINT / EMOTION LIBRARY');p.setPen(QColor('#252D29'));font(p,58,True);p.drawText(48,260,ANCHORS[key][0]);font(p,26);p.drawText(48,316,MEANINGS[key][0]);p.setPen(QColor('#626B65'));font(p,17);p.drawText(48,378,'One recognisable gesture, with its own movement.');p.drawText(48,414,'Pleasantness and activation stay beside the feeling.');font(p,13);p.drawText(48,672,'Illustrative player-selected states · Native rendering · 450ms transitions · No automatic emotion recognition');p.end();ff.stdin.write(bytes(im.bits()))
        if frame in [0,110,200,290,380,470,560,650]:im.save(str(OUT/f'emotion-library-motion-{frame:03}.png'))
    ff.stdin.close();assert ff.wait()==0;cleanup(stage)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--video',action='store_true');args=parser.parse_args();shots();atlas()
    if args.video:video()
