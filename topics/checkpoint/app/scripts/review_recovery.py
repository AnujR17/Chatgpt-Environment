"""Native frustration/choice/follow-up flow using explicitly scripted player reports."""
import json,tempfile,time
from pathlib import Path
from PySide6.QtCore import QTimer,Qt,QPoint,QCoreApplication,QEvent
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QPushButton
from checkpoint.app import create_application,MainWindow,CheckinDialog,EmotionLibraryDialog
from checkpoint.gameplay import GameObservation
from checkpoint.cma_report import make_pdf,report_html
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/design-review';OUT.mkdir(parents=True,exist_ok=True)
app=create_application([])


def check_in(window,key,v,a,context='No context'):
    def save():
        d=app.activeModalWidget();assert isinstance(d,CheckinDialog)
        d.sliders[0].setValue(round(v*100));d.sliders[1].setValue(round(a*100));d.context.setCurrentText(context);d.save.click()
    if window.session.report is None:
        def choose():
            d=app.activeModalWidget();assert isinstance(d,EmotionLibraryDialog)
            QTimer.singleShot(0,save);d.cards[key].click()
        QTimer.singleShot(0,choose);window.show_emotion_library()
    else:QTimer.singleShot(0,save);window.check_in(key)


def run():
 with tempfile.TemporaryDirectory() as directory:
    w=MainWindow(no_setup=True,data_dir=directory);w.timer.stop();w.reduced_motion=True;w.resize(1440,900);w.show();app.processEvents()
    assert w.source_mode==2 and w.worker is None
    w.session.started=time.monotonic()-60
    w.game_observation=GameObservation('Getting Over It','Scripted foreground context','Possible fall',{'kind':'falling','title':'Possible fall','basis':'Scripted game state, not actual gameplay','section':None})
    check_in(w,'frustrated',-.7,.8,'Repeated setback');w.next_export=0.;w.refresh();app.processEvents()
    assert w.session.reports[-1]['context']=='Repeated setback'
    assert w.break_button.property('primary') and not w.goal_control.property('primary')
    assert w.session.reports[-1]['game_context']['title']=='Possible fall'
    assert w.emblems[0].current_state=='frustrated' and not w.session.camera_active
    w.grab().save(str(OUT/'recovery-frustrated.png'))
    w.session.started-=30;w.break_button.click();assert w.session.responses[-1]['kind']=='pause'
    assert w.session.break_deadline is not None and not w.session.camera_active
    w.toggle_break();assert w.session.break_deadline is None and not w.session.camera_active
    w.session.started-=90;check_in(w,'neutral',.3,-.2,'No context')
    w.rate_response('yes');w.next_export=0.;w.refresh();app.processEvents()
    assert not w.break_button.property('primary') and not w.goal_control.property('primary')
    report=w.latest_report;row=report['recovery']['choices'][0]
    assert row['before']['feeling']=='Frustrated' and row['after']['feeling']=='Neutral'
    assert row['helpful']=='yes' and report['recovery']['helpful']=={'Take a pause':1}
    assert report['cma']['count']==2 and 'not detected causes' in report_html(report)
    w.grab().save(str(OUT/'recovery-later.png'))
    (OUT/'recovery-sample-report.pdf').write_bytes(make_pdf(report))
    # End must not fabricate another response, and controls must stop.
    w.end_or_new();assert len(w.session.responses)==1 and not w.continue_control.isEnabled()
    w.close();w.deleteLater();QCoreApplication.sendPostedEvents(None,QEvent.Type.DeferredDelete);app.processEvents()
 result={'fixture':'Scripted self-reports and game context; no participant or real-game result',
         'default_self_report_stage':'passed','context_and_game_estimate_separated':'passed','pause_then_later_cma':'passed',
         'player_helpfulness_rating':'passed','report_and_pdf':'passed','camera_stays_off':'passed','end_does_not_invent_response':'passed',
         'real_frustration_or_recovery_detection':'not established'}
 (OUT/'recovery-verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))


if __name__=='__main__':run()
