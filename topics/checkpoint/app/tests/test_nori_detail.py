import os
os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
from pathlib import Path
from types import SimpleNamespace
import numpy as np
import cv2
from PySide6.QtCore import QPoint,Qt
from PySide6.QtTest import QTest
from checkpoint.face_detail import hand_mouth,visible_teeth,INNER_LIPS
from checkpoint.face_mapping import movement_parameters,movement_label,neutral_movement
from checkpoint.character import FEELING_LOOKS
from checkpoint.vocabulary import CARDS
from checkpoint.blob import parameters
from checkpoint.app import create_application,MainWindow
from checkpoint.cues import Cue
from checkpoint.expression_view import expression_display


def test_stretched_tense_mouth_is_not_automatically_a_smile():
    scores={'mouthStretchLeft':.5,'mouthStretchRight':.5,'mouthSmileLeft':.5,'mouthSmileRight':.5,
            'mouthPressLeft':.3,'mouthPressRight':.3,'browDownLeft':.4,'browDownRight':.4}
    tense=movement_parameters(scores)
    assert movement_label(tense)[0]=='anger' and tense['smile']<.16
    smiling=movement_parameters({**scores,'cheekSquintLeft':.6,'cheekSquintRight':.6})
    assert movement_label(smiling)[0]=='happiness'
    widened=movement_parameters({'mouthStretchLeft':.5,'mouthStretchRight':.5})
    assert widened['smile']==0 and movement_label(widened)==('neutral','Mouth widened')


def test_eyes_are_independent_and_nose_asymmetry_have_physical_labels():
    wink=movement_parameters({'eyeBlinkLeft':.8,'eyeWideRight':.4})
    assert wink['eye_left']<.3 and wink['eye_right']>1.1
    disgust=movement_parameters({'noseSneerLeft':.4,'noseSneerRight':.4})
    assert movement_label(disgust)[0]=='disgust'
    uneven=movement_parameters({'mouthSmileLeft':.4,'mouthSmileRight':0})
    # One-sided mouth signal is preserved rather than averaged away.
    assert uneven['asymmetry']>.4


def test_hand_proximity_distinguishes_covering_from_far_away():
    mouth=np.array([[.4,.48],[.6,.48],[.6,.54],[.4,.54]],np.float32)
    hand=[SimpleNamespace(x=.4+(i%5)*.04,y=.45+(i//5)*.04) for i in range(21)]
    result=hand_mouth([hand],mouth)
    assert result['near'] and result['occluded']
    far=[SimpleNamespace(x=p.x+.5,y=p.y-.4) for p in hand]
    assert not hand_mouth([far],mouth)['near']


def mouth_points():
    points=[SimpleNamespace(x=.5,y=.5) for _ in range(478)]
    for i,idx in enumerate(INNER_LIPS):
        angle=2*np.pi*i/len(INNER_LIPS);points[idx]=SimpleNamespace(x=.5+.22*np.cos(angle),y=.5+.1*np.sin(angle))
    return points


def test_teeth_cue_requires_contrast_inside_the_mouth_and_is_masked_by_hand():
    frame=np.zeros((100,100,3),np.uint8)+25;cv2.rectangle(frame,(35,47),(65,52),(235,235,235),-1)
    points=mouth_points()
    assert visible_teeth(frame,points)>.15
    assert visible_teeth(frame,points,occluded=True)==0
    assert visible_teeth(np.full_like(frame,235),points)==0
    outside=np.zeros_like(frame)+25;outside[5:15]=235
    assert visible_teeth(outside,points)==0


def test_partial_face_with_hand_shows_gesture_without_inventing_a_mouth(tmp_path):
    app=create_application([]);w=MainWindow(no_setup=True,data_dir=tmp_path)
    try:
        w.session.experimental_analysis=True;generation=w.session.start_capture('camera');w.live_view=True
        movement=neutral_movement();movement.update(hand=1.,mouth_visible=0.)
        w.session.receive_cue(Cue('unavailable',reason='Face partly hidden',movement=movement,gesture={'near':True,'occluded':True}),generation)
        w.refresh();display=expression_display(w.session)
        assert display.title=='Hand near mouth' and display.movement['smile']==display.movement['teeth']==0
        assert w.session.report is None and w.session.valence is None
    finally:w.close();w.deleteLater();app.processEvents()


def test_43_checkin_profiles_are_distinct_and_cma_changes_body_not_expression():
    assert set(FEELING_LOOKS)==set(CARDS) and len(CARDS)==43
    assert len({tuple(parameters(key).values()) for key in CARDS})==43
    quiet=parameters('calm',.6,-.8);active=parameters('calm',.6,.8)
    assert active['energy']>quiet['energy'] and active['stretch']>quiet['stretch']
    assert active['smile']==quiet['smile']==0


def test_drag_release_relocks_and_remembers_position(tmp_path):
    app=create_application([]);w=MainWindow(no_setup=True,data_dir=tmp_path);w.show();w.toggle_overlay()
    try:
        overlay=w.overlay;overlay.begin_move();QTest.qWait(150);assert overlay.editing;overlay.move(120,130)
        QTest.mousePress(overlay,Qt.MouseButton.LeftButton,pos=QPoint(80,110));QTest.mouseRelease(overlay,Qt.MouseButton.LeftButton,pos=QPoint(80,110))
        assert not overlay.editing and overlay.windowFlags()&Qt.WindowType.WindowTransparentForInput
        point=overlay.pos();assert (tmp_path/'preferences.ini').exists()
        from checkpoint.overlay import NoriOverlay
        other=NoriOverlay();other.restore_position(tmp_path/'preferences.ini');assert other.pos()==point
        other.close();other.deleteLater()
    finally:w.close();w.deleteLater();app.processEvents()


def test_all_eight_physical_prototypes_have_distinct_broad_label_routes():
    # Synthetic route coverage, not evidence of recognition accuracy on people.
    fixtures={
      'neutral':{},'happiness':{'mouthSmileLeft':.3,'mouthSmileRight':.3},'surprise':{'jawOpen':.4},
      'sadness':{'mouthFrownLeft':.3,'mouthFrownRight':.3},
      'anger':{'browDownLeft':.3,'browDownRight':.3,'mouthPressLeft':.2,'mouthPressRight':.2},
      'disgust':{'noseSneerLeft':.4,'noseSneerRight':.4},
      'fear':{'eyeWideLeft':.5,'eyeWideRight':.5,'browInnerUp':.6,'mouthStretchLeft':.2,'mouthStretchRight':.2},
      'contempt':{'mouthSmileLeft':.3}}
    for expected,scores in fixtures.items():assert movement_label(movement_parameters(scores))[0]==expected,expected
