"""Real native interactions with synthetic player reports; no efficacy/accuracy claim."""
import json
from pathlib import Path
import tempfile
from PySide6.QtCore import QPoint
from checkpoint.app import create_application, MainWindow
from checkpoint.practice_ui import PracticeDialog
from checkpoint.attempts import active_attempt
from checkpoint.cma_report import make_pdf, report_html

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/session-review'
OUT.mkdir(parents=True, exist_ok=True)
app = create_application([])


def run():
    with tempfile.TemporaryDirectory() as directory:
        w = MainWindow(no_setup=True, data_dir=directory)
        w.timer.stop()
        w.reduced_motion = True
        w.resize(1024, 768)
        w.show()
        w.session.check_in('frustrated', -.7, .8)
        w.next_export = 0.
        w.refresh()
        app.processEvents()
        d = PracticeDialog(w)
        d.show()
        app.processEvents()
        assert not d.detail.isVisible(), 'Guidance must start short'
        assert 'one cue' in d.cma.text()
        d.sections.setCurrentRow(3)
        app.processEvents()
        assert 'shorter reach' in d.cue.text()
        d.grab().save(str(OUT / 'next-attempt.png'))
        d.pin.setChecked(True)
        d.try_button.click()
        w.next_export = 0.
        w.refresh()
        app.processEvents()
        assert active_attempt(w.session)['key'] == 'grip'
        assert w.overlay.message == 'Try a shorter reach and a slower pull.'
        assert w.latest_companion['practice']['section'] == 'Slippery ledges'
        assert w.overlay.windowFlags() & __import__('PySide6.QtCore', fromlist=['Qt']).Qt.WindowType.WindowDoesNotAcceptFocus
        review = PracticeDialog(w)
        review.show()
        app.processEvents()
        assert review.helped.isVisible() and not review.sections.isEnabled()
        review.note.setText('Shorter reach; settle before pulling.')
        review.helped.click()
        assert active_attempt(w.session) is None
        assert 'Shorter reach' in review.memory.text()
        review.grab().save(str(OUT / 'next-attempt-lesson.png'))
        # Explicit consent keeps the lesson across sessions; no capture data is stored.
        w.history.save(w.session.summary(), consent=True)
        from checkpoint.session import Session
        w.session = Session()
        recall = PracticeDialog(w)
        recall.sections.setCurrentRow(3)
        recall.show()
        app.processEvents()
        assert 'Shorter reach' in recall.memory.text()
        recall.smaller()
        recall.try_button.click()
        assert active_attempt(w.session)['mode'] == 'small'
        retry = PracticeDialog(w)
        retry.show()
        app.processEvents()
        retry.stuck.click()
        assert 'still stuck' in retry.status.text()
        w.next_export = 0.
        w.refresh()
        assert w.latest_companion['practice'] is None
        markup = report_html(w.latest_report)
        assert 'What helped your next attempt?' in markup
        assert '1 still stuck' in markup
        pdf = make_pdf(w.latest_report)
        assert pdf.startswith(b'%PDF-')
        (OUT / 'next-attempt-report.pdf').write_bytes(pdf)
        # Test a compact viewport, including feedback actions above the bottom edge.
        for dialog in (d, review, recall, retry):
            dialog.resize(820, 600)
            app.processEvents()
            for control in (dialog.try_button, dialog.helped, dialog.stuck):
                if control.isVisible():
                    assert control.mapTo(dialog, QPoint()).y()+control.height() <= dialog.height()
            dialog.close()
        w.close()
        app.processEvents()
    result = {'fixture': 'Synthetic check-ins and player actions', 'native_selection_and_cma': 'passed',
              'cue_to_overlay_and_phone_state': 'passed', 'feedback_and_cross_session_recall': 'passed',
              'small_target_and_still_stuck': 'passed', 'pdf': 'passed',
              'compact_native_viewport': '820x600 passed',
              'physical_game_camera_phone': 'not tested', 'usefulness_in_actual_play': 'not established'}
    (OUT / 'practice-verification.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(result))


if __name__ == '__main__':
    run()
