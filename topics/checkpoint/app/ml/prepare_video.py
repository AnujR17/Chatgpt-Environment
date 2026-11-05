"""Fetch official CC BY-NC-SA RAVDESS videos for external research evaluation."""
import concurrent.futures
import hashlib
import json
import shutil
import zipfile
from pathlib import Path
import requests
from ml.prepare import ROOT, download, sha256


def prepare(actors=(1, 2, 3, 4)):
    response = requests.get("https://zenodo.org/api/records/1188976", timeout=40)
    response.raise_for_status(); record = response.json()
    license_id = record["metadata"]["license"]["id"]
    if license_id != "cc-by-nc-sa-4.0": raise ValueError("Dataset licence changed; review before use")
    (ROOT / "data" / "ravdess-metadata.json").write_text(json.dumps(record,indent=2))
    wanted = [f"Video_Speech_Actor_{actor:02d}.zip" for actor in actors]
    sources = [f for f in record["files"] if f["key"] in wanted]
    if len(sources) != len(wanted): raise ValueError("Missing actor archive")
    def get(source):
        path = download(source["links"]["self"], ROOT/"data"/source["key"], max_bytes=650_000_000)
        if path.stat().st_size != source["size"]: raise ValueError("Archive size mismatch")
        checksum = hashlib.md5(path.read_bytes()).hexdigest()
        if source["checksum"] != "md5:"+checksum: raise ValueError("Official archive checksum mismatch")
        clips=[]
        with zipfile.ZipFile(path) as archive:
            for name in archive.namelist():
                leaf=Path(name).name
                if not leaf.endswith(".mp4") or not leaf.startswith("02-01-"): continue
                fields=leaf[:-4].split("-")
                if len(fields)!=7 or not all(x.isdigit() for x in fields): continue
                if archive.getinfo(name).file_size > 50_000_000: raise ValueError("Unexpected video member size")
                target=ROOT/"data"/"videos"/leaf
                target.parent.mkdir(exist_ok=True)
                if not target.exists():
                    with archive.open(name) as src, target.open("wb") as dst: shutil.copyfileobj(src,dst)
                clips.append({"file":leaf,"actor":int(fields[-1]),"emotion_id":int(fields[2]),"intensity":int(fields[3]),"sha256":sha256(target)})
        print(json.dumps({"archive":source["key"],"video_only_clips":len(clips)}),flush=True)
        return {"key":source["key"],"url":source["links"]["self"],"checksum":source["checksum"],"sha256":sha256(path),"clips":clips}
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        archives=list(pool.map(get,sources))
    manifest={"dataset":"RAVDESS / video-only emotional speech","source":"https://zenodo.org/records/1188976","license":license_id,
      "authors":"Steven R. Livingstone and Frank A. Russo (2018)","doi":"10.1371/journal.pone.0196391",
      "actors":list(actors),"usage":"Held-out external evaluation only; never training or threshold selection", "archives":archives,
      "limitations":["Acted recording-level emotion labels, not frame-level expressions or gamer mood","Four actors do not establish demographic fairness or Indian-context validity","Calm has no separate FER+ class and is excluded, never silently mapped to neutral","Confidence threshold calibrated on FER+ may not transfer to video"]}
    (ROOT/"data"/"video-manifest.json").write_text(json.dumps(manifest,indent=2))
    print(json.dumps({"ready":True,"clips":sum(len(x["clips"]) for x in archives)}),flush=True)


if __name__=="__main__": prepare()
