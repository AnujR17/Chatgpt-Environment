"""Real-time local video → capture/inference → reflection → native/phone state.
The small acted-clip selection is a smoke check, not an accuracy benchmark.
"""
import json,time
from collections import Counter
from pathlib import Path
import numpy as np
from checkpoint.app import create_application,MainWindow

ROOT=Path(__file__).resolve().parents[1]


def main():
    app=create_application([]);window=MainWindow(no_setup=True,data_dir=ROOT/'build/rebuild-video-check');window.show()
    results=[]
    try:
        files=[f'02-01-{emotion}-01-01-01-04.mp4' for emotion in ('01','03','05','04','06','07','08')]
        files+=['02-01-05-02-01-01-01.mp4','02-01-03-02-01-01-01.mp4']
        for filename in files:
            video=ROOT/'data/videos'/filename
            if not video.exists():raise FileNotFoundError('Separately sourced research clips are required')
            window.select_card_source(0);started=time.monotonic();window.start_source(str(video),analyze=True)
            token=None;frames=0;usable=0;latencies=[];model=Counter();reflected=Counter();first=None;maxpreview=0
            while window.worker is not None and time.monotonic()-started<12:
                app.processEvents();time.sleep(.005)
                if window.worker:maxpreview=max(maxpreview,window.worker.frames)
                cue=window.session.cue
                if cue is not None and window.session.cue_received_at!=token:
                    token=window.session.cue_received_at;frames+=1;usable+=cue.status=='accepted';latencies.append(cue.elapsed_ms)
                    estimate=cue.model_estimate or {};model[estimate.get('label') or estimate.get('status','missing')]+=1
                    state=window.reflection.display(window.session)
                    reflected[state.title]+=1
                    if state.artwork and first is None:first=time.monotonic()-started
                    assert window.session.report is None and window.session.valence is None
                    assert window.latest_report['cma']['count']==0
            window.pause()
            row={'file':video.name,'sampled_results':frames,'usable_results':usable,'preview_frames':maxpreview,
                 'seconds_from_start_to_first_reflected_pose':round(first,3) if first else None,
                 'pipeline_ms_median':round(float(np.median(latencies)),2) if latencies else None,
                 'model_labels':dict(model),'reflected_labels':dict(reflected)}
            results.append(row);print(json.dumps(row),flush=True)
            assert maxpreview>10 and frames>0,'Video-to-native path failed'
        output={'fixture':'Nine existing RAVDESS acted clips: seven normal-intensity actor04 and two high-intensity actor01, realtime playback, no training; smoke evidence only',
                'captures':'Preview and inference run independently; actual landmarks, hands and HSE inference enabled',
                'cma_invented':False,'results':results,'limits':'Not target-webcam/gamer accuracy; no confusion/recall estimate from this smoke selection'}
        (ROOT/'artifacts/reflection-video-smoke.json').write_text(json.dumps(output,indent=2))
    finally:window.close();window.deleteLater();app.processEvents()


if __name__=='__main__':main()
