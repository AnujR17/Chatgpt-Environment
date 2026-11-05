"""Bounded capture with Windows backend fallbacks and independent face tracking."""
import sys
import threading
import time
import cv2
from PySide6.QtCore import QThread
from PySide6.QtGui import QImage


def open_camera(index, interrupted=lambda: False, *, platform=None):
    """Try APIs for the chosen device only; require a real frame before success."""
    windows=(platform or sys.platform)=='win32'
    backends=[(cv2.CAP_DSHOW,'DirectShow'),(cv2.CAP_MSMF,'Media Foundation'),(cv2.CAP_ANY,'Windows default')] if windows else [(cv2.CAP_ANY,'System camera')]
    attempts=[]
    for api,name in backends:
        if interrupted():raise InterruptedError('Camera opening cancelled')
        capture=None
        try:
            capture=cv2.VideoCapture(index,api)
            if capture.isOpened():
                capture.set(cv2.CAP_PROP_FRAME_WIDTH,640);capture.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
                # Some drivers need several reads to warm up. Do not force an unsupported FPS.
                for _ in range(30):
                    if interrupted():raise InterruptedError('Camera opening cancelled')
                    ok,frame=capture.read()
                    if ok and frame is not None and frame.size:
                        return capture,frame,name
                    time.sleep(.05)
                attempts.append(name+': no frames')
            else:attempts.append(name+': could not open')
        except InterruptedError:
            if capture is not None:capture.release()
            raise
        except (cv2.error,OSError) as ex:attempts.append(name+': '+str(ex))
        if capture is not None:capture.release()
    detail='; '.join(attempts)
    raise RuntimeError(f'Camera {index+1} could not supply video. Close other camera apps, check the privacy shutter and Windows Settings > Privacy & security > Camera > Let desktop apps access your camera, or select another camera. ({detail})')


class CaptureWorker(QThread):
    def __init__(self, source, *, analyze=False, frequency=2, generation=0, realtime=True,face_mapping=False,face_gain=1.5,hands=True,categories=True):
        super().__init__()
        self.source=source;self.analyze=analyze;self.frequency=max(.25,min(5,float(frequency)));self.generation=generation
        self.realtime=realtime;self.lock=threading.Lock();self.latest_image=None;self.latest_cue=None
        self.finished_reason='';self.error='';self.analysis_error='';self.frames=0;self.backend=''
        self.face_mapping=face_mapping;self.neutral_requested=threading.Event();self.face_gain=face_gain;self.hands=hands;self.categories=categories

    def take_latest(self):
        with self.lock:
            image,cue=self.latest_image,self.latest_cue;self.latest_image=None;self.latest_cue=None
        return image,cue

    def publish_preview(self,frame):
        code=cv2.COLOR_GRAY2RGB if frame.ndim==2 else cv2.COLOR_BGRA2RGB if frame.shape[2]==4 else cv2.COLOR_BGR2RGB
        rgb=cv2.cvtColor(frame,code)
        image=QImage(rgb.data,rgb.shape[1],rgb.shape[0],rgb.strides[0],QImage.Format.Format_RGB888).copy()
        with self.lock:self.latest_image=image

    def tracking_failed(self,ex):
        from checkpoint.cues import Cue
        self.analysis_error=str(ex)
        with self.lock:self.latest_cue=(self.generation,Cue('unavailable',reason='Face tracking unavailable. Camera preview remains available. '+str(ex)))

    def run(self):
        capture=None;model=None;smoother=None;first=None
        try:
            if isinstance(self.source,str) and '://' in self.source:raise ValueError('Only local video files and local camera devices are supported')
            if isinstance(self.source,int):
                capture,first,self.backend=open_camera(self.source,self.isInterruptionRequested)
            else:
                capture=cv2.VideoCapture(self.source)
                if not capture.isOpened():raise RuntimeError('The selected video could not be opened. Choose another local video file.')
                ok,first=capture.read()
                if not ok or first is None or not first.size:raise RuntimeError('The selected video has no readable frames.')
                self.backend='Local video'
            self.publish_preview(first);self.frames=1
            fps=capture.get(cv2.CAP_PROP_FPS)
            frame_period=1/min(30,max(1,fps if fps>0 else 15))
            if self.analyze and not self.isInterruptionRequested():
                try:
                    from checkpoint.runtime import FacePipeline,CueSmoother
                    if self.face_mapping:
                        from checkpoint.face_mapping import LandmarkPipeline
                        model=LandmarkPipeline(hands=self.hands,categories=self.categories);model.gain=self.face_gain
                    else:model=FacePipeline(pretrained=True);smoother=CueSmoother()
                except Exception as ex:self.tracking_failed(ex)
            next_analysis=0.;next_preview=0.
            while not self.isInterruptionRequested():
                t=time.monotonic()
                if first is not None:frame=first;first=None;ok=True
                else:
                    ok,frame=capture.read()
                    if ok:self.frames+=1
                if not ok or frame is None or not frame.size:
                    self.finished_reason='Video finished' if isinstance(self.source,str) else 'Camera disconnected. Close other camera apps and restart the selected camera.'
                    break
                # Publish preview before inference; an ML error must never remove the camera feed.
                if t>=next_preview:self.publish_preview(frame);next_preview=t+1/15
                if model is not None and t>=next_analysis:
                    try:
                        if self.face_mapping and self.neutral_requested.is_set():model.start_neutral();self.neutral_requested.clear()
                        cue=model.infer(frame)
                        if smoother is not None:cue=smoother.update(cue)
                        with self.lock:self.latest_cue=(self.generation,cue)
                    except Exception as ex:
                        self.tracking_failed(ex)
                        if hasattr(model,'close'):
                            try:model.close()
                            except Exception:pass
                        model=None
                    next_analysis=t+1/self.frequency
                if self.realtime:
                    remaining=frame_period-(time.monotonic()-t)
                    while remaining>0 and not self.isInterruptionRequested():
                        self.msleep(min(10,max(1,int(remaining*1000))));remaining=frame_period-(time.monotonic()-t)
        except InterruptedError:self.finished_reason='Camera opening cancelled'
        except Exception as ex:self.error=str(ex)
        finally:
            if model is not None and hasattr(model,'close'):
                try:model.close()
                except Exception:pass
            if capture is not None:capture.release()
            with self.lock:self.latest_image=None;self.latest_cue=None

    def stop(self, timeout=3000):
        self.requestInterruption();return self.wait(timeout)
