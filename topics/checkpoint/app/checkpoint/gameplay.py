"""Opt-in Windows game-window observation and experimental Getting Over It motion cues.

No injection, game-memory reads, inputs, recordings, or remote uploads. A possible
climb/fall describes camera motion; it is not a validated player-event classifier.
"""
from dataclasses import dataclass
import ctypes
from ctypes import wintypes
import sys
import threading

import cv2
import numpy as np
import psutil
from PySide6.QtCore import QThread, Signal


GAMES = {'gettingoverit.exe': 'Getting Over It', 'cs2.exe': 'Counter-Strike 2',
         'valorant-win64-shipping.exe': 'Valorant'}


@dataclass(frozen=True)
class ActiveGame:
    name: str | None
    hwnd: int = 0
    pid: int = 0
    status: str = 'No supported game in the foreground'


@dataclass(frozen=True)
class GameObservation:
    game: str | None
    status: str
    cue: str = ''


def active_game():
    if sys.platform != 'win32':
        return ActiveGame(None, status='Live game-window tracking requires Windows')
    user = ctypes.WinDLL('user32', use_last_error=True)
    user.GetForegroundWindow.restype = wintypes.HWND
    hwnd = user.GetForegroundWindow()
    pid = wintypes.DWORD()
    user.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
    user.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    try:
        name = GAMES.get(psutil.Process(pid.value).name().casefold())
    except (psutil.Error, OSError):
        name = None
    return ActiveGame(name, int(hwnd or 0), pid.value)


def capture_game(game):
    """Copy only the foreground supported game's client area; reject focus changes."""
    if sys.platform != 'win32' or game.name != 'Getting Over It' or not game.hwnd:
        return None
    current = active_game()
    if current.hwnd != game.hwnd or current.pid != game.pid or current.name != game.name:
        return None
    user = ctypes.WinDLL('user32', use_last_error=True)
    gdi = ctypes.WinDLL('gdi32', use_last_error=True)
    user.GetClientRect.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.RECT)]
    user.GetDC.argtypes = [wintypes.HWND]; user.GetDC.restype = wintypes.HDC
    user.ReleaseDC.argtypes = [wintypes.HWND, wintypes.HDC]
    gdi.CreateCompatibleDC.argtypes = [wintypes.HDC]; gdi.CreateCompatibleDC.restype = wintypes.HDC
    gdi.CreateCompatibleBitmap.argtypes = [wintypes.HDC, ctypes.c_int, ctypes.c_int]; gdi.CreateCompatibleBitmap.restype = wintypes.HBITMAP
    gdi.SelectObject.argtypes = [wintypes.HDC, wintypes.HANDLE]; gdi.SelectObject.restype = wintypes.HANDLE
    gdi.DeleteObject.argtypes = [wintypes.HANDLE]; gdi.DeleteDC.argtypes = [wintypes.HDC]
    gdi.StretchBlt.argtypes = [wintypes.HDC, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
                              wintypes.HDC, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, wintypes.DWORD]
    gdi.GetDIBits.argtypes = [wintypes.HDC, wintypes.HBITMAP, wintypes.UINT, wintypes.UINT,
                            ctypes.c_void_p, ctypes.c_void_p, wintypes.UINT]
    rect = wintypes.RECT()
    if not user.GetClientRect(game.hwnd, ctypes.byref(rect)):
        return None
    w, h = rect.right, rect.bottom
    if min(w, h) < 100 or w > 16384 or h > 16384:
        return None
    scale = min(1., 640 / w, 480 / h); width = int(w * scale); height = int(h * scale)
    source = user.GetDC(game.hwnd)
    if not source: return None
    target = gdi.CreateCompatibleDC(source); bitmap = None; previous = None
    try:
        if not target: return None
        bitmap = gdi.CreateCompatibleBitmap(source, width, height)
        if not bitmap: return None
        previous = gdi.SelectObject(target, bitmap)
        if not gdi.StretchBlt(target, 0, 0, width, height, source, 0, 0, w, h, 0x00CC0020):
            return None
        # GetDIBits requires the bitmap not to be selected into a DC.
        gdi.SelectObject(target, previous); previous = None
        header = bytearray(40)
        import struct
        struct.pack_into('<IiiHHIIiiII', header, 0, 40, width, -height, 1, 32, 0, width * height * 4, 0, 0, 0, 0)
        info = (ctypes.c_ubyte * len(header)).from_buffer(header)
        pixels = np.empty((height, width, 4), dtype=np.uint8)
        if gdi.GetDIBits(target, bitmap, 0, height, pixels.ctypes.data, ctypes.byref(info), 0) != height:
            return None
        after = active_game()
        if after.hwnd != game.hwnd or after.pid != game.pid or after.name != game.name:
            return None
        return cv2.cvtColor(pixels, cv2.COLOR_BGRA2BGR)
    finally:
        if previous: gdi.SelectObject(target, previous)
        if bitmap: gdi.DeleteObject(bitmap)
        if target: gdi.DeleteDC(target)
        user.ReleaseDC(game.hwnd, source)


