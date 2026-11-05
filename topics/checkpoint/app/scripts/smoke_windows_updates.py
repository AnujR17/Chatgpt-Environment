"""Run the real Windows restart/rollback helper against disposable installations.
No camera, network, real update installation, or Windows firewall changes.
"""
from pathlib import Path
import base64
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from checkpoint.updates import APPLY_SCRIPT
from checkpoint.version import RELEASE_TAG

ROOT=Path(__file__).resolve().parents[1]
RUNTIME=ROOT/'build/Checkpoint-Windows/runtime'


def link_or_copy(src,dst):
    try:os.link(src,dst);return dst
    except OSError:return shutil.copy2(src,dst)


def run_fixture(base,fail=False):
    parent=base/('failure' if fail else 'success');root=parent/'Checkpoint test folder';stage=parent/'.checkpoint-updates/job/prepared';stage.mkdir(parents=True);root.mkdir(parents=True)
    for target in (root,stage):
        shutil.copytree(RUNTIME,target/'runtime',copy_function=link_or_copy,ignore=shutil.ignore_patterns('__pycache__'))
        (target/'checkpoint').mkdir()
    (root/'checkpoint/version.txt').write_text('previous')
    (root/'launch.py').write_text("from pathlib import Path\nPath(__file__).with_name('recovered.ok').write_text('previous app restarted')\n")
    (stage/'checkpoint/version.txt').write_text('updated')
    script="raise SystemExit(2)\n" if fail else """import os,json
from pathlib import Path
job=Path(os.environ['CHECKPOINT_UPDATE_JOB']);config=json.loads(job.read_text(encoding='utf8'))
(job.parent/'ready.json').write_text(json.dumps({'tag':config['tag']}),encoding='utf8')
Path(__file__).with_name('restarted.ok').write_text('updated app restarted')
"""
    (stage/'launch.py').write_text(script)
    dead=subprocess.Popen([sys.executable,'-c','pass']);dead.wait()
    config={'original':str(root),'staged':str(stage),'backup':str(parent/'.checkpoint-backups/previous/app'),'pid':dead.pid,'tag':RELEASE_TAG}
    job=stage.parent/'job.json';job.write_text(json.dumps(config),encoding='utf8')
    encoded=base64.b64encode(APPLY_SCRIPT.encode('utf-16le')).decode('ascii')
    result=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-EncodedCommand',encoded],cwd=parent,env=dict(os.environ,CHECKPOINT_UPDATE_JOB=str(job)),capture_output=True,text=True,timeout=65)
    state=json.loads((parent/'.checkpoint-updates/last-result.json').read_text(encoding='utf-8-sig'))
    if fail:
        assert result.returncode==1 and state['status']=='failed',(result.stdout,result.stderr,state)
        assert (root/'checkpoint/version.txt').read_text()=='previous'
        deadline=time.monotonic()+5
        while not (root/'recovered.ok').exists() and time.monotonic()<deadline:time.sleep(.1)
        assert (root/'recovered.ok').exists(),'Previous installation did not restart after rollback'
    else:
        assert result.returncode==0 and state['status']=='applied',(result.stdout,result.stderr,state)
        assert (root/'restarted.ok').exists() and (root/'checkpoint/version.txt').read_text()=='updated'
        assert (Path(config['backup'])/'checkpoint/version.txt').read_text()=='previous'
    return 'passed'


with tempfile.TemporaryDirectory(prefix='checkpoint-update-') as folder:
    base=Path(folder)
    success=run_fixture(base);rollback=run_fixture(base,fail=True)
result={'windows_restart_swap_fixture':success,'windows_failed_start_rollback_fixture':rollback,
        'fixture':'Disposable installations, actual embedded Python and PowerShell helper; no personal install modified',
        'user_network_and_physical_device':'not tested'}
(ROOT/'artifacts/windows-updater-smoke.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
