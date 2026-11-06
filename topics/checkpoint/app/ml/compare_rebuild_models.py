"""Matched frozen-video comparison. Candidate is provider B2 eight-class ONNX; no training."""
import argparse,json,time
from pathlib import Path
import cv2,numpy as np
from sklearn.metrics import classification_report,accuracy_score,f1_score
from checkpoint.runtime import FacePipeline,LABELS
from checkpoint.pretrained_expression import HSEExpressionModel
from ml.evaluate_video import MAP
parser=argparse.ArgumentParser();parser.add_argument('--data',type=Path,required=True);parser.add_argument('--candidate',type=Path,required=True);parser.add_argument('--output',default='rebuild-model-comparison.json');args=parser.parse_args()
root=Path(__file__).resolve().parents[1];data=args.data
manifest=json.loads((data/'video-manifest.json').read_text())
models={'existing_b0':HSEExpressionModel(),args.candidate.stem:HSEExpressionModel(model_path=args.candidate)}
pipes={k:FacePipeline(pretrained=True) for k in models}
for k,p in pipes.items():p.model=models[k]
records=[];lat={k:[] for k in models}
for entry in [x for a in manifest['archives'] for x in a['clips']]:
 if entry['emotion_id'] not in MAP:continue
 cap=cv2.VideoCapture(str(data/'videos'/entry['file']));n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT));indices=set(np.linspace(int(n*.2),max(int(n*.2),int(n*.8)-1),10,dtype=int).tolist());ps={k:[] for k in models};i=0
 while cap.grab():
  if i in indices:
   ok,frame=cap.retrieve()
   if not ok:raise RuntimeError('decode failure')
   for k,p in pipes.items():
    cue=p.infer(frame);lat[k].append(cue.elapsed_ms)
    if cue.probabilities:ps[k].append(cue.probabilities)
  i+=1
  if i>max(indices):break
 cap.release();records.append({'file':entry['file'],'actor':entry['actor'],'truth':MAP[entry['emotion_id']],**{k:int(np.mean(p,axis=0).argmax()) if p else 8 for k,p in ps.items()}})
 if len(records)%40==0:print('Compared',len(records),flush=True)
y=[x['truth'] for x in records];result={'protocol':'208 acted RAVDESS clips, actors01-04, ten frames middle60%, same YuNet/quality gates; no training or tuning; exploratory reuse of known benchmark','models':{}}
for k in models:
 pred=[x[k] for x in records];result['models'][k]={'accuracy':accuracy_score(y,pred),'macro_f1':f1_score(y,pred,labels=list(range(7)),average='macro',zero_division=0),'per_class':classification_report(y,pred,labels=list(range(8)),target_names=LABELS,output_dict=True,zero_division=0),'latency_ms':{'median':float(np.median(lat[k])),'p95':float(np.quantile(lat[k],.95))}}
result['records']=records;(root/('artifacts/'+args.output)).write_text(json.dumps(result,indent=2));print(json.dumps({k:{a:b for a,b in v.items() if a!='per_class'} for k,v in result['models'].items()},indent=2))