class GettingOverItAnalyzer:
    def __init__(self):
        self.previous = None; self.direction = 0; self.streak = 0; self.reference = None
        self.orb = cv2.ORB_create(nfeatures=700)

    def reset_motion(self):
        self.previous = None; self.direction = 0; self.streak = 0

    def clear(self):
        self.reset_motion(); self.reference = None

    def mark_start(self, frame):
        gray = self._gray(frame)
        keys, descriptors = self.orb.detectAndCompute(gray, None)
        if descriptors is None or len(keys) < 35:
            return False
        self.reference = (keys, descriptors, gray.shape)
        return True

    @staticmethod
    def _gray(frame):
        h, w = frame.shape[:2]; scale = min(1., 640 / w)
        small = cv2.resize(frame, (int(w * scale), int(h * scale)))
        return cv2.cvtColor(small, cv2.COLOR_BGR2GRAY) if small.ndim == 3 else small

    def _matches_start(self, gray):
        if self.reference is None or gray.shape != self.reference[2]: return False
        keys, descriptors = self.orb.detectAndCompute(gray, None)
        if descriptors is None or len(keys) < 35: return False
        reference_keys, reference_descriptors, _ = self.reference
        matches = cv2.BFMatcher(cv2.NORM_HAMMING).knnMatch(reference_descriptors, descriptors, k=2)
        good = [a for pair in matches if len(pair) == 2 for a, b in [pair] if a.distance < .7 * b.distance]
        if len(good) < 30: return False
        src = np.float32([reference_keys[m.queryIdx].pt for m in good])
        dst = np.float32([keys[m.trainIdx].pt for m in good])
        matrix, mask = cv2.findHomography(src, dst, cv2.RANSAC, 3.)
        if matrix is None or mask.mean() < .75: return False
        # Match the actual marked view, rather than any overlapping section of a scene.
        return (abs(matrix[0, 0] - 1) < .08 and abs(matrix[1, 1] - 1) < .08
                and abs(matrix[0, 1]) < .06 and abs(matrix[1, 0]) < .06
                and abs(matrix[0, 2]) < gray.shape[1] * .05
                and abs(matrix[1, 2]) < gray.shape[0] * .05)

    def observe(self, frame):
        if frame is None or frame.size == 0:
            self.reset_motion(); return 'Screen unavailable'
        gray = self._gray(frame)
        if gray.std() < 7:
            self.reset_motion(); return 'Screen unavailable or too little visual detail'
        old = self.previous; self.previous = gray
        if self._matches_start(gray):
            self.direction = 0; self.streak = 0
            return 'Marked start view visible · no restart inferred'
        if old is None or old.shape != gray.shape:
            self.direction = 0; self.streak = 0
            return 'Observing the game view'
        points = cv2.goodFeaturesToTrack(old, 180, .02, 12)
        if points is None or len(points) < 35:
            self.streak = 0; return 'Movement uncertain · too few scene features'
        moved, status, error = cv2.calcOpticalFlowPyrLK(old, gray, points, None, winSize=(31, 31), maxLevel=3)
        if moved is None:
            self.streak = 0; return 'Movement uncertain'
        backward, reverse_status, _ = cv2.calcOpticalFlowPyrLK(gray, old, moved, None, winSize=(31, 31), maxLevel=3)
        if backward is None:
            self.streak = 0; return 'Movement uncertain'
        good = (status.ravel() == 1) & (reverse_status.ravel() == 1) & (error.ravel() < 25)
        good &= np.linalg.norm((points - backward).reshape(-1, 2), axis=1) < 1.5
        if good.sum() < 35 or good.mean() < .5:
            self.streak = 0; return 'View changed · movement uncertain'
        delta = (moved - points).reshape(-1, 2)[good]
        dx, dy = np.median(delta, axis=0)
        coherent = np.mean(np.abs(delta[:, 1] - dy) < max(2., abs(dy) * .4))
        if abs(dy) < gray.shape[0] * .008 or abs(dy) < abs(dx) * 1.4 or coherent < .65:
            self.direction = 0; self.streak = 0; return 'No clear vertical camera movement'
        direction = 1 if dy > 0 else -1
        self.streak = self.streak + 1 if direction == self.direction else 1; self.direction = direction
        if self.streak < 3: return 'Checking sustained camera movement'
        return ('Possible climb · camera rising' if direction > 0 else 'Possible fall · camera descending')


