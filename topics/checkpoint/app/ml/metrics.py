"""Metrics with explicit denominators and uncertainty, including abstentions."""
import math
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, f1_score, balanced_accuracy_score


def wilson(successes,total):
    if not total:return None
    p=successes/total;z=1.96;den=1+z*z/total
    center=(p+z*z/(2*total))/den
    half=z*math.sqrt(p*(1-p)/total+z*z/(4*total*total))/den
    return [max(0,center-half),min(1,center+half)]


def ece(probs,y,bins=15):
    confidence=probs.max(1);correct=probs.argmax(1)==y;value=0.
    for low,high in zip(np.linspace(0,1,bins+1)[:-1],np.linspace(0,1,bins+1)[1:]):
        mask=(confidence>low)&(confidence<=high)
        if mask.any():value+=mask.mean()*abs(correct[mask].mean()-confidence[mask].mean())
    return float(value)


def score(y,probs,labels,threshold,*,bootstraps=500,seed=1729,groups=None,metric_labels=None):
    y=np.asarray(y,dtype=int);probs=np.asarray(probs);pred=probs.argmax(1);selected=probs.max(1)>=threshold
    n=len(y);accurate=int((pred==y).sum());accepted=int(selected.sum());accepted_right=int((pred[selected]==y[selected]).sum())
    metric_labels=list(range(len(labels))) if metric_labels is None else list(metric_labels)
    result={"n":n,"accuracy":float(accurate/n),"accuracy_ci95_wilson":wilson(accurate,n),
      "macro_f1":float(f1_score(y,pred,labels=metric_labels,average="macro",zero_division=0)),"macro_f1_label_indices":metric_labels,
      "balanced_accuracy":float(balanced_accuracy_score(y,pred)),"ece_15_bins":ece(probs,y),
      "brier_hard_label":float(((probs-np.eye(len(labels))[y])**2).sum(1).mean()),
      "nll_hard_label":float(-np.log(probs[np.arange(n),y].clip(1e-12)).mean()),
      "selective":{"threshold":threshold,"accepted":accepted,"abstained":n-accepted,"coverage":float(accepted/n),
         "accuracy":accepted_right/accepted if accepted else None,"accuracy_ci95_wilson":wilson(accepted_right,accepted)},
      "per_class":classification_report(y,pred,labels=list(range(len(labels))),target_names=labels,output_dict=True,zero_division=0),
      "confusion_matrix":confusion_matrix(y,pred,labels=list(range(len(labels)))).tolist()}
    rng=np.random.default_rng(seed);scores=[];accuracies=[]
    group_values=np.unique(groups) if groups is not None else None
    for _ in range(bootstraps):
        if group_values is None:ix=rng.integers(0,n,n)
        else:ix=np.concatenate([np.flatnonzero(np.asarray(groups)==g) for g in rng.choice(group_values,len(group_values),replace=True)])
        cm=np.bincount(y[ix]*len(labels)+pred[ix],minlength=len(labels)**2).reshape(len(labels),len(labels));den=cm.sum(0)+cm.sum(1)
        per_label=np.divide(2*cm.diagonal(),den,out=np.zeros(len(labels)),where=den>0)
        scores.append(float(per_label[metric_labels].mean()));accuracies.append(float((pred[ix]==y[ix]).mean()))
    result["macro_f1_ci95_bootstrap"]=np.quantile(scores,[.025,.975]).tolist()
    result["accuracy_ci95_bootstrap"]=np.quantile(accuracies,[.025,.975]).tolist()
    result["bootstrap_unit"]="actor" if groups is not None else "image; subject independence unavailable"
    if groups is not None:
        result["independence_note"]="Use actor-bootstrap intervals as primary. Wilson intervals assume independent clips and are diagnostic only; four actors are insufficient for population claims."
    return result
