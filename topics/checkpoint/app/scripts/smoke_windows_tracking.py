"""Windows-native fixture checks; no real camera, game, or gameplay accuracy claim."""
from pathlib import Path
import json
import os
import ctypes
from ctypes import wintypes
import numpy as np
from urllib.request import Request,urlopen
from PySide6.QtTest import QTest
from PySide6.QtCore import QPoint
from checkpoint.app import create_application, MainWindow
from checkpoint.runtime import Cue
import checkpoint.gameplay as game_module

ROOT = Path(__file__).resolve().parents[1]
app = create_application([])
window = MainWindow(no_setup=True, data_dir=ROOT / 'build/smoke-history')
window.show(); window.raise_(); window.activateWindow(); QTest.qWait(400)
tabs=window.view_selectors[0]
assert tabs.tabRect(2).right()<tabs.width(),'Card tabs are clipped in the actual Windows viewport'
start=window.camera_controls[0];position=start.mapTo(window,QPoint())
assert position.y()+start.height()<window.height(),'Start tracking is below the initial viewport'
assert position.y()<window.preview_widgets[0].mapTo(window,QPoint()).y(),'Start tracking must appear before preview'

window.session.check_in('calm', .6, -.4)
window.session.experimental_analysis = True
generation = window.session.start_capture('camera')
window.select_card_source(1)
window.session.receive_cue(Cue('accepted', 'anger', .9), generation)
window.refresh(); app.processEvents()
assert window.emblems[0].current_state == 'angry'
assert (window.session.report, window.session.valence, window.session.arousal) == ('calm', .6, -.4)
# Exercise default reflection through the real Qt refresh path and preserve check-ins.
from checkpoint.face_mapping import neutral_movement
window.select_card_source(0)
for _ in range(9):
    m=neutral_movement();m.update(smile=.75,cheek=.5)
    window.session.receive_cue(Cue('accepted','happiness',movement=m),generation)
    window.refresh();QTest.qWait(125)
assert window.emblems[0].current_state=='happy','Default reflection did not respond'
assert window.session.report=='calm','Live tracking overwrote the check-in'
window.session.check_in('sad',-.5,-.4);window.refresh()
assert window.emblems[0].current_state=='happy','Check-in pinned live reflection'
window.grab().save(str(ROOT/'build/Checkpoint-Windows/windows-responsive-reflection.png'))
# A learned anger estimate must survive weak handcrafted brow/mouth values.
for _ in range(10):
    estimate={'status':'accepted','label':'anger','score':.9,'scores':{'anger':.9,'neutral':.1}}
    window.session.receive_cue(Cue('accepted','neutral',movement=neutral_movement(),model_estimate=estimate),generation)
    window.refresh();QTest.qWait(125)
assert window.emblems[0].current_state=='angry','Learned anger was overridden by geometry'
# Confident happiness plus tense geometry is ambiguous, never a forced tense pose.
for _ in range(10):
    m=neutral_movement();m.update(brow=.8,pressed=.6)
    estimate={'status':'accepted','label':'happiness','score':.9,'scores':{'happiness':.9,'neutral':.1}}
    window.session.receive_cue(Cue('accepted','neutral',movement=m,model_estimate=estimate),generation)
    window.refresh();QTest.qWait(125)
assert window.emblems[0].current_state is None,'Conflicting evidence forced a pose'

window.select_card_source(1)
window.session.receive_cue(Cue('accepted','anger',.9),generation);window.refresh()

user=ctypes.WinDLL('user32');user.GetForegroundWindow.restype=wintypes.HWND
before=user.GetForegroundWindow();window.toggle_overlay();QTest.qWait(150)
assert user.GetForegroundWindow()==before,'Overlay stole focus'
get_style=user.GetWindowLongPtrW;get_style.argtypes=[wintypes.HWND,ctypes.c_int];get_style.restype=ctypes.c_ssize_t
style=get_style(int(window.overlay.winId()),-20)
assert style&0x20 and style&0x08000000,'Overlay is not click-through/no-activate'
window.overlay.grab().save(str(ROOT/'build/Checkpoint-Windows/windows-pip-overlay.png'))
assert window.overlay.grab().toImage().pixelColor(0,0).alpha()==0,'Overlay has an opaque background rectangle'
window.input_observer.start();assert window.input_observer.enabled;window.input_observer.stop()
from checkpoint.face_mapping import LandmarkPipeline
from checkpoint.cma_report import make_pdf,cma_summary
assert make_pdf(cma_summary(window.session)).startswith(b'%PDF-')
# Exercise model bytes from a non-ASCII installation path and the real graph.
folder=ROOT/'build/顔のモデル';folder.mkdir(parents=True,exist_ok=True)
(folder/'face_landmarker.task').write_bytes((ROOT/'artifacts/face_landmarker.task').read_bytes())
mapper=LandmarkPipeline(folder)
assert mapper.hand_detector is not None and not mapper.hand_error,'Hand model did not load'
try:
    assert mapper.infer(np.zeros((480,640,3),dtype=np.uint8)).status=='unavailable'
    assert mapper.infer(np.random.default_rng(8).integers(0,256,(480,640,3),dtype=np.uint8)).status in ('accepted','unavailable')
finally:mapper.close()
from checkpoint.pretrained_expression import HSEExpressionModel
model=HSEExpressionModel();assert abs(float(model.probabilities(np.zeros((112,112,3),dtype=np.uint8)).sum())-1)<1e-4
from checkpoint.phone import PhoneServer,private_firewall_command
window.phone_server=PhoneServer(window.phone_bridge,host='127.0.0.1',port=0).start()
request=Request(f'http://127.0.0.1:{window.phone_server.port}/api/state',headers={'Authorization':'Bearer '+window.phone_server.token})
assert json.load(urlopen(request))['character']=='Nori'
(ROOT/'artifacts/firewall-command-check.ps1').write_text(private_firewall_command(window.phone_server.port),encoding='utf8')
window.phone_server.stop();window.phone_server=None
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
result = {'windows_native_initial_controls_visible':'passed','windows_native_model_primary_and_conflict_fixture':'passed','windows_native_responsive_reflection_fixture':'passed','checkin_does_not_pin_live_reflection':'passed','windows_native_live_card_fixture': 'passed', 'windows_gdi_own_window_fixture': 'passed',
          'reject_wrong_window': 'passed', 'pause_clears_live_card': 'passed',
          'player_report_preserved': 'passed','overlay_no_focus_steal':'passed','overlay_native_clickthrough_style':'passed',
          'raw_input_registration':'passed','face_landmarker_native_load':'passed','hsemotion_inference':'passed','phone_loopback_api':'passed',
          'cma_pdf_native_render':'passed','hand_landmarker_native_load':'passed','face_landmarker_non_ascii_path':'passed','face_landmarker_native_graph_inference':'passed',
          'physical_camera_and_actual_game': 'not tested','physical_phone_wifi':'not tested'}
(ROOT / 'artifacts/windows-tracking-smoke.json').write_text(json.dumps(result, indent=2))
print(json.dumps(result))
