"""Opt-in game-focused Raw Input timing. No characters, key identities or raw paths are exported."""
from collections import deque
import ctypes
from ctypes import wintypes
import math
import sys
import struct
import time
from PySide6.QtCore import QAbstractNativeEventFilter


class RawHeader(ctypes.Structure):
    _fields_=[('kind',wintypes.DWORD),('size',wintypes.DWORD),('device',wintypes.HANDLE),('param',wintypes.WPARAM)]


class Activity:
    def __init__(self):self.samples=deque(maxlen=120);self.last_input=None;self.pressed={}
    def add(self,now,motion=0.,clicks=0,keys=0,hold=0.):
        tick=math.floor(now*10)/10
        if not self.samples or self.samples[-1][0]!=tick:self.samples.append([tick,0.,0,0,0.,0])
        row=self.samples[-1];row[1]+=motion;row[2]+=clicks;row[3]+=keys;row[4]+=hold;row[5]+=int(hold>0)
    def mouse(self,dx,dy,clicks=0,now=None):
        now=time.monotonic() if now is None else now
        if dx or dy or clicks:self.add(now,motion=math.hypot(dx,dy),clicks=clicks);self.last_input=now
    def key(self,code,released,now=None):
        now=time.monotonic() if now is None else now
        if released:
            start=self.pressed.pop(code,None)
            if start is not None:self.add(now,hold=min(10.,max(0.,now-start)))
        elif code not in self.pressed:
            self.pressed[code]=now;self.add(now,keys=1);self.last_input=now
    def snapshot(self,now=None):
        now=time.monotonic() if now is None else now
        while self.samples and now-self.samples[0][0]>10:self.samples.popleft()
        span=10.;hold_count=sum(x[5] for x in self.samples)
        return {'status':'Game-focused timing · not an emotion estimate','mouse_motion_per_second':round(sum(x[1] for x in self.samples)/span,1),
            'clicks_per_second':round(sum(x[2] for x in self.samples)/span,2),'key_presses_per_second':round(sum(x[3] for x in self.samples)/span,2),
            'mean_key_hold_seconds':round(sum(x[4] for x in self.samples)/hold_count,3) if hold_count else None,
            'idle_seconds':round(now-self.last_input,1) if self.last_input is not None else None}
    def clear(self):self.samples.clear();self.pressed.clear();self.last_input=None


class InputObserver(QAbstractNativeEventFilter):
    def __init__(self,app,hwnd):
        super().__init__();self.app=app;self.hwnd=hwnd;self.target=0;self.activity=Activity();self.enabled=False
    def start(self):
        if sys.platform!='win32':raise OSError('Live input observation requires Windows')
        class Device(ctypes.Structure):_fields_=[('page',wintypes.USHORT),('usage',wintypes.USHORT),('flags',wintypes.DWORD),('target',wintypes.HWND)]
        self.Device=Device;user=ctypes.WinDLL('user32',use_last_error=True)
        user.RegisterRawInputDevices.argtypes=[ctypes.POINTER(Device),wintypes.UINT,wintypes.UINT]
        devices=(Device*2)(Device(1,2,0x100,self.hwnd),Device(1,6,0x100,self.hwnd))
        if not user.RegisterRawInputDevices(devices,2,ctypes.sizeof(Device)):raise OSError('Windows Raw Input registration failed')
        self.user=user;user.GetForegroundWindow.restype=wintypes.HWND
        user.GetRawInputData.argtypes=[wintypes.HANDLE,wintypes.UINT,ctypes.c_void_p,ctypes.POINTER(wintypes.UINT),wintypes.UINT]
        self.app.installNativeEventFilter(self);self.enabled=True
    def set_target(self,hwnd):
        if hwnd!=self.target:self.activity.clear()
        self.target=hwnd
    def nativeEventFilter(self,event_type,message):
        if not self.enabled:return False,0
        try:
            msg=wintypes.MSG.from_address(int(message))
            if msg.message!=0x00FF:return False,0
            if not self.target or int(self.user.GetForegroundWindow() or 0)!=self.target:
                self.activity.clear();return False,0
            Header=RawHeader
            size=wintypes.UINT()
            if self.user.GetRawInputData(msg.lParam,0x10000003,None,ctypes.byref(size),ctypes.sizeof(Header))!=0:return False,0
            if size.value<ctypes.sizeof(Header) or size.value>1024:return False,0
            data=ctypes.create_string_buffer(size.value)
            if self.user.GetRawInputData(msg.lParam,0x10000003,data,ctypes.byref(size),ctypes.sizeof(Header))!=size.value:return False,0
            header=Header.from_buffer_copy(data);offset=ctypes.sizeof(Header)
            if header.kind==0 and size.value>=offset+24:
                flags=struct.unpack_from('<H',data,offset)[0];buttons=struct.unpack_from('<H',data,offset+4)[0]
                dx,dy=struct.unpack_from('<ii',data,offset+12)
                self.activity.mouse(dx if not flags&1 else 0,dy if not flags&1 else 0,sum(bool(buttons&b) for b in (1,4,16,64,256)))
            elif header.kind==1 and size.value>=offset+16:
                code,flags=struct.unpack_from('<HH',data,offset)
                self.activity.key((code,flags&6),bool(flags&1))
        except (ValueError,OSError,TypeError,struct.error):pass
        return False,0
    def stop(self):
        if self.enabled:
            devices=(self.Device*2)(self.Device(1,2,1,None),self.Device(1,6,1,None))
            self.user.RegisterRawInputDevices(devices,2,ctypes.sizeof(self.Device));self.app.removeNativeEventFilter(self)
        self.enabled=False;self.target=0;self.activity.clear()
