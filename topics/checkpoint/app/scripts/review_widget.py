"""Exercise actual Qt widget controls and capture the five-state interface."""
import json
import tempfile
import time
from pathlib import Path
from PySide6.QtCore import QPoint, Qt, QTimer
from PySide6.QtTest import QTest
from checkpoint.app import create_application, MainWindow, CheckinDialog, EmotionLibraryDialog
from checkpoint.primary import PRIMARY_KEYS, PRIMARY_LABELS

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/design-review'
OUT.mkdir(parents=True, exist_ok=True)


def run():
    app = create_application([])
    with tempfile.TemporaryDirectory() as directory:
        w = MainWindow(no_setup=True, data_dir=directory)
        w.timer.stop(); w.reduced_motion = True; w.show(); w.toggle_overlay()
        app.processEvents()
        assert not w.overlay.windowFlags() & Qt.WindowType.WindowTransparentForInput
        assert w.overlay.name_label.text() == 'Neutral'
        w.overlay.grab().save(str(OUT / 'widget-normal.png'))
        QTest.mouseClick(w.overlay, Qt.MouseButton.LeftButton, pos=QPoint(110,150))
        app.processEvents()
        menu = w.overlay.menu
        assert menu and menu.isVisible()
        assert [a.text() for a in menu.actions()[0].menu().actions()] == list(PRIMARY_LABELS.values())
        menu.grab().save(str(OUT / 'widget-menu.png')); menu.close()
        def save():
            dialog = app.activeModalWidget()
            assert isinstance(dialog, CheckinDialog)
            dialog.sliders[0].setValue(-65); dialog.sliders[1].setValue(-55)
            dialog.save.click()
        QTimer.singleShot(20, save); w.overlay_action('checkin:sad')
        assert w.session.report == 'sad' and w.source_mode == 2
        assert w.overlay.name_label.text() == 'Sad'
        w.overlay_action('break:60'); app.processEvents()
        assert w.overlay.timer_caption.text() == 'Break time'
        assert w.overlay.timer_value.text() == '1:00'
        assert w.overlay.timer_value.font().pixelSize() >= 28
        w.overlay.grab().save(str(OUT / 'widget-break.png'))
        w.session.break_deadline = time.monotonic() - 1; w.refresh()
        assert w.overlay.timer_value.text() == '0:00' and w.session.break_deadline is not None
        w.overlay_action('continue')
        assert w.session.break_deadline is None and not w.session.camera_active
        library = EmotionLibraryDialog(w); library.show(); app.processEvents()
        assert tuple(library.cards) == PRIMARY_KEYS
        library.grab().save(str(OUT / 'five-emotions.png')); library.close()
        w.close(); app.processEvents()
    result = {'five_choices':'passed','click_controls':'passed','input_updates_widget':'passed',
              'large_break_countdown':'passed','explicit_continue':'passed','camera_stays_off':'passed'}
    (OUT / 'widget-verification.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(result))


if __name__ == '__main__':
    run()
