"""Native update controls. Network and preparation run outside the UI thread."""
from pathlib import Path
import json
from PySide6.QtCore import QThread,Signal,QTimer
from PySide6.QtWidgets import QDialog,QVBoxLayout,QLabel,QPushButton,QProgressBar
from checkpoint.version import RELEASE_TAG
from checkpoint.updates import check_updates,prepare_update,launch_update,portable_root,package_kind,Cancelled

ROOT=Path(__file__).resolve().parents[1]


class UpdateWorker(QThread):
    progress=Signal(int,str)
    def __init__(self,manifest=None,parent=None):super().__init__(parent);self.manifest=manifest;self.result=None;self.error='';self.cancelled=False
    def run(self):
        try:
            self.result=check_updates() if self.manifest is None else prepare_update(ROOT,self.manifest,progress=self.progress.emit,cancel=self.isInterruptionRequested)
            self.cancelled=self.isInterruptionRequested()
        except Cancelled:self.cancelled=True
        except Exception as ex:self.error=str(ex)


class UpdateDialog(QDialog):
    def __init__(self,parent):
        super().__init__(parent);self.setWindowTitle('Checkpoint updates');self.resize(520,390);self.worker=None;self.manifest=None;self.installing=False;self.cancel_requested=False
        layout=QVBoxLayout(self);layout.setContentsMargins(28,24,28,24);layout.setSpacing(16)
        heading=QLabel('App updates');heading.setStyleSheet('font-size:26px;font-weight:600;');layout.addWidget(heading)
        self.version=QLabel('Installed: '+RELEASE_TAG.removeprefix('checkpoint-v'));layout.addWidget(self.version)
        self.status=QLabel('Checking the Checkpoint releases on GitHub…');self.status.setWordWrap(True);self.status.setAccessibleName('Update status');layout.addWidget(self.status)
        self.progress=QProgressBar();self.progress.setRange(0,100);self.progress.hide();layout.addWidget(self.progress)
        copy=QLabel('Updates are installed only when you choose. Camera, game tracking and phone sharing stop for the restart. Your saved check-ins stay in Windows app data.');copy.setWordWrap(True);layout.addWidget(copy)
        layout.addStretch();self.action=QPushButton('Check again');self.action.clicked.connect(self.act);self.action.setMinimumHeight(46);layout.addWidget(self.action)
        self.close_button=QPushButton('Close');self.close_button.clicked.connect(self.reject);self.close_button.setMinimumHeight(44);layout.addWidget(self.close_button)
        QTimer.singleShot(0,self.check)

    def act(self):
        if self.manifest and self.manifest['available']:
            window=self.parent()
            if not window.pause() or not window.stop_game_tracking():self.status.setText('Wait for capture to stop, then retry.');return
            self.installing=True;self.start_worker(self.manifest)
        else:self.check()

    def check(self):self.manifest=None;self.installing=False;self.start_worker()

    def start_worker(self,manifest=None):
        self.cancel_requested=False;self.worker=UpdateWorker(manifest,self);self.worker.progress.connect(self.progress_changed);self.worker.finished.connect(self.completed)
        self.action.setEnabled(False);self.close_button.setText('Cancel');self.progress.setVisible(manifest is not None);self.progress.setValue(0)
        self.status.setText('Preparing update…' if manifest else 'Checking Checkpoint releases on GitHub…');self.worker.start()

    def progress_changed(self,value,message):self.progress.setValue(value);self.status.setText(message)

    def completed(self):
        worker=self.worker;result,error,cancelled=worker.result,worker.error,worker.cancelled
        self.worker=None;worker.deleteLater();self.action.setEnabled(True);self.close_button.setText('Close')
        if cancelled or self.cancel_requested:super().reject();return
        if error:self.status.setText('Update could not complete: '+error);self.action.setText('Retry update' if self.manifest else 'Check again');return
        if self.installing:
            try:launch_update(result)
            except Exception as ex:self.status.setText('Could not start the restart helper: '+str(ex));return
            self.accept();QTimer.singleShot(0,self.parent().close);return
        self.manifest=result
        if not result or not result['available']:self.status.setText('You’re up to date.');self.action.setText('Check again');return
        self.version.setText('Installed: '+RELEASE_TAG.removeprefix('checkpoint-v')+'\nAvailable: '+result['tag'].removeprefix('checkpoint-v'))
        try:portable_root(ROOT);kind=package_kind(ROOT,result)
        except ValueError as ex:self.status.setText(str(ex));self.manifest=None;return
        size=result[kind]['bytes']/1024**2
        self.status.setText(f'An update is available ({size:.1f} MB). '+('Your existing runtime and models can be reused.' if kind=='app' else 'This version needs the full runtime package.'))
        self.action.setText('Update and restart')

    def request_cancel(self):
        if self.worker is not None:self.cancel_requested=True
        if self.worker and self.worker.isRunning():self.cancel_requested=True;self.worker.requestInterruption();self.status.setText('Cancelling safely…');return True
        return False

    def reject(self):
        if not self.request_cancel():super().reject()

    def closeEvent(self,event):
        if self.request_cancel():event.ignore()
        else:super().closeEvent(event)


def last_update_error(root):
    try:
        result=json.loads((root.parent/'.checkpoint-updates/last-result.json').read_text(encoding='utf-8-sig'))
        return 'The last update could not be applied. Open Settings > App updates to retry.' if isinstance(result,dict) and result.get('status')=='failed' else ''
    except (OSError,ValueError):return ''
