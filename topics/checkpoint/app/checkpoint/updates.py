"""Explicit GitHub-release updates: verified packages, staged install, rollback.
No credentials, silent installs, self-modifying running code or global policy changes.
"""
from pathlib import Path, PurePosixPath
import base64
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import urllib.request
import uuid
import zipfile
from checkpoint.version import RELEASE_TAG

REPO='AnujR17/Chatgpt-Environment'
API='https://api.github.com/repos/'+REPO+'/releases?per_page=30'
DOWNLOAD='https://github.com/'+REPO+'/releases/download/'
MANIFEST='Checkpoint-update.json'
ROOT_FILES={'launch.py','Start Checkpoint.cmd','Check setup.cmd','check_setup.py','READ ME FIRST.txt'}


class Cancelled(Exception):pass


def version_key(tag):
    m=re.fullmatch(r'checkpoint-v(\d+)\.(\d+)\.(\d+)(?:-(?:pip-)?preview\.(\d+))?',tag)
    if not m:raise ValueError('Unrecognised Checkpoint release version')
    return tuple(map(int,m.groups()[:3]))+(int(m[4]) if m[4] else 10**9,)


def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()


def runtime_fingerprint(sources):
    data={'python':sources['python']['sha256'],'wheels':sources['wheels']}
    return hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def safe_path(name):
    if not isinstance(name,str) or not name or '\\' in name or ':' in name or any(ord(c)<32 for c in name):raise ValueError('Unsafe update path')
    p=PurePosixPath(name)
    if p.is_absolute() or any(x in ('','..','.') for x in name.split('/')):raise ValueError('Unsafe update path')
    for part in p.parts:
        if part.rstrip(' .')!=part or any(c in part for c in '<>"|?*'):raise ValueError('Unsafe Windows update path')
        if re.fullmatch(r'(?i)(con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\..*)?',part):raise ValueError('Reserved Windows update path')
    return p


def app_path(name):
    p=safe_path(name)
    return name in ROOT_FILES or p.parts[0] in ('checkpoint','docs','third_party') or (p.parts[0]=='artifacts' and p.suffix in ('.json','.md'))


def read_json(url,limit=2*1024*1024):
    req=urllib.request.Request(url,headers={'User-Agent':'Checkpoint-updater','Accept':'application/vnd.github+json'})
    with urllib.request.urlopen(req,timeout=20) as response:
        data=response.read(limit+1)
    if len(data)>limit:raise ValueError('Update metadata is too large')
    return json.loads(data)


def check_updates():
    releases=read_json(API)
    if not isinstance(releases,list):raise ValueError('GitHub did not return a release list')
    candidates=[]
    for release in releases:
        if release.get('draft'):continue
        try:key=version_key(release['tag_name'])
        except (KeyError,ValueError):continue
        assets={a['name']:a for a in release.get('assets',[])}
        if MANIFEST in assets:candidates.append((key,release,assets))
    if not candidates:return None
    _,release,assets=max(candidates,key=lambda item:item[0]);tag=release['tag_name']
    expected=DOWNLOAD+tag+'/'+MANIFEST
    if assets[MANIFEST].get('browser_download_url')!=expected:raise ValueError('Unexpected update manifest host')
    manifest=read_json(expected)
    if manifest.get('protocol')!=1 or manifest.get('tag')!=tag:raise ValueError('Unsupported update manifest')
    for kind,name in [('app','Checkpoint-App-Update.zip'),('full','Checkpoint-Windows-Preview.zip')]:
        payload=manifest[kind]
        if payload['name']!=name or not re.fullmatch('[0-9a-f]{64}',payload['sha256']):raise ValueError('Invalid package metadata')
        if type(payload['bytes']) is not int or not 0<payload['bytes']<=512*1024*1024:raise ValueError('Invalid package size')
        asset=assets.get(name,{})
        if asset.get('browser_download_url')!=DOWNLOAD+tag+'/'+name or asset.get('size')!=payload['bytes']:raise ValueError('Release assets do not match their manifest')
        if asset.get('digest') and asset['digest']!='sha256:'+payload['sha256']:raise ValueError('GitHub package digest mismatch')
    for path,sha in manifest['app']['files'].items():
        if not app_path(path) or not re.fullmatch('[0-9a-f]{64}',sha):raise ValueError('Invalid app update entry')
    manifest['available']=version_key(tag)>version_key(RELEASE_TAG)
    return manifest


def portable_root(root):
    root=Path(root).resolve()
    if not (root/'runtime-sources.json').is_file() or not (root/'runtime/pythonw.exe').is_file() or not (root/'launch.py').is_file():raise ValueError('In-app installation is available in the portable Windows app. Install the new Windows release once to enable it.')
    return root


