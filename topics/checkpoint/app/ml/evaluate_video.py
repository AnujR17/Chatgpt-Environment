"""External video test with clip-level labels; frames are never counted as independent clips."""
import collections
import json
import time
import cv2
import numpy as np
from checkpoint.runtime import FacePipeline, LABELS
from ml.prepare import ROOT, sha256
from ml.metrics import score

# RAVDESS emotion IDs -> FER+ classes. Calm is intentionally unsupported.
MAP={1:0,3:1,4:3,5:4,6:6,7:5,8:2}


def run():
    out=ROOT/"artifacts";manifest=json.loads((ROOT/"data"/"video-manifest.json").read_text());pipeline=FacePipeline()
    records=[];times=[];reasons=collections.Counter();calm_excluded=0
    for entry in [clip for archive in manifest["archives"] for clip in archive["clips"]]:
        if entry["emotion_id"] not in MAP:calm_excluded+=1;continue
        path=ROOT/"data"/"videos"/entry["file"];cap=cv2.VideoCapture(str(path))
        if not cap.isOpened():raise RuntimeError("Could not open "+entry["file"])
        n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT));fps=cap.get(cv2.CAP_PROP_FPS)
        # Middle 60% focuses on acted speech; annotation remains recording-level, not frame ground truth.
        indices=set(np.linspace(int(n*.2),max(int(n*.2),int(n*.8)-1),10,dtype=int).tolist())
        frame_probs=[];accepted=0;attempted=0;i=0
        while cap.grab():
            if i in indices:
                ok,frame=cap.retrieve()
                if not ok:raise RuntimeError("Could not decode selected frame")
                cue=pipeline.infer(frame);attempted+=1;times.append(cue.elapsed_ms);reasons[cue.reason or cue.status]+=1
                if cue.probabilities:frame_probs.append(cue.probabilities)
                if cue.status=="accepted":accepted+=1
            i+=1
            if i>max(indices):break
        cap.release()
        # No face/quality failure counts as operational failure, never a fabricated class.
        probability=np.mean(frame_probs,axis=0) if frame_probs else None
        records.append({"file":entry["file"],"actor":entry["actor"],"truth":MAP[entry["emotion_id"]],"sampled_frames":attempted,"quality_eligible_frames":len(frame_probs),"accepted_frames":accepted,"probabilities":probability.tolist() if probability is not None else None})
        print(json.dumps({"evaluated_clips":len(records),"file":entry["file"],"eligible_frames":len(frame_probs)}),flush=True)
    valid=[r for r in records if r["probabilities"] is not None]
    if not valid:raise RuntimeError("No quality-eligible video clips; no accuracy can be reported")
    # Remove unsupported contempt output mass only for comparable seven-class benchmark.
    # The full eight-class operational result is retained below, including contempt mistakes.
    y=np.array([r["truth"] for r in valid]);probs=np.array([r["probabilities"] for r in valid]);groups=np.array([r["actor"] for r in valid])
    supported=[0,1,2,3,4,5,6]
    full=score(y,probs,list(LABELS),pipeline.model.threshold,groups=groups,metric_labels=supported)
    mapping={old:new for new,old in enumerate(supported)};p7=probs[:,supported];p7/=p7.sum(1,keepdims=True)
    comparable=score(np.array([mapping[i] for i in y]),p7,[LABELS[i] for i in supported],pipeline.model.threshold,groups=groups)
    # Seven supported truth classes, but errors into contempt are still counted.
    from sklearn.metrics import f1_score
    full["macro_f1_supported_truth_classes"]=float(f1_score(y,probs.argmax(1),labels=supported,average="macro",zero_division=0))
    failed=len(records)-len(valid);correct=int((probs.argmax(1)==y).sum())
    result={"dataset":"RAVDESS / external acted emotional speech / video-only / actors 01-04", "protocol":"Ten evenly spaced frames in middle 60% of each clip; mean probabilities after face/quality checks; clip-level labels",
      "model_sha256":sha256(out/"expression.onnx"),"calibration_sha256":sha256(out/"calibration.json"),"clips_attempted":len(records),"clips_with_predictions":len(valid),"operational_clip_coverage":len(valid)/len(records),"operational_accuracy_including_no_prediction_failures":correct/len(records),"unsupported_calm_clips_excluded":calm_excluded,
      "full_eight_output_metrics":full,"seven_class_renormalized_diagnostic":comparable,
      "frame_pipeline_ms":{"median":float(np.median(times)),"p95":float(np.quantile(times,.95)),"max":float(max(times))},"frame_status_counts":dict(reasons),"records":records,
      "limitations":["Acted clip-level categories are not frame ground truth or gamer mood","Only four actors; actor-bootstrap intervals are unstable and do not demonstrate population validity","Image-calibrated confidence is evaluated without tuning on this video set","The seven-class diagnostic renormalizes scores; it is not the operational deployed classifier","FER+ identity IDs are unavailable; disjoint recordings do not prove disjoint people"]}
    (out/"video-evaluation.json").write_text(json.dumps(result,indent=2))
    print(json.dumps({"complete":True,"accuracy":full["accuracy"],"macro_f1_supported_truth_classes":full["macro_f1_supported_truth_classes"],"clips":len(records),"latency":result["frame_pipeline_ms"]}),flush=True)


if __name__=="__main__":run()
