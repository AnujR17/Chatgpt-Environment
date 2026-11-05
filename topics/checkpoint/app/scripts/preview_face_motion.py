"""Render actual native Pip states/animation using labelled synthetic face signals."""
from pathlib import Path
import time
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget,QHBoxLayout,QVBoxLayout
from PIL import Image
from checkpoint.app import create_application,label
from checkpoint.blob import PipWidget
from checkpoint.face_mapping import movement_parameters,movement_label

ROOT=Path(__file__).resolve().parents[1]
PROFILES=[('Neutral',{}),('Happy',{'mouthSmileLeft':.22,'mouthSmileRight':.22,'eyeSquintLeft':.18,'eyeSquintRight':.18}),
 ('Open smile',{'mouthSmileLeft':.35,'mouthSmileRight':.35,'jawOpen':.32,'eyeSquintLeft':.4,'eyeSquintRight':.4}),
 ('Drawn brows',{'browDownLeft':.24,'browDownRight':.24,'browInnerUp':.16,'mouthPressLeft':.2,'mouthPressRight':.2})]
app=create_application([])
window=QWidget();window.setStyleSheet('background:#F4F2EC;');root=QVBoxLayout(window);root.setContentsMargins(24,22,24,20)
root.addWidget(label('Pip expressions',26,bold=True));root.addWidget(label('Synthetic face signals · actual native rendering',13,True));row=QHBoxLayout();root.addLayout(row)
for title,scores in PROFILES:
    col=QVBoxLayout();pip=PipWidget(190);pip.configure(reduced_motion=True);movement=movement_parameters(scores);key,_=movement_label(movement)
    pip.set_state(key,0,0);pip.set_movement(movement);col.addWidget(pip);caption=label(title,16);caption.setAlignment(Qt.AlignmentFlag.AlignCenter);col.addWidget(caption);row.addLayout(col)
window.show();app.processEvents();window.grab().save(str(ROOT/'artifacts/pip-expression-states.png'));window.close()
window=QWidget();window.setStyleSheet('background:#F4F2EC;');layout=QVBoxLayout(window);layout.setContentsMargins(22,16,22,18);layout.addWidget(label('Pip motion preview',19,bold=True));layout.addWidget(label('Synthetic face signals',12,True));pip=PipWidget(230);layout.addWidget(pip);caption=label('Neutral',15);caption.setAlignment(Qt.AlignmentFlag.AlignCenter);layout.addWidget(caption);window.show();app.processEvents();pip.timer.stop()
frames=[]
for i in range(105):
    index=0 if i<15 else 1 if i<35 else 2 if i<60 else 3 if i<85 else 0
    title,scores=PROFILES[index];movement=movement_parameters(scores);key,_=movement_label(movement)
    pip.set_state(key,0,0);pip.set_movement(movement);pip.timer.stop();pip.animation_time=i/15;pip.pip_clock=time.monotonic()-1/15;caption.setText(title)
    image=window.grab().toImage().convertToFormat(__import__('PySide6.QtGui',fromlist=['QImage']).QImage.Format.Format_RGBA8888)
    frames.append(Image.frombytes('RGBA',(image.width(),image.height()),image.bits().tobytes()).convert('RGB'))
frames[0].save(ROOT/'artifacts/pip-motion-preview.gif',save_all=True,append_images=frames[1:],duration=67,loop=0)
window.close();app.processEvents()
print('Rendered native expression states and motion preview; synthetic inputs, not recognition accuracy.')
