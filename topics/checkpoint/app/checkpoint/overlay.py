"""Nori: frameless companion with readable state, timer and deliberate click controls."""
from pathlib import Path
import sys,time
from PySide6.QtCore import Qt,QPoint,QTimer,QSettings,QRect,Signal
from PySide6.QtGui import QGuiApplication,QPainter,QColor,QFont,QRegion,QPainterPath
from PySide6.QtWidgets import QWidget,QLabel,QMenu
from checkpoint.blob import NoriWidget
from checkpoint.primary import PRIMARY_KEYS,PRIMARY_LABELS,primary_key

class NoriOverlay(QWidget):
    actionRequested=Signal(str)
    def __init__(self):
        super().__init__(None,Qt.WindowType.Tool|Qt.WindowType.FramelessWindowHint|Qt.WindowType.WindowStaysOnTopHint|Qt.WindowType.WindowDoesNotAcceptFocus)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground);self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setStyleSheet('background:transparent;');self.setWindowTitle('Nori');self.resize(220,330)
        self.blob=NoriWidget(160);self.blob.setParent(self);self.blob.move(30,66);self.blob.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.expression_label='Neutral';self.message='';self.message_until=0.;self.dragging=False;self.drag_offset=QPoint();self.editing=False;self.manual_until=0.;self.preference_file=None;self.recreating=False;self.pressed=False;self.press_position=QPoint()
        self.session_active=True;self.break_active=False;self.reminders_enabled=False;self.menu=None
        self.name_label=self.make_label(18,True,QRect(24,225,172,28))
        self.timer_caption=self.make_label(12,False,QRect(24,263,172,18))
        self.timer_value=self.make_label(30,True,QRect(24,281,172,35))
        self.update_status('neutral','Take a break','0:30')
        self.setAccessibleName('Nori. Click for check-in and break controls. Drag to move.');self.setCursor(Qt.CursorShape.PointingHandCursor);self.place('bottom-right')
        self.expiry=QTimer(self);self.expiry.timeout.connect(self.clear_expired);self.expiry.start(250)
        self.modifiers=QTimer(self);self.modifiers.setInterval(50);self.modifiers.timeout.connect(self.check_modifiers)

    def make_label(self,size,bold,rect):
        label=QLabel(self);label.setGeometry(rect);label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font=QFont('DM Sans');font.setPixelSize(size);font.setBold(bold);label.setFont(font)
        label.setStyleSheet('background:transparent;color:#29334b;border:0;padding:0;');label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        return label

    def update_status(self,emotion,caption,value,*,active=True,paused=False,reminders=False,camera=False):
        self.expression_label=PRIMARY_LABELS[primary_key(emotion)];self.name_label.setText(self.expression_label)
        self.timer_caption.setText(caption);self.timer_value.setText(value)
        self.session_active=active;self.break_active=paused;self.reminders_enabled=reminders;self.has_camera=camera
        self.update_mask();self.update()

    def update_mask(self):
        path=QPainterPath();path.addRoundedRect(32,67,156,158,55,55)
        region=QRegion(path.toFillPolygon().toPolygon())|QRegion(QRect(23,223,174,32))|QRegion(QRect(23,258,174,64))
        if self.message or self.editing:region=region|QRegion(QRect(5,3,210,61))
        if getattr(self,'_mask_region',None)!=region:
            self._mask_region=region;self.setMask(region)

    def showEvent(self,event):
        super().showEvent(event);self.modifiers.start()
        if sys.platform=='win32':
            import ctypes
            from ctypes import wintypes
            user=ctypes.WinDLL('user32');get=user.GetWindowLongPtrW;set_style=user.SetWindowLongPtrW
            get.argtypes=[wintypes.HWND,ctypes.c_int];get.restype=ctypes.c_ssize_t
            set_style.argtypes=[wintypes.HWND,ctypes.c_int,ctypes.c_ssize_t];set_style.restype=ctypes.c_ssize_t
            hwnd=int(self.winId());set_style(hwnd,-20,(get(hwnd,-20)|0x08000000|0x00080000|0x00000080)&~0x20)

    def hideEvent(self,event):
        self.modifiers.stop()
        if not self.recreating:self.manual_until=0.
        super().hideEvent(event)

    def place(self,corner):
        screen=QGuiApplication.primaryScreen()
        if screen:
            r=screen.availableGeometry();self.move(r.left()+16 if corner.endswith('left') else r.right()-self.width()-16,r.top()+16 if corner.startswith('top') else r.bottom()-self.height()-16);self.remember()

    def restore_position(self,path):
        self.preference_file=Path(path);position=QSettings(str(path),QSettings.Format.IniFormat).value('overlay/position')
        if isinstance(position,QPoint):self.move(position);self.clamp_position()

    def clamp_position(self):
        screen=QGuiApplication.screenAt(self.pos()+QPoint(self.width()//2,self.height()//2)) or QGuiApplication.primaryScreen()
        if screen:
            r=screen.availableGeometry();self.move(max(r.left(),min(r.right()-self.width()+1,self.x())),max(r.top(),min(r.bottom()-self.height()+1,self.y())))

    def remember(self):
        if self.preference_file:
            self.preference_file.parent.mkdir(parents=True,exist_ok=True);settings=QSettings(str(self.preference_file),QSettings.Format.IniFormat);settings.setValue('overlay/position',self.pos());settings.sync()

    def begin_move(self):self.manual_until=time.monotonic()+30;self.set_editable(True)
    def set_editable(self,enabled):
        self.editing=enabled;self.setCursor(Qt.CursorShape.SizeAllCursor if enabled else Qt.CursorShape.PointingHandCursor);self.update_mask();self.update()

    def check_modifiers(self):
        if sys.platform=='win32':
            import ctypes
            key=ctypes.windll.user32.GetAsyncKeyState;held=bool(key(0x11)&0x8000 and key(0x12)&0x8000)
            if self.dragging and not key(1)&0x8000:self.finish_move();return
        else:
            keys=QGuiApplication.keyboardModifiers();held=bool(keys&Qt.KeyboardModifier.ControlModifier and keys&Qt.KeyboardModifier.AltModifier)
        self.set_editable(bool(held or self.dragging or time.monotonic()<self.manual_until))

    def finish_move(self):
        self.dragging=False;self.manual_until=0.;self.clamp_position();self.remember();self.set_editable(False)

    def set_message(self,message,seconds=9):
        self.message=str(message)[:100];self.message_until=time.monotonic()+seconds;self.update_mask();self.update()

    def clear_expired(self):
        if self.message and time.monotonic()>self.message_until:self.message='';self.update_mask();self.update()
        if self.editing and not self.dragging:self.check_modifiers()

    def emit_action(self,command):QTimer.singleShot(0,lambda:self.actionRequested.emit(command))
    def open_controls(self):
        menu=QMenu(self);self.menu=menu
        menu.setStyleSheet('QMenu{background:#FFFCF4;color:#29334b;border:1px solid #CCD4C6;border-radius:8px;padding:6px;font:14px \"DM Sans\";}QMenu::item{padding:9px 18px;border-radius:5px;}QMenu::item:selected{background:#DFE9D8;}QMenu::item:disabled{color:#969b96;}QMenu::separator{height:1px;background:#D5DACE;margin:5px;}')
        def add(target,title,command,enabled=True):
            action=target.addAction(title);action.setData(command);action.setEnabled(enabled);action.triggered.connect(lambda checked=False,c=command:self.emit_action(c));return action
        check=menu.addMenu('Check in');check.setEnabled(self.session_active)
        for key in PRIMARY_KEYS:add(check,PRIMARY_LABELS[key],'checkin:'+key)
        if getattr(self,'has_camera',False):add(check,'Use camera expression','camera')
        if self.break_active:add(menu,'Continue playing','continue')
        else:
            breaks=menu.addMenu('Take a break');breaks.setEnabled(self.session_active)
            for seconds,title in ((30,'30 seconds'),(60,'1 minute'),(120,'2 minutes')):add(breaks,title,'break:'+str(seconds))
        add(menu,'I fell','setback',self.session_active and not self.break_active)
        add(menu,'Mute reminders' if self.reminders_enabled else 'Resume reminders','mute',self.session_active)
        menu.addSeparator();add(menu,'Move Nori','move');add(menu,'Open Regen','open')
        menu.popup(self.mapToGlobal(QPoint(15,self.height()-20)))

    def paintEvent(self,event):
        p=QPainter(self);p.setRenderHint(QPainter.RenderHint.Antialiasing);p.setPen(Qt.PenStyle.NoPen);p.setBrush(QColor('#FFFCF4'))
        p.drawRoundedRect(23,223,174,32,13,13);p.drawRoundedRect(23,258,174,64,15,15)
        if self.message or self.editing:
            p.drawRoundedRect(5,3,210,61,13,13);p.setPen(QColor('#34453E'));font=QFont('DM Sans');font.setPixelSize(12);p.setFont(font)
            p.drawText(14,8,192,50,Qt.AlignmentFlag.AlignCenter|Qt.TextFlag.TextWordWrap,'Drag Nori; release to lock' if self.editing else self.message)
        p.end()

    def mousePressEvent(self,event):
        if event.button()==Qt.MouseButton.LeftButton:
            self.pressed=True;self.press_position=event.globalPosition().toPoint();self.drag_offset=self.press_position-self.pos();self.dragging=self.editing
    def mouseMoveEvent(self,event):
        if self.pressed and (event.globalPosition().toPoint()-self.press_position).manhattanLength()>8:self.dragging=True;self.set_editable(True)
        if self.dragging:self.move(event.globalPosition().toPoint()-self.drag_offset)
    def mouseReleaseEvent(self,event):
        self.pressed=False
        if self.dragging:self.finish_move()
        elif event.button() in (Qt.MouseButton.LeftButton,Qt.MouseButton.RightButton):self.open_controls()

PipOverlay=NoriOverlay
