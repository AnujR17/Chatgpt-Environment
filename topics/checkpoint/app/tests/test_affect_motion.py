import math
import os
os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
import pytest
from PySide6.QtTest import QTest
from checkpoint.affect import ANCHORS, contours
from checkpoint.session import Session
from checkpoint.app import create_application, MainWindow, CheckinDialog


def test_continuous_dimensions_validate_and_face_cues_cannot_overwrite():
    s=Session(experimental_analysis=True);s.check_in('excited',-.15,.72)
    generation=s.start_capture('video');s.receive_cue({'expression':'sadness'},generation)
    assert (s.valence,s.arousal)==(-.15,.72)
    assert s.affect[1:3]==('In between','High activation')
    assert s.affect[3]=='Your description of this moment.'
    for v,a in [(float('nan'),0),(0,float('inf')),(1.01,0),(None,.2),(True,0)]:
        with pytest.raises(ValueError):s.check_in('calm',v,a)
    assert s.report=='excited' and len(s.reports)==1
    s.check_in('mixed');assert s.valence is None and s.arousal is None
    with pytest.raises(ValueError):s.check_in('mixed',0,0)
    s.check_in('calm',0,0);assert s.valence==s.arousal==0


def test_geometry_is_bounded_and_continuous_across_state_space():
    assert len(ANCHORS)==14
    for v in [-1,-.2,0,.7,1]:
        for a in [-1,0,1]:
            paths=contours(v,a,1.3);assert [len(p) for p in paths]==[96]*5
            assert all(math.isfinite(x) and math.isfinite(y) and abs(x)<1.1 and abs(y)<1.1 for p in paths for x,y in p)
            near=contours(v+.00001,a,1.30001)
            assert max(math.dist(p,q) for p1,p2 in zip(paths,near) for p,q in zip(p1,p2))<.0001
    assert contours(.7,.8)!=contours(-.7,.8)
    assert contours(.7,.8)!=contours(.7,-.8)


def test_motion_lifecycle_and_two_slider_checkin(tmp_path):
    app=create_application([]);w=MainWindow(no_setup=True,data_dir=tmp_path);w.show();QTest.qWait(40)
    assert all(not e.timer.isActive() for e in w.emblems)
    w.session.check_in('happy');w.select_card_source(2);w.refresh();QTest.qWait(50)
    assert w.emblems[0].timer.isActive() and not w.emblems[1].timer.isActive()
    w.change_view(2);assert not w.emblems[0].timer.isActive() and w.emblems[2].timer.isActive()
    w.toggle_motion();assert all(not e.timer.isActive() for e in w.emblems)
    w.toggle_motion();w.reduced_motion=True;w.refresh();assert all(not e.timer.isActive() for e in w.emblems)
    d=CheckinDialog(w);d.select('afraid');d.sliders[0].setValue(70);d.sliders[1].setValue(-60)
    assert d.chosen=='afraid' and (d.valence,d.arousal)==(.7,-.6)
    assert d.preview.target==(.7,-.6)
    d.choose('mixed');assert d.valence is None and d.arousal is None;d.deleteLater()
    w.reduced_motion=False;w.toggle_break();assert all(not e.timer.isActive() for e in w.emblems)
    w.toggle_break();assert w.emblems[2].timer.isActive()
    w.end_or_new();assert all(not e.timer.isActive() for e in w.emblems)
    w.close();w.deleteLater();app.processEvents()


def test_semantic_library_has_distinct_geometry_and_real_dialog_selection(tmp_path):
    import json
    from checkpoint.symbols import CORE, scene
    from checkpoint.app import EmotionLibraryDialog
    app=create_application([]);w=MainWindow(no_setup=True,data_dir=tmp_path)
    assert len(CORE)==8 and len({json.dumps(scene(k,0),sort_keys=True) for k in CORE})==8
    for key in CORE:
        for t in [0,1,3]:
            for item in scene(key,t):
                numbers=([item['x'],item['y'],item['r']] if item['kind']=='dot' else [v for c in item['commands'] for v in c[1:]])
                assert all(math.isfinite(v) and 0<=v<=360 for v in numbers)
    d=EmotionLibraryDialog(w);d.show();app.processEvents();d.choose('bewildered')
    assert d.chosen=='bewildered' and w.session.report is None
    d.deleteLater();w.close();w.deleteLater();app.processEvents()


def test_cancelling_word_or_dimension_change_preserves_report(tmp_path):
    from PySide6.QtCore import QTimer
    app=create_application([]);w=MainWindow(no_setup=True,data_dir=tmp_path);w.session.check_in('happy',.8,.4)
    before=w.session.summary()['check_ins'].copy()
    def cancel():
        dialog=app.activeModalWidget();dialog.select('confused');dialog.sliders[0].setValue(-90);dialog.reject()
    QTimer.singleShot(0,cancel);w.check_in()
    assert w.session.reports==before and w.session.report=='happy'
    assert (w.session.valence,w.session.arousal)==(.8,.4)
    w.close();w.deleteLater();app.processEvents()