class GameWorker(QThread):
    observation = Signal(object)

    def __init__(self, *, screen=False, detector=active_game, capture=capture_game):
        super().__init__(); self.screen = screen; self.detector = detector; self.capture = capture
        self.mark_requested = threading.Event(); self.analyzer = GettingOverItAnalyzer(); self.last_pid = None
        self.foreground = ActiveGame(None)

    def run(self):
        try:
            while not self.isInterruptionRequested():
                game = self.detector()
                self.foreground = game
                if game.name == 'Getting Over It':
                    if game.pid != self.last_pid:
                        self.analyzer.clear(); self.last_pid = game.pid
                else:
                    self.analyzer.reset_motion()
                cue = ''
                if self.screen and game.name == 'Getting Over It':
                    frame = self.capture(game)
                    if frame is not None and self.mark_requested.is_set():
                        self.mark_requested.clear()
                        cue = 'Start view marked in memory' if self.analyzer.mark_start(frame) else 'Could not mark start view · try a detailed scene'
                    else: cue = self.analyzer.observe(frame)
                elif self.screen and game.name:
                    cue = 'Screen events supported only for Getting Over It'
                self.observation.emit(GameObservation(game.name, 'Foreground process detected' if game.name else game.status, cue))
                for _ in range(10):
                    if self.isInterruptionRequested(): break
                    self.msleep(50)
        except Exception as ex:
            self.observation.emit(GameObservation(None, 'Game tracking stopped: ' + str(ex)))
        finally:
            self.analyzer.clear();self.foreground=ActiveGame(None)

    def stop(self):
        self.requestInterruption(); return self.wait(2000)


def main():
    """Inspect an explicit local gameplay recording; print derived cues only."""
    import argparse
    import json
    parser = argparse.ArgumentParser(description='Experimental Getting Over It camera-motion analysis; no emotion inference')
    parser.add_argument('--video', required=True, help='Local gameplay recording')
    args = parser.parse_args()
    if '://' in args.video: parser.error('Choose a local recording')
    capture = cv2.VideoCapture(args.video)
    if not capture.isOpened(): parser.error('Recording could not be opened')
    analyzer = GettingOverItAnalyzer()
    try:
        fps = capture.get(cv2.CAP_PROP_FPS)
        if not np.isfinite(fps) or fps < 1: fps = 30.
        step = max(1, round(fps / 2)); frame_index = 0
        while True:
            ok, frame = capture.read()
            if not ok: break
            if frame_index % step == 0:
                print(json.dumps({'seconds': round(frame_index / fps, 2), 'cue': analyzer.observe(frame),
                                  'status': 'experimental heuristic; not validated game-event recognition'}))
            frame_index += 1
    finally:
        capture.release(); analyzer.clear()


if __name__ == '__main__':
    main()
