import os
os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
from PySide6.QtCore import Qt,QByteArray,QCoreApplication,QEvent
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtTest import QTest
from checkpoint.app import create_application,MainWindow
from checkpoint.session import Session
from checkpoint.cma_report import cma_summary,make_pdf
from checkpoint.report_visual import report_pages,RecapDialog
from checkpoint.controls import Select,Switch


def test_empty_and_single_checkin_graphics_do_not_invent_a_journey():
    app=create_application([]);s=Session()
    svg=report_pages(cma_summary(s))[0]
    assert 'No check-ins yet' in svg and '<polyline' not in svg
    assert QSvgRenderer(QByteArray(svg.encode())).isValid()
    s.check_in('surprised',.1,.6)
    svg=report_pages(cma_summary(s))[0]
    assert '<polyline' not in svg and 'Add another to see a change' in svg


def test_graphic_report_escapes_notes_paginates_and_keeps_all_reported_samples():
    app=create_application([]);s=Session(game='<script>invalid</script>')
    for i in range(27):
        s.check_in('surprised',.1,.6,context='Last note <unsafe>' if i==26 else 'A difficult section')
        s.reports[-1]['elapsed_seconds']=i*20
    s.record_response('pause');s.responses[-1]['elapsed_seconds']=140
    report=cma_summary(s);pages=report_pages(report)
    assert len(pages)>5 and report['cma']['count']==27
    markup=''.join(pages)
    assert '<script>' not in markup and '&lt;script&gt;' in markup
    assert 'Last note &lt;unsafe&gt;' in markup
    for svg in pages:assert QSvgRenderer(QByteArray(svg.encode())).isValid()
    pdf=make_pdf(report);assert pdf.startswith(b'%PDF-') and len(pdf)>10000


def test_native_recap_replaces_text_dashboard_and_session_end_shows_the_same_graphic(tmp_path):
    app=create_application([]);w=MainWindow(no_setup=True,data_dir=tmp_path);w.timer.stop()
    try:
        w.resize(1024,768);w.show();app.processEvents()
        from PySide6.QtCore import QPoint
        for control in (w.capture_control,w.checkin_button,w.game_detection_control,w.setback_control):assert control.mapTo(w,QPoint(control.width(),control.height())).y()<=768
        w.session.check_in('surprised',.1,.6);w.next_export=0.;w.refresh()
        dialog=RecapDialog(w,w.latest_report);dialog.show();app.processEvents()
        assert dialog.sheets and dialog.sheets[0].renderer.isValid()
        assert any(b.text()=='Save PDF' for b in dialog.findChildren(__import__('PySide6.QtWidgets',fromlist=['QPushButton']).QPushButton))
        dialog.close();w.end_or_new();app.processEvents()
        assert w.summary_graphic.renderer.isValid() and not w.session_actions.isVisible()
        assert w.summary_graphic.report['cma']['count']==1
    finally:w.close();w.deleteLater();QCoreApplication.sendPostedEvents(None,QEvent.Type.DeferredDelete)


def test_drawn_controls_keep_keyboard_selection_and_toggle_behavior():
    app=create_application([]);select=Select();select.addItems(['30 seconds','1 minute']);select.show();select.setFocus();app.processEvents()
    QTest.keyClick(select,Qt.Key.Key_Down);assert select.currentIndex()==1
    select.showPopup();app.processEvents();assert select.view().isVisible();select.hidePopup();select.close()
    switch=Switch('Break reminders');switch.show();switch.setFocus();app.processEvents();QTest.keyClick(switch,Qt.Key.Key_Space)
    assert switch.isChecked();switch.close()
