"""Synchronise the verified Windows runtime with the final app and make a portable ZIP."""
from pathlib import Path
from shutil import copytree,copyfile
from zipfile import ZipFile,ZIP_DEFLATED
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];APP=ROOT/'build/Checkpoint-Windows';OUT=ROOT.parent/'Checkpoint-Windows-Preview.zip'
copytree(ROOT/'checkpoint',APP/'checkpoint',dirs_exist_ok=True,ignore=lambda d,n:[v for v in n if v=='__pycache__'])
(APP/'docs').mkdir(exist_ok=True)
for p in ['MODEL-CARD.md','release-gates.json']:copyfile(ROOT/'artifacts'/p,APP/'artifacts'/p)
# Exact source and runtime provenance are shipped for review, without training images or reference downloads.
manifest={str(p.relative_to(APP)):hashlib.sha256(p.read_bytes()).hexdigest() for p in APP.rglob('*') if p.is_file() and p.name!='application-manifest.json'}
(APP/'application-manifest.json').write_text(json.dumps(manifest,indent=2))
with ZipFile(OUT,'w',ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(APP.rglob('*')):
        if p.is_file():z.write(p,'Checkpoint-Windows/'+str(p.relative_to(APP)))
with ZipFile(OUT) as z:
    assert z.testzip() is None
    for name in ['Start Checkpoint.cmd','launch.py','runtime/pythonw.exe','runtime/python313.dll','runtime/Lib/site-packages/PySide6/plugins/platforms/qwindows.dll','checkpoint/vocabulary.py']:
        assert 'Checkpoint-Windows/'+name in z.namelist()
    assert hashlib.sha256(z.read('Checkpoint-Windows/artifacts/expression.onnx')).hexdigest()=='b0e28051075f6f9ed200bbd9e510c451d2e05ceb3fab0d548cb5e9b3942da466'
report={'file':str(OUT),'bytes':OUT.stat().st_size,'files':len(manifest)+1,'archive_integrity':'passed','runtime':'official Windows x64 embedded Python 3.13.17 and matching Windows wheels','app_tests':'see cards-app-tests.xml; run in Linux','windows_execution':'not verified in this Linux workspace','model_hash_unchanged':True}
(ROOT/'artifacts/windows-package-verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
