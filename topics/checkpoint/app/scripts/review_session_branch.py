"""Native Windows service/viewport check. All check-ins below are synthetic fixtures."""
import base64
import json
from pathlib import Path
from PySide6.QtCore import QPoint, QTimer
from checkpoint.app import create_application, MainWindow
from checkpoint.cma_report import make_pdf, report_html

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/session-review"
OUT.mkdir(parents=True, exist_ok=True)
app = create_application([])
window = MainWindow(no_setup=True, data_dir=ROOT / "build/session-review-history")
window.timer.stop()
window.reduced_motion = True
window.session.game = "Getting Over It"
window.session.intention = "Enjoy the challenge"
window.show()
app.processEvents()
views = []


def capture(name, width, height):
    window.resize(width, height)
    window.next_export = 0.
    window.refresh()
    app.processEvents()
    tabs = window.view_selectors[0]
    assert tabs.tabRect(2).right() < tabs.width(), "Reflection tabs clipped"
    start = window.camera_controls[0]
    assert start.mapTo(window, QPoint()).y() + start.height() < window.height(), "Camera action below viewport"
    assert window.scroll.widget().minimumSizeHint().width() <= window.scroll.viewport().width(), "Horizontal overflow"
    for text,key in window.state_labels:
        if key in ('valence','energy') and text.isVisible():
            assert text.mapTo(window,QPoint()).y()+text.height()<window.height(), "CMA value below initial viewport"
    reset=window.break_button
    if reset.isVisible():
        assert reset.mapTo(window,QPoint()).y()+reset.height()<window.height(), "Reset choice below viewport"
    path = OUT / (name + ".png")
    window.grab().save(str(path))
    views.append({"name": name, "actual_width": window.width(), "actual_height": window.height()})
    # Public synthetic screenshot chunks for the connector to inspect without a local executor.
    if name == "session-reset":
        raw = base64.b64encode(path.read_bytes()).decode()
        for i in range(0, len(raw), 24000):
            print("SESSION_PNG:" + raw[i:i + 24000], flush=True)


try:
    capture("session-empty-1024", 1024, 768)
    assert window.session.report is None
    window.session.check_in("frustrated", -.7, .8)
    window.select_card_source(2)
    capture("session-reset", 1360, 920)
    assert window.support.offer.kind == "reset"
    assert window.keepgoing_button.isVisible()
    assert window.break_button.isVisible()
    assert not window.focus_button.isVisible()
    window.keepgoing_button.click()
    assert window.support.offer is None and window.support.suppressed
    window.session.check_in("angry", -.8, .9)
    window.refresh()
    assert window.support.offer is None, "Dismissal was ignored"
    window.toggle_break()
    assert window.session.break_deadline is not None
    assert not window.session.camera_active
    assert window.latest_report["support"]["resets"] == 1
    window.toggle_break()
    assert window.support.feedback_reset is not None
    window.feedback_yes.click()
    assert window.latest_report["support"]["rated_helpful"] == 1
    assert len(window.session.reports) == 2
    # The focus path is a real text-entry dialog, with cancellation and confirmation.
    window.support.suppressed = False
    window.session.check_in("sad", -.6, -.7)
    window.refresh()
    assert window.support.offer.kind == "focus"
    def confirm_goal():
        dialog = app.activeModalWidget()
        dialog.setTextValue("One slower attempt")
        dialog.accept()
    QTimer.singleShot(50, confirm_goal)
    window.choose_practice_goal()
    assert window.session.practice_goal == "One slower attempt"
    assert window.latest_report["support"]["focus_goals"] == 1
    capture("session-goal-1024", 1024, 768)
    window.toggle_theme()
    capture("session-dark-1024", 1024, 768)
    markup = report_html(window.latest_report)
    assert "Your choices" in markup and "1 rated helpful" in markup
    pdf = make_pdf(window.latest_report)
    assert pdf.startswith(b"%PDF-") and len(pdf) > 5000
    (OUT / "session-report-fixture.pdf").write_bytes(pdf)
    result = {
        "fixture": "Synthetic check-ins; not emotion accuracy or intervention efficacy",
        "cma_routing": "passed", "keep_going_suppression": "passed",
        "real_reset_and_feedback": "passed", "real_practice_goal_dialog": "passed",
        "checkins_preserved": "passed", "cma_pdf_choices": "passed",
        "viewports": views, "physical_camera_game_phone": "not tested",
        "ota_or_release": "not published",
    }
    (OUT / "verification.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("SESSION_REVIEW:" + json.dumps(result), flush=True)
finally:
    window.close()
    app.processEvents()
