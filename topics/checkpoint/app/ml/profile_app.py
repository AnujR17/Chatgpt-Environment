"""Measure this native app locally; no browser/game or battery superiority claim."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import psutil
from ml.prepare import ROOT


def profile(args):
    env=os.environ.copy();env['QT_QPA_PLATFORM']='offscreen';env['XDG_CACHE_HOME']=str(ROOT/'.cache')
    command=[sys.executable,'-m','checkpoint.app','--no-setup']
    if args.video:command+=['--video',args.video,'--analyze']
    proc=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True);process=psutil.Process(proc.pid)
    samples=[]
    try:
        time.sleep(2);process.cpu_percent(None)
        for _ in range(6):
            cpu=process.cpu_percent(interval=.5);samples.append({'cpu_percent_one_core_basis':cpu,'rss_mb':process.memory_info().rss/1024**2})
        proc.terminate();_,stderr=proc.communicate(timeout=10)
    finally:
        if proc.poll() is None:proc.kill();proc.wait()
    out={'mode':'file playback and experimental analysis' if args.video else 'manual idle','samples':samples,'mean_cpu_percent_one_core_basis':sum(s['cpu_percent_one_core_basis'] for s in samples)/len(samples),'peak_rss_mb':max(s['rss_mb'] for s in samples),'display':'Qt offscreen software rendering','inference_hz':2,'limitations':['Short local observation, not a game-impact or energy benchmark','Video may finish before the final sample; individual observations are retained','No physical camera, GPU, battery or browser comparison'],'stderr':stderr[-2000:]}
    path=ROOT/'artifacts'/('app-profile-video.json' if args.video else 'app-profile-idle.json');path.write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--video');profile(parser.parse_args())
