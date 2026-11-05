"""One frozen-model evaluation on PrivateTest; thresholds were chosen on PublicTest."""
import json
import time
import cv2
import numpy as np
from checkpoint.runtime import ExpressionModel, preprocess, LABELS
from ml.prepare import ROOT, sha256
from ml.metrics import score


def run():
    out=ROOT/"artifacts";model=ExpressionModel(out);test=np.load(ROOT/"data"/"test.npz",allow_pickle=False)
    images=test["images"];y=test["targets"].argmax(1)
    def predict(imgs):
        return np.concatenate([model.probabilities(imgs[i:i+256,None].astype(np.float32)/127.5-1) for i in range(0,len(imgs),256)])
    started=time.perf_counter();probs=predict(images)
    result=score(y,probs,list(LABELS),model.threshold)
    result.update({"dataset":"FER+ / original FER2013 PrivateTest / eligible deduplicated rows","model_sha256":sha256(out/"expression.onnx"),"calibration_sha256":sha256(out/"calibration.json"),"temperature":model.temperature,"evaluation_seconds":time.perf_counter()-started,"test_used_for_training_or_threshold_selection":False})
    manifest=json.loads((ROOT/"data"/"manifest.json").read_text());majority=int(np.argmax(manifest["splits"]["train"]["class_counts"]));result["training_majority_baseline_accuracy"]=float((y==majority).mean())
    # Predeclared stress conditions, reported separately; no retuning on these results.
    rng=np.random.default_rng(1729);ix=np.sort(rng.choice(len(images),min(512,len(images)),replace=False));sample=images[ix]
    conditions={"dim_light":(sample.astype(float)*.45).astype(np.uint8),"blur":np.array([cv2.GaussianBlur(x,(7,7),2) for x in sample])}
    occluded=sample.copy();occluded[:,30:,:]=127;conditions["lower_face_occlusion"]=occluded
    result["stress_tests"]={}
    for key,imgs in conditions.items():
        condition=predict(imgs);result["stress_tests"][key]=score(y[ix],condition,list(LABELS),model.threshold,bootstraps=200)
    np.savez_compressed(out/"image-predictions.npz",row_ids=test["row_ids"],truth=y,probabilities=probs)
    (out/"image-evaluation.json").write_text(json.dumps(result,indent=2))
    print(json.dumps({k:result[k] for k in ["n","accuracy","macro_f1","ece_15_bins","selective","evaluation_seconds"]}),flush=True)


if __name__=="__main__":run()
