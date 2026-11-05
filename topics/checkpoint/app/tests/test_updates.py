"""Exercise download validation and staging without executing downloaded code."""
import hashlib
import io
import json
from pathlib import Path
import stat
import zipfile
import pytest
from checkpoint import updates as u


def zip_bytes(files):
    out=io.BytesIO()
    with zipfile.ZipFile(out,'w') as z:
        for name,value in files.items():z.writestr(name,value)
    return out.getvalue()


def fixture(tmp_path):
    root=tmp_path/'Checkpoint Windows';(root/'checkpoint').mkdir(parents=True);(root/'runtime').mkdir();(root/'artifacts').mkdir()
    (root/'checkpoint/obsolete.py').write_text('old')
    (root/'runtime/pythonw.exe').write_bytes(b'fixture-runtime');(root/'launch.py').write_text('old-launch')
    (root/'runtime-sources.json').write_text(json.dumps({'python':{'sha256':'a'*64},'wheels':{'fixture.whl':'b'*64}}))
    (root/'artifacts/face.onnx').write_bytes(b'fixture-model')
    files={'checkpoint/version.py':b"APP_VERSION = '0.4.1'\n",'checkpoint/__init__.py':b'', 'checkpoint/new.py':b'new code'}
    data=zip_bytes(files)
    sha=lambda b:hashlib.sha256(b).hexdigest()
    manifest={'protocol':1,'tag':'checkpoint-v0.4.1-preview.1','version':'0.4.1',
      'runtime':u.runtime_fingerprint(json.loads((root/'runtime-sources.json').read_text())),
      'models':{'artifacts/face.onnx':sha(b'fixture-model')},
      'app':{'name':'Checkpoint-App-Update.zip','bytes':len(data),'sha256':sha(data),'files':{p:sha(v) for p,v in files.items()}},
      'full':{'name':'Checkpoint-Windows-Preview.zip','bytes':len(data),'sha256':sha(data)}}
    return root,manifest,data


def test_small_update_stages_new_files_without_modifying_live_app_or_runtime(monkeypatch,tmp_path):
    root,manifest,data=fixture(tmp_path)
    monkeypatch.setattr(u.urllib.request,'urlopen',lambda *a,**k:io.BytesIO(data))
    job=u.prepare_update(root,manifest);config=json.loads(job.read_text());stage=Path(config['staged'])
    assert (root/'checkpoint/obsolete.py').read_text()=='old'
    assert not (root/'checkpoint/new.py').exists()
    assert (stage/'checkpoint/new.py').read_text()=='new code' and not (stage/'checkpoint/obsolete.py').exists()
    assert (root/'runtime/pythonw.exe').read_bytes()==(stage/'runtime/pythonw.exe').read_bytes()==b'fixture-runtime'
    assert Path(config['backup']).parent.parent==root.parent/'.checkpoint-backups'
    assert not (job.parent/'download.zip').exists()


def test_corrupt_download_preserves_live_install_and_removes_staging(monkeypatch,tmp_path):
    root,manifest,data=fixture(tmp_path)
    monkeypatch.setattr(u.urllib.request,'urlopen',lambda *a,**k:io.BytesIO(data[:-2]+b'xx'))
    with pytest.raises(ValueError,match='checksum'):u.prepare_update(root,manifest)
    assert (root/'checkpoint/obsolete.py').read_text()=='old'
    assert not list((root.parent/'.checkpoint-updates').iterdir())


def test_cancelled_download_never_changes_installed_app(monkeypatch,tmp_path):
    root,manifest,data=fixture(tmp_path)
    monkeypatch.setattr(u.urllib.request,'urlopen',lambda *a,**k:io.BytesIO(data))
    with pytest.raises(u.Cancelled):u.prepare_update(root,manifest,cancel=lambda:True)
    assert (root/'checkpoint/obsolete.py').read_text()=='old'


def test_changed_runtime_or_model_requires_full_package(tmp_path):
    root,manifest,_=fixture(tmp_path)
    assert u.package_kind(root,manifest)=='app'
    (root/'artifacts/face.onnx').write_bytes(b'modified')
    assert u.package_kind(root,manifest)=='full'
    manifest['runtime']='different';assert u.package_kind(root,manifest)=='full'


@pytest.mark.parametrize('name',['../escape.py','C:/escape.py','checkpoint/../../x','checkpoint\\x.py','checkpoint/file:stream','checkpoint/CON.py','checkpoint/abc.'])
def test_windows_archive_paths_reject_traversal_and_special_names(tmp_path,name):
    data=zip_bytes({name:b'bad'});file=tmp_path/'bad.zip';file.write_bytes(data)
    with pytest.raises(ValueError):u.unpack(file,tmp_path/'out')
    assert not (tmp_path/'escape.py').exists()


def test_archive_rejects_symlinks_and_case_collisions(tmp_path):
    file=tmp_path/'bad.zip'
    with zipfile.ZipFile(file,'w') as z:
        link=zipfile.ZipInfo('checkpoint/link');link.external_attr=(stat.S_IFLNK|0o777)<<16;z.writestr(link,'outside')
    with pytest.raises(ValueError,match='link'):u.unpack(file,tmp_path/'out')
    file.write_bytes(zip_bytes({'checkpoint/Foo.py':b'a','checkpoint/foo.py':b'b'}))
    with pytest.raises(ValueError,match='Duplicate'):u.unpack(file,tmp_path/'out')


