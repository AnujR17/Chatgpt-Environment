"""Train and calibrate using training and PublicTest only. Never read PrivateTest here."""
import argparse
import hashlib
import json
import math
import platform
import random
import time
from pathlib import Path
import numpy as np
import torch
from scipy.optimize import minimize_scalar
from scipy.special import softmax
from sklearn.metrics import accuracy_score, f1_score
from torch.nn import functional as F
from ml.network import ExpressionNet,TransferExpressionNet
from ml.prepare import ROOT, LABELS


def seed_all(seed):
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
    torch.use_deterministic_algorithms(True)


def load(name):
    data = np.load(ROOT / "data" / f"{name}.npz", allow_pickle=False)
    return torch.from_numpy(data["images"].copy()).unsqueeze(1).float() / 127.5 - 1, torch.from_numpy(data["targets"].copy())


def logits_for(model, x, batch=256):
    model.eval()
    with torch.inference_mode():
        return torch.cat([model(x[i:i+batch]) for i in range(0, len(x), batch)]).numpy()


def ece(probs, labels, bins=15):
    conf = probs.max(1); correct = probs.argmax(1) == labels
    value = 0.
    for lo, hi in zip(np.linspace(0, 1, bins+1)[:-1], np.linspace(0, 1, bins+1)[1:]):
        mask = (conf > lo) & (conf <= hi)
        if mask.any(): value += mask.mean() * abs(correct[mask].mean() - conf[mask].mean())
    return float(value)


def calibrate(logits, targets):
    y = targets.argmax(1)
    def nll(t):
        p = softmax(logits / t, axis=1)
        # Confidence is calibrated for the evaluated task: the crowd plurality label.
        return float(-np.log(p[np.arange(len(y)), y].clip(1e-12)).mean())
    temperature = float(minimize_scalar(nll, bounds=(.5, 8), method="bounded").x)
    probs = softmax(logits / temperature, axis=1)
    candidates = []
    # Threshold is selected only on validation. Wilson lower bound guards small samples.
    for threshold in np.linspace(.4, .99, 60):
        selected = probs.max(1) >= threshold
        n = int(selected.sum())
        if n < 50: continue
        p = float((probs.argmax(1)[selected] == y[selected]).mean())
        lower = (p+1.96**2/(2*n)-1.96*math.sqrt(p*(1-p)/n+1.96**2/(4*n*n)))/(1+1.96**2/n)
        if lower >= .8: candidates.append((float(selected.mean()), float(threshold), p, lower))
    choice = max(candidates) if candidates else None
    threshold = choice[1] if choice else 1.01
    return {"temperature": temperature, "abstention_threshold": threshold,
            "calibration_objective": "Temperature scaling: hard plurality-label NLL on PublicTest validation only",
            "threshold_selection": "Maximum validation coverage with 95% Wilson precision lower bound >=0.80; minimum 50 examples",
            "validation_selective_coverage": choice[0] if choice else 0.,
            "validation_selective_accuracy": choice[2] if choice else None,
            "validation_selective_precision_lower_bound": choice[3] if choice else None,
            "validation_nll": nll(temperature), "validation_vote_distribution_nll":float(-(targets*np.log(probs.clip(1e-12))).sum(1).mean()), "validation_ece": ece(probs, y),
            "validation_accuracy": float(accuracy_score(y, probs.argmax(1))),
            "validation_macro_f1": float(f1_score(y, probs.argmax(1), labels=list(range(8)), average="macro", zero_division=0))}


