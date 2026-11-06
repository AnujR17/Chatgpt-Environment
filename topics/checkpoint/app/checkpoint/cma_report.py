"""Self-report CMA summaries and shareable PDFs. No facial-event log or inferred mood."""
import base64
from collections import Counter
import html
import math
from PySide6.QtCore import QObject,Signal,QThread,QBuffer,QIODevice,Slot,Qt
from PySide6.QtGui import QPdfWriter,QTextDocument,QFont,QPageSize


def zone(v,a):
    pleasant='Pleasant' if v>.18 else 'Unpleasant' if v<-.18 else 'In between'
    energy='high energy' if a>.4 else 'low energy' if a<-.4 else 'steady energy'
    return pleasant+' · '+energy


def cma_summary(session,activity=None):
    points=[]
    for item in session.reports:
        v,a=item.get('pleasantness'),item.get('activation')
        # Session stores the same two coordinates under valence/arousal.
        if v is None:v=item.get('valence')
        if a is None:a=item.get('arousal')
        if not all(isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x) and -1<=x<=1 for x in (v,a)):continue
        key=item.get('feeling','mixed')
        from checkpoint.session import FEELINGS
        points.append({'feeling':FEELINGS.get(key,(key,))[0],'pleasantness':v,'activation':a,
                       'elapsed_seconds':max(0.,float(item.get('elapsed_seconds',0))),'zone':zone(v,a)})
    points.sort(key=lambda p:p['elapsed_seconds']);counts=Counter(p['zone'] for p in points)
    result={'count':len(points),'points':points,'zones':dict(counts),'first':points[0] if points else None,'latest':points[-1] if points else None,
            'most_activated':max(points,key=lambda p:p['activation']) if points else None,'change':None}
    if len(points)>1:
        dv=points[-1]['pleasantness']-points[0]['pleasantness'];da=points[-1]['activation']-points[0]['activation']
        result['change']={'pleasantness':round(dv,3),'activation':round(da,3)}
        result['trend']=('More pleasant' if dv>.18 else 'Less pleasant' if dv<-.18 else 'Similar pleasantness')+' · '+('more activated' if da>.18 else 'less activated' if da<-.18 else 'similar activation')
    else:result['trend']='Add another check-in to see change' if points else 'No CMA check-ins yet'
    if not points:
        insight='Face tracking cannot fill a CMA report. Check in at the start, during play and near the end to build your own journey.'
        prompt='Next time, choose a feeling and adjust pleasantness and energy when something changes.'
    elif len(points)==1:
        insight='One check-in describes one moment. It does not establish how the whole session felt.'
        prompt='Add a later check-in to see whether pleasantness or activation changed.'
    elif any(p['pleasantness']<-.18 and p['activation']>.4 for p in points):
        insight='You recorded at least one unpleasant, highly activated moment. Compare it with your later check-in rather than treating high energy alone as a problem.'
        prompt='For the next session, consider a brief pause between attempts and check in again afterwards.'
    elif points[-1]['pleasantness']<-.18 and points[-1]['activation']<-.4:
        insight='Your latest check-in combines low activation with unpleasantness. This is your report of that moment, not a diagnosis.'
        prompt='Consider a shorter session or a smaller next goal, then see how it feels in another check-in.'
    else:
        insight='Your check-ins show '+result['trend'].lower()+'. The unreported time between them remains unknown.'
        prompt='What was different around the moments that felt better? Keep one thing you would repeat next time.'
    result.update(insight=insight,next_step=prompt)
    report={'schema':3,'game':session.game,'intention':session.intention,'duration_seconds':round(session.elapsed(),1),
            'cma':result,'basis':'Player check-ins; facial estimates and input timings do not establish pleasantness or activation.'}
    if activity:report['activity_summary']=activity
    return report


def journey_svg(points,duration):
    w,h=680,160;left=100;right=650
    duration=max(1.,duration,max((p['elapsed_seconds'] for p in points),default=0))
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="680" height="160" fill="#f6f4ee"/>']
    for key,title,y,colour in [('pleasantness','Pleasantness',38,'#285c48'),('activation','Activation',108,'#a17c33')]:
        parts.append(f'<text x="10" y="{y+4}" fill="#34453e" font-family="sans-serif" font-size="11">{title}</text><line x1="{left}" x2="{right}" y1="{y}" y2="{y}" stroke="#d9ddd3"/>')
        coords=[(left+(right-left)*p['elapsed_seconds']/duration,y-p[key]*28) for p in points]
        # Lines describe transitions between reported samples, never continuous measured mood.
        if len(coords)>1:parts.append('<polyline fill="none" stroke="'+colour+'" stroke-width="2" stroke-dasharray="5 4" points="'+' '.join(f'{x:.2f},{py:.2f}' for x,py in coords)+'"/>')
        for x,py in coords:parts.append(f'<circle cx="{x:.2f}" cy="{py:.2f}" r="4" fill="{colour}"/>')
    parts.append('<text x="100" y="151" font-family="sans-serif" font-size="10" fill="#66756b">Start</text><text x="615" y="151" font-family="sans-serif" font-size="10" fill="#66756b">Latest</text></svg>')
    return ''.join(parts)


