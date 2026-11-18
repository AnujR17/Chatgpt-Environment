"""Assemble a portable Windows x64 app using official embedded Python and wheels.
This builds a Windows distribution on Linux; it does not claim Windows execution.
"""
from pathlib import Path
from zipfile import ZipFile
from shutil import copytree,copyfile
import json,hashlib,struct,sys
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'build/Checkpoint-Windows';RUNTIME=OUT/'runtime';SITE=RUNTIME/'Lib/site-packages'
RUNTIME.mkdir(parents=True,exist_ok=True);SITE.mkdir(parents=True,exist_ok=True)
with ZipFile(ROOT/'build/windows-runtime/python-embed.zip') as z:z.extractall(RUNTIME)
for wheel in sorted((ROOT/'build/windows-wheels').glob('*.whl')):
    with ZipFile(wheel) as z:
        for info in z.infolist():
            parts=Path(info.filename).parts
            if '..' in parts or info.filename.startswith('/'):raise ValueError('Unsafe archive path')
            if '.data' in parts[0] and len(parts)>2:
                if parts[1] not in ('purelib','platlib'):continue
                relative=Path(*parts[2:])
            else:relative=Path(info.filename)
            if info.is_dir():continue
            target=SITE/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(z.read(info))
version=json.loads((ROOT/'build/windows-runtime/source.json').read_text())['version'];tag=''.join(version.split('.')[:2])
(RUNTIME/f'python{tag}._pth').write_text(f'python{tag}.zip\n.\nLib\\site-packages\n..\nimport site\n')
# Make common C runtime imports available before loading numerical extensions.
for dll in (SITE/'PySide6').glob('*140*.dll'):copyfile(dll,RUNTIME/dll.name)
copytree(ROOT/'checkpoint',OUT/'checkpoint',dirs_exist_ok=True,ignore=lambda d,n:[x for x in n if x=='__pycache__'])
(OUT/'artifacts').mkdir(exist_ok=True)
for name in ['expression.onnx','calibration.json','yunet.onnx','release-gates.json','MODEL-CARD.md','face_landmarker.task','face-landmarker-provenance.json','hsemotion-afew.onnx','hsemotion-provenance.json','game-scene-model.json','game-scene-training.json','pretrained-comparison.json','hand-landmarker-provenance.json']:
    copyfile(ROOT/'artifacts'/name,OUT/'artifacts'/name)
copytree(ROOT/'third_party',OUT/'third_party',dirs_exist_ok=True)
(OUT/'launch.py').write_text('''import os,sys,ctypes,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parent
handles=[]
for folder in [ROOT/'runtime',ROOT/'runtime/Lib/site-packages/PySide6',ROOT/'runtime/Lib/site-packages/onnxruntime/capi',ROOT/'runtime/Lib/site-packages/cv2']:
    if folder.exists():handles.append(os.add_dll_directory(str(folder)))
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH']=str(ROOT/'runtime/Lib/site-packages/PySide6/plugins/platforms')
try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('Checkpoint.Companion.Preview')
    from checkpoint.app import main
    raise SystemExit(main())
except Exception:
    folder=Path(os.environ.get('LOCALAPPDATA',str(ROOT)))/'CheckpointResearch/Checkpoint'
    folder.mkdir(parents=True,exist_ok=True);log=folder/'startup-error.log';log.write_text(traceback.format_exc())
    ctypes.windll.user32.MessageBoxW(None,'Checkpoint could not start. A diagnostic log is saved at:\\n'+str(log),'Checkpoint',16)
''',encoding='utf8')
(OUT/'Start Checkpoint.cmd').write_bytes(b'@echo off\r\ncd /d "%~dp0"\r\nstart "" "%~dp0runtime\\pythonw.exe" "%~dp0launch.py"\r\n')
(OUT/'Check setup.cmd').write_bytes(b'@echo off\r\ncd /d "%~dp0"\r\n"%~dp0runtime\\python.exe" "%~dp0check_setup.py"\r\npause\r\n')
(OUT/'check_setup.py').write_text('''import sys,platform
print('Python:',sys.version)
print('Platform:',platform.platform())
import PySide6,numpy,cv2,onnxruntime,psutil
from PySide6.QtWidgets import QApplication
from checkpoint.app import create_application,MainWindow
app=create_application([]);w=MainWindow(no_setup=True);w.show()
print('Native window created. Close it to finish this check.')
app.exec()
print('Setup check completed.')
''')
(OUT/'READ ME FIRST.txt').write_text('Regen with Nori - Windows 10/11 x64\n\n1. Extract the entire ZIP and open Checkpoint-Windows.\n2. Double-click Start Checkpoint.cmd.\n3. Choose Start play support, then switch to the game.\n\nNori gives a short reminder after about 2½ minutes of active play and after a\npossible fall in Getting Over It. Use borderless or windowed play for the overlay.\nCamera is optional. Reminders pause when you switch away from the game.\n\nReminders: mute or unmute. Ctrl+Alt+F8: I fell. Ctrl+Alt+F9: mute reminders.\nHold Ctrl+Alt to move Nori. Phone pairs a display over the same trusted Wi-Fi.\nYour check-in supplies CMA; camera estimates are a separate source.\n\nFuture updates: Settings > Check for updates > Update and restart.\nKeep runtime, checkpoint and artifacts beside the launcher. No separate Python\ninstallation is required. For startup diagnostics, run Check setup.cmd.\n\nRuntime: official Python embedded distribution and PyPI wheels. Third-party\nlicenses are retained in runtime and package metadata. PySide6/Qt is dynamically\nlinked and replaceable. App source is in checkpoint/. Qt/PySide source:\nhttps://code.qt.io/cgit/pyside/pyside-setup.git/\nhttps://code.qt.io/cgit/qt/\n',encoding='utf8')

# Validate machine code, imports present, plugin, provenance and trained model hash.
def amd64(path):
    data=path.read_bytes();assert data[:2]==b'MZ';offset=struct.unpack_from('<I',data,0x3c)[0];assert data[offset:offset+4]==b'PE\0\0';assert struct.unpack_from('<H',data,offset+4)[0]==0x8664
for relative in ['python.exe','pythonw.exe',f'python{tag}.dll','Lib/site-packages/PySide6/Qt6Core.dll','Lib/site-packages/PySide6/plugins/platforms/qwindows.dll']:
    amd64(RUNTIME/relative)
assert hashlib.sha256((OUT/'artifacts/expression.onnx').read_bytes()).hexdigest()=='b0e28051075f6f9ed200bbd9e510c451d2e05ceb3fab0d548cb5e9b3942da466'
for name,provenance in [('face_landmarker.task','face-landmarker-provenance.json'),('hsemotion-afew.onnx','hsemotion-provenance.json')]:
    expected=json.loads((ROOT/'artifacts'/provenance).read_text())['sha256']
    assert hashlib.sha256((OUT/'artifacts'/name).read_bytes()).hexdigest()==expected
sources={'python':json.loads((ROOT/'build/windows-runtime/source.json').read_text()),'wheels':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'build/windows-wheels').glob('*.whl')}}
(OUT/'runtime-sources.json').write_text(json.dumps(sources,indent=2))
result={'directory':str(OUT),'python':version,'windows_x64_pe_headers':'passed','qt_windows_platform_plugin':'present','vc_runtime':'bundled from official Qt/Python distributions','assembly_platform':sys.platform,'native_windows_execution':'See separate Windows fixture checks','bytes':sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file())}
(ROOT/'artifacts/windows-assembly-verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
