"""Camera failures exercised with explicit device fixtures, not physical-camera claims."""
import os
os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
import time
import cv2
import numpy as np
import pytest
from checkpoint import capture as capture_module
from checkpoint.capture import open_camera
from checkpoint.app import create_application,MainWindow


class CameraFixture:
    def __init__(self,*,opened=True,empty=0,frame=None):
        self.opened=opened;self.empty=empty;self.released=False;self.reads=0
        self.frame=frame if frame is not None else np.random.default_rng(7).integers(0,256,(240,320,3),dtype=np.uint8)
    def isOpened(self):return self.opened
    def set(self,*args):return True
    def get(self,*args):return 30.
    def read(self):
        self.reads+=1
        return (False,None) if self.reads<=self.empty else (True,self.frame.copy())
    def release(self):self.released=True


def test_windows_backend_fallback_requires_frames_and_keeps_chosen_device(monkeypatch):
    bad=CameraFixture(empty=40);good=CameraFixture(empty=2);calls=[]
    def create(index,api):calls.append((index,api));return bad if api==cv2.CAP_DSHOW else good
    monkeypatch.setattr(capture_module.cv2,'VideoCapture',create);monkeypatch.setattr(capture_module.time,'sleep',lambda _:None)
    camera,frame,backend=open_camera(2,platform='win32')
    try:
        assert calls==[(2,cv2.CAP_DSHOW),(2,cv2.CAP_MSMF)]
        assert bad.released and not good.released and good.reads==3
        assert frame.size and backend=='Media Foundation'
    finally:camera.release()


def test_camera_failure_releases_all_handles_and_explains_windows_permissions(monkeypatch):
    cameras=[]
    def create(*args):camera=CameraFixture(opened=False);cameras.append(camera);return camera
    monkeypatch.setattr(capture_module.cv2,'VideoCapture',create)
    with pytest.raises(RuntimeError,match='Let desktop apps access your camera') as error:open_camera(0,platform='win32')
    assert 'Camera 1' in str(error.value) and len(cameras)==3 and all(c.released for c in cameras)


def test_cancelling_camera_warmup_releases_handle_without_opening_more_devices(monkeypatch):
    camera=CameraFixture(empty=99);calls=[]
    def create(*args):calls.append(args);return camera
    monkeypatch.setattr(capture_module.cv2,'VideoCapture',create);monkeypatch.setattr(capture_module.time,'sleep',lambda _:None)
    with pytest.raises(InterruptedError):open_camera(1,lambda:camera.reads>0,platform='win32')
    assert camera.released and len(calls)==1


@pytest.mark.parametrize('failure',['startup','inference'])
def test_model_failure_keeps_camera_preview_running_and_shows_tracking_error(monkeypatch,tmp_path,failure):
    import checkpoint.face_mapping as mapping
    class BrokenModel:
        def __init__(self,**kwargs):
            if failure=='startup':raise RuntimeError('Synthetic model startup error')
        def infer(self,frame):raise RuntimeError('Synthetic model inference error')
        def close(self):pass
    camera=CameraFixture()
    monkeypatch.setattr(capture_module,'open_camera',lambda *a:(camera,camera.frame.copy(),'Fixture backend'))
    monkeypatch.setattr(mapping,'LandmarkPipeline',BrokenModel)
    app=create_application([]);window=MainWindow(no_setup=True,data_dir=tmp_path);window.show();window.select_camera(2)
    try:
        window.toggle_expression_tracking(True);window.toggle_camera()
        deadline=time.monotonic()+4
        while time.monotonic()<deadline:
            app.processEvents();time.sleep(.01)
            if window.worker is not None and window.worker.frames>3 and window.worker.analysis_error:break
        assert window.session.camera_active and window.worker.isRunning() and window.last_image is not None
        assert window.worker.source==2 and window.worker.error==''
        assert ('startup error' if failure=='startup' else 'inference error') in window.worker.analysis_error
        assert any('Face tracking unavailable' in label.text() for label in window.camera_messages)
        assert window.emblems[0].current_state is None
        assert all(not selector.isEnabled() for selector in window.camera_selectors)
        window.pause();assert camera.released
        assert all(selector.isEnabled() for selector in window.camera_selectors)
    finally:window.close();window.deleteLater();app.processEvents()


def test_camera_open_error_reaches_visible_preview_and_allows_retry(monkeypatch,tmp_path):
    def fail(*a):raise RuntimeError('Synthetic camera permission failure. Let desktop apps access your camera.')
    monkeypatch.setattr(capture_module,'open_camera',fail)
    app=create_application([]);window=MainWindow(no_setup=True,data_dir=tmp_path);window.show()
    try:
        window.toggle_camera();deadline=time.monotonic()+3
        while window.worker is not None and time.monotonic()<deadline:app.processEvents();time.sleep(.01)
        assert not window.session.camera_active and window.worker is None
        assert 'Let desktop apps' in window.preview_widgets[0].text()
        assert all(selector.isEnabled() for selector in window.camera_selectors)
    finally:window.close();window.deleteLater();app.processEvents()


def test_network_picker_prefers_live_wifi_over_virtual_and_omits_down_interfaces(monkeypatch):
    import socket
    import psutil
    from types import SimpleNamespace
    from checkpoint.phone import local_networks
    addr=lambda ip:SimpleNamespace(family=socket.AF_INET,address=ip)
    monkeypatch.setattr(psutil,'net_if_addrs',lambda:{'vEthernet (WSL)':[addr('192.168.1.1')],'Wi-Fi':[addr('10.0.0.15')],'Ethernet':[addr('192.168.0.9')],'Disconnected':[addr('10.0.0.20')]})
    monkeypatch.setattr(psutil,'net_if_stats',lambda:{name:SimpleNamespace(isup=name!='Disconnected') for name in ['Wi-Fi','Ethernet','vEthernet (WSL)','Disconnected']})
    assert local_networks()==[('Wi-Fi','10.0.0.15'),('Ethernet','192.168.0.9'),('vEthernet (WSL)','192.168.1.1')]


def test_firewall_helper_is_private_subnet_exact_port_app_scoped_and_quotes_paths():
    from checkpoint.phone import private_firewall_command
    command=private_firewall_command(18765,r"C:\Anuj's files\runtime\pythonw.exe")
    assert command.count('-LocalPort 18765')==2
    assert command.count('-Profile Private -RemoteAddress LocalSubnet')==2
    assert "C:\\Anuj''s files\\runtime\\pythonw.exe" in command and 'python.exe' in command
    assert '-Profile Any' not in command and '-Profile Public' not in command and 'Set-NetFirewallProfile' not in command
    with pytest.raises(ValueError):private_firewall_command(0)
