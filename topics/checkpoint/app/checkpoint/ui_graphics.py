"""Original native line icons and game-session artwork. No icon font or remote assets."""
from functools import lru_cache
from PySide6.QtCore import QByteArray, QRectF, QSize, Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPainterPath, QPen, QPixmap
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QFrame

PATHS = {
    'session': '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
    'flag': '<path d="M5 21V4c5-4 9 4 14 0v10c-5 4-9-4-14 0"/>',
    'feeling': '<circle cx="12" cy="12" r="9"/><path d="M8 14c2 3 6 3 8 0M8 9h.01M16 9h.01"/>',
    'report': '<path d="M5 3h10l4 4v14H5zM14 3v5h5M8 17v-3M12 17v-6M16 17v-4"/>',
    'history': '<path d="M3 11a9 9 0 1 1 2 7M3 4v7h7M12 7v5l3 2"/>',
    'settings': '<path d="m9 3-1 3-3 1-2 4 2 2-1 3 3 3 3-1 2 3 4-1 1-3 3-1 1-4-3-2 1-3-3-3-3 1z"/><circle cx="12" cy="12" r="3"/>',
    'moon': '<path d="M20 14A9 9 0 0 1 10 3a9 9 0 1 0 10 11z"/>',
    'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M5 5l1 1M18 18l1 1M5 19l1-1M18 6l1-1"/>',
    'pause': '<rect x="6" y="4" width="4" height="16" rx="1"/><rect x="14" y="4" width="4" height="16" rx="1"/>',
    'play': '<path d="m8 4 12 8-12 8z"/>',
    'camera': '<path d="M3 7h5l2-3h4l2 3h5v13H3z"/><circle cx="12" cy="13" r="4"/>',
    'video': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m10 9 5 3-5 3z"/>',
    'phone': '<rect x="6" y="2" width="12" height="20" rx="2"/><path d="M10 18h4"/>',
    'overlay': '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 8h18"/><rect x="12" y="12" width="7" height="6" rx="1"/>',
    'game': '<path d="M8 7h8c4 0 6 10 4 11-2 2-4-3-6-3h-4c-2 0-4 5-6 3-2-1 0-11 4-11zM6 11h5M8.5 8.5v5M16 10h.01M18 12h.01"/>',
    'help': '<circle cx="12" cy="12" r="9"/><path d="M9 8a3 3 0 0 1 6 1c0 2-3 2-3 5M12 17h.01"/>',
    'stop': '<rect x="5" y="5" width="14" height="14" rx="2"/>',
    'edit': '<path d="m4 16 12-12 4 4L8 20H4zM13 7l4 4"/>',
    'sliders': '<path d="M4 6h16M4 12h16M4 18h16"/><circle cx="8" cy="6" r="2"/><circle cx="16" cy="12" r="2"/><circle cx="10" cy="18" r="2"/>',
}


@lru_cache(maxsize=192)
def icon(name, color='#344D39'):
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="'+color+'" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'+PATHS[name]+'</svg>')
    result = QIcon()
    for scale in (1, 2):
        pix = QPixmap(24*scale, 24*scale);pix.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pix);QSvgRenderer(QByteArray(svg.encode())).render(painter);painter.end()
        pix.setDevicePixelRatio(scale);result.addPixmap(pix)
    return result


def with_icon(button, name, color='#344D39'):
    key=name+color
    if button.property('regenIcon')!=key:
        button.setIcon(icon(name,color));button.setIconSize(QSize(19,19));button.setProperty('regenIcon',key)
    return button


class SessionHeader(QFrame):
    """Authored terrain motif for the session identity, never a live game view."""
    def __init__(self):
        super().__init__();self.setFixedHeight(112);self.setObjectName('sessionHeader')

    def paintEvent(self, event):
        p=QPainter(self);p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(Qt.PenStyle.NoPen);p.setBrush(QColor('#D5E1C5'));p.drawRoundedRect(self.rect(),12,12)
        # Cropped ascending ledges give this a game identity without a fake HUD.
        x=self.width()*.54
        p.save();p.setClipRect(QRectF(x,0,self.width()-x,122))
        for offset in (-22,6,34):
            path=QPainterPath();path.moveTo(x+offset,128);path.lineTo(x+70+offset,83);path.lineTo(x+112+offset,83);path.lineTo(x+170+offset,28);path.lineTo(x+205+offset,28);path.lineTo(x+260+offset,-12)
            p.setPen(QPen(QColor('#B6C7A3'),1.2));p.drawPath(path)
        path=QPainterPath();path.moveTo(x+62,122);path.lineTo(x+120,90);path.lineTo(x+163,90);path.lineTo(x+213,42);path.lineTo(x+251,42);path.lineTo(x+293,0)
        p.setPen(QPen(QColor('#839A6F'),3));p.drawPath(path);p.restore()
        p.end()


class EmotionStage(QFrame):
    """An open colour field. Cyan shade and warm light frame the expression."""
    def __init__(self):
        super().__init__();self.setObjectName('emotionStage');self.scene_theme='light'
    def set_theme(self,theme):
        if theme!=self.scene_theme:self.scene_theme=theme;self.update()
    def paintEvent(self,event):
        from PySide6.QtGui import QRadialGradient
        p=QPainter(self);p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w,h=self.width(),self.height()
        cyan=QRadialGradient(w*.34,h*.55,max(w,h)*.5)
        cyan.setColorAt(0,QColor(108,173,180,33 if self.scene_theme=='light' else 22));cyan.setColorAt(1,QColor(108,173,180,0));p.fillRect(self.rect(),cyan)
        warm=QRadialGradient(w*.62,h*.2,max(w,h)*.48)
        warm.setColorAt(0,QColor(243,196,105,28 if self.scene_theme=='light' else 17));warm.setColorAt(1,QColor(243,196,105,0));p.fillRect(self.rect(),warm);p.end()
