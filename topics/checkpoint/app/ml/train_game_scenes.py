"""Train a source-labelled research scene matcher; never labels player affect or falls."""
import argparse
import hashlib
import json
from pathlib import Path
import cv2
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,balanced_accuracy_score,confusion_matrix
from checkpoint.scene_model import features

ROOT=Path(__file__).resolve().parents[1]
# Human-reviewed contact sheet, excluding transition boundaries. Split by time block.
SEGMENTS={
 'title_or_non_game':{'train':[(0.,1.8)],'validation':[(2.2,3.5)],'test':[(37.8,43.1)]},
 'opening_lake':{'train':[(4.5,9.5)],'validation':[(11.,12.5)],'test':[(14.5,17.)]},
 'rock_slope':{'train':[(18.5,23.)],'validation':[(24.5,26.)],'test':[(28.5,31.)]},
 'pipe_grey_rock':{'train':[(32.,33.)],'validation':[(34.,34.5)],'test':[(35.,36.2)]},
}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--video',required=True);args=parser.parse_args()
    capture=cv2.VideoCapture(args.video)
    if not capture.isOpened():raise ValueError('Video unavailable')
    data={key:[] for key in ['train','validation','test']};labels={key:[] for key in data};manifest=[]
    try:
        for label,splits in SEGMENTS.items():
            for split,segments in splits.items():
                for start,end in segments:
                    for second in np.arange(start,end,.25):
                        capture.set(cv2.CAP_PROP_POS_MSEC,float(second)*1000);ok,frame=capture.read()
                        if not ok:continue
                        data[split].append(features(frame));labels[split].append(label)
                        manifest.append({'seconds':round(float(second),2),'label':label,'split':split})
    finally:capture.release()
    candidates=[]
    for regularization in [.1,1.,10.]:
        model=LogisticRegression(C=regularization,max_iter=2000,class_weight='balanced',random_state=19).fit(data['train'],labels['train'])
        candidates.append((balanced_accuracy_score(labels['validation'],model.predict(data['validation'])),model))
    score,model=max(candidates,key=lambda x:x[0])
    result={'schema':1,'classes':model.classes_.tolist(),'weights':model.coef_.tolist(),'bias':model.intercept_.tolist(),'minimum_match_score':.75,
            'source':'Official Getting Over It Steam trailer 256696623','source_sha256':hashlib.sha256(Path(args.video).read_bytes()).hexdigest(),
            'limitations':['Single 43-second publisher trailer','Limited inspected opening views and title screens','Temporal blocks from one source are not independent-player/video generalization','Not a fall, mood, frustration or full-map model']}
    report={'source_sha256':result['source_sha256'],'samples':{k:len(v) for k,v in labels.items()},'validation_balanced_accuracy':float(score),
            'test_accuracy':float(accuracy_score(labels['test'],model.predict(data['test']))),'test_balanced_accuracy':float(balanced_accuracy_score(labels['test'],model.predict(data['test']))),
            'classes':model.classes_.tolist(),'test_confusion':confusion_matrix(labels['test'],model.predict(data['test']),labels=model.classes_).tolist(),
            'limitations':result['limitations'],'test_used_for_selection':False}
    (ROOT/'artifacts/game-scene-model.json').write_text(json.dumps(result,indent=2));(ROOT/'artifacts/game-scene-training.json').write_text(json.dumps(report,indent=2))
    (ROOT/'design/game-scene-annotations.json').write_text(json.dumps({'annotation_method':'Human inspection of contact sheet and timestamps; visual scene labels only','samples':manifest},indent=2))
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
