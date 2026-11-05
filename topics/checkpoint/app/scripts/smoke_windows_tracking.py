"""Windows-native fixture checks; no real camera, game, or gameplay accuracy claim."""
from pathlib import Path
import json
import os
from PySide6.QtTest import QTest
from checkpoint.app import create_application, MainWindow
from checkpoint.runtime import Cue
import checkpoint.gameplay as game_module

ROOT = Path(__file__).resolve().parents[1]
app = create_application([])
window = MainWindow(no_setup=True, data_dir=ROOT / 'build/smoke-history')
window.show(); window.raise_(); window.activateWindow(); QTest.qWait(400)
window.session.check_in('calm', .6, -.4)
window.session.experimental_analysis = True
generation = window.session.start_capture('camera')
window.select_card_source(1)
window.session.receive_cue(Cue('accepted', 'anger', .9), generation)
window.refresh(); app.processEvents()
assert window.emblems[0].current_state == 'angry'
assert (window.session.report, window.session.valence, window.session.arousal) == ('calm', .6, -.4)
window.last_status = 'Synthetic expression fixture · no camera connected'
window.refresh()
window.grab().save(str(ROOT / 'build/Checkpoint-Windows/windows-live-tracking.png'))
# Capture our own visible Qt window with an explicitly injected game-window fixture.
# This tests real GDI calls, not recognition of a running game or real gameplay.
fixture = game_module.ActiveGame('Getting Over It', int(window.winId()), os.getpid())
original = game_module.active_game
try:
    game_module.active_game = lambda: fixture
    frame = game_module.capture_game(fixture)
    assert frame is not None and frame.std() > 7 and frame.shape[1] <= 640
    game_module.active_game = lambda: game_module.ActiveGame(None)
    assert game_module.capture_game(fixture) is None
finally:
    game_module.active_game = original
window.pause(); assert window.emblems[0].current_state is None
window.close(); app.processEvents()
result = {'windows_native_live_card_fixture': 'passed', 'windows_gdi_own_window_fixture': 'passed',
          'reject_wrong_window': 'passed', 'pause_clears_live_card': 'passed',
          'player_report_preserved': 'passed', 'physical_camera_and_actual_game': 'not tested'}
(ROOT / 'artifacts/windows-tracking-smoke.json').write_text(json.dumps(result, indent=2))
print(json.dumps(result))
