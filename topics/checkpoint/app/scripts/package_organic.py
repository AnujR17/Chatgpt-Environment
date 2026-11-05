"""Create a review bundle, retaining prior model artifacts and current native code."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib,json
ROOT=Path(__file__).resolve().parents[2];APP=ROOT/'checkpoint'
base=ROOT/'checkpoint-research-build.zip';out=ROOT/'checkpoint-organic-emotions-review.zip'
files={}
with ZipFile(base) as z:
    for item in z.infolist():
        if item.is_dir():continue
        current=ROOT/item.filename
        files[item.filename]=current.read_bytes() if current.is_file() else z.read(item.filename)
for folder in ['checkpoint','tests','scripts','docs','design']:
    for p in (APP/folder).rglob('*'):
        if not p.is_file() or '__pycache__' in p.parts:continue
        if p.suffix not in ['.py','.md','.json']:continue
        files[str(p.relative_to(ROOT))]=p.read_bytes()
for p in (APP/'artifacts').glob('organic-*'):
    if p.is_file():files[str(p.relative_to(ROOT))]=p.read_bytes()
for name in ['README.md','FINAL-HANDOFF.md','pyproject.toml']:
    p=APP/name;files[str(p.relative_to(ROOT))]=p.read_bytes()
for name in ['organic-family-state.json','organic-family-build.js','organic-family-notes.js','emotion-motion-helpers.js']:
    p=ROOT/'figma-design'/name;files[str(p.relative_to(ROOT))]=p.read_bytes()
manifest={name:hashlib.sha256(data).hexdigest() for name,data in files.items()}
files['checkpoint/review-manifest.json']=json.dumps(manifest,indent=2).encode()
with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=6) as z:
    for name,data in sorted(files.items()):z.writestr(name,data)
with ZipFile(out) as z:
    assert z.testzip() is None
    assert 'checkpoint/checkpoint/symbols.py' in z.namelist()
    assert 'checkpoint/artifacts/organic-emotion-motion.mp4' in z.namelist()
    assert hashlib.sha256(z.read('checkpoint/artifacts/expression.onnx')).hexdigest()=='b0e28051075f6f9ed200bbd9e510c451d2e05ceb3fab0d548cb5e9b3942da466'
result={'file':str(out),'files':len(files),'bytes':out.stat().st_size,'archive_integrity':'passed','model_hash_unchanged':True,'software_tests':23,'recognition_study':'not conducted'}
(APP/'artifacts/organic-review-bundle-verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
