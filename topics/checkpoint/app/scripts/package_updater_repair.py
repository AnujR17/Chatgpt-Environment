"""Package the small legacy bridge without including or requiring a new runtime."""
import base64
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED

ROOT=Path(__file__).resolve().parents[1]
script=r'''
$ErrorActionPreference='Stop'
$directory=$env:CHECKPOINT_REPAIR_DIRECTORY
$root=$directory.TrimEnd('\')
if (!(Test-Path -LiteralPath (Join-Path $root 'runtime\python.exe'))) {
    $root=(Read-Host 'Paste the EXISTING Checkpoint-Windows folder path').Trim().Trim('"')
}
if (!(Test-Path -LiteralPath (Join-Path $root 'runtime\python.exe'))) { Write-Host 'That folder does not contain the Checkpoint runtime.'; Read-Host 'Press Enter to close'; exit 1 }
Write-Host 'Close all Checkpoint app and Check setup windows first. Do not delete your app folder.'
Read-Host 'Press Enter when they are closed'
& (Join-Path $root 'runtime\python.exe') -B (Join-Path $directory 'repair_update.py') $root
if ($LASTEXITCODE -ne 0) { Read-Host 'Press Enter to close'; exit 1 }
Write-Host 'The helper will install and restart Checkpoint. You may close this window.'
Read-Host 'Press Enter to close'
'''
encoded=base64.b64encode(script.encode('utf-16le')).decode('ascii')
command='@echo off\r\nsetlocal\r\nset "CHECKPOINT_REPAIR_DIRECTORY=%~dp0"\r\npowershell.exe -NoProfile -EncodedCommand '+encoded+'\r\n'
notes='''Checkpoint updater repair (one time for a legacy folder-swap failure)

Extract this small ZIP, then run Repair Checkpoint update.cmd.
Paste the EXISTING Checkpoint-Windows folder path when asked.
Close all Checkpoint and Check setup windows, then press Enter.
The repair verifies and reuses/downloads the small app package using your existing runtime.
It does not install Python, change your firewall, or modify Windows execution policy.
Your saved check-ins remain in Windows app data.
Future updates use Settings > Check for updates > Update and restart.
The runtime and installation folder remain in place for app-only updates.
'''
with ZipFile(ROOT.parent/'Checkpoint-Updater-Repair.zip','w',ZIP_DEFLATED) as archive:
    archive.writestr('Repair Checkpoint update.cmd',command)
    archive.write(ROOT/'scripts/repair_update.py','repair_update.py')
    archive.writestr('READ ME.txt',notes)
print('Updater repair package created.')
