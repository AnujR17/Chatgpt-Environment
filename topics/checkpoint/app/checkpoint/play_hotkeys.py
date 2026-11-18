"""Two explicit Windows shortcuts, without a keyboard hook or input recording."""
import sys
from PySide6.QtCore import QAbstractNativeEventFilter


class PlayHotkeys(QAbstractNativeEventFilter):
    def __init__(self, app, window, setback, mute):
        super().__init__()
        self.app=app;self.window=window;self.callbacks={0x5247:setback,0x5248:mute};self.registered=[];self.user=None

    def start(self):
        self.stop()
        if sys.platform!='win32':return False
        import ctypes
        from ctypes import wintypes
        self.user=ctypes.WinDLL('user32',use_last_error=True)
        self.user.RegisterHotKey.argtypes=[wintypes.HWND,ctypes.c_int,wintypes.UINT,wintypes.UINT]
        self.user.UnregisterHotKey.argtypes=[wintypes.HWND,ctypes.c_int]
        for key_id,vk in ((0x5247,0x77),(0x5248,0x78)):  # F8, F9
            if not self.user.RegisterHotKey(self.window,key_id,0x4003,vk):
                self.stop();return False
            self.registered.append(key_id)
        self.app.installNativeEventFilter(self);return True

    def stop(self):
        self.app.removeNativeEventFilter(self)
        if self.user:
            for key_id in self.registered:self.user.UnregisterHotKey(self.window,key_id)
        self.registered=[]

    def nativeEventFilter(self,event_type,message):
        if sys.platform=='win32' and self.registered:
            import ctypes
            from ctypes import wintypes
            msg=wintypes.MSG.from_address(int(message))
            if msg.message==0x0312 and msg.wParam in self.registered:
                self.callbacks[msg.wParam]();return True,0
        return False,0
