"""Run the actual published repair against 0.4 source and a held-open Windows folder."""
from pathlib import Path
import base64
import ctypes
from ctypes import wintypes
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.request

APP=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(APP))
from checkpoint.updates import unpack

TAG='checkpoint-v0.6.1-preview.1'
BASE='https://github.com/AnujR17/Chatgpt-Environment/releases/download/'+TAG+'/'


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Checkpoint-repair-review'}),timeout=60) as response:return response.read()


def close_app(pid):
    user=ctypes.WinDLL('user32');callback=ctypes.WINFUNCTYPE(wintypes.BOOL,wintypes.HWND,wintypes.LPARAM)
    user.GetWindowThreadProcessId.argtypes=[wintypes.HWND,ctypes.POINTER(wintypes.DWORD)]
    user.PostMessageW.argtypes=[wintypes.HWND,wintypes.UINT,wintypes.WPARAM,wintypes.LPARAM]
    user.EnumWindows.argtypes=[callback,wintypes.LPARAM]
    def visit(hwnd,unused):
        owner=wintypes.DWORD();user.GetWindowThreadProcessId(hwnd,ctypes.byref(owner))
        if owner.value==pid:user.PostMessageW(hwnd,0x10,0,0)
        return True
    user.EnumWindows(callback(visit),0)


manifest=json.loads(get(BASE+'Checkpoint-update.json'))
release=json.loads(get('https://api.github.com/repos/AnujR17/Chatgpt-Environment/releases/tags/'+TAG))
assets={a['name']:a for a in release['assets']}
with tempfile.TemporaryDirectory(prefix='checkpoint-real-repair-') as directory:
    parent=Path(directory);root=parent/'Checkpoint-Windows';root.mkdir()
    full=parent/'full.zip';full.write_bytes(get(BASE+'Checkpoint-Windows-Preview.zip'))
    assert hashlib.sha256(full.read_bytes()).hexdigest()==manifest['full']['sha256']
    unpack(full,root,prefix='Checkpoint-Windows/')
    # Actual legacy application source, with the unchanged compatible vendor runtime.
    legacy=subprocess.check_output(['git','archive','b9e421b5548aa5371b00563966c0a8a0ffa1630f:topics/checkpoint/app/checkpoint'],cwd=APP.parents[2])
    shutil.rmtree(root/'checkpoint');(root/'checkpoint').mkdir()
    with tarfile.open(fileobj=io.BytesIO(legacy)) as archive:archive.extractall(root/'checkpoint',filter='data')
    assert '0.4.0' in (root/'checkpoint/version.py').read_text()
    repair=parent/'repair.zip';repair.write_bytes(get(BASE+'Checkpoint-Updater-Repair.zip'))
    assert 'sha256:'+hashlib.sha256(repair.read_bytes()).hexdigest()==assets['Checkpoint-Updater-Repair.zip']['digest']
    folder=parent/'repair';unpack(repair,folder)
    held=parent/'held.txt'
    locker=subprocess.Popen([sys.executable,'-c',"import os,sys,time;from pathlib import Path;os.chdir(sys.argv[1]);Path(sys.argv[2]).write_text('held');time.sleep(240)",str(root),str(held)],cwd=parent)
    live=[]
    try:
        deadline=time.monotonic()+10
        while not held.exists() and time.monotonic()<deadline:time.sleep(.1)
        assert held.exists()
        repaired=subprocess.run([str(root/'runtime/python.exe'),'-B',str(folder/'repair_update.py'),str(root)],cwd=folder,capture_output=True,text=True,timeout=100)
        assert repaired.returncode==0,(repaired.stdout,repaired.stderr)
        result=parent/'.checkpoint-updates/last-result.json';deadline=time.monotonic()+100;status={}
        while time.monotonic()<deadline:
            try:status=json.loads(result.read_text(encoding='utf-8-sig'))
            except (OSError,ValueError):pass
            if status.get('status') in ('applied','failed'):break
            time.sleep(.2)
        assert status.get('status')=='applied',status
        startup=json.loads((root/'.checkpoint-startup.json').read_text());live.append(startup['pid'])
        assert startup['tag']==TAG
        close_app(startup['pid']);time.sleep(1)
        (root/'.checkpoint-startup.json').unlink()
        launched=subprocess.run(['cmd.exe','/c',str(root/'Start Checkpoint.cmd')],cwd=parent,capture_output=True,text=True,timeout=15)
        assert launched.returncode==0,(launched.stdout,launched.stderr)
        deadline=time.monotonic()+30
        while not (root/'.checkpoint-startup.json').exists() and time.monotonic()<deadline:time.sleep(.1)
        normal=json.loads((root/'.checkpoint-startup.json').read_text());live.append(normal['pid'])
        assert normal['tag']==TAG,'Original launcher reverted to the old version'
        output={'published_tag':TAG,'actual_legacy_source':'0.4.0-preview.2','published_repair_package':'hash and execution passed',
                'held_open_installation_folder':'repair passed','actual_qt_startup':'passed','original_cmd_reopen_stays_updated':'passed',
                'runtime_download_by_repair':'none; existing compatible runtime reused',
                'fixture':'Disposable Windows installation, no personal install changed'}
        (APP/'artifacts/windows-repair-bridge.json').write_text(json.dumps(output,indent=2))
        print(json.dumps(output))
    finally:
        for pid in live:close_app(pid)
        time.sleep(1);locker.terminate();locker.wait(timeout=10)
