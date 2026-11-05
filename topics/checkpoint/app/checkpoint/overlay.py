"""A separate transparent top-level Qt companion: no injection or game hooks."""
from PySide6.QtCore import Qt, QPoint, QTimer
from PySide6.QtGui import QGuiApplication, QPainter, QColor, QFont, QPainterPath
from PySide6.QtWidgets import QWidget
from checkpoint.blob import PipWidget


class PipOverlay(QWidget):
    def __init__(self):
        super().__init__(None,Qt.WindowType.Tool|Qt.WindowType.FramelessWindowHint|Qt.WindowType.WindowStaysOnTopHint|Qt.WindowType.WindowDoesNotAcceptFocus|Qt.WindowType.WindowTransparentForInput)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground);self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setStyleSheet('background:transparent;');self.setWindowTitle('Pip');self.resize(164,190)
        self.blob=PipWidget(132);self.blob.setParent(self);self.blob.move(16,48)
        self.message='';self.message_until=0.;self.dragging=False;self.drag_offset=QPoint();self.editing=False
        self.setAccessibleName('Pip desktop companion · click-through while playing')
        self.place('bottom-right');self.expiry=QTimer(self);self.expiry.timeout.connect(self.clear_expired);self.expiry.start(500)

    def showEvent(self,event):
        super().showEvent(event)
        import sys
        if sys.platform=='win32':
            import ctypes
            from ctypes import wintypes
            user=ctypes.WinDLL('user32');get=user.GetWindowLongPtrW;set_style=user.SetWindowLongPtrW
            get.argtypes=[wintypes.HWND,ctypes.c_int];get.restype=ctypes.c_ssize_t
            set_style.argtypes=[wintypes.HWND,ctypes.c_int,ctypes.c_ssize_t];set_style.restype=ctypes.c_ssize_t
            hwnd=int(self.winId());style=get(hwnd,-20)|0x08000000|0x00080000|0x00000080
            style=(style&~0x20) if self.editing else (style|0x20)
            set_style(hwnd,-20,style)

    def place(self,corner):
        screen=QGuiApplication.primaryScreen()
        if not screen:return
        rect=screen.availableGeometry();left=corner.endswith('left');top=corner.startswith('top')
        self.move(rect.left()+16 if left else rect.right()-self.width()-16,rect.top()+16 if top else rect.bottom()-self.height()-16)

    def set_editable(self,enabled):
        self.editing=enabled;visible=self.isVisible();self.setWindowFlag(Qt.WindowType.WindowTransparentForInput,not enabled)
        self.setCursor(Qt.CursorShape.SizeAllCursor if enabled else Qt.CursorShape.ArrowCursor)
        if visible:self.show()

    def set_message(self,message,seconds=9):
        import time
        self.message=str(message)[:80];self.message_until=time.monotonic()+seconds;self.update()

    def clear_expired(self):
        import time
        if self.message and time.monotonic()>self.message_until:self.message='';self.update()

    def paintEvent(self,event):
        if not self.message and not self.editing:return
        p=QPainter(self);p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(Qt.PenStyle.NoPen);p.setBrush(QColor('#FFFCF4'));p.drawRoundedRect(3,3,self.width()-6,46,13,13)
        p.setPen(QColor('#34453E'));font=QFont('DM Sans');font.setPixelSize(11);p.setFont(font)
        p.drawText(10,7,self.width()-20,37,Qt.AlignmentFlag.AlignCenter|Qt.TextFlag.TextWordWrap,'Drag Pip here. Finish in the app.' if self.editing else self.message);p.end()

    def mousePressEvent(self,event):
        if self.editing and event.button()==Qt.MouseButton.LeftButton:self.dragging=True;self.drag_offset=event.globalPosition().toPoint()-self.pos()

    def mouseMoveEvent(self,event):
        if self.dragging:self.move(event.globalPosition().toPoint()-self.drag_offset)

    def mouseReleaseEvent(self,event):self.dragging=False
