"""Build a model card and standalone scientific figures from measured outputs only."""
import json
import os
from pathlib import Path
import textwrap
import numpy as np
from ml.prepare import ROOT,sha256,LABELS
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.cache'/'matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def pct(value):return 'unavailable' if value is None else f'{value*100:.1f}%'


def run():
    out=ROOT/'artifacts';figdir=out/'figures';figdir.mkdir(exist_ok=True)
    read=lambda name:json.loads((out/name).read_text())
    image=read('image-evaluation.json');video=read('video-evaluation.json');selection=read('model-selection.json');calibration=read('calibration.json');targets=read('acceptance-targets.json')
    dataset=json.loads((ROOT/'data/manifest.json').read_text());v=video['full_eight_output_metrics'];figures=[]
    for name,result,title in [('image-confusion',image,'FER+ eligible PrivateTest / image classification'),('video-confusion',v,'RAVDESS external acted speech / clip classification')]:
        cm=np.array(result['confusion_matrix']);den=cm.sum(1,keepdims=True);norm=np.divide(cm,den,out=np.zeros_like(cm,dtype=float),where=den>0)
        fig,ax=plt.subplots(figsize=(9,8),layout='constrained');picture=ax.imshow(norm,cmap='Blues',vmin=0,vmax=1)
        ax.set(xticks=range(8),yticks=range(8),xticklabels=LABELS,yticklabels=LABELS,xlabel='Predicted expression category',ylabel='Crowd / acted clip category',title=title)
        plt.setp(ax.get_xticklabels(),rotation=35,ha='right');fig.colorbar(picture,ax=ax,label='Fraction of true class')
        for i in range(8):
            for j in range(8):ax.text(j,i,str(cm[i,j]) if den[i,0] else 'n/a',ha='center',va='center',color='white' if norm[i,j]>.5 else 'black',fontsize=9)
        path=figdir/(name+'.png');fig.savefig(path,dpi=180);figures.append(fig)
    fig,ax=plt.subplots(figsize=(10,5),layout='constrained')
    for model in ['compact','transfer']:
        history=read(model+'/training-history.json');ax.plot([r['epoch'] for r in history],[r['validation_macro_f1'] for r in history],marker='.',label=model)
    ax.axhline(targets['image_macro_f1_min'],ls='--',color='gray',label='Project macro-F1 target')
    ax.set(xlabel='Training epoch',ylabel='Validation macro-F1',title='Candidate comparison / validation only',ylim=(0,1));ax.legend();ax.grid(alpha=.2);fig.savefig(figdir/'learning-curves.png',dpi=180);figures.append(fig)
    data=np.load(out/'image-predictions.npz',allow_pickle=False);probs=data['probabilities'];y=data['truth'];conf=probs.max(1);correct=probs.argmax(1)==y
    xs=[];ys=[];sizes=[]
    for lo,hi in zip(np.linspace(0,1,16)[:-1],np.linspace(0,1,16)[1:]):
        mask=(conf>lo)&(conf<=hi)
        if mask.any():xs.append(conf[mask].mean());ys.append(correct[mask].mean());sizes.append(int(mask.sum()))
    fig,ax=plt.subplots(figsize=(7,6),layout='constrained');ax.plot([0,1],[0,1],color='gray',ls='--',label='Ideal calibration');ax.scatter(xs,ys,s=np.sqrt(sizes)*15);ax.plot(xs,ys,alpha=.4)
    ax.set(xlabel='Mean calibrated confidence',ylabel='Accuracy within confidence bin',title='FER+ test reliability / plurality labels',xlim=(0,1),ylim=(0,1));ax.legend();ax.grid(alpha=.2);fig.savefig(figdir/'classification-reliability.png',dpi=180);figures.append(fig)
    tests={
      'image_top1_accuracy':(image['accuracy']>=targets['image_top1_accuracy_min'],image['accuracy'],targets['image_top1_accuracy_min']),
      'image_macro_f1':(image['macro_f1']>=targets['image_macro_f1_min'],image['macro_f1'],targets['image_macro_f1_min']),
      'image_ece':(image['ece_15_bins']<=targets['image_ece_max'],image['ece_15_bins'],targets['image_ece_max']),
      'image_selective_accuracy':(image['selective']['accuracy'] is not None and image['selective']['accuracy']>=targets['selective_accuracy_min'],image['selective']['accuracy'],targets['selective_accuracy_min']),
      'image_selective_coverage':(image['selective']['coverage']>=targets['selective_coverage_min'],image['selective']['coverage'],targets['selective_coverage_min']),
      'external_video_macro_f1':(v['macro_f1_supported_truth_classes']>=targets['external_video_macro_f1_min'],v['macro_f1_supported_truth_classes'],targets['external_video_macro_f1_min']),
      'frame_pipeline_latency':(video['frame_pipeline_ms']['p95']<=targets['frame_pipeline_p95_ms_max'],video['frame_pipeline_ms']['p95'],targets['frame_pipeline_p95_ms_max'])}
    gates={name:{'pass':bool(passed),'measured':value,'target':target} for name,(passed,value,target) in tests.items()}
    release={'production_ready':False,'quantitative_checks':gates,'mandatory_unmet_requirements':targets['release_requirements'],'automatic_cma_enabled':False,'reason':'Benchmark expression results do not validate gamer mood/frustration or continuous CMA. Target-device, representative-user, data-rights and UI approval requirements remain.'}
    (out/'release-gates.json').write_text(json.dumps(release,indent=2))
    rows='\n'.join(f"| {name} | {row['measured']} | {row['target']} | {'Pass' if row['pass'] else 'Fail'} |" for name,row in gates.items())
    classes='\n'.join(f"| {name} | {image['per_class'][name]['support']:.0f} | {image['per_class'][name]['precision']:.3f} | {image['per_class'][name]['recall']:.3f} | {image['per_class'][name]['f1-score']:.3f} |" for name in LABELS)
    card=f'''# Checkpoint expression model / research model card

Status: experimental; not production ready. Automatic CMA and frustration prediction are unavailable.

## Intended use

Local, opt-in testing of eight crowd-annotated facial-expression categories in an academic gaming-companion prototype. The app's CMA values come from player check-ins. Expression cues cannot overwrite them, change games, or trigger automatic interventions.

This model is not a mood, frustration, stress, mental-health, identity, protected-attribute or continuous valence/arousal estimator. Benchmark category labels are not observations of an internal emotional state.

## Model and data

Selected candidate: **{selection['selected']}**, chosen using validation macro-F1 only. No test set was used for selection or calibration. Model SHA256: `{selection['frozen_model_sha256']}`. Calibration SHA256: `{sha256(out/'calibration.json')}`.

FER2013 images with FER+ ten-tagger vote distributions: {dataset['splits']['train']['samples']:,} training, {dataset['splits']['valid']['samples']:,} validation, {dataset['splits']['test']['samples']:,} eligible held-out images. Split/eligibility rules, rejected counts and hashes are in data/manifest.json. Exact pixel and coarse quantized-signature duplicates were removed across splits; identities were unavailable, so this does not prove subject independence. Original dataset rights remain a deployment/redistribution review item.

Compact CNN: trained from scratch, stopped after 23 completed epochs and preserved as a baseline. Transfer candidate: MobileNetV3-Small with ImageNet-1k object pretraining, fine-tuned on the same facial dataset. No pretrained facial-expression weights were used. Both use 48x48 grayscale input; the transfer graph includes its own 96x96 RGB expansion and ImageNet normalization.

Training uses soft crowd vote targets. Temperature scaling uses hard plurality-label NLL on validation only. Temperature {calibration['temperature']:.4f}; confidence acceptance threshold {calibration['abstention_threshold']:.3f}. Threshold selection maximises validation coverage with a 95% Wilson precision lower bound of at least .80 and at least 50 examples. These are project choices, not a universal standard.

## Held-out image evaluation

Accuracy: **{pct(image['accuracy'])}**, nominal image-level 95% Wilson CI {pct(image['accuracy_ci95_wilson'][0])} to {pct(image['accuracy_ci95_wilson'][1])}. Macro-F1: **{image['macro_f1']:.3f}**; balanced accuracy {pct(image['balanced_accuracy'])}. Majority-class training baseline: {pct(image['training_majority_baseline_accuracy'])}. ECE (15 bins): {image['ece_15_bins']:.3f}.

After confidence abstention: {pct(image['selective']['accuracy'])} accuracy on {pct(image['selective']['coverage'])} of eligible images ({image['selective']['accepted']} accepted, {image['selective']['abstained']} abstained). Coverage is part of the result, not a hidden filter. This does not include excluded non-face/ambiguous source rows or all possible real-world inputs. Image-level confidence intervals do not establish participant-independent performance.

| Expression category | Test support | Precision | Recall | F1 |
| --- | ---: | ---: | ---: | ---: |
{classes}

Dim-light, blur and lower-face-occlusion results are reported separately in image-evaluation.json. No model or threshold was retuned on these test transformations.

## External video evaluation

RAVDESS video-only emotional speech, actors 01–04: {video['clips_attempted']} supported-category clips attempted, {video['clips_with_predictions']} with quality-eligible predictions. {video['unsupported_calm_clips_excluded']} calm clips excluded because FER+ has no separate calm category. No calm-to-neutral relabelling was performed.

Protocol: ten evenly spaced frames in the middle 60% of each clip, then mean probabilities after face and image-quality checks. Recording-level acted labels are used. **This is clip classification, not live frame-level emotion ground truth.** Video recordings were not used for training, selection or thresholds.

Conditional clip accuracy: **{pct(v['accuracy'])}**. Actor-bootstrap 95% interval: {pct(v['accuracy_ci95_bootstrap'][0])} to {pct(v['accuracy_ci95_bootstrap'][1])}. Only four actor groups make this interval unstable. Macro-F1 over seven supported truth classes: **{v['macro_f1_supported_truth_classes']:.3f}**; errors into the eighth contempt output remain errors. Operational accuracy including no-prediction failures: {pct(video['operational_accuracy_including_no_prediction_failures'])}. Operational clip coverage: {pct(video['operational_clip_coverage'])}.

At the unchanged image-selected threshold: {pct(v['selective']['accuracy'])} selective clip accuracy with {pct(v['selective']['coverage'])} coverage ({v['selective']['accepted']} accepted clips). These mean-pooled clip confidences have not been calibrated for video and can fail under domain shift.

The eight-output metrics are primary. A separately named seven-class renormalised diagnostic is not the deployed classifier. Per-class tables retain all eight outputs; the declared macro-F1 label indices specify the supported video classes. Image-calibrated confidence has not been retuned to video. Acted clips are not representative Indian gamers, natural frustration episodes or successful interventions.

Frame pipeline p95: **{video['frame_pipeline_ms']['p95']:.1f} ms**, median {video['frame_pipeline_ms']['median']:.1f} ms on the recorded CPU environment. This excludes source decoding, display, the 2 Hz sampling interval and three-frame stability delay; it does not measure game FPS, GPU or battery impact. App streaming applies stability gating separately from the mean-pooled clip evaluation.

## Project acceptance checks

| Check | Measured | Target | Result |
| --- | ---: | ---: | --- |
{rows}

Even passing quantitative checks would not approve production use. Mandatory open items are independent consented gamer videos, participant-disjoint target-context evaluation, paired participant-reported CMA/frustration, Indian-context evidence without inferring demographic attributes from faces, source-rights review, real target-OS camera and game-performance checks, and UI approval.

## Privacy and product behaviour

Camera and analysis are off by default. All runtime inference is local. Normal app use saves no raw frames, camera recordings or audio. User-requested command-line annotated output and screenshot flags are explicit research-output exceptions. Retaining derived summaries requires opt-in. Deleting app summaries does not delete imported media. Source loss, pause, break, end and close stop capture and clear expression cues. Mixed/unknown and manual-only use are supported.

## Reproduction and artifacts

See README.md, the two candidate folders, training-config.json, training-history.json, environment.json, model-selection.json, image-evaluation.json, video-evaluation.json, runtime-verification.json and release-gates.json. Source and data checksums are recorded. Third-party sources/licences are in ../third_party/NOTICES.md. Feature applicability is in ../docs/FEATURE-APPLICABILITY.md. Earlier persona interviews remain simulated and were never used as model training or validation data.

![Image confusion matrix](figures/image-confusion.png)
![External video confusion matrix](figures/video-confusion.png)
![Validation learning curves](figures/learning-curves.png)
![Test reliability](figures/classification-reliability.png)
'''
    (out/'MODEL-CARD.md').write_text(card)
    with PdfPages(out/'evaluation-report.pdf') as pdf:
        fig=plt.figure(figsize=(8.3,11.7));fig.text(.08,.94,'Checkpoint / expression model evaluation',fontsize=20,weight='bold');fig.text(.08,.90,'Research prototype / not production ready',fontsize=13)
        summary=f"Selected model: {selection['selected']}\n\nHeld-out images: {image['n']} eligible FER+ examples\nAccuracy: {pct(image['accuracy'])} / Macro-F1: {image['macro_f1']:.3f}\nSelective accuracy: {pct(image['selective']['accuracy'])} / coverage: {pct(image['selective']['coverage'])}\n\nExternal videos: {video['clips_attempted']} supported RAVDESS clips, four actors\nClip accuracy: {pct(v['accuracy'])} / supported-label Macro-F1: {v['macro_f1_supported_truth_classes']:.3f}\nPipeline p95: {video['frame_pipeline_ms']['p95']:.1f} ms (inference path only)\n\nExpressions are not gamer mood, frustration or continuous CMA.\nCMA remains player-reported. No automatic interventions are enabled.\n\nConfidence is calibrated on validation only. All accuracy results use\nheld-out data. Identity separation cannot be verified for FER+.\nFour acted-video subjects do not establish target population validity.\nData-rights, Indian-context, target-device and UI-approval gates remain.\n\nFull methods, per-class results, stress tests and source hashes:\nMODEL-CARD.md and the evaluation JSON artifacts."
        fig.text(.08,.84,summary,fontsize=11,va='top',linespacing=1.7);pdf.savefig(fig);plt.close(fig)
        for fig in figures:pdf.savefig(fig);plt.close(fig)
    print(json.dumps({'model_card':str(out/'MODEL-CARD.md'),'report':str(out/'evaluation-report.pdf'),'release_gates':gates},indent=2))


if __name__=='__main__':run()
