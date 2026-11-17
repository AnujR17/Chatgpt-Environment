"""One-time bridge for legacy updaters: use their runtime, not their folder-swap helper."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import sys
import tempfile
import urllib.request
import zipfile

REPO='AnujR17/Chatgpt-Environment'
DOWNLOAD='https://github.com/'+REPO+'/releases/download/'


def read_json(url):
    request=urllib.request.Request(url,headers={'User-Agent':'Checkpoint-updater-repair','Accept':'application/vnd.github+json'})
    with urllib.request.urlopen(request,timeout=30) as response:data=response.read(2*1024*1024+1)
    if len(data)>2*1024*1024:raise ValueError('Update metadata is too large')
    return json.loads(data)


def main():
    if sys.platform!='win32':raise RuntimeError('Run this repair on the Windows computer with Checkpoint installed.')
    if len(sys.argv)!=2:raise ValueError('Choose the existing Checkpoint-Windows folder.')
    root=Path(sys.argv[1]).resolve()
    if not (root/'runtime/python.exe').is_file() or not (root/'launch.py').is_file():raise ValueError('This is not a Checkpoint installation folder.')
    releases=read_json('https://api.github.com/repos/'+REPO+'/releases?per_page=30')
    choices=[]
    for release in releases:
        match=re.fullmatch(r'checkpoint-v(\d+)\.(\d+)\.(\d+)(?:-preview\.(\d+))?',release.get('tag_name',''))
        assets={a['name']:a for a in release.get('assets',[])}
        if match and not release.get('draft') and 'Checkpoint-update.json' in assets:
            choices.append((tuple(int(x) if x is not None else 10**9 for x in match.groups()),release,assets))
    if not choices:raise ValueError('No published Checkpoint update was found.')
    _,release,assets=max(choices,key=lambda x:x[0]);tag=release['tag_name']
    url=DOWNLOAD+tag+'/Checkpoint-update.json'
    if assets['Checkpoint-update.json']['browser_download_url']!=url:raise ValueError('Unexpected update manifest URL.')
    manifest=read_json(url)
    if manifest.get('protocol')!=1 or manifest.get('tag')!=tag:raise ValueError('Unsupported update manifest.')
    payload=manifest['app'];asset=assets[payload['name']]
    if (payload['name']!='Checkpoint-App-Update.zip' or not re.fullmatch('[a-f0-9]{64}',payload['sha256'])
            or not 0<payload['bytes']<=512*1024*1024 or asset['size']!=payload['bytes']
            or asset['browser_download_url']!=DOWNLOAD+tag+'/'+payload['name']
            or asset.get('digest') not in (None,'sha256:'+payload['sha256'])):
        raise ValueError('Update asset verification failed.')
    print('Repairing '+str(root)+' using '+tag,flush=True)
    with tempfile.TemporaryDirectory(prefix='checkpoint-repair-') as directory:
        folder=Path(directory);package=folder/'update.zip'
        cache=root.parent/'.checkpoint-updates/downloads'/(payload['sha256']+'.zip')
        if cache.is_file() and cache.stat().st_size==payload['bytes'] and hashlib.sha256(cache.read_bytes()).hexdigest()==payload['sha256']:
            shutil.copyfile(cache,package);print('Reusing the verified download.',flush=True)
        else:
            request=urllib.request.Request(asset['browser_download_url'],headers={'User-Agent':'Checkpoint-updater-repair'})
            total=0;digest=hashlib.sha256()
            with urllib.request.urlopen(request,timeout=30) as response,package.open('wb') as output:
                while block:=response.read(512*1024):
                    total+=len(block)
                    if total>payload['bytes']:raise ValueError('Package exceeds expected size.')
                    digest.update(block);output.write(block)
            if total!=payload['bytes'] or digest.hexdigest()!=payload['sha256']:raise ValueError('Downloaded package checksum mismatch.')
        # Load only the three publisher-verified updater modules, without changing the old app.
        source=folder/'source'
        with zipfile.ZipFile(package) as archive:
            for name in ('checkpoint/__init__.py','checkpoint/version.py','checkpoint/updates.py'):
                if archive.namelist().count(name)!=1:raise ValueError('Invalid bootstrap source entry.')
                data=archive.read(name)
                if hashlib.sha256(data).hexdigest()!=manifest['app']['files'].get(name):raise ValueError('Updater source checksum mismatch.')
                target=source/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
        sys.path.insert(0,str(source))
        from checkpoint import updates
        updates.portable_root(root)
        if updates.version_key(tag)<=updates.version_key(updates.installed_tag(root)):
            print('This folder already has '+updates.installed_tag(root)+'. Reopen Start Checkpoint.cmd from this folder.',flush=True);return
        if updates.package_kind(root,manifest)!='app':raise ValueError('This installation needs a full runtime update; use the full portable release instead of this small repair.')
        cache.parent.mkdir(parents=True,exist_ok=True)
        temporary=cache.with_suffix('.tmp');shutil.copyfile(package,temporary);temporary.replace(cache)
        job=updates.prepare_update(root,manifest,progress=lambda value,message:print(message,flush=True))
        updates.launch_update(job)
        print('The repair helper is starting. Checkpoint will reopen automatically. No full runtime download was needed.',flush=True)


if __name__=='__main__':
    try:main()
    except Exception as error:
        print('Repair could not complete: '+str(error),file=sys.stderr,flush=True)
        raise SystemExit(1)
