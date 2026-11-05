import os
import time
os.environ.setdefault("QT_QPA_PLATFORM","offscreen")
from pathlib import Path
import pytest
from PySide6.QtCore import QTimer
from PySide6.QtTest import QTest
from checkpoint.app import create_application,MainWindow,CheckinDialog,ASSETS


@pytest.fixture(scope="module")
def app():
    return create_application([])


@pytest.fixture
def window(app,tmp_path):
    w=MainWindow(no_setup=True,data_dir=tmp_path);w.show();QTest.qWait(100)
    yield w
    w.close();w.deleteLater();app.processEvents()


def test_native_starts_private_and_all_visual_views_load(window):
    assert window.worker is None and not window.session.camera_active
    assert not window.retain and not window.session.experimental_analysis
    for index in range(3):
        window.change_view(index);assert window.bodies.currentIndex()==index
    for emblem in window.emblems:assert emblem.target is None and not emblem.timer.isActive()
    for name in ["tense","engaged","calm","low","unknown"]:assert (ASSETS/(name+".svg")).stat().st_size>0


def test_manual_checkin_cma_is_immediate_and_camera_stays_off(window):
    window.session.check_in("engaged");window.refresh()
    assert all(obj.text()=="Engaged" for obj,key in window.state_labels if key=="title")
    assert not window.session.camera_active
    window.toggle_break();assert window.session.break_deadline is not None
    window.toggle_break();assert window.session.break_deadline is None and not window.session.camera_active


def test_dialog_accepts_mixed_without_enabling_capture(window):
    dialog=CheckinDialog(window);QTimer.singleShot(0,lambda:dialog.choose("mixed"))
    assert dialog.exec()==dialog.DialogCode.Accepted and dialog.chosen=="mixed"
    assert window.worker is None


def test_pause_clears_real_video_frames_and_end_stops_worker(window):
    videos=sorted((Path(__file__).resolve().parents[1]/"data"/"videos").glob("02-01-*.mp4"))
    if not videos:pytest.skip("Run ml.prepare_video to exercise real video capture")
    window.start_source(str(videos[0]),analyze=False);QTest.qWait(700)
    assert window.session.camera_active and window.last_image is not None
    assert window.pause();assert not window.session.camera_active and window.last_image is None and window.worker is None
    window.start_source(str(videos[0]),analyze=False);QTest.qWait(250);window.end_or_new()
    assert not window.session.active and window.worker is None


def test_failed_capture_recovers_to_manual_mode(window,tmp_path):
    window.start_source(str(tmp_path/"missing-video.mp4"),analyze=False);QTest.qWait(500)
    assert window.worker is None and not window.session.camera_active
    assert "could not be opened" in window.last_status.lower()
    window.session.check_in("calm");window.refresh();assert window.session.affect[0]=="Calm"


def test_actual_model_video_input_cannot_fill_cma(window,app):
    root=Path(__file__).resolve().parents[1];video=root/"data/videos/02-01-05-01-01-01-04.mp4"
    if not video.exists() or not (root/"artifacts/expression.onnx").exists():pytest.skip("Requires trained model and explicit research fixture")
    window.start_source(str(video),analyze=True)
    # Let both the native event loop and Python capture worker run during cold startup.
    deadline=time.monotonic()+6
    while window.session.cue is None and window.session.camera_active and time.monotonic()<deadline:
        app.processEvents();time.sleep(.01)
    assert window.session.camera_active and window.session.cue is not None
    window.refresh();assert all(obj.isVisible() for obj,key in window.state_labels if key=="cue" and obj.parent().isVisible())
    assert window.session.report is None and window.session.affect[1]=="Not reported"
    assert window.pause() and window.session.cue is None and window.last_image is None
