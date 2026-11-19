"""Native 0.6 review using labelled synthetic facial signals, not emotion accuracy."""
import json
from pathlib import Path
import runpy
import tempfile
from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QWidget,QGridLayout,QVBoxLayout,QLabel
from PySide6.QtTest import QTest
from checkpoint.app import create_application,MainWindow
from checkpoint.blob import NoriWidget
from checkpoint.cues import Cue
from checkpoint.face_mapping import neutral_movement
from checkpoint.gameplay import GameObservation

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/expression-review';OUT.mkdir(parents=True,exist_ok=True)
app=create_application([])
tests=runpy.run_path(str(ROOT/'tests/test_expression_and_game_state.py'))
checks=0
for name,fn in tests.items():
    if name.startswith('test_'):fn();checks+=1

with tempfile.TemporaryDirectory() as directory:
    w=MainWindow(no_setup=True,data_dir=directory);w.reduced_motion=True;w.resize(1024,768);w.show()
    w.session.experimental_analysis=True;generation=w.session.start_capture('video')
    cases=[('Neutral','neutral',{},'neutral'),('Happy','happy',dict(smile=.8,cheek=.5),'happiness'),
           ('Happy','happy',dict(smile=.8,cheek=.5,jaw=.6,laugh=.6,teeth=.5),'happiness'),
           ('Frustrated','frustrated',dict(brow=.7,pressed=.6),'anger'),
           ('Surprised','surprised',dict(brow_raise_left=.6,brow_raise_right=.5,jaw=.2),None),
           ('Neutral',None,dict(brow=-.5,eye_wide=.8,jaw=.7),'surprise')]
    for title,key,features,model in cases:
        for _ in range(14):
            m=neutral_movement();m.update(features)
            estimate={'status':'accepted','label':model,'score':.9,'scores':{model:.9,'neutral' if model!='neutral' else 'anger':.1}} if model else None
            w.session.receive_cue(Cue('accepted','neutral',movement=m,model_estimate=estimate),generation)
            w.refresh();QTest.qWait(125)
        assert w.latest_companion['title']==title,(title,w.latest_companion['title'])
        assert w.latest_companion['artwork']==key
        assert w.latest_report['cma']['count']==0
        assert all(not obj.isVisible() for obj,name in w.state_labels if name=='description')
    # Current game state reaches the paired phone as an independent field.
    state={'kind':'climbing','title':'Climbing?','section':None,'basis':'Synthetic background-motion fixture'}
    w.game_observation=GameObservation('Getting Over It','Foreground process detected','Possible climb',state)
    w.next_export=0.;w.refresh();app.processEvents()
    assert w.latest_companion['game_state']==state
    assert 'Climbing?' in w.latest_companion['game_state']['title']
    w.grab().save(str(OUT/'expressions-app.png'))
    start=w.camera_controls[0]
    assert start.mapTo(w,QPoint()).y()+start.height()<w.height()
    w.session.receive_cue(Cue('unavailable',reason='No face detected'),generation)
    w.next_export=0.;w.refresh();app.processEvents()
    assert w.latest_companion['unknown'] and w.latest_companion['blob']['smile']==0
    assert w.overlay.expression_label=='Neutral'
    w.close();app.processEvents()

gallery=QWidget();gallery.setWindowTitle('Nori expression study · authored fixtures')
gallery.setStyleSheet('background:#F5F3ED;color:#29334B;');grid=QGridLayout(gallery)
from checkpoint.primary import PRIMARY_LABELS
for i,(key,title) in enumerate(PRIMARY_LABELS.items()):
    cell=QWidget();layout=QVBoxLayout(cell)
    art=NoriWidget(180);art.set_state(key);art.configure(reduced_motion=True)
    layout.addWidget(art,alignment=Qt.AlignmentFlag.AlignCenter)
    label=QLabel(title);label.setAlignment(Qt.AlignmentFlag.AlignCenter);layout.addWidget(label)
    grid.addWidget(cell,i//3,i%3)
gallery.resize(760,520);gallery.show();app.processEvents()
gallery.grab().save(str(OUT/'nori-expression-family.png'));gallery.close();app.processEvents()
result={'fixture':'Synthetic action features and authored art; not measured emotion accuracy',
        'policy_and_vision_checks':checks,'native_expression_names':'passed','commentary_hidden':'passed',
        'unknown_face_flat':'passed','cma_not_invented':'passed','game_state_to_phone_payload':'passed',
        'physical_windows_camera_game_phone':'not tested'}
(OUT/'verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
