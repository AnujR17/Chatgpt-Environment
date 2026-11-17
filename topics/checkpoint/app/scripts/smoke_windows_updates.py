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
import ctypes
from ctypes import wintypes
from checkpoint.updates import APPLY_SCRIPT
from checkpoint.version import RELEASE_TAG

ROOT=Path(__file__).resolve().parents[1]
RUNTIME=ROOT/'build/Checkpoint-Windows/runtime'


def link_or_copy(src,dst):
    try:os.link(src,dst);return dst
    except OSError:return shutil.copy2(src,dst)


def run_fixture(base,fail=False,kind="full"):
    parent=base/(kind+('-failure' if fail else '-success'));root=parent/'Checkpoint test folder';stage=parent/'.checkpoint-updates/job/prepared';stage.mkdir(parents=True);root.mkdir(parents=True)
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
    config={'original':str(root),'staged':str(stage),'backup':str(parent/'.checkpoint-backups/previous/app'),'pid':dead.pid,'tag':RELEASE_TAG,'kind':kind,'components':['checkpoint','launch.py'] if kind=='app' else []}
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


def close_window_process(pid):
    """Close only the actual app created by this disposable fixture."""
    user=ctypes.WinDLL('user32');callback=ctypes.WINFUNCTYPE(wintypes.BOOL,wintypes.HWND,wintypes.LPARAM)
    user.GetWindowThreadProcessId.argtypes=[wintypes.HWND,ctypes.POINTER(wintypes.DWORD)]
    user.PostMessageW.argtypes=[wintypes.HWND,wintypes.UINT,wintypes.WPARAM,wintypes.LPARAM]
    user.EnumWindows.argtypes=[callback,wintypes.LPARAM]
    def visit(hwnd,unused):
        process=wintypes.DWORD();user.GetWindowThreadProcessId(hwnd,ctypes.byref(process))
        if process.value==pid:user.PostMessageW(hwnd,0x10,0,0)
        return True
    user.EnumWindows(callback(visit),0)


def real_app_locked_directory_fixture(base):
    parent=base/'actual-gui';parent.mkdir();root=parent/'Checkpoint stable folder'
    stage=parent/'.checkpoint-updates/actual/prepared';source=ROOT/'build/Checkpoint-Windows'
    def copy(src,dst):
        return link_or_copy(src,dst) if Path(src).is_relative_to(source/'runtime') else shutil.copy2(src,dst)
    shutil.copytree(source,root,copy_function=copy,ignore=shutil.ignore_patterns('__pycache__'))
    shutil.copytree(source,stage,copy_function=copy,ignore=shutil.ignore_patterns('__pycache__'))
    (root/'checkpoint/version.py').write_text("APP_VERSION='0.4.0'\nRELEASE_TAG='checkpoint-v0.4.0-preview.2'\n")
    (root/'launch.py').write_text("from pathlib import Path\nPath(__file__).with_name('old-restarted.txt').write_text('old')\n")
    ready=parent/'directory-held.txt'
    hold="import os,sys,time;from pathlib import Path;os.chdir(sys.argv[1]);Path(sys.argv[2]).write_text('held');time.sleep(180)"
    holder=subprocess.Popen([str(RUNTIME/'python.exe'),'-c',hold,str(root),str(ready)],cwd=parent)
    new_pid=None;reopened=None
    try:
        deadline=time.monotonic()+15
        while not ready.exists() and time.monotonic()<deadline:time.sleep(.1)
        assert ready.exists()
        # This reproduces the reported sharing violation in the legacy whole-folder swap.
        legacy="$ErrorActionPreference='Stop'; Move-Item -LiteralPath $env:CHECKPOINT_LOCK_ROOT -Destination $env:CHECKPOINT_LOCK_DEST"
        encoded=base64.b64encode(legacy.encode('utf-16le')).decode('ascii')
        old_result=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-EncodedCommand',encoded],
          env=dict(os.environ,CHECKPOINT_LOCK_ROOT=str(root),CHECKPOINT_LOCK_DEST=str(parent/'legacy-moved')),capture_output=True,text=True,timeout=15)
        assert old_result.returncode!=0 and root.exists(),'Legacy directory lock was not reproduced'
        old_runtime=(root/'runtime/pythonw.exe').stat()
        dead=subprocess.Popen([sys.executable,'-c','pass']);dead.wait()
        job=stage.parent/'job.json';backup=parent/'.checkpoint-backups/old/app'
        job.write_text(json.dumps({'original':str(root),'staged':str(stage),'backup':str(backup),'pid':dead.pid,
            'tag':RELEASE_TAG,'kind':'app','components':['checkpoint','launch.py']}),encoding='utf8')
        encoded=base64.b64encode(APPLY_SCRIPT.encode('utf-16le')).decode('ascii')
        applied=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-EncodedCommand',encoded],
            env=dict(os.environ,CHECKPOINT_UPDATE_JOB=str(job)),cwd=parent,capture_output=True,text=True,timeout=130)
        status=json.loads((parent/'.checkpoint-updates/last-result.json').read_text(encoding='utf-8-sig'))
        assert applied.returncode==0 and status['status']=='applied',(applied.stdout,applied.stderr,status)
        receipt=json.loads((job.parent/'ready.json').read_text());new_pid=receipt['pid']
        assert receipt['tag']==RELEASE_TAG and (root/'runtime/pythonw.exe').stat().st_ino==old_runtime.st_ino
        assert (backup/'checkpoint/version.py').read_text().find('0.4.0')>=0
        close_window_process(new_pid);time.sleep(1)
        startup=root/'.checkpoint-startup.json';startup.unlink(missing_ok=True)
        env=dict(os.environ);env.pop('CHECKPOINT_UPDATE_JOB',None)
        reopened=subprocess.Popen([str(root/'runtime/pythonw.exe'),str(root/'launch.py'),'--no-setup'],cwd=parent,env=env)
        deadline=time.monotonic()+30
        while not startup.exists() and time.monotonic()<deadline:time.sleep(.1)
        identity=json.loads(startup.read_text())
        assert identity['tag']==RELEASE_TAG and identity['pid']==reopened.pid,'Normal reopening reverted the version'
        return {'legacy_root_rename_lock':'reproduced','actual_qt_update_startup':'passed',
                'runtime_and_root_preserved':'passed','normal_reopen_stays_updated':'passed'}
    finally:
        if new_pid:close_window_process(new_pid)
        if reopened:
            close_window_process(reopened.pid)
            try:reopened.wait(timeout=10)
            except subprocess.TimeoutExpired:reopened.terminate();reopened.wait(timeout=10)
        holder.terminate();holder.wait(timeout=10)


with tempfile.TemporaryDirectory(prefix='checkpoint-update-') as folder:
    base=Path(folder)
    success=run_fixture(base);rollback=run_fixture(base,fail=True)
    app_success=run_fixture(base,kind='app');app_rollback=run_fixture(base,fail=True,kind='app')
    locked=real_app_locked_directory_fixture(base)
result={'windows_restart_swap_fixture':success,'windows_failed_start_rollback_fixture':rollback,
        'real_app_locked_install_directory':locked,'windows_component_update':app_success,'windows_component_rollback':app_rollback,
        'fixture':'Disposable installations, actual embedded Python and PowerShell helper; no personal install modified',
        'user_network_and_physical_device':'not tested'}
(ROOT/'artifacts/windows-updater-smoke.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
