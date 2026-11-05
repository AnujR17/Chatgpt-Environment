"""Prepare FER+ with documented provenance and conservative split deduplication.

Images: FER2013 mirror. Annotations: Microsoft FER+. No arbitrary face scraping.
The mirror's MIT label does not independently establish image rights. Research only.
"""
import argparse
import csv
import hashlib
import io
import json
import zipfile
from pathlib import Path
import numpy as np
import requests

ROOT = Path(__file__).resolve().parents[1]
LABELS = ["neutral", "happiness", "surprise", "sadness", "anger", "disgust", "fear", "contempt"]
IMAGE_REVISION = "4ad26b38d1dcc1c3891d841a48758653b6c67105"
IMAGE_SHA256 = "0cef395bbf67f80b8968362818f7fe00ddc1d6604b5f79795ca263e656d937cb"
ANNOTATION_SHA256 = "9206e20d62f56475939f516847d61753e4860caeac9718b560129541b776fc2c"


def download(url, path, max_bytes=700_000_000):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return path
    temp = path.with_suffix(path.suffix + ".part")
    size = 0
    with requests.get(url, stream=True, timeout=(20, 90)) as response:
        response.raise_for_status()
        with temp.open("wb") as stream:
            for chunk in response.iter_content(1024 * 1024):
                size += len(chunk)
                if size > max_bytes:
                    raise ValueError("Download exceeds declared size budget")
                stream.write(chunk)
    temp.replace(path)
    print(json.dumps({"downloaded": str(path), "bytes": size}), flush=True)
    return path


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for b in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def prepare():
    data = ROOT / "data"
    data.mkdir(exist_ok=True)
    revision = IMAGE_REVISION
    image_url = f"https://huggingface.co/datasets/chitradrishti/fer2013/resolve/{revision}/fer2013.csv.zip"
    label_url = "https://raw.githubusercontent.com/microsoft/FERPlus/master/fer2013new.csv"
    image_archive = download(image_url, data / "fer2013.csv.zip")
    annotations = download(label_url, data / "fer2013new.csv", max_bytes=5_000_000)
    if sha256(image_archive)!=IMAGE_SHA256 or sha256(annotations)!=ANNOTATION_SHA256:
        raise ValueError("Pinned dataset content changed; review rather than train on misaligned labels")
    with zipfile.ZipFile(image_archive) as archive:
        candidates = [n for n in archive.namelist() if n.endswith("fer2013.csv")]
        if len(candidates) != 1:
            raise ValueError(f"Expected exactly one fer2013.csv, found {candidates}")
        original = list(csv.DictReader(io.StringIO(archive.read(candidates[0]).decode("utf-8-sig"))))
    plus = list(csv.DictReader(annotations.open(encoding="utf-8-sig")))
    if len(original) != len(plus) or len(original) != 35887:
        raise ValueError(f"Unexpected FER/FER+ row counts {len(original)}, {len(plus)}")
    images, targets, usage, row_ids, hashes, signatures = [], [], [], [], [], []
    exclusions = {"non_face_unknown_or_ambiguous": 0}
    for idx, (raw, vote) in enumerate(zip(original, plus)):
        if raw["Usage"].strip() != vote["Usage"].strip():
            raise ValueError(f"Usage alignment failure at original row {idx}")
        votes = np.array([float(vote[k]) for k in LABELS], dtype=np.float32)
        unknown = float(vote["unknown"]) + float(vote["NF"])
        # Require emotion majority and an unambiguous plurality, never fabricate a label.
        if votes.sum() < 6 or unknown >= votes.max() or (votes == votes.max()).sum() != 1:
            exclusions["non_face_unknown_or_ambiguous"] += 1
            continue
        image = np.fromstring(raw["pixels"], sep=" ", dtype=np.uint8)
        if image.size != 2304:
            raise ValueError(f"Malformed pixel array at {idx}")
        image = image.reshape(48, 48)
        images.append(image)
        targets.append(votes / votes.sum())
        usage.append(raw["Usage"].strip())
        row_ids.append(idx)
        hashes.append(hashlib.sha256(image.tobytes()).hexdigest())
        # Coarse 16x16 signatures catch near-identical compression variants, not identities.
        small = image.reshape(16, 3, 16, 3).mean(axis=(1, 3))
        signatures.append(hashlib.sha256((small / 8).astype(np.uint8).tobytes()).hexdigest())
    images, targets = np.array(images), np.array(targets)
    usage, row_ids, hashes, signatures = map(np.array, (usage, row_ids, hashes, signatures))
    seen_hash, seen_sig = set(), set()
    splits = {}
    removed = {}
    # Preserve held-out test first, validation second; remove leaked images from training.
    for name, value in [("test", "PrivateTest"), ("valid", "PublicTest"), ("train", "Training")]:
        accepted = []
        removed[name] = 0
        for i in np.flatnonzero(usage == value):
            if hashes[i] in seen_hash or signatures[i] in seen_sig:
                removed[name] += 1
                continue
            accepted.append(i)
            seen_hash.add(hashes[i]); seen_sig.add(signatures[i])
        ix = np.array(accepted, dtype=np.int64)
        np.savez_compressed(data / f"{name}.npz", images=images[ix], targets=targets[ix], row_ids=row_ids[ix], hashes=hashes[ix])
        splits[name] = {"samples": len(ix), "class_counts": np.bincount(targets[ix].argmax(1), minlength=8).tolist()}
    manifest = {
        "dataset": "FER2013 images / FER+ vote distributions",
        "image_source": image_url, "image_revision": revision, "image_archive_sha256": sha256(image_archive),
        "annotation_source": label_url, "annotation_sha256": sha256(annotations),
        "labels": LABELS, "splits": splits, "excluded": exclusions, "deduplicated": removed,
        "eligibility": "At least six emotion votes; unique plurality; unknown+NF below top emotion count",
        "deduplication": "Exact pixel SHA256 and quantized 16x16 signature; does not establish subject disjointness",
        "identity_ids_available": False,
        "limitations": ["Web-sourced faces; subject independence cannot be verified", "No gamer/CMA/frustration labels", "No reliable demographic or Indian-context evaluation labels", "Image rights require review before production/distribution; mirror MIT metadata alone is insufficient"],
    }
    (data / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(json.dumps(manifest, indent=2), flush=True)


if __name__ == "__main__":
    prepare()
