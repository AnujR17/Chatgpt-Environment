"""Verify frozen ONNX parity, actual video I/O, and measured inference latency."""
import json
import time
from pathlib import Path
import cv2
import numpy as np
import onnx
import torch
from checkpoint.runtime import ExpressionModel,FacePipeline
from ml.prepare import ROOT,sha256
from ml.network import ExpressionNet,TransferExpressionNet


def run():
    torch.set_num_threads(1);out=ROOT/'artifacts';selection=json.loads((out/'model-selection.json').read_text())
    config=json.loads((out/'training-config.json').read_text());model=TransferExpressionNet(pretrained=False) if 'MobileNetV3' in config['architecture'] else ExpressionNet()
    model.load_state_dict(torch.load(out/'expression-best.pt',map_location='cpu',weights_only=True));model.eval();onnx.checker.check_model(str(out/'expression.onnx'))
    runtime=ExpressionModel();data=np.load(ROOT/'data/valid.npz',allow_pickle=False);x=data['images'][:64,None].astype(np.float32)/127.5-1
    with torch.inference_mode():expected=model(torch.from_numpy(x)).numpy()
    actual=runtime.session.run(['logits'],{'face':x})[0];error=float(np.max(np.abs(expected-actual)))
    if error>1e-3:raise AssertionError(f'ONNX/PyTorch mismatch {error}')
    for _ in range(10):runtime.probabilities(x[:1])
    times=[]
    for _ in range(100):
        t=time.perf_counter();runtime.probabilities(x[:1]);times.append((time.perf_counter()-t)*1000)
    pipeline=FacePipeline();blank=pipeline.infer(np.zeros((480,640,3),np.uint8))
    if blank.expression is not None:raise AssertionError('Blank frame produced expression')
    video=ROOT/'data/videos/02-01-05-01-01-01-04.mp4';cap=cv2.VideoCapture(str(video));ok,frame=cap.read();cap.release()
    if not ok:raise AssertionError('Real test video unavailable')
    result={'model_sha256':sha256(out/'expression.onnx'),'selection_hash_matches':sha256(out/'expression.onnx')==selection['frozen_model_sha256'],
      'onnx_checker_pass':True,'onnx_pytorch_max_logit_error_on_64_validation_faces':error,
      'single_crop_inference_ms':{'median':float(np.median(times)),'p95':float(np.quantile(times,.95))},
      'blank_frame_status':blank.status,'real_video_first_frame':pipeline.infer(frame).to_dict(),
      'real_webcam_tested':False,'windows_camera_permissions_tested':False,'scope':'CPU inference and actual local video I/O; not game FPS or power comparison'}
    (out/'runtime-verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))


if __name__=='__main__':run()
