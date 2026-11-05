"""Exploratory matched-protocol comparison on the frozen external acted-video set.
No tuning or training on these recordings. Not a gamer or personal-camera accuracy claim.
"""
import argparse
import json
import time
from pathlib import Path
import cv2
import numpy as np
from sklearn.metrics import f1_score,classification_report,confusion_matrix
from checkpoint.runtime import FacePipeline,LABELS
from checkpoint.pretrained_expression import HSEExpressionModel
from ml.evaluate_video import MAP


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--data',required=True);args=parser.parse_args();data=Path(args.data)
    root=Path(__file__).resolve().parents[1];manifest=json.loads((data/'video-manifest.json').read_text())
    pipeline=FacePipeline();pipeline.model=HSEExpressionModel();records=[];latencies=[]
    for entry in [x for a in manifest['archives'] for x in a['clips']]:
        if entry['emotion_id'] not in MAP:continue
        cap=cv2.VideoCapture(str(data/'videos'/entry['file']));n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        indices=set(np.linspace(int(n*.2),max(int(n*.2),int(n*.8)-1),10,dtype=int).tolist());probabilities=[];index=0
        while cap.grab():
            if index in indices:
                ok,frame=cap.retrieve()
                if not ok:raise ValueError('Video decode failed')
                cue=pipeline.infer(frame);latencies.append(cue.elapsed_ms)
                if cue.probabilities:probabilities.append(cue.probabilities)
            index+=1
            if index>max(indices):break
        cap.release();p=np.mean(probabilities,axis=0) if probabilities else None
        records.append({'file':entry['file'],'actor':entry['actor'],'truth':MAP[entry['emotion_id']],
                        'prediction':int(p.argmax()) if p is not None else None,'eligible_frames':len(probabilities)})
        if len(records)%20==0:print('Compared clips:',len(records),flush=True)
    y=[x['truth'] for x in records];pred=[x['prediction'] if x['prediction'] is not None else 8 for x in records]
    baseline=json.loads((root/'artifacts/video-evaluation.json').read_text())
    result={'protocol':'Same 208 RAVDESS actor 01-04 clips, ten middle-60% frames, same face/quality gate, mean probabilities; calm excluded',
       'candidate':'HSEmotion enet_b0_8_best_afew, pretrained provider ONNX, no fine-tuning',
       'clips':len(records),'accuracy_including_no_prediction':float(np.mean(np.array(y)==pred)),
       'macro_f1_supported_truth':float(f1_score(y,pred,labels=list(range(7)),average='macro',zero_division=0)),
       'per_class':classification_report(y,pred,labels=list(range(8)),target_names=LABELS,output_dict=True,zero_division=0),
       'confusion':confusion_matrix(y,pred,labels=list(range(8))).tolist(),
       'latency_ms':{'median':float(np.median(latencies)),'p95':float(np.quantile(latencies,.95))},
       'baseline_accuracy':baseline['operational_accuracy_including_no_prediction_failures'],
       'limitations':['Acted clip-level labels, not natural gamer emotions','Four actors only','Exploratory comparison on an already reported benchmark; fresh target-context validation still required','Unknown overlap with provider training datasets','No personal emotion photos required'],'records':records}
    (root/'artifacts/pretrained-comparison.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k not in ['records','per_class','confusion']},indent=2))


if __name__=='__main__':main()
