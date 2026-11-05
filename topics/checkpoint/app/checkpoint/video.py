"""Offline video inference with explicit output recording, or local camera selection."""
import argparse
import json
import time
from pathlib import Path
import cv2
from checkpoint.runtime import FacePipeline, CueSmoother


def main():
    p=argparse.ArgumentParser();source=p.add_mutually_exclusive_group(required=True);source.add_argument("--video",type=Path);source.add_argument("--camera",type=int)
    p.add_argument("--jsonl",type=Path);p.add_argument("--annotated-out",type=Path);p.add_argument("--max-frames",type=int,default=0);p.add_argument("--hz",type=float,default=2);args=p.parse_args()
    if not .25<=args.hz<=5:p.error("--hz must be between 0.25 and 5")
    if args.video and not args.video.is_file():p.error("Local video does not exist")
    if args.video and args.annotated_out and args.video.resolve()==args.annotated_out.resolve():p.error("Output must not overwrite the source video")
    for output in [args.jsonl,args.annotated_out]:
        if output and output.exists():p.error("Output exists; choose a new path rather than overwrite a recording")
    cap=cv2.VideoCapture(str(args.video) if args.video else args.camera)
    if not cap.isOpened():raise RuntimeError("Capture could not be opened; check file or camera permission")
    pipeline=FacePipeline();smoother=CueSmoother();fps=cap.get(cv2.CAP_PROP_FPS) or 15;writer=None;stream=None;count=0;next_at=0.;cue=None;start=time.monotonic()
    try:
        if args.jsonl:args.jsonl.parent.mkdir(parents=True,exist_ok=True);stream=args.jsonl.open("x")
        while True:
            ok,frame=cap.read()
            if not ok:break
            t=count/fps if args.video else time.monotonic()-start
            if t>=next_at:
                cue=smoother.update(pipeline.infer(frame));next_at=t+1/args.hz
                row={"seconds":round(t,3),**cue.to_dict()}
                if stream:stream.write(json.dumps(row)+"\n")
                else:print(json.dumps(row),flush=True)
            if args.annotated_out:
                if writer is None:
                    args.annotated_out.parent.mkdir(parents=True,exist_ok=True);writer=cv2.VideoWriter(str(args.annotated_out),cv2.VideoWriter_fourcc(*"mp4v"),fps,(frame.shape[1],frame.shape[0]))
                    if not writer.isOpened():raise RuntimeError("Video output codec unavailable")
                text="Expression: "+(cue.expression if cue and cue.expression else "uncertain / unavailable")
                cv2.rectangle(frame,(0,0),(frame.shape[1],100),(15,17,19),-1)
                cv2.putText(frame,text,(18,36),cv2.FONT_HERSHEY_SIMPLEX,.8,(210,235,190),2)
                cv2.putText(frame,"Research cue. CMA requires a player check-in.",(18,74),cv2.FONT_HERSHEY_SIMPLEX,.65,(230,230,230),1)
                if cue and cue.face_box:
                    x,y,w,h=cue.face_box;cv2.rectangle(frame,(x,y),(x+w,y+h),(155,200,170),2)
                writer.write(frame)
            count+=1
            if args.max_frames and count>=args.max_frames:break
    finally:
        cap.release()
        if writer:writer.release()
        if stream:stream.close()


if __name__=="__main__":main()
