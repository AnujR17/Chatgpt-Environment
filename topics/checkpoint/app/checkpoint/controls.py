"""Drawn selectors and animated buttons, retaining Qt's keyboard/accessibility behavior."""
from PySide6.QtCore import Qt,QRectF,QVariantAnimation,QEasingCurve,QAbstractAnimation
from PySide6.QtGui import QPainter,QColor,QPen,QPainterPath
from PySide6.QtWidgets import QComboBox,QListView,QPushButton,QApplication
from checkpoint.theme import PALETTES


def palette_for(widget):
    window=widget.window()
    return PALETTES[getattr(window,'theme',getattr(window.parentWidget(),'theme','light'))]


def motion_reduced(widget):
    node=widget
    while node is not None:
        if getattr(node,'reduced_motion',False):return True
        node=node.parentWidget()
    return False


class Select(QComboBox):
    def __init__(self,parent=None):
        super().__init__(parent);self.setMinimumHeight(44);self.setCursor(Qt.CursorShape.PointingHandCursor)
        view=QListView(self);view.setSpacing(3);view.setUniformItemSizes(True)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setView(view);self.setMaxVisibleItems(7);self.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
        self.setMinimumContentsLength(7)

    def showPopup(self):
        c=palette_for(self)
        self.view().setStyleSheet(f'''QListView{{font-family:"DM Sans";font-size:14px;background:{c['surface']};color:{c['text']};border:1px solid {c['border']};padding:6px;outline:0;selection-background-color:{c['soft']};selection-color:{c['text']};}}QListView::item{{min-height:36px;padding:4px 12px;border-radius:5px;}}QListView::item:hover{{background:{c['surface_alt']};}}QListView::item:selected{{background:{c['soft']};color:{c['text']};}}''')
        super().showPopup()

    def paintEvent(self,event):
        c=palette_for(self);p=QPainter(self);p.setRenderHint(QPainter.RenderHint.Antialiasing)
        border=c['accent'] if self.hasFocus() else c['secondary'] if self.underMouse() else c['border']
        p.setPen(QPen(QColor(border),1.5 if self.hasFocus() else 1));p.setBrush(QColor(c['surface'] if self.isEnabled() else c['surface_alt']))
        p.drawRoundedRect(QRectF(1,1,self.width()-2,self.height()-2),7,7)
        if not self.isEditable():
            p.setFont(self.font());p.setPen(QColor(c['text'] if self.isEnabled() else c['muted']))
            text=self.fontMetrics().elidedText(self.currentText(),Qt.TextElideMode.ElideRight,self.width()-49)
            p.drawText(QRectF(13,0,self.width()-49,self.height()),Qt.AlignmentFlag.AlignVCenter,text)
        x=self.width()-22;y=self.height()/2
        path=QPainterPath();path.moveTo(x-4,y-2);path.lineTo(x,y+2);path.lineTo(x+4,y-2)
        p.setBrush(Qt.BrushStyle.NoBrush);p.setPen(QPen(QColor(c['secondary']),1.6,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap,Qt.PenJoinStyle.RoundJoin));p.drawPath(path);p.end()


class ActionButton(QPushButton):
    def __init__(self,text,parent=None):
        super().__init__(text,parent);self._hover=0.;self.animation=QVariantAnimation(self)
        self.animation.setDuration(140);self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.valueChanged.connect(self._animate)
    def _animate(self,value):self._hover=float(value);self.update()
    def _transition(self,target):
        if motion_reduced(self):self._hover=target;self.update();return
        self.animation.stop();self.animation.setStartValue(self._hover);self.animation.setEndValue(target);self.animation.start()
    def enterEvent(self,event):self._transition(1.);super().enterEvent(event)
    def leaveEvent(self,event):self._transition(0.);super().leaveEvent(event)
    def paintEvent(self,event):
        super().paintEvent(event)
        if self._hover and self.isEnabled():
            p=QPainter(self);p.setRenderHint(QPainter.RenderHint.Antialiasing);p.setPen(Qt.PenStyle.NoPen)
            colour=QColor('#FFFFFF' if self.property('primary') else '#315D45');colour.setAlpha(round(self._hover*13));p.setBrush(colour);p.drawRoundedRect(QRectF(2,2,self.width()-4,self.height()-4),7,7);p.end()


from PySide6.QtCore import QSize
from PySide6.QtWidgets import QCheckBox


class Switch(QCheckBox):
    """A drawn toggle retaining QCheckBox semantics, labels and keyboard activation."""
    def __init__(self,text='',parent=None):
        super().__init__(text,parent);self.position=0.;self.setCursor(Qt.CursorShape.PointingHandCursor);self.setMinimumHeight(34)
        self.transition=QVariantAnimation(self);self.transition.setDuration(140);self.transition.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.transition.valueChanged.connect(self._position);self.toggled.connect(self._toggle)
    def _position(self,value):self.position=float(value);self.update()
    def _toggle(self,checked):
        self.transition.stop()
        if motion_reduced(self):self._position(1. if checked else 0.);return
        self.transition.setStartValue(self.position);self.transition.setEndValue(1. if checked else 0.);self.transition.start()
    def sizeHint(self):return QSize(52+self.fontMetrics().horizontalAdvance(self.text()),max(34,self.fontMetrics().height()+12))
    def minimumSizeHint(self):return self.sizeHint()
    def hitButton(self,pos):return self.rect().contains(pos)
    def paintEvent(self,event):
        c=palette_for(self);p=QPainter(self);p.setRenderHint(QPainter.RenderHint.Antialiasing);y=self.height()/2
        if not self.isEnabled():p.setOpacity(.45)
        p.setPen(Qt.PenStyle.NoPen);p.setBrush(QColor(c['accent'] if self.isChecked() else c['secondary']));p.drawRoundedRect(QRectF(1,y-10,36,20),10,10)
        position=self.position if self.transition.state()==QAbstractAnimation.State.Running else (1. if self.isChecked() else 0.)
        p.setBrush(QColor(c['on_accent'] if self.isChecked() else '#FFFFFF'));p.drawEllipse(QRectF(4+16*position,y-7,14,14))
        p.setPen(QColor(c['text']));p.setFont(self.font());p.drawText(QRectF(48,0,self.width()-48,self.height()),Qt.AlignmentFlag.AlignVCenter,self.text())
        if self.hasFocus():p.setBrush(Qt.BrushStyle.NoBrush);p.setPen(QPen(QColor(c['accent']),1.5));p.drawRoundedRect(QRectF(0,y-13,40,26),12,12)
        p.end()


from PySide6.QtWidgets import QStackedWidget,QLayout


class PageStack(QStackedWidget):
    """Inactive report pages must not force the live session to their document height."""
    def __init__(self,parent=None):
        super().__init__(parent);self.layout().setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint);self.currentChanged.connect(lambda _:self.updateGeometry())
    def minimumSizeHint(self):
        page=self.currentWidget()
        return page.minimumSizeHint() if page else super().minimumSizeHint()
    def sizeHint(self):
        page=self.currentWidget()
        return page.sizeHint() if page else super().sizeHint()
    def hasHeightForWidth(self):return False
    def heightForWidth(self,width):return -1