def package_kind(root,manifest):
    try:
        if runtime_fingerprint(json.loads((root/'runtime-sources.json').read_text()))!=manifest['runtime']:return 'full'
        for path,sha in manifest['models'].items():
            if safe_path(path).parts[0]!='artifacts' or digest(root/path)!=sha:return 'full'
    except (OSError,KeyError,ValueError):return 'full'
    return 'app'


def unpack(package,destination,*,prefix='',files=None,cancel=lambda:False):
    with zipfile.ZipFile(package) as archive:
        entries=[];seen=set();total=0
        for info in archive.infolist():
            name=info.filename.rstrip('/')
            if not name:continue
            safe_path(name)
            if prefix:
                if name==prefix.rstrip('/') and info.is_dir():continue
                if not name.startswith(prefix):raise ValueError('Unexpected full-package prefix')
                name=name[len(prefix):];safe_path(name)
            if info.is_dir():continue
            if stat.S_IFMT(info.external_attr>>16) not in (0,stat.S_IFREG):raise ValueError('Update archive contains a link or special file')
            if name.casefold() in seen:raise ValueError('Duplicate update path')
            seen.add(name.casefold());total+=info.file_size
            if total>2*1024**3 or len(seen)>40000:raise ValueError('Expanded update is too large')
            if files is not None and (name not in files or not app_path(name)):raise ValueError('Unexpected app update file')
            entries.append((info,name))
        if files is not None and {name for _,name in entries}!=set(files):raise ValueError('App update is incomplete')
        for info,name in entries:
            if cancel():raise Cancelled()
            target=destination/name;target.parent.mkdir(parents=True,exist_ok=True)
            if target.is_symlink():raise ValueError('Unsafe update destination')
            with archive.open(info) as src,target.open('wb') as dst:shutil.copyfileobj(src,dst,1024*1024)
            if files is not None and digest(target)!=files[name]:raise ValueError('App file checksum mismatch')


def prepare_update(root,manifest,progress=lambda value,message:None,cancel=lambda:False):
    root=portable_root(root)
    if version_key(manifest['tag'])<=version_key(RELEASE_TAG):raise ValueError('This update is not newer than the installed app')
    kind=package_kind(root,manifest);payload=manifest[kind]
    job=root.parent/'.checkpoint-updates'/uuid.uuid4().hex;job.mkdir(parents=True)
    stage=job/root.name;package=job/'download.zip'
    try:
        req=urllib.request.Request(DOWNLOAD+manifest['tag']+'/'+payload['name'],headers={'User-Agent':'Checkpoint-updater'})
        size=0;h=hashlib.sha256()
        with urllib.request.urlopen(req,timeout=30) as response,package.open('wb') as output:
            while True:
                if cancel():raise Cancelled()
                block=response.read(512*1024)
                if not block:break
                size+=len(block)
                if size>payload['bytes']:raise ValueError('Package exceeds expected size')
                output.write(block);h.update(block);progress(min(75,round(size/payload['bytes']*75)),'Downloading '+('app update' if kind=='app' else 'full runtime update'))
        if size!=payload['bytes'] or h.hexdigest()!=payload['sha256']:raise ValueError('Downloaded package checksum mismatch')
        progress(80,'Preparing the next installation')
        if kind=='app':
            def copy(src,dst):
                if cancel():raise Cancelled()
                if Path(src).is_relative_to(root/'runtime'):
                    try:os.link(src,dst);return dst
                    except OSError:pass
                return shutil.copy2(src,dst)
            shutil.copytree(root,stage,copy_function=copy,ignore=shutil.ignore_patterns('__pycache__','.pytest_cache'))
            # Copy-only app files, never overwrite runtime hard links.
            shutil.rmtree(stage/'checkpoint')
            unpack(package,stage,files=payload['files'],cancel=cancel)
            index=stage/'application-manifest.json'
            entries=json.loads(index.read_text()) if index.exists() else {}
            entries={k.replace('\\','/'):v for k,v in entries.items() if not k.replace('\\','/').startswith('checkpoint/')}
            entries.update(payload['files']);index.write_text(json.dumps(entries,indent=2),encoding='utf8')
        else:unpack(package,stage,prefix='Checkpoint-Windows/',cancel=cancel)
        portable_root(stage)
        if not (stage/'checkpoint/version.py').is_file():raise ValueError('Updated version information is missing')
        if cancel():raise Cancelled()
        package.unlink()
        backup=root.parent/'.checkpoint-backups'/job.name/root.name
        config={'original':str(root),'staged':str(stage),'backup':str(backup),'pid':os.getpid(),'tag':manifest['tag']}
        path=job/'job.json';path.write_text(json.dumps(config),encoding='utf8')
        progress(100,'Ready to restart')
        return path
    except BaseException:
        shutil.rmtree(job,ignore_errors=True);raise


