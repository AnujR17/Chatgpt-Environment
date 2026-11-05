"""Small trained scene matcher. Coverage is limited to inspected publisher-trailer views."""
from pathlib import Path
import json
import cv2
import numpy as np


def features(frame):
    small=cv2.resize(frame,(160,90));small=small[:76]  # Exclude most trailer subtitles.
    hsv=cv2.cvtColor(small,cv2.COLOR_BGR2HSV)
    hist=cv2.calcHist([hsv],[0,1],None,[12,8],[0,180,0,256]).ravel();hist/=max(1.,hist.sum())
    colour=cv2.resize(small,(8,4),interpolation=cv2.INTER_AREA).astype(np.float32).ravel()/255
    return np.concatenate([hist,colour]).astype(np.float32)


class SceneModel:
    def __init__(self,path=None):
        path=path or Path(__file__).resolve().parents[1]/'artifacts/game-scene-model.json'
        self.data=json.loads(Path(path).read_text());self.weights=np.array(self.data['weights']);self.bias=np.array(self.data['bias'])
    def predict(self,frame):
        logits=self.weights@features(frame)+self.bias;prob=np.exp(logits-logits.max());prob/=prob.sum();i=int(prob.argmax())
        return self.data['classes'][i] if prob[i]>=self.data['minimum_match_score'] else None,float(prob[i])
