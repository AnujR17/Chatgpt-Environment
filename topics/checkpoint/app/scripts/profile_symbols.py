import json,statistics,time
from pathlib import Path
from PySide6.QtGui import QImage
from checkpoint.app import create_application,MainWindow
from checkpoint.symbols import CORE
from PySide6.QtCore import QEvent
app=create_application([]);w=MainWindow(no_setup=True);w.show();app.processEvents();w.timer.stop();g=w.emblems[0];g.fade_override=1.
result={}
for key in CORE:
    g.set_state(key);g.timer.stop();times=[];im=QImage(g.size(),QImage.Format.Format_ARGB32)
    for i in range(120):
        g.animation_time=i/30;start=time.perf_counter();g.render(im);times.append((time.perf_counter()-start)*1000)
    result[key]={'median_ms':round(statistics.median(times),3),'p95_ms':round(sorted(times)[113],3)}
w.reduced_motion=True;w.refresh();result['animation_timers_when_reduced']=sum(e.timer.isActive() for e in w.emblems)
result['scope']='120 native artwork renders per word, Linux offscreen cloud CPU. Drawing only; no physical camera, running game, GPU, battery or browser comparison.'
Path('artifacts/emotion-symbol-profile.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));w.close();w.deleteLater();app.sendPostedEvents(None,QEvent.Type.DeferredDelete);app.processEvents()
