import os
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
import sys
import time
from pathlib import Path
import cv2
import numpy as np
import pytest
from PySide6.QtTest import QTest
from checkpoint.app import create_application, MainWindow
from checkpoint.runtime import Cue, CueSmoother
from checkpoint.expression_view import expression_display
from checkpoint.gameplay import ActiveGame, GameWorker, GettingOverItAnalyzer, active_game


def test_live_model_result_changes_card_without_overwriting_report(tmp_path):
    app = create_application([]); window = MainWindow(no_setup=True, data_dir=tmp_path)
    window.session.check_in('calm', .6, -.4)
    window.session.experimental_analysis = True; generation = window.session.start_capture('camera')
    window.select_card_source(1); window.show()
    smoother = CueSmoother()
    for _ in range(3):
        window.session.receive_cue(smoother.update(Cue('accepted', 'anger', .9)), generation)
    window.refresh(); app.processEvents()
    assert window.emblems[0].current_state == 'angry'
    assert any(obj.text() == 'Angry expression' for obj, key in window.state_labels if key == 'title')
    assert (window.session.report, window.session.valence, window.session.arousal) == ('calm', .6, -.4)
    window.session.receive_cue(Cue('unavailable', reason='No face in frame'), generation); window.refresh()
    assert window.emblems[0].current_state is None
    assert expression_display(window.session).title == 'No face detected'
    window.select_card_source(0); assert window.emblems[0].current_state == 'calm'
    window.select_card_source(1); window.pause(); assert window.emblems[0].current_state is None
    assert expression_display(window.session).title == 'Camera paused'
    window.close(); window.deleteLater(); app.processEvents()


def test_stale_expression_is_not_presented_as_live(tmp_path):
    app = create_application([]); window = MainWindow(no_setup=True, data_dir=tmp_path)
    window.session.experimental_analysis = True; generation = window.session.start_capture('video')
    window.session.receive_cue(Cue('accepted', 'happiness', .9), generation)
    window.session.cue_received_at -= 10
    assert expression_display(window.session).artwork is None
    window.close(); window.deleteLater(); app.processEvents()


def textured_scene(seed=3):
    rng = np.random.default_rng(seed)
    return cv2.GaussianBlur(rng.integers(0, 256, (360, 640, 3), dtype=np.uint8), (3, 3), 0)


@pytest.mark.parametrize('shift,expected', [(9, 'Possible climb'), (-9, 'Possible fall')])
def test_optical_flow_direction_and_temporal_gate(shift, expected):
    analyzer = GettingOverItAnalyzer(); base = textured_scene()
    labels = []
    for i in range(5):
        frame = cv2.warpAffine(base, np.float32([[1, 0, 0], [0, 1, shift * i]]), (640, 360), borderMode=cv2.BORDER_REFLECT)
        labels.append(analyzer.observe(frame))
    assert not any(x.startswith(expected) for x in labels[:3])
    assert labels[-1].startswith(expected)
    assert 'unavailable' in analyzer.observe(np.zeros_like(base)).lower()
    assert not analyzer.observe(base).startswith('Possible')


def test_scene_cut_and_marked_view_do_not_infer_failure():
    analyzer = GettingOverItAnalyzer(); base = textured_scene()
    assert analyzer.mark_start(base)
    assert analyzer.observe(base).startswith('Marked start view')
    assert not analyzer.observe(textured_scene(55)).startswith('Possible')
    analyzer.clear(); assert analyzer.reference is None


def test_worker_does_not_capture_another_game_or_app():
    app = create_application([]); captures = []; observed = []
    game = ActiveGame('Valorant', 123, 456)
    worker = GameWorker(screen=True, detector=lambda: game, capture=lambda game: captures.append(game))
    worker.observation.connect(observed.append); worker.start(); QTest.qWait(150)
    assert worker.stop(); app.processEvents()
    assert not captures and observed
    assert 'only for Getting Over It' in observed[0].cue


def test_real_expression_pipeline_updates_native_live_view(tmp_path):
    video = Path(os.environ.get('CHECKPOINT_TEST_VIDEO', 'data/videos/02-01-05-01-01-01-04.mp4'))
    if not video.exists(): pytest.skip('Requires separately sourced research video; no recording is committed')
    app = create_application([]); window = MainWindow(no_setup=True, data_dir=tmp_path); window.show()
    window.frequency = 5.; window.start_source(str(video), analyze=True)
    seen = []; deadline = time.monotonic() + 8
    while window.worker is not None and time.monotonic() < deadline:
        app.processEvents(); time.sleep(.01)
        if window.session.cue is not None and window.session.cue.status == 'accepted':
            seen.append(window.emblems[0].current_state)
            assert seen[-1] is not None
            break
    assert seen, 'No stable accepted estimate in this explicitly selected recording'
    assert window.live_view and window.session.report is None
    assert window.session.valence is None and window.session.arousal is None
    window.pause(); assert window.emblems[0].current_state is None
    window.close(); window.deleteLater(); app.processEvents()


@pytest.mark.skipif(sys.platform != 'win32', reason='Windows-only native GDI capture')
def test_windows_native_window_capture(monkeypatch, tmp_path):
    import checkpoint.gameplay as game_module
    app = create_application([]); window = MainWindow(no_setup=True, data_dir=tmp_path)
    window.show(); window.raise_(); window.activateWindow(); QTest.qWait(300)
    fixture = ActiveGame('Getting Over It', int(window.winId()), os.getpid())
    # Explicit synthetic game-window fixture, not evidence of actual game recognition.
    monkeypatch.setattr(game_module, 'active_game', lambda: fixture)
    frame = game_module.capture_game(fixture)
    assert frame is not None and frame.shape[1] <= 640 and frame.std() > 7
    monkeypatch.setattr(game_module, 'active_game', lambda: ActiveGame(None))
    assert game_module.capture_game(fixture) is None
    window.close(); window.deleteLater(); app.processEvents()
