"""Real Qt interaction with scripted game events; never a game-accuracy claim."""
import json,tempfile,time
from pathlib import Path
from PySide6.QtCore import QCoreApplication,QEvent,Qt,QPoint
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QWidget,QGridLayout,QVBoxLayout
from checkpoint.app import create_application,MainWindow,label
from checkpoint.blob import NoriWidget
from checkpoint.gameplay import GameObservation

OUT=Path(__file__).resolve().parents[1]/'artifacts/design-review';OUT.mkdir(parents=True,exist_ok=True)
app=create_application([])


def run():
 with tempfile.TemporaryDirectory() as directory:
    w=MainWindow(no_setup=True,data_dir=directory);w.resize(1440,900);w.reduced_motion=True;w.show();app.processEvents()
    w.nudges_enabled=True;w.overlay_enabled=True;w.detect_games=True
    def scene(kind):
        w.receive_game_observation(None,GameObservation('Getting Over It','Foreground process detected',state={'kind':kind,'title':kind,'possible_falls':1,'basis':'Scripted fixture'}))
    for _ in range(4):scene('falling');QTest.qWait(500)
    assert not w.last_nudge
    for _ in range(6):scene('steady');QTest.qWait(500)
    assert w.last_nudge.startswith('Possible fall.')
    assert w.last_nudge==w.overlay.message==w.latest_companion['nudge']
    assert w.session.report is None and not w.session.camera_active and not w.input_observer.enabled
    w.grab().save(str(OUT/'play-support.png'));w.overlay.grab().save(str(OUT/'setback-overlay.png'))
    w.support_toggle.click();assert not w.last_nudge and not w.overlay.message
    w.setback_control.click();assert w.last_nudge and w.latest_companion['play_support']['basis']=='Player marked a setback'
    assert not w.nudges_enabled  # Manual help preserves the player's mute preference.
    w.nudges_enabled=True;policy=w.companion.support;policy.play_seconds=149.9;policy.last_tick=time.monotonic()-.5;policy.was_foreground=True;policy.last_prompt=time.monotonic()-151
    w.next_export=0.;scene('steady');app.processEvents()
    assert w.last_nudge=='A quick reset? Relax your grip, then go again.'
    assert w.latest_companion['play_support']['basis']=='Active gaming reminder'
    w.overlay.grab().save(str(OUT/'reminder-overlay.png'));w.grab().save(str(OUT/'play-reminder.png'))
    for width,height in ((1440,900),(1024,768)):
        w.resize(width,height);app.processEvents()
        for b in (w.capture_control,w.checkin_button,w.setback_control,w.game_detection_control):
            assert b.mapTo(w,QPoint(b.width(),b.height())).y()<=height
    w.close();w.deleteLater();QCoreApplication.sendPostedEvents(None,QEvent.Type.DeferredDelete);app.processEvents()
    gallery=QWidget();gallery.setStyleSheet('background:#f7f5ec;color:#29334b');grid=QGridLayout(gallery)
    from checkpoint.primary import PRIMARY_LABELS
    for i,(key,title) in enumerate(PRIMARY_LABELS.items()):
        tile=QWidget();column=QVBoxLayout(tile);blob=NoriWidget(180);blob.set_state(key);blob.configure(reduced_motion=True);column.addWidget(blob);column.addWidget(label(title,16));grid.addWidget(tile,i//4,i%4)
    gallery.show();QTest.qWait(800);gallery.grab().save(str(OUT/'expression-gallery.png'));gallery.close();gallery.deleteLater();QCoreApplication.sendPostedEvents(None,QEvent.Type.DeferredDelete)
 result={'fixture':'Scripted game observations and authored expression poses; no real-game accuracy or user benefit established',
         'fall_then_settled_view_to_native_overlay_and_phone_payload':'passed','no_camera_input_or_checkin_required':'passed',
         'active_play_reminder_to_overlay_and_phone':'passed','mute_and_manual_fallback':'passed','1440_and_1024_controls_visible':'passed',
         'short_brow_native_gallery':'rendered','windows_global_shortcuts':'requires Windows check'}
 (OUT/'play-support-verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))


if __name__=='__main__':run()
