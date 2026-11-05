"""Nori: transparent no-focus overlay, modifier drag and remembered placement."""
from pathlib import Path
import sys
import time
from PySide6.QtCore import Qt,QPoint,QTimer,QSettings
from PySide6.QtGui import QGuiApplication,QPainter,QColor,QFont
from PySide6.QtWidgets import QWidget
from checkpoint.blob import NoriWidget


class NoriOverlay(QWidget):
    def __init__(self):
        super().__init__(None,Qt.WindowType.Tool|Qt.WindowType.FramelessWindowHint|Qt.WindowType.WindowStaysOnTopHint|Qt.WindowType.WindowDoesNotAcceptFocus|Qt.WindowType.WindowTransparentForInput)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground);self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setStyleSheet('background:transparent;');self.setWindowTitle('Nori');self.resize(164,190)
        self.blob=NoriWidget(132);self.blob.setParent(self);self.blob.move(16,48);self.blob.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.message='';self.message_until=0.;self.dragging=False;self.drag_offset=QPoint();self.editing=False;self.manual_until=0.;self.preference_file=None;self.recreating=False
        self.setAccessibleName('Nori desktop companion · hold Ctrl+Alt to drag; release to lock');self.place('bottom-right')
        self.expiry=QTimer(self);self.expiry.timeout.connect(self.clear_expired);self.expiry.start(500)
        self.modifiers=QTimer(self);self.modifiers.setInterval(50);self.modifiers.timeout.connect(self.check_modifiers)

    def showEvent(self,event):
        super().showEvent(event);self.modifiers.start()
        if sys.platform=='win32':
            import ctypes
            from ctypes import wintypes
            user=ctypes.WinDLL('user32');get=user.GetWindowLongPtrW;set_style=user.SetWindowLongPtrW
            get.argtypes=[wintypes.HWND,ctypes.c_int];get.restype=ctypes.c_ssize_t
            set_style.argtypes=[wintypes.HWND,ctypes.c_int,ctypes.c_ssize_t];set_style.restype=ctypes.c_ssize_t
            hwnd=int(self.winId());style=get(hwnd,-20)|0x08000000|0x00080000|0x00000080
            set_style(hwnd,-20,(style&~0x20) if self.editing else (style|0x20))

    def hideEvent(self,event):
        self.modifiers.stop()
        if not self.recreating:self.manual_until=0.
        super().hideEvent(event)

    def place(self,corner):
        screen=QGuiApplication.primaryScreen()
        if not screen:return
        rect=screen.availableGeometry();left=corner.endswith('left');top=corner.startswith('top')
        self.move(rect.left()+16 if left else rect.right()-self.width()-16,rect.top()+16 if top else rect.bottom()-self.height()-16);self.remember()

    def restore_position(self,path):
        self.preference_file=Path(path);settings=QSettings(str(path),QSettings.Format.IniFormat);position=settings.value('overlay/position')
        if isinstance(position,QPoint):self.move(position);self.clamp_position()

    def clamp_position(self):
        center=self.pos()+QPoint(self.width()//2,self.height()//2);screen=QGuiApplication.screenAt(center)
        if screen is None:screen=QGuiApplication.primaryScreen()
        if screen:
            r=screen.availableGeometry();self.move(max(r.left(),min(r.right()-self.width()+1,self.x())),max(r.top(),min(r.bottom()-self.height()+1,self.y())))

    def remember(self):
        if self.preference_file is None:return
        self.preference_file.parent.mkdir(parents=True,exist_ok=True)
        settings=QSettings(str(self.preference_file),QSettings.Format.IniFormat);settings.setValue('overlay/position',self.pos());settings.sync()

    def begin_move(self):self.manual_until=time.monotonic()+30;self.set_editable(True)

    def set_editable(self,enabled):
        if enabled==self.editing:return
        self.editing=enabled;visible=self.isVisible();position=self.pos();self.recreating=True;self.setWindowFlag(Qt.WindowType.WindowTransparentForInput,not enabled)
        self.setCursor(Qt.CursorShape.SizeAllCursor if enabled else Qt.CursorShape.ArrowCursor)
        if visible:self.show();self.move(position)
        self.recreating=False;self.update()

    def check_modifiers(self):
        if sys.platform=='win32':
            import ctypes
            key=ctypes.windll.user32.GetAsyncKeyState
            held=bool(key(0x11)&0x8000 and key(0x12)&0x8000)
            if self.dragging and not key(1)&0x8000:self.finish_move();return
        else:
            keys=QGuiApplication.keyboardModifiers();held=bool(keys&Qt.KeyboardModifier.ControlModifier and keys&Qt.KeyboardModifier.AltModifier)
        self.set_editable(bool(held or self.dragging or time.monotonic()<self.manual_until))

    def finish_move(self):
        self.dragging=False;self.manual_until=0.;self.clamp_position();self.remember();self.set_editable(False)

    def set_message(self,message,seconds=9):self.message=str(message)[:80];self.message_until=time.monotonic()+seconds;self.update()

    def clear_expired(self):
        if self.message and time.monotonic()>self.message_until:self.message='';self.update()
        if self.editing and not self.dragging:self.check_modifiers()

    def paintEvent(self,event):
        if not self.message and not self.editing:return
        p=QPainter(self);p.setRenderHint(QPainter.RenderHint.Antialiasing);p.setPen(Qt.PenStyle.NoPen);p.setBrush(QColor('#FFFCF4'));p.drawRoundedRect(3,3,self.width()-6,46,13,13)
        p.setPen(QColor('#34453E'));font=QFont('DM Sans');font.setPixelSize(11);p.setFont(font)
        p.drawText(10,7,self.width()-20,37,Qt.AlignmentFlag.AlignCenter|Qt.TextFlag.TextWordWrap,'Drag Nori; release to lock' if self.editing else self.message);p.end()

    def mousePressEvent(self,event):
        if self.editing and event.button()==Qt.MouseButton.LeftButton:self.dragging=True;self.drag_offset=event.globalPosition().toPoint()-self.pos()
    def mouseMoveEvent(self,event):
        if self.dragging:self.move(event.globalPosition().toPoint()-self.drag_offset)
    def mouseReleaseEvent(self,event):
        if self.dragging:self.finish_move()


PipOverlay=NoriOverlay
