"""Shared vector artwork for the native recap and PDF. Every mark comes from a report."""
import base64,html,math,textwrap
from collections import Counter
from PySide6.QtCore import QByteArray,QRectF,Qt
from PySide6.QtGui import QPainter,QColor
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QWidget,QVBoxLayout,QScrollArea,QDialog,QHBoxLayout,QPushButton,QLabel,QFileDialog,QMessageBox,QTextBrowser

INK='#25392E';MUTED='#52675B';PAPER='#F7F5EC';GREEN='#315D45';SAGE='#DDE6CF';GOLD='#A05D24'
COLOURS={'Neutral':'#578574','Happy':'#AE701F','Frustrated':'#AF5745','Sad':'#527CA1','Surprised':'#7765A1'}


def esc(value):return html.escape(str(value),quote=True)
def clock(seconds):
    seconds=max(0,int(seconds));return f'{seconds//60}:{seconds%60:02d}'
def txt(x,y,value,size=16,colour=INK,weight=400,anchor='start'):
    return f'<text x="{x}" y="{y}" font-family="DM Sans, sans-serif" font-size="{size}" font-weight="{weight}" fill="{colour}" text-anchor="{anchor}">{esc(value)}</text>'
def lines(x,y,value,width=60,size=16,colour=INK,max_lines=None,weight=400):
    rows=textwrap.wrap(str(value),width=width,break_long_words=True,replace_whitespace=True) or ['']
    if max_lines and len(rows)>max_lines:rows=rows[:max_lines];rows[-1]=rows[-1].rstrip(' .,')+'…'
    return ''.join(txt(x,y+i*size*1.48,row,size,colour,weight) for i,row in enumerate(rows))
def line(x1,y1,x2,y2,colour='#CED7C8',width=1,dash=''):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{colour}" stroke-width="{width}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def circle(x,y,r,fill,stroke='none',sw=1):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def wrap_svg(parts,title):
    return '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="848" viewBox="0 0 1200 848"><title>'+esc(title)+'</title><rect width="1200" height="848" fill="'+PAPER+'"/>'+''.join(parts)+'</svg>'


def nori(x,y,size=100,feeling='Neutral'):
    colour={'Neutral':'#83D2BB','Happy':'#EBC16D','Frustrated':'#DB977E','Sad':'#9AAEC7','Surprised':'#A99AD0'}.get(feeling,'#83D2BB')
    bits=[f'<g transform="translate({x},{y}) scale({size/100})">',f'<path d="M15 84 C5 61 12 15 36 9 C63 -1 86 15 88 49 C93 79 84 93 72 92 L53 86 Q44 84 32 91 Q21 97 15 84" fill="{colour}"/>']
    for ex in (36,64):bits.append(f'<ellipse cx="{ex}" cy="48" rx="2.6" ry="{4.8 if feeling=="Surprised" else 4}" fill="#29334B"/>')
    if feeling=='Surprised':bits.extend([f'<path d="M{ex-5} 32 Q{ex} 27 {ex+5} 32" fill="none" stroke="#29334B" stroke-width="2.2" stroke-linecap="round"/>' for ex in (36,64)]);bits.append('<ellipse cx="50" cy="66" rx="4" ry="5" fill="#29334B"/>')
    else:
        curve=72 if feeling=='Happy' else 58 if feeling in ('Sad','Frustrated') else 65
        bits.append(f'<path d="M40 65 Q50 {curve} 60 65" fill="none" stroke="#29334B" stroke-width="2.3" stroke-linecap="round"/>')
    bits.append('</g>');return ''.join(bits)