# Static code: all paths are data read from our local job JSON, never interpolated code.
APPLY_SCRIPT=r'''
$ErrorActionPreference = 'Stop'
$jobPath = $env:CHECKPOINT_UPDATE_JOB
$config = Get-Content -LiteralPath $jobPath -Raw -Encoding UTF8 | ConvertFrom-Json
$root = $config.original; $stage = $config.staged; $backup = $config.backup
$jobDir = Split-Path -Parent $jobPath
$receipt = Join-Path $jobDir 'ready.json'
$result = Join-Path (Split-Path -Parent $jobDir) 'last-result.json'
$oldMoved = $false; $newMoved = $false
function Status($state, $message) {
    @{status=$state; tag=$config.tag; message=$message; backup=$backup} | ConvertTo-Json | Set-Content -LiteralPath $result -Encoding UTF8
}
function Launch {
    Start-Process -FilePath (Join-Path $root 'runtime\pythonw.exe') -ArgumentList ('"' + (Join-Path $root 'launch.py') + '" --no-setup') -WorkingDirectory $root -PassThru -ErrorAction Stop
}
try {
    $process = Get-Process -Id $config.pid -ErrorAction SilentlyContinue
    if ($process -and -not $process.WaitForExit(90000)) { throw 'Checkpoint did not exit. Close its other windows and retry.' }
    if (!(Test-Path -LiteralPath (Join-Path $stage 'runtime\pythonw.exe')) -or !(Test-Path -LiteralPath (Join-Path $stage 'launch.py'))) { throw 'Prepared installation is incomplete.' }
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $backup) | Out-Null
    Move-Item -LiteralPath $root -Destination $backup -ErrorAction Stop; $oldMoved = $true
    Move-Item -LiteralPath $stage -Destination $root -ErrorAction Stop; $newMoved = $true
    Status 'starting' 'Starting the updated app'
    $started = Launch
    $deadline = (Get-Date).AddSeconds(35)
    while (!(Test-Path -LiteralPath $receipt)) {
        if ($started.HasExited -or (Get-Date) -gt $deadline) { throw 'The updated app did not finish starting.' }
        Start-Sleep -Milliseconds 250
    }
    $ready = Get-Content -LiteralPath $receipt -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($ready.tag -ne $config.tag) { throw 'The restarted app has the wrong version.' }
    Status 'applied' 'Update installed successfully'
} catch {
    $message = $_.Exception.Message
    try {
        if ($newMoved) {
            if ($started -and !$started.HasExited) { Stop-Process -Id $started.Id -ErrorAction SilentlyContinue; $started.WaitForExit(10000) | Out-Null }
            Move-Item -LiteralPath $root -Destination ($stage + '.failed') -ErrorAction Stop
        }
        if ($oldMoved) { Move-Item -LiteralPath $backup -Destination $root -ErrorAction Stop }
        Status 'failed' ($message + ' The previous installation was preserved.')
        if (Test-Path -LiteralPath (Join-Path $root 'runtime\pythonw.exe')) { Launch | Out-Null }
    } catch { Status 'failed' ($message + ' Recovery details: ' + $_.Exception.Message) }
    exit 1
}
'''


def launch_update(job):
    if sys.platform!='win32':raise OSError('Restart installation requires Windows')
    encoded=base64.b64encode(APPLY_SCRIPT.encode('utf-16le')).decode('ascii')
    env=dict(os.environ,CHECKPOINT_UPDATE_JOB=str(job))
    return subprocess.Popen(['powershell.exe','-NoProfile','-NonInteractive','-EncodedCommand',encoded],env=env,cwd=Path(job).parents[2],creationflags=subprocess.CREATE_NO_WINDOW)


def signal_update_ready(root):
    job=os.environ.get('CHECKPOINT_UPDATE_JOB')
    if not job:return
    try:
        root=Path(root).resolve();path=Path(job).resolve()
        if not path.is_relative_to(root.parent/'.checkpoint-updates') or path.name!='job.json':return
        config=json.loads(path.read_text(encoding='utf8'))
        if Path(config['original']).resolve()!=root or config['tag']!=RELEASE_TAG:return
        (path.parent/'ready.json').write_text(json.dumps({'tag':RELEASE_TAG,'pid':os.getpid()}),encoding='utf8')
    except (OSError,ValueError,KeyError):pass
