import os
os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
from pathlib import Path
import json
import time
from urllib.request import Request,urlopen
from urllib.error import HTTPError
import pytest
from PySide6.QtCore import Qt,QTimer
from PySide6.QtGui import QImage
from PySide6.QtTest import QTest
from checkpoint.app import create_application,MainWindow
from checkpoint.blob import parameters,movement_visual,PipWidget
from checkpoint.phone import PhoneBridge,PhoneServer
from checkpoint.companion import CompanionState
from checkpoint.session import Session
from checkpoint.expression_view import ExpressionDisplay
from checkpoint.gameplay import GameObservation
from checkpoint.input_activity import Activity
from checkpoint.face_mapping import movement_parameters


def test_neutral_and_no_face_are_flat_not_happy():
    assert parameters('neutral')['smile']==0 and parameters(None)['smile']==0
    assert parameters('composed')['brow']==0
    assert movement_parameters({})['smile']==0
    assert movement_parameters({'mouthSmileLeft':.02,'mouthSmileRight':.02})['smile']==0
    brow=movement_parameters({'browDownLeft':.3,'browDownRight':.3})
    assert brow['brow']>.5 and brow['smile']==0
    flat=movement_parameters({'mouthSmileLeft':.3,'mouthSmileRight':.3},{'mouthSmileLeft':.3,'mouthSmileRight':.3})
    assert flat['smile']==0


