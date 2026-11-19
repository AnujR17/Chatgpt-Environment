from checkpoint.break_reminder import BreakReminder


def test_explicit_opt_in_starts_a_fresh_thirty_second_timer():
    r=BreakReminder()
    assert not r.update(100,enabled=False) and r.deadline is None
    assert not r.update(1000,enabled=True)
    assert r.remaining(1000)==30
    assert not r.update(1029.99,enabled=True)
    assert r.update(1030,enabled=True)=="Let's take a break?"
    assert not r.update(1039,enabled=True)
    assert r.update(1060,enabled=True)==r.MESSAGE


def test_disable_break_end_and_interval_change_reset_the_timer():
    r=BreakReminder();r.update(0,enabled=True)
    for options in ({'enabled':False},{'enabled':True,'paused':True},{'enabled':True,'active':False}):
        assert not r.update(30,**options) and r.deadline is None
        assert not r.update(40,enabled=True) and r.remaining(40)==30
    assert not r.update(50,enabled=True,seconds=120)
    assert not r.update(169,enabled=True,seconds=120)
    assert r.update(170,enabled=True,seconds=120)==r.MESSAGE


def test_companion_reminder_needs_no_game_camera_or_checkin():
    from checkpoint.companion import CompanionState
    from checkpoint.session import Session
    c=CompanionState();s=Session()
    c.update(s,None,None,now=0)
    assert c.reminder.deadline is None
    c.update(s,None,None,now=10,break_reminders=True)
    state,_=c.update(s,None,None,now=40,break_reminders=True)
    assert state['nudge']==c.reminder.MESSAGE
    assert state['break_reminder']['remaining_seconds']==30
    assert not s.camera_active and s.report is None


def test_session_controls_apply_interval_and_opt_out_immediately(tmp_path):
    from checkpoint.app import create_application,MainWindow
    from PySide6.QtCore import QCoreApplication,QEvent
    app=create_application([]);w=MainWindow(no_setup=True,data_dir=tmp_path);w.timer.stop()
    try:
        assert not w.break_reminders_enabled and not w.companion.reminder.deadline
        w.reminder_toggle.click()
        assert w.break_reminders_enabled and w.overlay_enabled
        assert w.overlay.timer_value.text()=='0:30'
        w.reminder_interval.setCurrentIndex(w.reminder_interval.findData(120))
        assert w.reminder_seconds==120 and w.overlay.timer_value.text()=='2:00'
        w.overlay_action('reminders')
        assert not w.break_reminders_enabled and not w.overlay.message
        assert w.overlay.timer_value.text()==''
        w.set_break_reminders(True);w.start_break(30)
        assert w.companion.reminder.deadline is None
        w.overlay_action('continue')
        assert w.overlay.timer_value.text()=='2:00'
    finally:
        w.close();w.deleteLater();QCoreApplication.sendPostedEvents(None,QEvent.Type.DeferredDelete)


def test_settings_custom_interval_and_transparent_label_rendering(tmp_path):
    from checkpoint.app import create_application,MainWindow,PreferencesDialog
    from PySide6.QtCore import QCoreApplication,QEvent,QTimer
    app=create_application([]);w=MainWindow(no_setup=True,data_dir=tmp_path);w.timer.stop()
    try:
        def save():
            dialog=app.activeModalWidget();assert isinstance(dialog,PreferencesDialog)
            dialog.break_reminders.setChecked(True);dialog.reminder_seconds.setValue(75);dialog.accept()
        QTimer.singleShot(10,save);w.show_preferences()
        assert w.reminder_seconds==75 and w.reminder_interval.currentData()==75
        assert w.overlay.timer_value.text()=='1:15'
        w.overlay.show();app.processEvents();image=w.overlay.grab().toImage()
        assert image.pixelColor(25,230).alpha()==0  # No label backing box.
        pixels=[image.pixelColor(x,y) for x in range(65,155) for y in range(225,253)]
        assert any(c.red()>245 and c.green()>245 and c.blue()>245 and c.alpha()>240 for c in pixels)
        assert not w.session.camera_active and not w.detect_games
    finally:
        w.close();w.deleteLater();QCoreApplication.sendPostedEvents(None,QEvent.Type.DeferredDelete)
