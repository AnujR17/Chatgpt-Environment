"""Native design review and task flow. All check-ins/cues are scripted fixtures."""
import json
import tempfile
from pathlib import Path
from PySide6.QtCore import QPoint
from PySide6.QtTest import QTest
from checkpoint.app import create_application,MainWindow
from checkpoint.practice_ui import PracticeDialog
from checkpoint.attempts import active_attempt
from checkpoint.cma_report import make_pdf,report_html
from checkpoint.session import Session

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/design-review'
OUT.mkdir(parents=True,exist_ok=True)
app=create_application([])


def run():
    with tempfile.TemporaryDirectory() as directory:
        w=MainWindow(no_setup=True,data_dir=directory);w.timer.stop();w.reduced_motion=True;w.show()
        for width,height,name in [(1440,900,'session'),(1024,768,'compact')]:
            w.resize(width,height);w.refresh();app.processEvents()
            tabs=w.view_selectors[0]
            assert tabs.tabRect(2).right()<tabs.width(),'Source tabs clipped'
            for control in (w.capture_control,w.checkin_button):
                corner=control.mapTo(w,QPoint(control.width(),control.height()))
                assert corner.y()<w.height() and corner.x()<w.width(),'Core action outside viewport'
                assert not control.icon().isNull(),'Conventional action icon missing'
            w.grab().save(str(OUT/(name+'.png')))
        assert not w.session.camera_active and not w.detect_games
        assert w.latest_report['cma']['count']==0
        # A selected camera expression never supplies either CMA coordinate.
        assert w.session.valence is None
        w.session.check_in('frustrated',-.7,.8);w.select_card_source(2);w.next_export=0.;w.refresh();app.processEvents()
        w.resize(1440,900);app.processEvents();w.grab().save(str(OUT/'check-in.png'))
        w.toggle_theme();app.processEvents();w.grab().save(str(OUT/'dark.png'));w.toggle_theme()
        d=PracticeDialog(w);d.show();app.processEvents()
        assert not d.detail.isVisible() and 'one cue' in d.cma.text()
        d.sections.setCurrentRow(3);app.processEvents()
        assert 'shorter reach' in d.cue.text()
        d.grab().save(str(OUT/'next-attempt.png'))
        d.pin.setChecked(True);d.try_button.click();w.practice_changed();app.processEvents()
        assert active_attempt(w.session)['key']=='grip'
        assert w.overlay.message=='Try a shorter reach and a slower pull.'
        assert w.latest_companion['practice']['section']=='Slippery ledges'
        w.overlay.grab().save(str(OUT/'overlay.png'))
        review=PracticeDialog(w);review.show();app.processEvents()
        assert review.helped.isVisible() and not review.sections.isEnabled()
        # A later explicit report can coexist with player-rated cue usefulness.
        w.session.check_in('calm',.4,-.5)
        review.note.setText('Shorter reach; settle before pulling.');review.helped.click()
        assert active_attempt(w.session) is None and 'Shorter reach' in review.memory.text()
        review.grab().save(str(OUT/'lesson.png'))
        w.practice_changed();assert w.latest_companion['practice'] is None
        assert w.latest_report['practice']['helped']==1
        assert 'What helped your next attempt?' in report_html(w.latest_report)
        (OUT/'sample-session-report.pdf').write_bytes(make_pdf(w.latest_report))
        # Consent off saves nothing. Explicit consent allows recall on the same device.
        assert not w.history.save(w.session.summary(),consent=False) and not w.history.read()
        assert w.history.save(w.session.summary(),consent=True)
        w.session=Session();recall=PracticeDialog(w);recall.sections.setCurrentRow(3);recall.show();app.processEvents()
        assert 'Shorter reach' in recall.memory.text()
        recall.smaller();recall.try_button.click();assert active_attempt(w.session)['mode']=='small'
        retry=PracticeDialog(w);retry.show();app.processEvents();retry.stuck.click();assert 'still stuck' in retry.status.text()
        for dialog in (d,review,recall,retry):
            dialog.resize(820,600);app.processEvents()
            for control in (dialog.try_button,dialog.helped,dialog.stuck):
                if control.isVisible():assert control.mapTo(dialog,QPoint()).y()+control.height()<=dialog.height()
            dialog.close()
        w.toggle_break();w.next_export=0.;w.refresh();assert w.latest_companion['practice'] is None
        w.toggle_break();assert not w.session.camera_active
        w.end_or_new();assert not w.session.active
        w.close();app.processEvents()
    result={'fixture':'Scripted check-ins and player choices; no real participants',
            'native_viewports':'1440x900 and 1024x768: camera/check-in visible, source tabs fit',
            'light_and_dark':'rendered','cma_adapted_practice_and_player_override':'passed',
            'cue_to_overlay_and_phone_payload':'passed','feedback_and_consented_recall':'passed',
            'still_stuck_and_break':'passed','report_pdf':'passed',
            'physical_camera_game_phone':'not tested','gamer_usefulness':'not established'}
    (OUT/'verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))


if __name__=='__main__':run()