def report_html(report):
    e=lambda v:html.escape(str(v));c=report['cma'];minutes=int(report['duration_seconds'])//60
    parts=['<html><head><meta charset="utf-8"><style>body{font-family:"DM Sans",sans-serif;color:#293b32;background:white;font-size:12px;line-height:1.2}h1{font-size:27px;margin-bottom:8px}h2{font-size:17px;margin-top:14px;margin-bottom:6px}p{margin:8px 0}.muted{color:#6c786e;font-size:11px}td{padding:9px;vertical-align:top}th{text-align:left;padding:8px;background:#e9ece3}table{border-collapse:collapse;width:100%}.card{background:#f6f4ee}li{margin:6px}</style></head><body>',
           '<p class="muted">CHECKPOINT / CMA SESSION REPORT</p><h1>Your session, in your words</h1>',
           f'<p>{e(report["game"])} · {minutes} minutes · {c["count"]} CMA check-ins</p><p class="muted">{e(report["intention"])}</p>',
           '<h2>Pleasantness and activation</h2><p>'+e(c['trend'])+'</p>']
    if c['count']:
        svg=base64.b64encode(journey_svg(c['points'],report['duration_seconds']).encode()).decode()
        parts.append('<img alt="Two journeys of your reported pleasantness and activation" src="data:image/svg+xml;base64,'+svg+'" width="680" height="160"/>')
        parts.append('<p class="muted">Each dot is a check-in. Dashed connections guide the eye; unreported time is unknown. Both scales run from −1 to +1.</p><table width="100%"><tr>')
        for title,key in [('First check-in','first'),('Most activated check-in','most_activated'),('Latest check-in','latest')]:
            p=c[key];parts.append(f'<td class="card"><b>{title}</b><p>{e(p["feeling"])}</p><p class="muted">{e(p["zone"])}</p></td>')
        parts.append('</tr></table>')
        if c['change']:
            d=c['change'];parts.append(f'<p>First to latest: pleasantness {d["pleasantness"]:+.2f}; activation {d["activation"]:+.2f}.</p>')
        parts.append('<h2>Where your check-ins landed</h2><p>')
        parts.append(' · '.join(f'{e(name)}: <b>{count} of {c["count"]}</b>' for name,count in sorted(c['zones'].items(),key=lambda p:-p[1])))
        parts.append('</p><p class="muted">Counts refer to check-ins, not time spent in a feeling.</p>')
    observed=report.get('observations')
    patterns=(observed or {}).get('expression_transitions',(observed or {}).get('sustained_patterns',{}))
    if observed and any(patterns.values()):
        label='Visual context (includes video testing)' if observed.get('video_test') else 'Visual context'
        parts.append('<h2>'+label+'</h2><p>'+e(observed.get('usable_face_seconds',0))+' seconds of usable observation, with '+e(sum(patterns.values()))+' smoothed expression transitions. These describe visual tracking, not time spent feeling an emotion.</p>')
    parts.extend(['<h2>What stands out</h2><p>'+e(c['insight'])+'</p>','<h2>For your next session</h2><p>'+e(c['next_step'])+'</p>',
                  '<p class="muted">CMA describes pleasantness and activation. Coordinates are adjustable check-in values, not clinical measurements. Facial estimates, hand gestures and input activity are not used to invent an emotional history.</p></body></html>'])
    return ''.join(parts)


def make_pdf(report):
    buffer=QBuffer();buffer.open(QIODevice.OpenModeFlag.WriteOnly)
    writer=QPdfWriter(buffer);writer.setPageSize(QPageSize(QPageSize.PageSizeId.A4));writer.setResolution(96);writer.setTitle('Checkpoint CMA session report')
    document=QTextDocument();document.setDefaultFont(QFont('DM Sans',11));document.setHtml(report_html(report));document.print_(writer)
    del writer
    return bytes(buffer.data())


class PdfService(QObject):
    requested=Signal(object,object)
    def __init__(self,parent=None):super().__init__(parent);self.requested.connect(self._render,Qt.ConnectionType.QueuedConnection)
    @Slot(object,object)
    def _render(self,report,job):
        try:job['data']=make_pdf(report)
        except Exception as ex:job['error']=str(ex)
        finally:job['event'].set()
    def render(self,report):
        if QThread.currentThread()==self.thread():return make_pdf(report)
        import threading
        job={'event':threading.Event(),'data':None,'error':None};self.requested.emit(report,job)
        if not job['event'].wait(5):raise TimeoutError('CMA report is not ready; keep the laptop app open and retry')
        if job['error']:raise RuntimeError(job['error'])
        return job['data']
