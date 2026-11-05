"""Local headless render timing, not a device power or gaming-impact benchmark."""
import json,statistics,time
from pathlib import Path
from PySide6.QtCore import QEvent
from PySide6.QtGui import QImage
from checkpoint.app import create_application,MainWindow
app=create_application([]);w=MainWindow(no_setup=True);w.show();app.processEvents();w.timer.stop();w.session.check_in('excited');w.refresh()
results={}
for mode in range(3):
    w.change_view(mode);app.processEvents();g=w.emblems[mode];g.timer.stop();g.value=g.target
    durations=[];im=QImage(g.size(),QImage.Format.Format_ARGB32)
    for i in range(120):
        g.phase=i/30;start=time.perf_counter();g.render(im);durations.append((time.perf_counter()-start)*1000)
    results[['form','lines','dots'][mode]]={'render_median_ms':round(statistics.median(durations),3),'render_p95_ms':round(sorted(durations)[113],3),'samples':120,'widget_size':[g.width(),g.height()]}
w.reduced_motion=True;w.refresh();results['reduced_motion_timer_count']=sum(g.timer.isActive() for g in w.emblems)
w.resize(1100,820);app.processEvents();im=QImage(w.size(),QImage.Format.Format_ARGB32);w.render(im);im.save('artifacts/emotion-ui-compact.png')
w.close();w.deleteLater();app.sendPostedEvents(None,QEvent.Type.DeferredDelete);app.processEvents()
results['scope']='Linux offscreen Qt on the current cloud CPU. Measures drawing only; no physical webcam, game, GPU, battery or browser comparison.'
Path('artifacts/emotion-render-profile.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
