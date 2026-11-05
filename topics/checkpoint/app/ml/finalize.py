"""Export a preserved best checkpoint after an intentionally stopped training run."""
import argparse
import json
from pathlib import Path
import torch
from ml.prepare import ROOT
from ml.network import ExpressionNet,TransferExpressionNet
from ml.train import load,logits_for,calibrate


def finalize(directory):
    torch.set_num_threads(1);out=Path(directory);config=json.loads((out/'training-config.json').read_text())
    model=TransferExpressionNet(pretrained=False) if 'MobileNetV3' in config['architecture'] else ExpressionNet()
    model.load_state_dict(torch.load(out/'expression-best.pt',map_location='cpu',weights_only=True));model.eval()
    x,y=load('valid');calibration=calibrate(logits_for(model,x),y.numpy());(out/'calibration.json').write_text(json.dumps(calibration,indent=2))
    torch.onnx.export(model,torch.zeros(1,1,48,48),out/'expression.onnx',input_names=['face'],output_names=['logits'],dynamic_axes={'face':{0:'batch'},'logits':{0:'batch'}},opset_version=17)
    print(json.dumps(calibration),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('directory',type=Path);args=p.parse_args();finalize(args.directory)
