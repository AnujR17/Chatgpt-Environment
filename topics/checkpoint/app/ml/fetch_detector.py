"""Download only the public, hash-verified YuNet face detector, not expression weights."""
import json
from ml.prepare import ROOT, download, sha256

URL = "https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx"
HASH = "8f2383e4dd3cfbb4553ea8718107fc0423210dc964f9f4280604804ed2552fa4"

if __name__ == "__main__":
    p=download(URL,ROOT/"artifacts"/"yunet.onnx",max_bytes=1_000_000)
    if sha256(p)!=HASH: raise ValueError("YuNet checksum mismatch")
    (ROOT/"artifacts"/"detector-provenance.json").write_text(json.dumps({"source":URL,"sha256":HASH,"license":"MIT","purpose":"Face localisation only; no identity recognition"},indent=2))
