import os,time
os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
from PySide6.QtCore import Qt,QPoint,QTimer,QCoreApplication,QEvent
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QMenu
from checkpoint.app import create_application,MainWindow,EmotionLibraryDialog,CheckinDialog
from checkpoint.primary import PRIMARY_KEYS,PRIMARY_LABELS,limit_display
from checkpoint.expression_view import ExpressionDisplay


def test_primary_routes_collapse_extra_labels_without_adding_new_states():
    cases={'happy':'Happy','amused':'Happy','angry':'Frustrated','frustrated':'Frustrated','sad':'Sad','confused':'Confused','composed':'Neutral'}
    for artwork,title in cases.items():
        display=limit_display(ExpressionDisplay('Raw',artwork,''))
        assert display.title==title and display.artwork in PRIMARY_KEYS
    for artwork in ('surprised','afraid','disgust'):
        d=limit_display(ExpressionDisplay('Raw',artwork,''));assert d.title=='Neutral' and d.artwork is None


def test_widget_click_opens_controls_with_only_five_checkin_choices(tmp_path):
    app=create_application([]);w=MainWindow(no_setup=True,data_dir=tmp_path);w.timer.stop();w.show();w.toggle_overlay();app.processEvents()
    try:
        assert not w.overlay.windowFlags()&Qt.WindowType.WindowTransparentForInput
        QTest.mouseClick(w.overlay,Qt.MouseButton.LeftButton,pos=QPoint(110,150));app.processEvents()
        menu=w.overlay.menu;assert menu and menu.isVisible()
        choices=menu.actions()[0].menu().actions()
        assert [a.text() for a in choices]==list(PRIMARY_LABELS.values())
        assert w.overlay.name_label.text()=='Neutral'
        menu.close()
    finally:w.close();w.deleteLater();QCoreApplication.sendPostedEvents(None,QEvent.Type.DeferredDelete)


def test_widget_checkin_saves_input_and_reflects_it_immediately(tmp_path):
    app=create_application([]);w=MainWindow(no_setup=True,data_dir=tmp_path);w.timer.stop();w.show();w.toggle_overlay()
    try:
        def save():
            d=app.activeModalWidget();assert isinstance(d,CheckinDialog)
            d.sliders[0].setValue(-65);d.sliders[1].setValue(-55);d.save.click()
        QTimer.singleShot(20,save);w.overlay_action('checkin:sad');app.processEvents()
        assert w.session.report=='sad' and w.source_mode==2
        assert w.overlay.name_label.text()=='Sad'
        assert (w.session.valence,w.session.arousal)==(-.65,-.55)
        assert not w.session.camera_active
    finally:w.close();w.deleteLater();QCoreApplication.sendPostedEvents(None,QEvent.Type.DeferredDelete)


def test_widget_break_timer_is_readable_and_ends_on_explicit_continue(tmp_path):
    app=create_application([]);w=MainWindow(no_setup=True,data_dir=tmp_path);w.timer.stop();w.show();w.toggle_overlay()
    try:
        w.overlay_action('break:60');app.processEvents()
        assert w.overlay.timer_caption.text()=='Break time' and w.overlay.timer_value.text()=='1:00'
        assert w.overlay.timer_value.font().pixelSize()>=28 and w.countdown.font().pixelSize()==64
        assert w.overlay.name_label.text() in PRIMARY_LABELS.values()
        w.session.break_deadline=time.monotonic()-1;w.refresh()
        assert w.overlay.timer_value.text()=='0:00' and w.overlay.timer_caption.text()=='Break complete'
        assert w.session.break_deadline is not None
        w.overlay_action('continue');assert w.session.break_deadline is None
        assert not w.session.camera_active
    finally:w.close();w.deleteLater();QCoreApplication.sendPostedEvents(None,QEvent.Type.DeferredDelete)


def test_widget_pause_all_cancels_pending_observation_resume(tmp_path):
    app=create_application([]);w=MainWindow(no_setup=True,data_dir=tmp_path);w.timer.stop()
    try:
        w.break_resume_options=(True,True);w.pause_all();assert w.break_resume_options is None
    finally:w.close();w.deleteLater();QCoreApplication.sendPostedEvents(None,QEvent.Type.DeferredDelete)