def overview_svg(report):
    c=report['cma'];points=c['points'];duration=max(1,report['duration_seconds'],max((p['elapsed_seconds'] for p in points),default=0))
    recovery=report.get('recovery',{});latest=c.get('latest');feeling=(latest or {}).get('feeling','Neutral')
    p=['<rect width="1200" height="196" fill="#243D32"/>',
       '<path d="M660 196 L766 93 L819 128 L924 33 L1004 126 L1064 72 L1200 196Z" fill="#345545"/>',
       '<path d="M730 196 L846 141 L900 163 L1037 83 L1200 153 L1200 196Z" fill="#49634A"/>',
       txt(44,35,'REGEN / SESSION RECAP',12,'#D6E3CB',600),
       lines(44,80,report['game'],width=43,size=32,colour='#FFFEF8',max_lines=2,weight=600),
       txt(45,170,report['intention'],15,'#D6E3CB'),nori(1060,53,112,feeling),
       txt(796,77,clock(report['duration_seconds']),30,'#FFFEF8',600),txt(796,102,'Session time',12,'#D6E3CB'),
       txt(951,77,c['count'],30,'#FFFEF8',600),txt(951,102,'Check-ins',12,'#D6E3CB'),
       txt(44,236,'Your check-in journey',25,INK,600),txt(44,263,'Reported moments over time',13,MUTED),
       txt(795,236,'Where you checked in',23,INK,600)]
    # Time-series plots retain discrete samples and explicit zero/reference values.
    for key,title,cy,colour in [('pleasantness','Pleasantness',350,GREEN),('activation','Activation',478,GOLD)]:
        left,right=142,715
        p.extend([txt(44,cy-52,title,15,colour,600),txt(110,cy-43,'+1',11,MUTED),txt(113,cy+4,'0',11,MUTED),txt(109,cy+48,'−1',11,MUTED)])
        for offset in (-44,0,44):p.append(line(left,cy+offset,right,cy+offset,'#D6DDCE',1,'3 5' if offset else ''))
        coords=[(left+(right-left)*pt['elapsed_seconds']/duration,cy-pt[key]*44) for pt in points]
        if len(coords)>1:p.append('<polyline fill="none" stroke="'+colour+'" stroke-width="2" stroke-dasharray="5 6" points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in coords)+'"/>')
        for i,(x,y) in enumerate(coords):
            p.append(circle(x,y,5.5,colour,PAPER,2))
            if len(coords)<=8:p.append(txt(x,y-11,str(i+1),10,colour,600,'middle'))
    p.extend([txt(142,549,'0:00',11,MUTED),txt(715,549,clock(max(report['duration_seconds'],max((pt['elapsed_seconds'] for pt in points),default=0))),11,MUTED,anchor='end')])
    if not points:
        p.extend([txt(432,373,'No check-ins yet',19,MUTED,600,'middle'),txt(432,398,'Your first report creates the first point.',13,MUTED,anchor='middle')])
    elif len(points)==1:p.append(txt(142,575,'One check-in is one moment. Add another to see a change.',12,MUTED))
    # CMA map: both axes are explicitly reported, not inferred from the face or gameplay.
    cx,cy,r=976,404,113
    p.extend([circle(cx,cy,r,'#E8EDDF'),circle(cx,cy,r/2,'none','#C7D3BF'),line(cx-r,cy,cx+r,cy,'#AABBA1'),line(cx,cy-r,cx,cy+r,'#AABBA1'),txt(cx,277,'High activation',12,MUTED,anchor='middle'),txt(cx,545,'Low activation',12,MUTED,anchor='middle'),txt(843,564,'Unpleasant',12,MUTED),txt(1110,564,'Pleasant',12,MUTED,anchor='end')])
    for i,pt in enumerate(points):
        x=cx+pt['pleasantness']*r*.82;y=cy-pt['activation']*r*.82;col=COLOURS.get(pt['feeling'],GREEN)
        p.append(circle(x,y,7,col,PAPER,2))
        if len(points)<=9:p.append(txt(x,y-12,i+1,10,INK,600,'middle'))
    if not points:p.extend([txt(cx,cy-5,'No reported',14,MUTED,anchor='middle'),txt(cx,cy+17,'coordinates',14,MUTED,anchor='middle')])
    for i,(name,col) in enumerate(COLOURS.items()):p.extend([circle(799+i*72,590,3.5,col),txt(807+i*72,594,name,9,MUTED)])
    p.extend([line(44,604,1156,604),txt(44,638,'The choices you made',23,INK,600),txt(698,638,'For your next session',23,INK,600)])
    counts=Counter(row['title'] for row in recovery.get('choices',[]));total=sum(counts.values())
    if counts:
        for i,(title,count) in enumerate(counts.items()):
            y=673+i*34;p.extend([txt(44,y,title,14),f'<rect x="250" y="{y-12}" width="{max(3,count/max(counts.values())*250)}" height="10" rx="3" fill="{GREEN}"/>',txt(520,y,count,14,INK,600)])
    else:p.extend([txt(44,679,'No choices recorded',16,MUTED),txt(44,704,'Pauses, smaller goals and continuing appear here.',13,MUTED)])
    practice=report.get('practice',{})
    if practice.get('started'):p.append(txt(44,773,f"Practice cues: {practice['started']} / Helpful: {practice['helped']} / Awaiting feedback: {practice['unrated']}",12,MUTED))
    next_step=c['next_step']
    p.append(lines(698,673,next_step,width=49,size=15,max_lines=5))
    p.extend([line(44,797,1156,797),txt(44,824,'Each point is a check-in. Dashed lines connect reports; unreported time is unknown.',11,MUTED),txt(1156,824,'01 / OVERVIEW',10,MUTED,600,'end')])
    return wrap_svg(p,'Regen session overview')


def detail_pages(report):
    c=report['cma'];events=[]
    for i,pt in enumerate(c['points']):
        details=f"Pleasantness {pt['pleasantness']:+.2f} / Activation {pt['activation']:+.2f}"
        if pt.get('context'):details+=' / '+pt['context']
        events.append((pt['elapsed_seconds'],str(i+1).zfill(2),pt['feeling'],details))
    for row in report.get('recovery',{}).get('choices',[]):
        details=row.get('detail','')
        if row.get('helpful'):details+=' / '+{'yes':'Marked helpful','no':'Not helpful','unsure':'Not sure'}.get(row['helpful'],'')
        after=row.get('after')
        if after:details+=' / Next check-in: '+after['feeling']
        events.append((row['elapsed_seconds'],'CHOICE',row['title'],details or 'No feedback recorded'))
    for row in report.get('practice',{}).get('lessons',[]):
        events.append((row.get('elapsed_seconds'),'PRACTICE',row.get('section','Technique cue'),row.get('cue','')+' / '+row.get('lesson','')+' / '+row.get('outcome','')))
    events.sort(key=lambda x:x[0] if x[0] is not None else float('inf'))
    if not events:return []
    # Long notes continue onto subsequent rows/pages rather than being silently clipped.
    expanded=[]
    for stamp,kind,title,detail in events:
        chunks=textwrap.wrap(str(detail),width=108,break_long_words=True) or ['']
        for start in range(0,len(chunks),3):expanded.append((stamp,kind,title if start==0 else title+' / continued','\n'.join(chunks[start:start+3])))
    pages=[]
    for offset in range(0,len(expanded),5):
        number=len(pages)+2;p=[txt(44,38,'REGEN / SESSION RECAP',12,GREEN,600),txt(44,91,'Your session trail',34,INK,600),txt(44,122,'Check-ins, choices and practice notes in the order you recorded them.',15,MUTED),line(75,164,75,728,'#A8BBA0',2)]
        for index,(stamp,kind,title,detail) in enumerate(expanded[offset:offset+5]):
            y=184+index*114;p.extend([circle(75,y-4,8,GREEN,PAPER,3),txt(104,y-1,(clock(stamp) if stamp is not None else 'Time not recorded')+' / '+kind,11,MUTED,600),txt(104,y+27,title[:80],20,INK,600)])
            for j,row in enumerate(detail.splitlines()):p.append(txt(104,y+50+j*17,row,12,MUTED))
        p.extend([line(44,785,1156,785),lines(44,809,report.get('basis','Player-reported moments; changes do not establish causes.'),width=135,size=10,max_lines=2),txt(1156,824,f'{number:02d} / SESSION TRAIL',10,MUTED,600,'end')]);pages.append(wrap_svg(p,'Regen chronological session trail'))
    return pages


def report_pages(report):return [overview_svg(report),*detail_pages(report)]


class ReportSheet(QWidget):
    def __init__(self,svg,parent=None):
        super().__init__(parent);self.report=None;self.renderer=QSvgRenderer(QByteArray(svg.encode()),self);self.setMinimumWidth(480)
        self.setAccessibleName('Graphical session recap');self.setAccessibleDescription('Check-in timeline, pleasantness and activation map, and player choices. Use Read report data for a text version.')
    def set_report(self,report):
        self.report=report;self.renderer.load(QByteArray(overview_svg(report).encode()));self.update()
    def resizeEvent(self,event):self.setMinimumHeight(round(self.width()*848/1200));super().resizeEvent(event)
    def paintEvent(self,event):
        p=QPainter(self);p.setRenderHint(QPainter.RenderHint.Antialiasing);self.renderer.render(p,QRectF(0,0,self.width(),self.width()*848/1200));p.end()


class RecapDialog(QDialog):
    def __init__(self,parent,report):
        super().__init__(parent);self.report=report;self.theme=getattr(parent,'theme','light');self.setWindowTitle('Regen / Session recap');self.resize(1250,850)
        root=QVBoxLayout(self);root.setContentsMargins(22,18,22,18);root.setSpacing(16)
        bar=QHBoxLayout();title=QLabel('Session recap');title.setStyleSheet('font-size:22px;font-weight:600;background:transparent');bar.addWidget(title,1)
        from checkpoint.controls import ActionButton
        for text,callback,primary in [('Read report data',self.read_data,False),('Save PDF',self.save_pdf,True),('Close',self.accept,False)]:
            b=ActionButton(text);b.setProperty('primary',primary);b.setMinimumHeight(42);b.clicked.connect(callback);bar.addWidget(b)
        root.addLayout(bar);scroll=QScrollArea();scroll.setWidgetResizable(True);body=QWidget();layout=QVBoxLayout(body);layout.setContentsMargins(0,0,10,0);layout.setSpacing(20)
        self.sheets=[]
        for svg in report_pages(report):sheet=ReportSheet(svg);layout.addWidget(sheet);self.sheets.append(sheet)
        scroll.setWidget(body);root.addWidget(scroll,1)
    def save_pdf(self):
        from checkpoint.cma_report import make_pdf
        path,_=QFileDialog.getSaveFileName(self,'Save session recap','regen-session-recap.pdf','PDF (*.pdf)')
        if path:
            try:
                from pathlib import Path
                Path(path).write_bytes(make_pdf(self.report))
            except Exception as ex:QMessageBox.warning(self,'Report unavailable',str(ex))
    def read_data(self):
        from checkpoint.cma_report import report_html
        dialog=QDialog(self);dialog.setWindowTitle('Report data');dialog.resize(780,680);layout=QVBoxLayout(dialog);text=QTextBrowser();text.setHtml(report_html(self.report,graphical=False));layout.addWidget(text);close=QPushButton('Close');close.clicked.connect(dialog.accept);layout.addWidget(close);dialog.exec()
