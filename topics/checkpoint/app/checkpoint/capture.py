"""One bounded worker; latest-frame storage prevents a video-frame queue backlog."""
import threading
import time
import cv2
from PySide6.QtCore import QThread
from PySide6.QtGui import QImage


class CaptureWorker(QThread):
    def __init__(self, source, *, analyze=False, frequency=2, generation=0, realtime=True):
        super().__init__()
        self.source=source;self.analyze=analyze;self.frequency=max(.25,min(5,float(frequency)));self.generation=generation
        self.realtime=realtime;self.lock=threading.Lock();self.latest_image=None;self.latest_cue=None
        self.finished_reason="";self.error="";self.frames=0

    def take_latest(self):
        with self.lock:
            image,cue=self.latest_image,self.latest_cue;self.latest_image=None;self.latest_cue=None
        return image,cue

    def run(self):
        capture=None
        try:
            if isinstance(self.source,str) and "://" in self.source:raise ValueError("Only local video files and local camera devices are supported")
            capture=cv2.VideoCapture(self.source)
            if not capture.isOpened():raise RuntimeError("Capture source could not be opened. Check OS camera permission or choose a local video.")
            if isinstance(self.source,int):
                capture.set(cv2.CAP_PROP_FRAME_WIDTH,640);capture.set(cv2.CAP_PROP_FRAME_HEIGHT,480);capture.set(cv2.CAP_PROP_FPS,15)
            fps=capture.get(cv2.CAP_PROP_FPS)
            frame_period=1/min(30,max(1,fps if fps>0 else 15))
            if self.analyze:
                from checkpoint.runtime import FacePipeline, CueSmoother
                model=FacePipeline();smoother=CueSmoother()
            else:model=None;smoother=None
            next_analysis=0.;next_preview=0.
            while not self.isInterruptionRequested():
                t=time.monotonic();ok,frame=capture.read()
                if not ok:
                    self.finished_reason="Video finished" if isinstance(self.source,str) else "Camera disconnected"
                    break
                self.frames+=1
                if self.analyze and t>=next_analysis:
                    cue=smoother.update(model.infer(frame));next_analysis=t+1/self.frequency
                    with self.lock:self.latest_cue=(self.generation,cue)
                if t>=next_preview:
                    rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                    image=QImage(rgb.data,rgb.shape[1],rgb.shape[0],rgb.strides[0],QImage.Format.Format_RGB888).copy()
                    with self.lock:self.latest_image=image
                    next_preview=t+1/15
                if self.realtime:
                    # Thread-local, interruptible pacing; UI never sleeps on video reads.
                    remaining=frame_period-(time.monotonic()-t)
                    while remaining>0 and not self.isInterruptionRequested():
                        self.msleep(min(10,max(1,int(remaining*1000))));remaining=frame_period-(time.monotonic()-t)
        except Exception as ex:
            self.error=str(ex)
        finally:
            if capture is not None:capture.release()
            with self.lock:self.latest_image=None;self.latest_cue=None

    def stop(self, timeout=3000):
        self.requestInterruption()
        return self.wait(timeout)
