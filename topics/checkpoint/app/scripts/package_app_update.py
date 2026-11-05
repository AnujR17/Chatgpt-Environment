"""Publish a small app payload alongside the full runtime fallback and its manifest."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json
from checkpoint.version import APP_VERSION,RELEASE_TAG
from checkpoint.updates import digest,runtime_fingerprint,app_path

ROOT=Path(__file__).resolve().parents[1]
APP=ROOT/'build/Checkpoint-Windows'
OUT=ROOT.parent
payload=OUT/'Checkpoint-App-Update.zip'
paths=[p for p in APP.rglob('*') if p.is_file() and '__pycache__' not in p.parts and app_path(str(p.relative_to(APP)).replace('\\','/'))]
files={str(p.relative_to(APP)).replace('\\','/'):digest(p) for p in paths}
with ZipFile(payload,'w',ZIP_DEFLATED,compresslevel=6) as z:
    for p in paths:z.write(p,str(p.relative_to(APP)).replace('\\','/'))
full=OUT/'Checkpoint-Windows-Preview.zip'
manifest={'protocol':1,'version':APP_VERSION,'tag':RELEASE_TAG,
 'runtime':runtime_fingerprint(json.loads((APP/'runtime-sources.json').read_text())),
 'models':{str(p.relative_to(APP)).replace('\\','/'):digest(p) for p in (APP/'artifacts').iterdir() if p.suffix in ('.onnx','.task')},
 'app':{'name':payload.name,'bytes':payload.stat().st_size,'sha256':digest(payload),'files':files},
 'full':{'name':full.name,'bytes':full.stat().st_size,'sha256':digest(full)}}
(OUT/'Checkpoint-update.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
print(json.dumps({'app_bytes':payload.stat().st_size,'app_files':len(files),'full_bytes':full.stat().st_size,'tag':RELEASE_TAG}))
