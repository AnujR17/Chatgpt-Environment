"""Freeze selection using validation only, before reading either evaluation dataset."""
import json
import shutil
from ml.prepare import ROOT,sha256


def select():
    out=ROOT/'artifacts';candidates=[]
    for name in ['compact','transfer']:
        directory=out/name
        if not (directory/'expression.onnx').exists():raise RuntimeError(f'{name} export missing')
        calibration=json.loads((directory/'calibration.json').read_text())
        candidates.append({'name':name,'validation_macro_f1':calibration['validation_macro_f1'],'validation_accuracy':calibration['validation_accuracy'],'onnx_sha256':sha256(directory/'expression.onnx')})
    chosen=max(candidates,key=lambda d:d['validation_macro_f1'])['name'];directory=out/chosen
    for name in ['expression.onnx','expression-best.pt','calibration.json','training-config.json','training-history.json']:
        shutil.copy2(directory/name,out/name)
    selection={'selected':chosen,'criterion':'Highest macro-F1 on eligible deduplicated FER+ PublicTest validation split','candidates':candidates,'private_test_used':False,'external_video_used':False,'frozen_model_sha256':sha256(out/'expression.onnx')}
    (out/'model-selection.json').write_text(json.dumps(selection,indent=2));print(json.dumps(selection,indent=2))


if __name__=='__main__':select()