def test_release_discovery_uses_only_checkpoint_assets_and_checks_github_digest(monkeypatch,tmp_path):
    _,manifest,_=fixture(tmp_path)
    assets=[{'name':u.MANIFEST,'browser_download_url':u.DOWNLOAD+manifest['tag']+'/'+u.MANIFEST}]
    for key in ('app','full'):
        p=manifest[key];assets.append({'name':p['name'],'browser_download_url':u.DOWNLOAD+manifest['tag']+'/'+p['name'],'size':p['bytes'],'digest':'sha256:'+p['sha256']})
    releases=[{'tag_name':'job-search-v99.0.0','assets':[]},{'tag_name':manifest['tag'],'assets':assets}]
    monkeypatch.setattr(u,'read_json',lambda url:releases if url==u.API else json.loads(json.dumps(manifest)))
    assert u.check_updates()['available']
    assets[1]['digest']='sha256:'+'0'*64
    with pytest.raises(ValueError,match='digest mismatch'):u.check_updates()


def test_version_order_and_unrelated_repo_releases():
    assert u.version_key('checkpoint-v0.3.0-preview.2')>u.version_key('checkpoint-v0.3.0-preview.1')
    assert u.version_key('checkpoint-v0.3.0')>u.version_key('checkpoint-v0.3.0-preview.5')
    with pytest.raises(ValueError):u.version_key('job-search-v9.0.0')


def test_native_update_button_downloads_and_prepares_without_touching_live_install(monkeypatch,tmp_path):
    import os,time
    os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
    from checkpoint.app import create_application,MainWindow
    import checkpoint.update_ui as ui
    root,manifest,data=fixture(tmp_path);manifest['available']=True
    monkeypatch.setattr(ui,'ROOT',root);monkeypatch.setattr(ui,'check_updates',lambda:manifest)
    monkeypatch.setattr(u.urllib.request,'urlopen',lambda *a,**k:io.BytesIO(data))
    started=[];monkeypatch.setattr(ui,'launch_update',started.append)
    app=create_application([]);window=MainWindow(no_setup=True,data_dir=tmp_path/'history');window.show();dialog=ui.UpdateDialog(window);dialog.show()
    try:
        deadline=time.monotonic()+4
        while time.monotonic()<deadline and dialog.action.text()!='Update and restart':app.processEvents();time.sleep(.01)
        assert dialog.action.text()=='Update and restart'
        dialog.action.click();deadline=time.monotonic()+5
        while time.monotonic()<deadline and not started:app.processEvents();time.sleep(.01)
        assert len(started)==1 and Path(started[0]).is_file()
        assert (root/'checkpoint/obsolete.py').read_text()=='old'
    finally:
        dialog.close();window.close();dialog.deleteLater();window.deleteLater();app.processEvents()


def test_full_runtime_fallback_is_staged_without_replacing_live_root(monkeypatch,tmp_path):
    root,manifest,_=fixture(tmp_path);manifest['runtime']='changed'
    data=zip_bytes({'Checkpoint-Windows/runtime/pythonw.exe':b'next-runtime','Checkpoint-Windows/launch.py':b'next-launch',
      'Checkpoint-Windows/runtime-sources.json':(root/'runtime-sources.json').read_bytes(),'Checkpoint-Windows/checkpoint/version.py':b'next-version'})
    manifest['full'].update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
    monkeypatch.setattr(u.urllib.request,'urlopen',lambda *a,**k:io.BytesIO(data))
    config=json.loads(u.prepare_update(root,manifest).read_text())
    assert (Path(config['staged'])/'runtime/pythonw.exe').read_bytes()==b'next-runtime'
    assert (root/'runtime/pythonw.exe').read_bytes()==b'fixture-runtime'


def test_app_file_hash_mismatch_cannot_change_current_code(monkeypatch,tmp_path):
    root,manifest,data=fixture(tmp_path);manifest['app']['files']['checkpoint/new.py']='0'*64
    monkeypatch.setattr(u.urllib.request,'urlopen',lambda *a,**k:io.BytesIO(data))
    with pytest.raises(ValueError,match='App file checksum'):u.prepare_update(root,manifest)
    assert (root/'checkpoint/obsolete.py').read_text()=='old'


def test_startup_acknowledgement_is_confined_to_this_install_job(monkeypatch,tmp_path):
    root,_,_=fixture(tmp_path);job=root.parent/'.checkpoint-updates/job/job.json';job.parent.mkdir(parents=True)
    monkeypatch.setenv('CHECKPOINT_UPDATE_JOB',str(job))
    job.write_text(json.dumps({'original':str(root),'tag':u.RELEASE_TAG}))
    u.signal_update_ready(root);assert (job.parent/'ready.json').exists()
    (job.parent/'ready.json').unlink();job.write_text(json.dumps({'original':str(root),'tag':'checkpoint-v99.0.0'}))
    u.signal_update_ready(root);assert not (job.parent/'ready.json').exists()