def train(args):
    torch.set_num_threads(args.threads); seed_all(args.seed)
    out = ROOT / args.output; out.mkdir(parents=True,exist_ok=True)
    x, targets = load("train"); vx, vy = load("valid")
    model = TransferExpressionNet(cache=ROOT/".cache"/"torch") if args.architecture=="transfer" else ExpressionNet()
    counts = targets.sum(0)
    weights = (counts.max() / counts.clamp_min(1)).sqrt().clamp_max(4)
    weights /= weights.mean()
    optimizer = torch.optim.AdamW(model.parameters(), lr=.0004 if args.architecture=="transfer" else .002, weight_decay=.0001)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, args.epochs, eta_min=.00005)
    best, stale = -1., 0
    started = time.perf_counter()
    history = []
    config = vars(args) | {"classes": LABELS, "architecture": "MobileNetV3-Small / ImageNet-1k pretraining / grayscale48 resized96 in graph" if args.architecture=="transfer" else "ExpressionNet / depthwise separable CNN / 48x48 grayscale", "parameters": sum(p.numel() for p in model.parameters()), "pretrained_expression_weights": False, "pretraining":"ImageNet-1k" if args.architecture=="transfer" else None, "training_samples": len(x), "validation_samples": len(vx), "class_weights": weights.tolist(), "python": platform.python_version(), "torch": torch.__version__, "test_used_during_training": False}
    (out / "training-config.json").write_text(json.dumps(config, indent=2))
    for epoch in range(args.epochs):
        t0 = time.perf_counter(); model.train(); losses=[]
        for ix in torch.randperm(len(x)).split(args.batch_size):
            bx = x[ix].clone(); by = targets[ix]
            flip = torch.rand(len(bx)) < .5; bx[flip] = bx[flip].flip(-1)
            shift_x, shift_y = torch.randint(0, 5, (2,)).tolist()
            bx = F.pad(bx, (2,2,2,2), mode="replicate")[:,:,shift_y:shift_y+48,shift_x:shift_x+48]
            bx = (bx * (torch.rand(len(bx),1,1,1)*.2+.9) + (torch.rand(len(bx),1,1,1)-.5)*.12).clamp(-1,1)
            logits = model(bx)
            weighted = by * weights
            loss = -(weighted * F.log_softmax(logits, dim=1)).sum() / weighted.sum()
            optimizer.zero_grad(set_to_none=True); loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(), 5); optimizer.step()
            losses.append(loss.item())
        pred = logits_for(model, vx).argmax(1); truth = vy.argmax(1).numpy()
        score = float(f1_score(truth, pred, labels=list(range(8)), average="macro", zero_division=0))
        row = {"epoch": epoch+1, "train_loss": float(np.mean(losses)), "validation_accuracy": float(accuracy_score(truth,pred)), "validation_macro_f1": score, "seconds": round(time.perf_counter()-t0,2), "elapsed_seconds": round(time.perf_counter()-started,2)}
        history.append(row); print(json.dumps(row), flush=True)
        (out / "training-history.json").write_text(json.dumps(history, indent=2))
        if score > best:
            best=score; stale=0; torch.save(model.state_dict(), out / "expression-best.pt")
        else: stale += 1
        scheduler.step()
        if args.stop_after and epoch+1>=args.stop_after:
            print(json.dumps({"stopped_after_completed_epochs":epoch+1,"cosine_schedule_epochs":args.epochs}),flush=True);break
        if stale >= args.patience:
            print(json.dumps({"early_stopping": epoch+1, "patience": args.patience}), flush=True); break
    model.load_state_dict(torch.load(out / "expression-best.pt", map_location="cpu", weights_only=True)); model.eval()
    calibration = calibrate(logits_for(model,vx),vy.numpy())
    (out / "calibration.json").write_text(json.dumps(calibration,indent=2))
    torch.onnx.export(model, torch.zeros(1,1,48,48), out / "expression.onnx", input_names=["face"],output_names=["logits"], dynamic_axes={"face":{0:"batch"},"logits":{0:"batch"}}, opset_version=17)
    print(json.dumps({"complete": True, "calibration": calibration, "training_seconds":time.perf_counter()-started}),flush=True)


if __name__ == "__main__":
    p=argparse.ArgumentParser();p.add_argument("--epochs",type=int,default=40);p.add_argument("--batch-size",type=int,default=128);p.add_argument("--threads",type=int,default=2);p.add_argument("--seed",type=int,default=1729);p.add_argument("--patience",type=int,default=10);p.add_argument("--architecture",choices=["compact","transfer"],default="compact");p.add_argument("--output",default="artifacts");p.add_argument("--stop-after",type=int,default=0)
    train(p.parse_args())
