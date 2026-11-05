import numpy as np
from checkpoint.runtime import preprocess,Cue,CueSmoother,FacePipeline


def test_preprocessing_shape_range_and_determinism():
    x=np.full((90,130,3),127,dtype=np.uint8);a=preprocess(x)
    assert a.shape==(1,1,48,48) and a.dtype==np.float32
    assert np.allclose(a,preprocess(x)) and -1<=a.min()<=a.max()<=1


def test_smoother_needs_agreement_and_clears_on_source_quality_loss():
    smoother=CueSmoother(3);cue=Cue("accepted","happiness",.95)
    assert smoother.update(cue).status=="uncertain"
    assert smoother.update(cue).status=="uncertain"
    assert smoother.update(cue).status=="accepted"
    smoother.update(Cue("unavailable",reason="No face"))
    assert smoother.update(cue).status=="uncertain"


def test_detector_refuses_blank_and_multiple_faces_without_emotion_guess():
    class Detector:
        def __init__(self,faces):self.faces=faces
        def setInputSize(self,size):pass
        def detect(self,frame):return None,self.faces
    pipeline=FacePipeline.__new__(FacePipeline);pipeline.min_face_pixels=80
    pipeline.detector=Detector(None)
    assert pipeline.infer(np.zeros((480,640,3),np.uint8)).reason=="No face in frame"
    pipeline.detector=Detector(np.zeros((2,15)))
    assert pipeline.infer(np.zeros((480,640,3),np.uint8)).status=="unavailable"
    assert pipeline.infer(None).expression is None
