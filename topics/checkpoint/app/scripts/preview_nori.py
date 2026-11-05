"""Actual native renders with explicitly synthetic signals and check-ins."""
from pathlib import Path
from PySide6.QtCore import Qt,QTimer
from PySide6.QtWidgets import QWidget,QVBoxLayout,QGridLayout,QApplication
from checkpoint.app import create_application,MainWindow,label
from checkpoint.blob import NoriWidget
from checkpoint.face_mapping import movement_parameters,neutral_movement,movement_label
from checkpoint.expression_view import EXPRESSIONS
from checkpoint.vocabulary import CARDS
from checkpoint.affect import REFERENCES
from checkpoint.cma_report import make_pdf

ROOT=Path(__file__).resolve().parents[1];app=create_application([])
profiles=[('Neutral',neutral_movement()),
 ('Smile',movement_parameters({'mouthSmileLeft':.3,'mouthSmileRight':.3,'cheekSquintLeft':.3,'cheekSquintRight':.3})),
 ('Teeth visible',{**movement_parameters({'mouthSmileLeft':.35,'mouthSmileRight':.35,'jawOpen':.3}),'teeth':.85}),
 ('Tense mouth',{**movement_parameters({'mouthSmileLeft':.5,'mouthSmileRight':.5,'mouthStretchLeft':.5,'mouthStretchRight':.5,'mouthPressLeft':.3,'mouthPressRight':.3,'browDownLeft':.4,'browDownRight':.4}),'teeth':.8}),
 ('Hand near mouth',{**neutral_movement(),'hand':1.,'mouth_visible':0.}),
 ('Rounded lips',movement_parameters({'mouthPucker':.7,'jawOpen':.25})),
 ('One brow',movement_parameters({'browOuterUpLeft':.6,'browOuterUpRight':.1}))]
window=QWidget();window.setStyleSheet('background:#F4F2EC;');layout=QVBoxLayout(window);layout.setContentsMargins(24,20,24,20);layout.addWidget(label('Nori · Face preview',25,bold=True));layout.addWidget(label('Synthetic signals · native rendering, not a recognition accuracy test',13,True));grid=QGridLayout();layout.addLayout(grid)
for i,(name,movement) in enumerate(profiles):
    col=QVBoxLayout();form=NoriWidget(150);form.configure(reduced_motion=True);key,_=movement_label(movement);form.set_state(EXPRESSIONS[key][1],0,0);form.set_movement(movement);col.addWidget(form);text=label(name,14);text.setAlignment(Qt.AlignmentFlag.AlignCenter);col.addWidget(text);grid.addLayout(col,0,i)
window.show();app.processEvents();window.grab().save(str(ROOT/'artifacts/nori-face-detail-states.png'));window.close()
window=QWidget();window.setStyleSheet('background:#F4F2EC;');layout=QVBoxLayout(window);layout.setContentsMargins(24,20,24,20);layout.addWidget(label('Nori · 43 check-in compositions',25,bold=True));layout.addWidget(label('Selectable feeling vocabulary · not 43 inferred camera classes',13,True));grid=QGridLayout();layout.addLayout(grid)
for i,(key,card) in enumerate(CARDS.items()):
    col=QVBoxLayout();form=NoriWidget(130);form.configure(reduced_motion=True);form.set_state(key,*REFERENCES[key][1:3]);col.addWidget(form);text=label(card['label'],13);text.setAlignment(Qt.AlignmentFlag.AlignCenter);col.addWidget(text);grid.addLayout(col,i//7,i%7)
window.show();app.processEvents();window.grab().save(str(ROOT/'artifacts/nori-43-feelings.png'));window.close()
w=MainWindow(no_setup=True,data_dir=ROOT/'build/nori-preview-data');w.session.game='Example session · synthetic check-ins';w.session.started-=900
for word,v,a in [('calm',.5,-.5),('frustrated',-.6,.8),('calm',.6,-.5)]:w.session.check_in(word,v,a)
for entry,elapsed in zip(w.session.reports,[30,420,880]):entry['elapsed_seconds']=elapsed
w.next_export=0.;w.reduced_motion=True;w.show();w.refresh();app.processEvents();w.grab().save(str(ROOT/'artifacts/nori-reflection-screen.png'))
(ROOT/'artifacts/nori-cma-preview.pdf').write_bytes(make_pdf(w.latest_report))
def grab_report():
    dialog=QApplication.activeModalWidget();dialog.grab().save(str(ROOT/'artifacts/nori-cma-report-screen.png'));dialog.accept()
QTimer.singleShot(200,grab_report);w.show_report();w.close();app.processEvents()
print('Nori face detail, 43 profiles, reflection screen and synthetic CMA report rendered')
