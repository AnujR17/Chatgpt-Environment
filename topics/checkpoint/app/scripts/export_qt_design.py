"""Export native widget geometry and semantics for editable Figma assembly."""
import json
from pathlib import Path
from PySide6.QtCore import Qt,QEvent
from PySide6.QtWidgets import QWidget,QFrame,QLabel,QPushButton,QLineEdit,QSlider,QCheckBox,QDoubleSpinBox,QScrollBar,QToolButton
from checkpoint.app import create_application,MainWindow,EmotionLibraryDialog,EmotionCard,CheckinDialog,PreferencesDialog,VideoPreview
from checkpoint.motion import AffectWidget
from checkpoint.session import Session
ROOT=Path(__file__).resolve().parents[1];app=create_application([])

def export(w,root=False):
    cls=type(w).__name__
    if not root and (not w.isVisible() or isinstance(w,(QScrollBar,QToolButton))):return None
    g=w.geometry();d={'name':w.objectName() or cls,'kind':'group','x':g.x(),'y':g.y(),'w':w.width(),'h':w.height()}
    if root:d.update(x=0,y=0)
    font=w.font();d['font']=font.pixelSize() if font.pixelSize()>0 else round(font.pointSizeF()*96/72);d['bold']=font.weight()>=600
    if isinstance(w,EmotionCard):
        a=w.art.geometry();title=next(x for x in w.children() if isinstance(x,QLabel));r=title.geometry();d.update(kind='card',key=w.key,artRect=[a.x(),a.y(),a.width(),a.height()],labelRect=[r.x(),r.y(),r.width(),r.height()]);return d
    if isinstance(w,AffectWidget):d.update(kind='art',key=w.current_state);return d
    if isinstance(w,VideoPreview):d.update(kind='preview',text=w.text());return d
    if isinstance(w,QLabel):
        d.update(kind='text',text=w.text(),secondary=w.objectName()=='secondary',single=w.fontMetrics().horizontalAdvance(w.text())<=w.width(),align='CENTER' if w.alignment()&Qt.AlignmentFlag.AlignHCenter else 'RIGHT' if w.alignment()&Qt.AlignmentFlag.AlignRight else 'LEFT');return d
    if isinstance(w,QCheckBox):d.update(kind='checkbox',text=w.text(),checked=w.isChecked());return d
    if isinstance(w,QPushButton):d.update(kind='button',text=w.text(),primary=bool(w.property('primary')),plain=w.objectName()=='navButton',enabled=w.isEnabled());return d
    if isinstance(w,QLineEdit):d.update(kind='input',text=w.text() or w.placeholderText(),placeholder=not bool(w.text()));return d
    if isinstance(w,QDoubleSpinBox):d.update(kind='input',text=str(w.value()),placeholder=False);return d
    if isinstance(w,QSlider):d.update(kind='slider',value=w.value());return d
    if d['name']=='qt_scrollarea_viewport':d['clip']=True;d['scroll']=True
    if d['name'] in ['panel','stateCard','artStage','nav']:d['surface']=d['name']
    children=[]
    for child in w.children():
        if isinstance(child,QWidget):
            v=export(child)
            if v is not None:children.append(v)
    d['children']=children;return d


def capture(widget):
    app.processEvents();return export(widget,True)
def close(widget):
    widget.close();widget.deleteLater();app.sendPostedEvents(None,QEvent.Type.DeferredDelete);app.processEvents()

w=MainWindow(no_setup=True);w.show();w.timer.stop();screens={'empty':capture(w)};w.session.check_in('frustrated',-.6,.6);w.refresh();screens['session']=capture(w)
d=EmotionLibraryDialog(w);d.show();screens['common']=capture(d);d.set_group(False);screens['all']=capture(d);d.search.setText('annoyed');screens['search']=capture(d);close(d)
for key in ['calm','frustrated','confused','happy','excited','sad','angry','exhausted','annoyed']:
    c=CheckinDialog(w,key);c.show();screens['checkin_'+key]=capture(c);close(c)
    old=w.session;w.session=Session();w.session.check_in(key,*((-.6,.6) if key=='frustrated' else ()));w.refresh();screens['session_'+key]=capture(w);w.session=old;w.refresh()
p=PreferencesDialog(w);p.show();screens['settings']=capture(p);close(p)
w.toggle_theme();screens['dark']=capture(w);w.toggle_theme();w.toggle_break();screens['break']=capture(w);w.toggle_break();w.end_or_new();screens['summary']=capture(w);close(w)
(ROOT/'design/native-app-geometry.json').write_text(json.dumps(screens,separators=(',',':')));print({k:(v['w'],v['h']) for k,v in screens.items()})
