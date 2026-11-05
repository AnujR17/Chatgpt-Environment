"""Provider-trained HSEmotion ONNX adapter, using the existing eight-label contract."""
from pathlib import Path
import cv2
import numpy as np
import onnxruntime as ort
from checkpoint.runtime import Cue,LABELS


class HSEExpressionModel:
    def __init__(self,directory=None):
        directory=Path(directory or Path(__file__).resolve().parents[1]/'artifacts')
        options=ort.SessionOptions();options.intra_op_num_threads=1;options.inter_op_num_threads=1
        self.session=ort.InferenceSession(str(directory/'hsemotion-afew.onnx'),sess_options=options,providers=['CPUExecutionProvider'])
        self.threshold=.7  # Presentation abstention, not calibrated probability of a felt emotion.
        self.input_name=self.session.get_inputs()[0].name
        # Provider: anger, contempt, disgust, fear, happiness, neutral, sadness, surprise.
        self.order=[5,4,7,6,0,2,3,1]
    def probabilities(self,crop):
        image=cv2.cvtColor(crop,cv2.COLOR_BGR2RGB) if crop.ndim==3 else cv2.cvtColor(crop,cv2.COLOR_GRAY2RGB)
        x=cv2.resize(image,(224,224)).astype(np.float32)/255
        x=(x-np.array([.485,.456,.406],np.float32))/np.array([.229,.224,.225],np.float32)
        logits=self.session.run(None,{self.input_name:x.transpose(2,0,1)[None]})[0][0]
        logits=logits[self.order];p=np.exp(logits-logits.max());return p/p.sum()
    def predict_crop(self,crop):
        p=self.probabilities(crop);i=int(p.argmax());accepted=float(p[i])>=self.threshold
        return Cue('accepted' if accepted else 'uncertain',LABELS[i] if accepted else None,float(p[i]),tuple(float(x) for x in p),
                   '' if accepted else 'Expression estimate below display threshold')