def test_pip_overlay_has_transparent_corners_and_no_window_chrome(tmp_path):
    app=create_application([]);window=MainWindow(no_setup=True,data_dir=tmp_path);window.show();window.toggle_overlay();app.processEvents()
    overlay=window.overlay
    assert overlay.windowFlags() & Qt.WindowType.FramelessWindowHint
    assert overlay.windowFlags() & Qt.WindowType.WindowTransparentForInput
    assert overlay.windowFlags() & Qt.WindowType.WindowDoesNotAcceptFocus
    assert overlay.testAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    overlay.blob.set_state('angry',0,0);overlay.blob.configure(reduced_motion=True)
    image=QImage(overlay.size(),QImage.Format.Format_ARGB32);image.fill(Qt.GlobalColor.transparent);overlay.render(image)
    assert image.pixelColor(0,0).alpha()==0 and image.pixelColor(image.width()-1,image.height()-1).alpha()==0
    overlay.blob.set_state(None);overlay.blob.set_movement(None)
    neutral=overlay.blob.grab().toImage()
    assert neutral.pixelColor(neutral.width()//2,neutral.height()//2).name()=='#97beaf'
    overlay.set_editable(True);assert not overlay.windowFlags() & Qt.WindowType.WindowTransparentForInput
    overlay.set_editable(False);assert overlay.windowFlags() & Qt.WindowType.WindowTransparentForInput
    window.close();window.deleteLater();app.processEvents()


def test_phone_authentication_real_http_and_report_boundary():
    bridge=PhoneBridge();bridge.publish({'title':'Neutral appearance','unknown':False},{'schema':2,'moments':[]})
    server=PhoneServer(bridge,host='127.0.0.1',port=0).start();base=f'http://127.0.0.1:{server.port}'
    try:
        assert urlopen(base+'/').status==200
        with pytest.raises(HTTPError) as ex:urlopen(base+'/api/state')
        assert ex.value.code==401
        request=lambda path:Request(base+path,headers={'Authorization':'Bearer '+server.token})
        assert json.load(urlopen(request('/api/state')))['title']=='Neutral appearance'
        report=json.load(urlopen(request('/api/report')));assert report=={'schema':2,'moments':[]}
        with pytest.raises(HTTPError) as ex:urlopen(request('/../../checkpoint/session.py'))
        assert ex.value.code==404
        with pytest.raises(TypeError):bridge.publish({'raw_frame':object()},{})
    finally:server.stop()


def test_input_timing_exports_no_key_names_and_clears():
    activity=Activity();activity.mouse(3,4,1,now=100);activity.key('private-scan-code',False,now=100)
    activity.key('private-scan-code',True,now=100.3);data=activity.snapshot(now=105)
    assert data['mouse_motion_per_second']==.5 and data['mean_key_hold_seconds']==.3
    assert 'private-scan-code' not in json.dumps(data)
    activity.clear();assert activity.snapshot(now=105)['idle_seconds'] is None


def test_nudge_waits_for_quiet_input_is_optional_and_has_cooldown():
    state=CompanionState();session=Session();face=ExpressionDisplay('Brows drawn','angry','physical movement',movement={'brow':.5},source='face_movement')
    fall=GameObservation('Getting Over It','Foreground process detected','Possible fall · camera descending')
    quiet=GameObservation('Getting Over It','Foreground process detected','No clear vertical camera movement')
    state.update(session,face,fall,input_stats={'idle_seconds':0},nudges=True,now=100)
    snapshot,report=state.update(session,face,quiet,input_stats={'idle_seconds':4},nudges=True,now=105)
    assert snapshot['nudge'] and session.report is None
    snapshot,_=state.update(session,face,fall,input_stats={'idle_seconds':0},nudges=True,now=110)
    snapshot,_=state.update(session,face,quiet,input_stats={'idle_seconds':4},nudges=True,now=115)
    assert not snapshot['nudge']
    snapshot,_=state.update(session,face,quiet,input_stats={'idle_seconds':4},nudges=False,now=116)
    assert not snapshot['nudge']
    assert 'frame' not in report and report['moments'][0]['source']=='face_movement'


def test_app_report_dialog_closes_and_pair_dialog_stops_sharing(tmp_path):
    from PySide6.QtWidgets import QDialog,QPushButton
    app=create_application([]);window=MainWindow(no_setup=True,data_dir=tmp_path);window.show()
    QTimer.singleShot(0,lambda:app.activeModalWidget().accept());window.show_report()
    def stop():
        dialog=app.activeModalWidget();assert isinstance(dialog,QDialog)
        controls=dialog.findChildren(QPushButton);button=next(b for b in controls if b.text()=='Stop phone sharing');QTest.mouseClick(button,Qt.MouseButton.LeftButton)
    QTimer.singleShot(100,stop);window.show_phone();assert window.phone_server is None
    window.close();window.deleteLater();app.processEvents()


def test_existing_physical_mapper_on_recorded_face_and_neutral_calibration(tmp_path):
    import cv2
    import numpy as np
    from checkpoint.face_mapping import LandmarkPipeline
    fixture=Path(os.environ.get('CHECKPOINT_TEST_VIDEO','data/videos/02-01-05-01-01-01-04.mp4'))
    if not fixture.exists():pytest.skip('Requires separately sourced research video')
    cap=cv2.VideoCapture(str(fixture));cap.set(cv2.CAP_PROP_POS_MSEC,1500);ok,frame=cap.read();cap.release();assert ok
    # Non-ASCII install directories must work on Windows as well as Linux.
    folder=tmp_path/'顔のモデル';folder.mkdir()
    (folder/'face_landmarker.task').write_bytes(Path('artifacts/face_landmarker.task').read_bytes())
    mapper=LandmarkPipeline(folder)
    try:
        cue=mapper.infer(frame);assert cue.status=='accepted' and cue.movement is not None
        assert set(cue.movement)=={'smile','brow','eyes','jaw','tension','laugh'}
        mapper.start_neutral()
        for _ in range(8):cue=mapper.infer(frame)
        assert cue.mapping_label=='Neutral face calibrated'
        cue=mapper.infer(frame);assert cue.movement is not None
        assert all(0<=value<=.18 for value in mapper.baseline.values())
        missing=mapper.infer(np.zeros_like(frame));assert missing.status=='unavailable' and missing.movement is None
    finally:mapper.close()
