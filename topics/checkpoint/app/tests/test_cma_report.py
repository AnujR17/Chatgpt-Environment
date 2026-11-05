import os
os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
from checkpoint.app import create_application
from checkpoint.session import Session
from checkpoint.cma_report import cma_summary,report_html,make_pdf


def test_report_uses_checkins_not_facial_events_or_time_coverage():
    session=Session();session.check_in('angry',-.7,.8);session.check_in('calm',.6,-.6)
    session.reports[0]['elapsed_seconds']=30;session.reports[1]['elapsed_seconds']=200
    report=cma_summary(session);c=report['cma']
    assert report['schema']==3 and c['count']==2 and c['change']=={'pleasantness':1.3,'activation':-1.4}
    assert 'More pleasant' in c['trend'] and c['most_activated']['feeling']=='Angry'
    assert sum(c['zones'].values())==2
    assert 'moments' not in report and 'input_activity' not in report
    markup=report_html(report)
    assert 'Counts refer to check-ins, not time' in markup and 'For your next session' in markup


def test_no_checkins_does_not_make_a_cma_estimate_from_a_face():
    session=Session();report=cma_summary(session)
    assert report['cma']['count']==0 and report['cma']['change'] is None
    assert 'Face tracking cannot fill' in report['cma']['insight']
    assert 'No CMA check-ins' not in report_html(report) or not report['cma']['points']


def test_report_html_escapes_context_and_exports_real_pdf():
    app=create_application([]);session=Session(game='<script>bad()</script>');session.check_in('happy',.6,.3)
    report=cma_summary(session);markup=report_html(report)
    assert '<script>bad' not in markup and '&lt;script&gt;' in markup
    pdf=make_pdf(report)
    assert pdf.startswith(b'%PDF-') and len(pdf)>5000
