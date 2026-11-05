"""Actual native application review assets; uses no synthetic UI screenshot."""
import json
from pathlib import Path
from PySide6.QtCore import QEvent,Qt
from PySide6.QtGui import QImage,QPainter,QColor,QFont
from checkpoint.app import create_application,MainWindow,EmotionLibraryDialog,CheckinDialog,PreferencesDialog
from checkpoint.motion import AffectWidget
from checkpoint.vocabulary import CARDS,COMMON
from checkpoint.symbols import scene,svg_path
OUT=Path('artifacts');app=create_application([])

def render(widget,name):
    app.processEvents()
    for art in widget.findChildren(AffectWidget):art.timer.stop();art.fade_override=1.;art.animation_time=1.
    im=QImage(widget.size(),QImage.Format.Format_ARGB32);im.fill(0);widget.render(im);im.save(str(OUT/name))

def close(widget):
    widget.close();widget.deleteLater();app.sendPostedEvents(None,QEvent.Type.DeferredDelete);app.processEvents()

w=MainWindow(no_setup=True);w.show();w.timer.stop();render(w,'cards-app-empty.png');w.session.check_in('frustrated',-.6,.6);w.refresh();render(w,'cards-app-session.png')
d=EmotionLibraryDialog(w);d.show();render(d,'cards-app-library.png');d.search.setText('annoyed');render(d,'cards-app-search.png');d.search.setText('');d.set_group(False);render(d,'cards-app-all-feelings.png');close(d)
c=CheckinDialog(w,'frustrated');c.show();render(c,'cards-app-checkin.png');close(c)
p=PreferencesDialog(w);p.show();render(p,'cards-app-settings.png');close(p)
w.toggle_theme();render(w,'cards-app-dark.png');w.toggle_theme();w.resize(1000,680);render(w,'cards-app-compact.png');w.resize(1440,940);w.toggle_break();render(w,'cards-app-break.png');w.toggle_break();w.end_or_new();render(w,'cards-app-summary.png');close(w)
# A reference sheet of all available cards, outside the product's common-first flow.
rows=(len(CARDS)+5)//6;im=QImage(1440,120+rows*236,QImage.Format.Format_ARGB32);im.fill(QColor('#FFF2E4'));p=QPainter(im);p.setRenderHint(QPainter.RenderHint.Antialiasing)
def font(size,bold=False):
 f=QFont('DM Sans');f.setPixelSize(size);f.setBold(bold);p.setFont(f)
p.setPen(QColor('#343C36'));font(32,True);p.drawText(36,48,'Feelings vocabulary');font(15);p.drawText(36,80,'39 words from your reference, plus four project check-in words. These are selectable descriptions, not diagnoses.')
g=AffectWidget(190);g.show()
for i,(key,card) in enumerate(CARDS.items()):
 x=18+i%6*236;y=104+i//6*236;g.set_state(key);g.timer.stop();g.fade_override=1.;g.animation_time=1.;a=QImage(190,190,QImage.Format.Format_ARGB32);a.fill(0);g.render(a);p.drawImage(x+20,y,a);font(16,True);p.setPen(QColor('#343C36'));p.drawText(x+24,y+212,card['label'])
p.end();im.save(str(OUT/'cards-vocabulary.png'));close(g)
data=[{**card,'items':[{**item,**({'path':svg_path(item['commands'])} if item['kind']=='path' else {})} for item in scene(key,1.)]} for key,card in CARDS.items()]
Path('design/reference-card-scenes.json').write_text(json.dumps(data,indent=2))
print('Native session, card library, search, check-in, settings, break, summary and compact screenshots rendered.')
