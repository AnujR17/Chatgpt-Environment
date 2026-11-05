"""Native Qt companion. Camera/video and facial cues are local and explicitly enabled."""
import argparse
import json
import math
import os
from pathlib import Path
import sys
import time
from PySide6.QtCore import Qt, QTimer, QStandardPaths, QEvent, QUrl
from PySide6.QtGui import QFont, QFontDatabase, QImage, QPixmap, QCloseEvent, QIcon, QShortcut, QKeySequence, QDesktopServices
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import (QApplication,QMainWindow,QWidget,QFrame,QLabel,QPushButton,QVBoxLayout,QHBoxLayout,
 QStackedWidget,QDialog,QDialogButtonBox,QComboBox,QLineEdit,QCheckBox,QDoubleSpinBox,QMessageBox,QFileDialog,QMenu,QScrollArea,QSystemTrayIcon,QGridLayout,QSlider,QSizePolicy)
from checkpoint.session import Session, History, FEELINGS
from checkpoint.theme import STYLE, make_style, PALETTES
from checkpoint.affect import ANCHORS, REFERENCES, dimension_words
from checkpoint.motion import AffectWidget
from checkpoint.symbols import CORE, MEANINGS
from checkpoint.vocabulary import CARDS, COMMON, search_cards
from checkpoint.expression_view import expression_display
from checkpoint.gameplay import GameWorker
from checkpoint.blob import PipWidget
from checkpoint.overlay import PipOverlay
from checkpoint.phone import PhoneBridge,PhoneServer,local_networks,private_firewall_command
from checkpoint.companion import CompanionState
from checkpoint.input_activity import InputObserver

ASSETS=Path(__file__).with_name("assets")


def label(text="",size=14,secondary=False,bold=False):
    obj=QLabel(text);obj.setWordWrap(True);font=QFont("DM Sans");font.setPixelSize(size);font.setWeight(QFont.Weight.DemiBold if bold else QFont.Weight.Normal);obj.setFont(font)
    if secondary:obj.setObjectName("secondary")
    obj.setTextFormat(Qt.TextFormat.PlainText)
    return obj


def button(text,callback,primary=False):
    obj=QPushButton(text);obj.setProperty("primary",primary);obj.setCursor(Qt.CursorShape.PointingHandCursor);obj.setMinimumHeight(48);obj.clicked.connect(callback);obj.setAccessibleName(text);return obj


def panel(name="panel",padding=24):
    obj=QFrame();obj.setObjectName(name);layout=QVBoxLayout(obj);layout.setContentsMargins(padding,padding,padding,padding);layout.setSpacing(16);return obj,layout


Emblem = AffectWidget


class VideoPreview(QLabel):
    def __init__(self):
        super().__init__("Camera is off\n\nResume only when you choose.");self.setAlignment(Qt.AlignmentFlag.AlignCenter);self.setWordWrap(True)
        self.setMinimumSize(280,210);self.setObjectName("cameraPreview");self.setStyleSheet("background:#EEEEE6; border-radius:14px; color:#626B65;");self.image=None
        self.setAccessibleName("Local camera or video preview")

    def set_image(self,image):
        if self.image is not None and self.image.cacheKey()==image.cacheKey():return
        self.image=image;self._draw()

    def _draw(self):
        if self.image is not None:self.setPixmap(QPixmap.fromImage(self.image).scaled(self.size(),Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation))

    def clear_image(self,text="Camera is off\n\nResume only when you choose."):
        if self.image is None and self.text()==text:return
        self.image=None;self.clear();self.setText(text)

    def resizeEvent(self,event):
        super().resizeEvent(event);self._draw()


class EmotionCard(QPushButton):
    def __init__(self,key,parent_window,callback):
        super().__init__();self.key=key;self.setObjectName('emotionCard');self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumSize(190,184);self.setAccessibleName(CARDS[key]['label']);self.clicked.connect(lambda checked=False:callback(key))
        layout=QVBoxLayout(self);layout.setContentsMargins(12,8,12,12);layout.setSpacing(0)
        self.art=Emblem(154);self.art.configure(theme=parent_window.theme,reduced_motion=True);self.art.set_state(key);self.art.fade_override=1.
        self.art.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents);layout.addWidget(self.art,alignment=Qt.AlignmentFlag.AlignCenter)
        title=label(CARDS[key]['label'],17,bold=True);title.setAlignment(Qt.AlignmentFlag.AlignCenter);title.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents);layout.addWidget(title)


class EmotionLibraryDialog(QDialog):
    def __init__(self,parent):
        super().__init__(parent);self.setWindowTitle('Choose a feeling');self.resize(min(1100,max(900,parent.width()-40)),min(780,max(600,parent.height()-40)));self.setMinimumSize(900,600);self.chosen=None;self.common=True
        root=QVBoxLayout(self);root.setContentsMargins(28,24,28,24);root.setSpacing(16)
        root.addWidget(label('How are you feeling?',30,bold=True));root.addWidget(label('Choose a card. You can add detail before saving.',15,True))
        controls=QHBoxLayout();self.common_button=button('Common feelings',lambda:self.set_group(True),True);self.all_button=button(f'All feelings ({len(CARDS)})',lambda:self.set_group(False));controls.addWidget(self.common_button);controls.addWidget(self.all_button);controls.addStretch()
        self.search=QLineEdit();self.search.setPlaceholderText('Search feelings, e.g. annoyed');self.search.setClearButtonEnabled(True);self.search.setAccessibleName('Search all feelings');self.search.setMinimumWidth(340);self.search.textChanged.connect(self.search_changed);self.search.returnPressed.connect(self.choose_search_result);controls.addWidget(self.search);root.addLayout(controls)
        self.scroll=QScrollArea();self.scroll.setWidgetResizable(True);content=QWidget();self.scroll.setWidget(content);container=QVBoxLayout(content);container.setContentsMargins(0,0,0,0);self.grid=QGridLayout();self.grid.setSpacing(12)
        for column in range(4):self.grid.setColumnStretch(column,1)
        container.addLayout(self.grid);container.addStretch();root.addWidget(self.scroll,1)
        self.cards={key:EmotionCard(key,parent,self.choose) for key in CARDS}
        self.empty=label('No matching feelings. Try another word, or choose Not sure.',17,True);self.empty.setAlignment(Qt.AlignmentFlag.AlignCenter);container.addWidget(self.empty)
        footer=QHBoxLayout();footer.addWidget(button('Not sure',lambda:self.choose('mixed')));footer.addStretch();self.count=label('',13,True);footer.addWidget(self.count);footer.addSpacing(16);footer.addWidget(button('Cancel',self.reject));root.addLayout(footer);self.filter_cards()

    def choose_search_result(self):
        if len(self.visible_keys)==1:self.choose(self.visible_keys[0])
    def set_group(self,common):self.common=common;self.filter_cards()
    def search_changed(self,text):
        if text.strip():self.common=False
        self.filter_cards()
    def filter_cards(self):
        while self.grid.count():self.grid.takeAt(0)
        for card in self.cards.values():card.hide()
        keys=search_cards(self.search.text(),self.common);self.visible_keys=keys
        for i,key in enumerate(keys):self.grid.addWidget(self.cards[key],i//4,i%4);self.cards[key].show()
        self.empty.setVisible(not keys);self.count.setText(f"{len(keys)} {'feeling' if len(keys)==1 else 'feelings'}" if keys else '')
        for b,active in [(self.common_button,self.common),(self.all_button,not self.common)]:b.setProperty('primary',active);b.style().unpolish(b);b.style().polish(b)
        self.scroll.verticalScrollBar().setValue(0)
    def choose(self,key):self.chosen=key;self.accept()


class CheckinDialog(QDialog):
    def __init__(self,parent,initial=None):
        super().__init__(parent);self.setWindowTitle('Your check-in');self.resize(820,590);self.chosen=None;self.valence=None;self.arousal=None
        root=QVBoxLayout(self);root.setContentsMargins(28,28,28,24);root.setSpacing(20)
        root.addWidget(label('Your check-in',30,bold=True));root.addWidget(label('Adjust the balance to fit this moment.',15,True))
        main=QHBoxLayout();main.setSpacing(28);card,cl=panel('artStage',20);card.setFixedWidth(260)
        self.preview=Emblem(210);self.preview.configure(theme=parent.theme,reduced_motion=parent.reduced_motion,paused=parent.motion_paused);cl.addWidget(self.preview,alignment=Qt.AlignmentFlag.AlignCenter)
        self.feeling_label=label('Choose a feeling',23,bold=True);self.feeling_label.setAlignment(Qt.AlignmentFlag.AlignCenter);cl.addWidget(self.feeling_label);cl.addWidget(button('Change feeling',self.change_feeling));main.addWidget(card)
        dimensions=QVBoxLayout();dimensions.setSpacing(14);self.sliders=[];self.readouts=[];self.choices={}
        for heading,left,right in [('Pleasantness','Unpleasant','Pleasant'),('Energy / activation','Low energy','High energy')]:
            row=QHBoxLayout();row.addWidget(label(heading,17,bold=True),1);readout=label('Not reported',13,True);row.addWidget(readout);dimensions.addLayout(row);self.readouts.append(readout)
            slider=QSlider(Qt.Orientation.Horizontal);slider.setRange(-100,100);slider.setAccessibleName(heading);slider.setEnabled(False);slider.valueChanged.connect(self.adjust);dimensions.addWidget(slider);self.sliders.append(slider)
            ends=QHBoxLayout();ends.addWidget(label(left,12,True));ends.addStretch();ends.addWidget(label(right,12,True));dimensions.addLayout(ends);dimensions.addSpacing(24)
        dimensions.addWidget(label('These two dimensions describe your own experience.',13,True));dimensions.addStretch();main.addLayout(dimensions,1);root.addLayout(main,1)
        footer=QHBoxLayout();footer.addWidget(button('Not sure',lambda:self.choose('mixed')));footer.addStretch();footer.addWidget(button('Cancel',self.reject));self.save=button('Save check-in',self.commit,True);self.save.setEnabled(False);self.save.setDefault(True);footer.addWidget(self.save);root.addLayout(footer)
        key=initial if initial in FEELINGS else parent.session.report
        if key in FEELINGS:
            self.select(key)
            if key==parent.session.report and parent.session.valence is not None:
                self.sliders[0].setValue(round(parent.session.valence*100));self.sliders[1].setValue(round(parent.session.arousal*100))

    def select(self,key):
        if key not in FEELINGS:raise ValueError('Unknown feeling')
        self.chosen=key;self.feeling_label.setText(FEELINGS[key][0]);self.save.setEnabled(True)
        if key=='mixed':
            self.valence=None;self.arousal=None
            for slider in self.sliders:slider.setEnabled(False)
            for readout in self.readouts:readout.setText('Not specified')
            self.preview.set_state(None);return
        for slider,value in zip(self.sliders,REFERENCES[key][1:3]):slider.blockSignals(True);slider.setEnabled(True);slider.setValue(round(value*100));slider.blockSignals(False)
        self.adjust()
    def change_feeling(self):
        dialog=EmotionLibraryDialog(self.parentWidget())
        if dialog.exec()==QDialog.DialogCode.Accepted:self.select(dialog.chosen)
    def adjust(self):
        if self.chosen not in REFERENCES:return
        self.valence,self.arousal=[x.value()/100 for x in self.sliders]
        for obj,word in zip(self.readouts,dimension_words(self.valence,self.arousal)):obj.setText(word)
        self.preview.set_state(self.chosen,self.valence,self.arousal)
    def commit(self):
        if self.chosen is not None:self.accept()
    def choose(self,key):self.select(key);self.accept()


class SetupDialog(QDialog):
    def __init__(self,parent,session):
        super().__init__(parent);self.setWindowTitle("Session setup");self.resize(620,480)
        root=QVBoxLayout(self);root.setContentsMargins(28,28,28,28);root.setSpacing(16)
        root.addWidget(label("Start a session",30,bold=True));root.addWidget(label("Choose your game and intention. Your camera starts off.",16,True))
        root.addWidget(label("Game"));self.game=QComboBox();self.game.setEditable(True);self.game.addItems(["Getting Over It","Valorant","Counter-Strike 2","Other / manual context"]);self.game.setCurrentText(session.game);root.addWidget(self.game)
        root.addWidget(label("Session intention"));self.intention=QComboBox();self.intention.addItems(["Enjoy the challenge","Practice","Play with friends","Decompress"]);self.intention.setCurrentText(session.intention);root.addWidget(self.intention)
        self.competitive=QCheckBox("Competitive session");self.competitive.setChecked(session.competitive);root.addWidget(self.competitive)
        root.addWidget(label("You can change the game context during your session.",14,True))
        box=QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel);box.button(QDialogButtonBox.StandardButton.Ok).setText("Start session");box.accepted.connect(self.accept);box.rejected.connect(self.reject);root.addWidget(box)


class PreferencesDialog(QDialog):
    def __init__(self,parent):
        super().__init__(parent);self.setWindowTitle('Settings');self.resize(680,min(650,max(540,parent.height()-40)))
        outer=QVBoxLayout(self);outer.setContentsMargins(24,24,24,24);outer.setSpacing(16)
        from checkpoint.version import RELEASE_TAG
        header=QHBoxLayout();header.addWidget(label('Settings',28,bold=True),1);header.addWidget(label(RELEASE_TAG.removeprefix('checkpoint-v'),12,True))
        def open_updates():self.reject();QTimer.singleShot(0,parent.show_updates)
        header.addWidget(button('Check for updates',open_updates));outer.addLayout(header)
        scroll=QScrollArea();scroll.setWidgetResizable(True);content=QWidget();scroll.setWidget(content);root=QVBoxLayout(content);root.setContentsMargins(4,4,12,8);root.setSpacing(14);outer.addWidget(scroll,1)
        root.addWidget(label('Display',18,bold=True));self.reduced=QCheckBox('Reduce animation');self.reduced.setChecked(parent.reduced_motion);root.addWidget(self.reduced)
        self.pip=QCheckBox('Show Pip on the desktop');self.pip.setChecked(parent.overlay_enabled);root.addWidget(self.pip)
        root.addWidget(label('Pip is transparent, frameless and click-through while playing. Borderless/windowed games are recommended; exclusive fullscreen and protected game surfaces may hide a separate desktop window.',13,True))
        self.corner=QComboBox();self.corner.addItems(['bottom-right','bottom-left','top-right','top-left']);self.corner.setCurrentText(parent.overlay_corner);root.addWidget(self.corner)
        if parent.overlay_enabled:
            def move_pip():self.reject();QTimer.singleShot(0,parent.edit_overlay_position)
            root.addWidget(button('Move Pip on the desktop',move_pip))
        root.addWidget(label('History',18,bold=True));self.retention=QCheckBox('Save session summaries on this device');self.retention.setChecked(parent.retain);root.addWidget(self.retention);root.addWidget(label('Stores your check-ins, game and session duration. Camera frames are never saved.',13,True))
        root.addWidget(label('Expression research',18,bold=True));self.experimental=QCheckBox('Enable experimental facial-expression cues');self.experimental.setChecked(parent.session.experimental_analysis);root.addWidget(self.experimental)
        self.engine=QComboBox();self.engine.addItems(['Facial movements · recommended','HSEmotion expression estimates · experimental']);self.engine.setCurrentIndex(0 if parent.session.face_mapping else 1);root.addWidget(self.engine)
        strength=QHBoxLayout();strength.addWidget(label('Pip facial movement strength',14),1);self.face_gain=QDoubleSpinBox();self.face_gain.setRange(.7,3.);self.face_gain.setSingleStep(.1);self.face_gain.setValue(parent.session.face_gain);strength.addWidget(self.face_gain);root.addLayout(strength)
        root.addWidget(label('Research only. Expression categories cannot establish mood, frustration or either CMA dimension. They never change your check-in.',13,True))
        root.addWidget(label('Game context',18,bold=True));self.detect_games=QCheckBox('Detect supported foreground games on Windows');self.detect_games.setChecked(parent.detect_games);root.addWidget(self.detect_games)
        self.screen_tracking=QCheckBox('Observe the Getting Over It game window');self.screen_tracking.setChecked(parent.screen_tracking);root.addWidget(self.screen_tracking)
        root.addWidget(label('Only the foreground Getting Over It window is sampled, twice per second. Possible climb/fall cues use camera motion and are not validated event labels. No screen images are saved. Other windows are not analysed.',13,True))
        self.input_timing=QCheckBox('Observe game-focused mouse and key timing');self.input_timing.setChecked(parent.input_observer.enabled);root.addWidget(self.input_timing)
        root.addWidget(label('Counts movement, clicks, key intervals and hold times only while a supported game has focus. No typed text or key identities are exported. Activity is not a mood measurement.',13,True))
        self.nudges=QCheckBox('Let Pip offer a quiet pause after possible setbacks');self.nudges.setChecked(parent.nudges_enabled);root.addWidget(self.nudges)
        root.addWidget(label('Requires game observation and input timing. Waits for a quiet moment, with at least two minutes between invitations. Does not pause or control the game.',13,True))
        frequency=QHBoxLayout();frequency.addWidget(label('Analysis frames per second',14),1);self.frequency=QDoubleSpinBox();self.frequency.setRange(.25,5);self.frequency.setSingleStep(.25);self.frequency.setValue(parent.frequency);self.frequency.setEnabled(self.experimental.isChecked());self.experimental.toggled.connect(self.frequency.setEnabled);frequency.addWidget(self.frequency);root.addLayout(frequency)
        root.addWidget(label('Applies to this app launch. Saving settings pauses an active camera or video; resume it when you choose.',13,True));root.addStretch()
        box=QDialogButtonBox(QDialogButtonBox.StandardButton.Save|QDialogButtonBox.StandardButton.Cancel);box.accepted.connect(self.accept);box.rejected.connect(self.reject);outer.addWidget(box)


class MainWindow(QMainWindow):
    def __init__(self, *, no_setup=False, data_dir=None):
        super().__init__();self.setWindowTitle("Checkpoint");self.resize(1440,940);self.setMinimumSize(1000,640)
        self.session=Session();self.worker=None;self.frequency=4.;self.retain=False;self.saved=False;self.current_view=0;self.theme="light";self.reduced_motion=False;self.motion_paused=False;self.last_image=None;self.last_status="";self._closing=False;self.update_dialog=None
        self.live_view=False;self.expression_controls=[];self.neutral_controls=[];self.view_selectors=[];self.detect_games=False;self.screen_tracking=False;self.game_worker=None;self.game_observation=None
        self.overlay=PipOverlay();self.overlay_enabled=False;self.overlay_corner='bottom-right';self.nudges_enabled=False;self.last_nudge=''
        self.phone_bridge=PhoneBridge();self.phone_server=None;self.companion=CompanionState();self.latest_report={};self.latest_companion={};self.next_export=0.
        self.input_observer=InputObserver(QApplication.instance(),int(self.winId()))
        directory=data_dir or os.environ.get("CHECKPOINT_DATA_DIR") or QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppLocalDataLocation)
        self.history=History(directory);self.preview_widgets=[];self.emblems=[];self.state_labels=[];self.camera_index=0;self.camera_selectors=[];self.camera_messages=[]
        outer=QWidget();self.setCentralWidget(outer);all_layout=QVBoxLayout(outer);all_layout.setContentsMargins(0,0,0,0);all_layout.setSpacing(0)
        nav=QFrame();nav.setObjectName('nav');nav.setFixedHeight(72);nl=QHBoxLayout(nav);nl.setContentsMargins(28,8,28,8);nl.setSpacing(12)
        mark=label('c.',26,bold=True);mark.setFixedSize(36,36);mark.setAlignment(Qt.AlignmentFlag.AlignCenter);mark.setStyleSheet('background:#235C49;color:#FFFFFF;border-radius:12px;');nl.addWidget(mark);nl.addWidget(label('checkpoint',18,bold=True));nl.addSpacing(36)
        for text,cb in [('Session',self.return_to_session),('Feelings',self.show_emotion_library),('Check-ins',self.show_history),('Report',self.show_report),('Settings',self.show_preferences)]:
            b=button(text,cb);b.setObjectName('navButton');nl.addWidget(b)
            if text=='Feelings':self.library_control=b
        nl.addStretch();self.theme_button=button('Dark theme',self.toggle_theme);nl.addWidget(self.theme_button);all_layout.addWidget(nav)
        self.scroll=QScrollArea();self.scroll.setWidgetResizable(True);all_layout.addWidget(self.scroll,1);canvas=QWidget();self.scroll.setWidget(canvas);root=QVBoxLayout(canvas);root.setContentsMargins(28,24,28,20);root.setSpacing(16)
        h=QHBoxLayout();words=QVBoxLayout();words.setSpacing(6);self.title=label('Your session',30,bold=True);self.subtitle=label('',14,True);words.addWidget(self.title);words.addWidget(self.subtitle);h.addLayout(words,1)
        self.game_tag=label('',12,True);h.addWidget(self.game_tag);h.addSpacing(24);self.end_control=button('End session',self.end_or_new);h.addWidget(self.end_control);root.addLayout(h)
        context_row=QHBoxLayout();self.game_status=label('Game detection is off · Game events are not being observed.',13,True);context_row.addWidget(self.game_status,1)
        self.game_detection_control=button('Detect game',self.toggle_game_tracking);context_row.addWidget(self.game_detection_control)
        self.mark_start_control=button('Mark start view',self.mark_start_view);self.mark_start_control.setVisible(False);context_row.addWidget(self.mark_start_control);root.addLayout(context_row)
        self.pip_control=button('Show Pip',self.toggle_overlay);context_row.addWidget(self.pip_control)
        self.phone_control=button('Phone dashboard',self.show_phone);context_row.addWidget(self.phone_control)
        self.view_buttons=[];self.camera_controls=[];self.file_controls=[];self.checkin_controls=[];self.motion_controls=[]
        for i in range(3):
            b=button('Development view',lambda checked=False,idx=i:self.change_view(idx));b.setParent(self);b.hide();self.view_buttons.append(b)
        self.bodies=QStackedWidget();self.bodies.setMinimumHeight(550);root.addWidget(self.bodies,1)
        for mode in range(3):self.bodies.addWidget(self.build_body(mode))
        self.bodies.addWidget(self.build_break_body());self.bodies.addWidget(self.build_summary_body())
        support,sl=panel(padding=18);support.setMinimumHeight(82);support_row=QHBoxLayout();copy=QVBoxLayout();copy.setSpacing(4);self.support_title=label('Need a break?',18,bold=True);self.support_copy=label('Your camera pauses while you step away.',13,True);copy.addWidget(self.support_title);copy.addWidget(self.support_copy);support_row.addLayout(copy,1)
        self.break_button=button('30-second break',self.toggle_break);support_row.addWidget(self.break_button);support_row.addWidget(button('Support options',self.show_support));sl.addLayout(support_row);root.addWidget(support)
        foot=QHBoxLayout();self.footer=label('',12,True);foot.addWidget(self.footer,1);context=button('Edit game context',self.edit_context);context.setObjectName('navButton');foot.addWidget(context);root.addLayout(foot)
        self.timer=QTimer(self);self.timer.timeout.connect(self.poll);self.timer.start(66);self.tray=None
        self.shortcuts=[]
        for key,callback in [("Ctrl+Shift+P",self.pause_all),("Ctrl+Shift+C",self.check_in),("Ctrl+Shift+B",self.toggle_break)]:
            shortcut=QShortcut(QKeySequence(key),self);shortcut.activated.connect(callback);self.shortcuts.append(shortcut)
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray=QSystemTrayIcon(QIcon(str(ASSETS/"unknown.svg")),self);menu=QMenu(self)
            menu.addAction("Open Checkpoint",self.showNormal);menu.addAction('Check for updates',self.show_updates);menu.addAction("Show / hide Pip",self.toggle_overlay);menu.addAction("Pause all sources",self.pause_all);menu.addAction("Check in",self.check_in);menu.addAction("Take a break",self.toggle_break);menu.addAction("Quit",self.close);self.tray.setContextMenu(menu);self.tray.show()
        from checkpoint.update_ui import last_update_error
        self.last_status=last_update_error(Path(__file__).resolve().parents[1])
        self.refresh()
        QApplication.instance().applicationStateChanged.connect(self.application_state)
        if not no_setup:QTimer.singleShot(0,self.new_session)

    def build_body(self,mode):
        body=QWidget();row=QHBoxLayout(body);row.setContentsMargins(0,0,0,0);row.setSpacing(18)
        state_panel,sl=panel(padding=24);sl.setSpacing(14)
        header=QHBoxLayout();selector=QComboBox();selector.addItems(['Your check-in','Live expression']);selector.setAccessibleName('Card source');selector.setFixedWidth(185);selector.currentIndexChanged.connect(self.select_card_source);self.view_selectors.append(selector);header.addWidget(selector);header.addStretch();source=label('',12,True);self.state_labels.append((source,'source'));header.addWidget(source);motion=button('Pause animation',self.toggle_motion);motion.setMinimumHeight(36);motion.setObjectName('navButton');header.addWidget(motion);self.motion_controls.append(motion)
        if mode==0:self.motion_button=motion
        sl.addLayout(header);middle=QHBoxLayout();middle.setSpacing(24)
        stage,stage_layout=panel('artStage',0);stage.setFixedSize(230,230);em=PipWidget(220,mode=mode);self.emblems.append(em);stage_layout.addWidget(em,alignment=Qt.AlignmentFlag.AlignCenter);middle.addWidget(stage)
        words=QVBoxLayout();words.setSpacing(10);words.addStretch();title=label('',38,bold=True);desc=label('',15,True);self.state_labels.extend([(title,'title'),(desc,'description')]);words.addWidget(title);words.addWidget(desc)
        check=button('Choose a feeling',self.primary_action,True);self.checkin_controls.append(check)
        if mode==0:self.checkin_button=check
        words.addSpacing(10);words.addWidget(check);words.addStretch();middle.addLayout(words,1);sl.addLayout(middle,1)
        dimensions,dl=panel('stateCard',14);dl.addWidget(label('Your reported CMA · updated by your check-in',12,True));self.add_dimensions(dl);sl.addWidget(dimensions);row.addWidget(state_panel,7)
        camera,cl=panel(padding=24);cl.setSpacing(14);ch=QHBoxLayout();ch.addWidget(label('Your camera',18,bold=True),1);status=label('',12,True);self.state_labels.append((status,'capture'));ch.addWidget(status);cl.addLayout(ch)
        preview=VideoPreview();preview.setMinimumSize(300,230);preview.setMaximumHeight(260);self.preview_widgets.append(preview);cl.addWidget(preview)
        devices=QComboBox();devices.setAccessibleName('Camera device');devices.addItems(['Camera 1 · default']+[f'Camera {i+1}' for i in range(1,10)]);devices.currentIndexChanged.connect(self.select_camera);self.camera_selectors.append(devices);cl.addWidget(devices)
        feedback=label('',13,True);self.camera_messages.append(feedback);cl.addWidget(feedback)
        track=QCheckBox('Track my face');track.setAccessibleName('Track expressions');track.toggled.connect(self.toggle_expression_tracking);self.expression_controls.append(track);cl.addWidget(track)
        neutral=button('Set my neutral face',self.calibrate_neutral);self.neutral_controls.append(neutral);cl.addWidget(neutral)
        cl.addWidget(label('Optional preview. Your check-in is always your choice.',14,True));actions=QHBoxLayout();capture=button('Start camera',self.toggle_camera);self.camera_controls.append(capture);actions.addWidget(capture,1);file=button('Open video',self.open_video);self.file_controls.append(file);actions.addWidget(file,1);cl.addLayout(actions)
        if mode==0:self.capture_control=capture
        cl.addWidget(label('On this device · No recording · Microphone off',12,True));cue=label('',12,True);cue.setVisible(False);self.state_labels.append((cue,'cue'));cl.addWidget(cue);cl.addStretch();row.addWidget(camera,4)
        return body

    def return_to_session(self):self.refresh();self.scroll.verticalScrollBar().setValue(0)
    def select_card_source(self,index):
        self.live_view=index==1;self.refresh()

    def toggle_expression_tracking(self,enabled):
        source=self.worker.source if self.worker is not None and self.session.camera_active else None
        if not self.pause():return
        self.session.experimental_analysis=bool(enabled)
        if enabled:self.live_view=True
        if source is not None:self.start_source(source)
        self.refresh()

    def calibrate_neutral(self):
        if self.worker is not None and self.worker.face_mapping and self.session.experimental_analysis:
            self.worker.neutral_requested.set();self.last_status='Relax your face and look at the camera for a few seconds. No photos are saved.'

    def toggle_game_tracking(self):
        if self.detect_games:self.stop_game_tracking();self.refresh()
        else:self.configure_game_tracking(True,False)

    def configure_game_tracking(self,enabled,screen):
        if not self.stop_game_tracking():return
        self.detect_games=bool(enabled or screen);self.screen_tracking=bool(screen);self.game_observation=None
        if self.detect_games and sys.platform=='win32' and self.session.active:
            worker=GameWorker(screen=self.screen_tracking);self.game_worker=worker
            worker.observation.connect(lambda observation,w=worker:self.receive_game_observation(w,observation));worker.start()
        elif self.detect_games:self.game_status.setText('Live game-window tracking requires Windows.')
        self.refresh()

    def stop_game_tracking(self):
        self.input_observer.stop()
        if self.game_worker is not None:
            if not self.game_worker.stop():return False
            self.game_worker.deleteLater();self.game_worker=None
        self.detect_games=False;self.screen_tracking=False;self.game_observation=None
        self.companion.fall_pending=False;self.companion.nudge='';self.overlay.message='';self.overlay.update()
        return True

    def toggle_overlay(self):
        self.overlay_enabled=not self.overlay_enabled;self.overlay.setVisible(self.overlay_enabled);self.refresh()

    def edit_overlay_position(self):
        self.overlay_enabled=True;self.overlay.show();self.overlay.set_editable(True)
        dialog=QDialog(self);dialog.setWindowTitle('Move Pip');dialog.setWindowModality(Qt.WindowModality.NonModal);dialog.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        layout=QVBoxLayout(dialog);layout.addWidget(label('Drag Pip to a comfortable position. Click Done to restore click-through play.',15));layout.addWidget(button('Done',dialog.accept,True))
        dialog.finished.connect(lambda *_:self.overlay.set_editable(False));self.position_dialog=dialog;dialog.show()

    def application_state(self,state):
        if state==Qt.ApplicationState.ApplicationInactive and self.overlay.editing:self.overlay.set_editable(False)

    def show_phone(self):
        if self.phone_server is None:
            try:self.phone_server=PhoneServer(self.phone_bridge).start()
            except OSError as ex:
                self.phone_server=None;QMessageBox.warning(self,'Phone connection unavailable','Could not start local sharing: '+str(ex));return
        self.refresh();dialog=QDialog(self);dialog.setWindowTitle('Pip on your phone');dialog.resize(510,740)
        outer=QVBoxLayout(dialog);scroll=QScrollArea();scroll.setWidgetResizable(True);content=QWidget();layout=QVBoxLayout(content);layout.setContentsMargins(24,20,24,20);scroll.setWidget(content);outer.addWidget(scroll,1)
        layout.addWidget(label('Pip on your phone',28,bold=True));layout.addWidget(label('Use the same trusted Wi-Fi on both devices. Choose your Wi-Fi or Ethernet adapter below, then scan.',15,True))
        networks=QComboBox()
        for name,address in local_networks():networks.addItem(name+' · '+address,address)
        networks.setAccessibleName('Laptop network address');layout.addWidget(networks)
        qr=QSvgWidget();qr.setFixedSize(240,240);layout.addWidget(qr,alignment=Qt.AlignmentFlag.AlignCenter);address=label('',14,True);layout.addWidget(address)
        connection=label('',14);layout.addWidget(connection)
        import qrcode
        from qrcode.image.svg import SvgPathImage
        def update_qr():
            url=self.phone_server.url(networks.currentData());image=qrcode.make(url,image_factory=SvgPathImage,border=4)
            qr.load(image.to_string());address.setText(f'Local address: http://{networks.currentData()}:{self.phone_server.port}')
        networks.currentIndexChanged.connect(update_qr);update_qr()
        def connection_status():
            server=self.phone_server
            if server is None:return
            if self.phone_bridge.last_client>=server.started and time.monotonic()-self.phone_bridge.last_client<6:message='Dashboard connected · receiving updates'
            elif server.last_page_request>=server.started:message='Dashboard page reached · waiting for paired updates'
            else:message='Local server ready · no dashboard has connected yet'
            if networks.currentData()=='127.0.0.1':message='No LAN connection found. Connect the laptop to Wi-Fi or Ethernet first.'
            connection.setText(message)
        timer=QTimer(dialog);timer.timeout.connect(connection_status);timer.start(500);dialog.finished.connect(timer.stop);connection_status()
        layout.addWidget(button('Test this link on the laptop',lambda:QDesktopServices.openUrl(QUrl(self.phone_server.url(networks.currentData())))))
        layout.addWidget(button('Copy pairing link',lambda:QApplication.clipboard().setText(self.phone_server.url(networks.currentData()))))
        layout.addWidget(label('If it opens here but not on your phone: use the same non-guest Wi-Fi, check for VPN or router device isolation, and allow this app through Windows Firewall on Private networks. Keep the address as http://.',13,True))
        if sys.platform=='win32':
            def copy_firewall_fix():
                QApplication.clipboard().setText(private_firewall_command(self.phone_server.port))
                QMessageBox.information(dialog,'Private Wi-Fi firewall command copied','On your trusted home Wi-Fi, make sure the Windows network profile is Private. Open Windows Terminal as administrator, select PowerShell and paste the copied command. It allows only this bundled Python app, this dashboard port and devices on the local subnet. It does not turn off the firewall or change Public-network access. Then rescan the QR code.')
            layout.addWidget(button('Copy Private-network firewall fix',copy_firewall_fix))
        layout.addWidget(label('Only derived data is shared. No camera/game images leave the laptop. The phone does not use its own camera for tracking. This local preview uses HTTP on your private network.',13,True));layout.addStretch()
        def stop():self.phone_server.stop();self.phone_server=None;dialog.accept()
        outer.addWidget(button('Stop phone sharing',stop));outer.addWidget(button('Keep sharing and close',dialog.accept,True));dialog.exec()

    def receive_game_observation(self,worker,observation):
        if worker is not self.game_worker or not self.session.active or self.session.break_deadline is not None:return
        self.game_observation=observation
        if observation.game:self.session.game=observation.game
        self.refresh()

    def mark_start_view(self):
        if self.game_worker is not None and self.screen_tracking:
            self.game_worker.mark_requested.set();self.game_status.setText('Switch to the game at your start view. The next captured game frame will be marked in memory.')
    def select_camera(self,index):
        self.camera_index=index;self.refresh()

    def toggle_camera(self):
        if self.session.camera_active:self.pause()
        elif self.session.active and self.session.break_deadline is None:self.start_source(self.camera_index)
    def open_video(self):
        if not self.session.active or self.session.break_deadline is not None:return
        path,_=QFileDialog.getOpenFileName(self,'Open a local video',str(Path.home()),'Video files (*.mp4 *.avi *.mov *.mkv);;All files (*)')
        if path:self.start_source(path)

    def toggle_theme(self):
        self.theme='dark' if self.theme=='light' else 'light';QApplication.instance().setStyleSheet(make_style(self.theme));self.theme_button.setText('Light theme' if self.theme=='dark' else 'Dark theme')
        c=PALETTES[self.theme]
        for preview in self.preview_widgets:preview.setStyleSheet('background:'+c['surface_alt']+';border-radius:14px;color:'+c['secondary']+';')
        self.refresh()

    def toggle_motion(self):
        self.motion_paused=not self.motion_paused;self.refresh()

    def build_break_body(self):
        body=QWidget();row=QHBoxLayout(body);row.setContentsMargins(0,0,0,0);row.setSpacing(24)
        card,layout=panel(padding=40);layout.addWidget(label("A short pause is available.",32,bold=True));self.countdown=label("00:30",104,bold=True);layout.addWidget(self.countdown)
        layout.addWidget(label("Look away from the screen. Unclench your hands. Let your next breath be easy.",24,True));layout.addWidget(label("Skip or finish whenever you want. There is no need to complete the timer.",16,True));layout.addStretch();layout.addWidget(button("Back to session",self.toggle_break,True));row.addWidget(card,2)
        privacy,layout=panel(padding=32);layout.addWidget(label("Your sources are off.",28,bold=True));layout.addWidget(label("Camera and video stay paused when you return to the session.",20,True));layout.addStretch();row.addWidget(privacy,1)
        return body

    def build_summary_body(self):
        body=QWidget();row=QHBoxLayout(body);row.setContentsMargins(0,0,0,0);row.setSpacing(24)
        card,layout=panel(padding=40);layout.addWidget(label("Session complete.",56,bold=True));layout.addWidget(label("A check-in is a reflection, not a rating.",24,True));self.summary_stats=label("",32,bold=True);layout.addWidget(self.summary_stats);self.summary_retention=label("",18,True);layout.addWidget(self.summary_retention);layout.addStretch();layout.addWidget(button("Start a new session",self.new_session,True));row.addWidget(card,2)
        privacy,layout=panel(padding=32);layout.addWidget(label("Start on your terms.",36,bold=True));layout.addWidget(label("All sensing has stopped. Your next session starts with sources off.",22,True));layout.addStretch();row.addWidget(privacy,1)
        return body

    def add_dimensions(self,layout):
        row=QHBoxLayout();row.setSpacing(16)
        for key,title in [("valence","Pleasantness"),("energy","Energy / activation")]:
            col=QVBoxLayout();col.addWidget(label(title,13,True));value=label("",20,bold=True);self.state_labels.append((value,key));col.addWidget(value);row.addLayout(col,1)
        layout.addLayout(row)

    def change_view(self,index):
        self.current_view=index
        for i,b in enumerate(self.view_buttons):b.setProperty("primary",i==index);b.style().unpolish(b);b.style().polish(b)
        self.refresh()

    def poll(self):
        if self.input_observer.enabled:
            game=self.game_worker.foreground if self.game_worker is not None else None
            self.input_observer.set_target(game.hwnd if game and game.name else 0)
        if self.worker is not None:
            image,item=self.worker.take_latest()
            if image is not None and self.session.camera_active:self.last_image=image
            if item is not None:self.session.receive_cue(item[1],item[0])
            if not self.worker.isRunning():
                self.last_status=self.worker.error or self.worker.finished_reason or "Capture stopped"
                self.session.stop_capture();self.last_image=None;self.worker.deleteLater();self.worker=None
        self.refresh()

    def refresh(self):
        s=self.session;title,valence,energy,desc=s.affect
        self.bodies.setCurrentIndex(4 if not s.active else 3 if s.break_deadline is not None else self.current_view)
        if not s.active:self.title.setText("Session complete")
        elif s.break_deadline is not None:self.title.setText("A moment away")
        else:self.title.setText("Your session")
        self.subtitle.setText(s.game+"  ·  "+s.intention)
        self.game_tag.setText('Windows game detection' if self.detect_games else "Competitive session" if s.competitive else "Manual game context")
        observation=self.game_observation
        status=(observation.game+' · ' if observation and observation.game else '')+(observation.status if observation else 'Looking for a supported foreground game…' if sys.platform=='win32' else 'Live game-window tracking requires Windows')
        if observation and observation.cue:status+=' · '+observation.cue
        if self.detect_games:
            if self.game_worker is not None and self.game_worker.mark_requested.is_set():status='Switch to Getting Over It at the start view to mark it.'
            self.game_status.setText(status+(' · Screen sampling on' if self.screen_tracking else ' · Screen sampling off'))
        else:self.game_status.setText('Game detection is off · Game events are not being observed.')
        self.game_detection_control.setText('Stop game tracking' if self.detect_games else 'Detect game');self.game_detection_control.setEnabled(s.active and s.break_deadline is None)
        self.mark_start_control.setVisible(self.screen_tracking and self.game_worker is not None)
        for control in self.expression_controls:
            control.blockSignals(True);control.setChecked(s.experimental_analysis);control.blockSignals(False);control.setEnabled(s.active and s.break_deadline is None)
        for control in self.neutral_controls:control.setVisible(s.camera_active and s.experimental_analysis and s.face_mapping)
        for selector in self.view_selectors:
            selector.blockSignals(True);selector.setCurrentIndex(1 if self.live_view else 0);selector.blockSignals(False)
        if self.tray is not None:self.tray.setToolTip("Checkpoint / "+("Capture active" if s.camera_active else "Capture off"))
        for selector in self.camera_selectors:
            selector.blockSignals(True);selector.setCurrentIndex(self.camera_index);selector.blockSignals(False);selector.setEnabled(not s.camera_active and s.active and s.break_deadline is None)
        worker=self.worker
        feedback=('Camera connected. Face tracking unavailable: '+worker.analysis_error) if worker is not None and worker.analysis_error else ''
        if worker is not None and not worker.frames:feedback=f'Opening Camera {self.camera_index+1}…' if s.source_kind=='camera' else 'Opening the selected video…'
        for message in self.camera_messages:message.setText(feedback);message.setVisible(bool(feedback))
        for control in self.camera_controls:
            control.setText('Pause video' if s.source_kind=='video' else 'Pause camera' if s.camera_active else 'Start camera');control.setEnabled(s.active and s.break_deadline is None)
        for control in self.file_controls:control.setEnabled(s.active and s.break_deadline is None)
        self.library_control.setEnabled(s.active and s.break_deadline is None)
        self.end_control.setText("End session" if s.active else "New session")
        for control in self.checkin_controls:control.setEnabled(s.active and s.break_deadline is None);control.setText('Update check-in' if s.report else 'Choose a feeling')
        remaining=max(0,math.ceil(s.break_deadline-time.monotonic())) if s.break_deadline is not None else None
        self.break_button.setVisible(s.active and remaining is None)
        self.support_title.setText("Ready when you are." if not s.active else "Your sources are paused." if remaining is not None else "Need a break?")
        self.support_copy.setText("A new session starts with capture off." if not s.active else "Returning to the session keeps capture off." if remaining is not None else "Your camera pauses while you step away.")
        cue_text="Expression cues off. Enable experimental analysis in Preferences if you want to test the model."
        if s.experimental_analysis:
            if s.cue is None:cue_text="Expression cue: unavailable"+(" / "+self.last_status if self.last_status else "")
            elif s.cue.status=="accepted":cue_text=('Face mapping · '+str(s.cue.mapping_label)) if s.cue.movement is not None else "Experimental expression cue: "+s.cue.expression+" / not a mood or CMA estimate"
            else:cue_text="Expression cue: uncertain / "+s.cue.reason
        source='Your check-in' if s.report else 'Not reported'
        if s.report:
            elapsed=int(s.reports[-1]['elapsed_seconds']);desc=f'Checked in at {elapsed//60:02d}:{elapsed%60:02d} into this session.'
        else:desc='Choose a card that fits this moment.' 
        displayed=expression_display(s,max_age=max(3.,2/self.frequency)) if self.live_view else None
        artwork=s.report
        if displayed is not None:
            title=displayed.title;desc=displayed.detail;source='Experimental estimate';artwork=displayed.artwork
            if displayed.source=='face_movement':source='Tracked face movement'
        for obj,key in self.state_labels:
            if key=='cue':obj.setVisible(s.experimental_analysis)
            obj.setText({"title":title,"valence":valence,"energy":energy,"description":desc,"source":source,"cue":cue_text,"capture":"Video file" if s.source_kind=="video" else ("On · "+worker.backend if worker is not None and worker.frames else "Starting…") if s.camera_active else "Off"}[key])
        for control in self.motion_controls:control.setText('Motion reduced' if self.reduced_motion else 'Resume animation' if self.motion_paused else 'Pause animation');control.setEnabled(not self.reduced_motion)
        for em in self.emblems:
            em.configure(theme=self.theme,reduced_motion=self.reduced_motion,paused=self.motion_paused,enabled=s.active and s.break_deadline is None)
            if self.live_view:
                # Fixed presentation coordinates animate artwork only; they are never CMA estimates.
                em.set_state(artwork,0. if artwork else None,0. if artwork else None)
                em.setAccessibleName(title)
            else:em.set_state(s.report,s.valence,s.arousal)
            em.set_movement(displayed.movement if displayed else None)
        self.pip_control.setText('Hide Pip' if self.overlay_enabled else 'Show Pip');self.overlay.setVisible(self.overlay_enabled)
        self.overlay.blob.configure(theme=self.theme,reduced_motion=self.reduced_motion,paused=self.motion_paused,enabled=s.active and s.break_deadline is None)
        if self.live_view:self.overlay.blob.set_state(artwork,0. if artwork else None,0. if artwork else None)
        else:self.overlay.blob.set_state(s.report,s.valence,s.arousal)
        self.overlay.blob.set_movement(displayed.movement if displayed else None)
        now=time.monotonic()
        if now>=self.next_export:
            self.next_export=now+.25
            activity=self.input_observer.activity.snapshot() if self.input_observer.enabled and self.input_observer.target else None
            state,report=self.companion.update(s,displayed,self.game_observation,input_stats=activity,nudges=self.nudges_enabled,motion_enabled=not(self.reduced_motion or self.motion_paused),now=now)
            self.latest_companion=state;self.latest_report=report;self.phone_bridge.publish(state,report)
            if state['nudge'] and state['nudge']!=self.last_nudge:self.overlay.set_message(state['nudge'])
            self.last_nudge=state['nudge']
        for preview in self.preview_widgets:
            if s.camera_active and self.last_image is not None:
                if preview.isVisible():preview.set_image(self.last_image)
            elif s.camera_active:preview.clear_image("Starting the selected source…")
            else:preview.clear_image("Camera is off\n\n"+(self.last_status or "Start the camera to see your own preview."))
        if remaining is not None:
            self.countdown.setText(f"00:{remaining:02d}")
        if not s.active:
            self.summary_stats.setText(f"{int(s.elapsed())//60:02d}:{int(s.elapsed())%60:02d} session time\n{len(s.reports)} player check-ins\nCapture off")
            self.summary_retention.setText("Derived summary saved on this device." if self.retain and self.saved else "No summary retained." if not self.retain else "Summary was not saved. "+self.last_status)
        minutes,seconds=divmod(int(s.elapsed()),60);self.footer.setText(f"{minutes:02d}:{seconds:02d} elapsed · {len(s.reports)} {'check-in' if len(s.reports)==1 else 'check-ins'} · On-device session"+(" / "+self.last_status if self.last_status else ""))

    def choose_source(self):
        if self.session.camera_active:self.pause();return
        if not self.session.active:return
        menu=QMenu(self);camera=menu.addAction("Start local camera");video=menu.addAction("Open local video file");choice=menu.exec(self.capture_control.mapToGlobal(self.capture_control.rect().bottomLeft()))
        if choice==camera:self.start_source(self.camera_index)
        elif choice==video:
            path,_=QFileDialog.getOpenFileName(self,"Open local video",str(Path.home()),"Videos (*.mp4 *.avi *.mov *.mkv);;All files (*)")
            if path:self.start_source(path)

    def start_source(self,source,*,analyze=None):
        from checkpoint.capture import CaptureWorker
        if not self.pause():return
        self.last_status=""
        if analyze is not None:self.session.experimental_analysis=bool(analyze)
        if self.session.experimental_analysis:self.live_view=True
        try:
            generation=self.session.start_capture("camera" if isinstance(source,int) else "video")
            worker=CaptureWorker(source,analyze=self.session.experimental_analysis,frequency=self.frequency,generation=generation,face_mapping=self.session.face_mapping,face_gain=self.session.face_gain)
            self.worker=worker;worker.start()
        except Exception as ex:self.last_status=str(ex);self.session.stop_capture()
        self.refresh()

    def pause(self):
        self.session.stop_capture();self.last_image=None
        if self.worker is not None:
            if not self.worker.stop():
                self.last_status="Stopping the source; waiting for the device driver."
                self.refresh();return False
            self.worker.deleteLater();self.worker=None
        self.refresh();return True

    def pause_all(self):
        if self.pause():self.stop_game_tracking();self.next_export=0.;self.refresh()

    def show_emotion_library(self):
        if not self.session.active or self.session.break_deadline is not None:return
        dialog=EmotionLibraryDialog(self)
        if dialog.exec()==QDialog.DialogCode.Accepted:self.check_in(dialog.chosen)

    def check_in(self,initial=None):
        if not self.session.active:return
        if initial not in FEELINGS and self.session.report is None:self.show_emotion_library();return
        dialog=CheckinDialog(self,initial if initial in FEELINGS else None)
        if dialog.exec()==QDialog.DialogCode.Accepted:self.session.check_in(dialog.chosen,dialog.valence,dialog.arousal);self.refresh()

    def primary_action(self):
        if not self.session.active:self.new_session()
        elif self.session.break_deadline is not None:self.toggle_break()
        elif self.session.report:self.check_in()
        else:self.show_emotion_library()

    def toggle_break(self):
        if not self.session.active:return
        if self.session.break_deadline is not None:self.session.finish_break()
        else:
            if not self.pause():return
            self.stop_game_tracking()
            self.session.take_break()
        self.refresh()

    def end_or_new(self):
        if not self.session.active:self.new_session();return
        if not self.pause():return
        self.stop_game_tracking()
        self.session.end()
        if not self.saved:
            try:self.history.save(self.session.summary(),consent=self.retain);self.saved=True
            except Exception as ex:self.last_status="Summary could not be saved: "+str(ex)
        self.refresh()

    def new_session(self):
        dialog=SetupDialog(self,self.session)
        if dialog.exec()!=QDialog.DialogCode.Accepted:return
        if not self.pause():return
        if not self.stop_game_tracking():return
        prior=self.session
        self.session=Session(game=dialog.game.currentText().strip()[:100] or "Other / manual",intention=dialog.intention.currentText(),competitive=dialog.competitive.isChecked(),experimental_analysis=prior.experimental_analysis,face_mapping=prior.face_mapping,face_gain=prior.face_gain,quiet=prior.quiet)
        self.companion=CompanionState();self.next_export=0.;self.saved=False;self.last_status="";self.refresh()

    def show_updates(self):
        from checkpoint.update_ui import UpdateDialog
        dialog=UpdateDialog(self);self.update_dialog=dialog;dialog.exec();self.update_dialog=None;dialog.deleteLater()

    def show_preferences(self):
        dialog=PreferencesDialog(self)
        if dialog.exec()!=QDialog.DialogCode.Accepted:return
        if not self.pause():return
        self.session.experimental_analysis=dialog.experimental.isChecked();self.retain=dialog.retention.isChecked();self.frequency=dialog.frequency.value();self.reduced_motion=dialog.reduced.isChecked()
        self.session.face_mapping=dialog.engine.currentIndex()==0
        self.session.face_gain=dialog.face_gain.value()
        if self.session.experimental_analysis:self.live_view=True
        self.overlay_enabled=dialog.pip.isChecked()
        if self.overlay_corner!=dialog.corner.currentText():self.overlay_corner=dialog.corner.currentText();self.overlay.place(self.overlay_corner)
        self.nudges_enabled=dialog.nudges.isChecked()
        self.configure_game_tracking(dialog.detect_games.isChecked() or dialog.input_timing.isChecked(),dialog.screen_tracking.isChecked())
        if dialog.input_timing.isChecked():
            try:self.input_observer.start()
            except OSError as ex:self.last_status=str(ex)
        self.next_export=0.;self.refresh()

    def show_report(self):
        self.next_export=0.;self.refresh();dialog=QDialog(self);dialog.setWindowTitle('Session report');dialog.resize(680,620)
        layout=QVBoxLayout(dialog);layout.setContentsMargins(26,24,26,24);layout.addWidget(label('Your session report',28,bold=True))
        layout.addWidget(label(f'{self.session.game} · {int(self.session.elapsed())//60} minutes · {len(self.session.reports)} check-ins',15,True))
        scroll=QScrollArea();scroll.setWidgetResizable(True);content=QWidget();rows=QVBoxLayout(content);scroll.setWidget(content);layout.addWidget(scroll,1)
        rows.addWidget(label('Session moments',18,bold=True))
        moments=self.latest_report.get('moments',[])
        if not moments:rows.addWidget(label('No observations yet. Start face or game tracking to see derived moments here.',14,True))
        for moment in reversed(moments[-30:]):
            elapsed=int(moment['elapsed_seconds']);rows.addWidget(label(f'{elapsed//60:02d}:{elapsed%60:02d} · {moment["label"]}',16))
            if moment['game_cue']:rows.addWidget(label(moment['game_cue'],13,True))
        rows.addStretch();layout.addWidget(label('Movement and expression estimates are not a verified emotional history. Raw frames and typed text are not included.',13,True))
        def save():
            path,_=QFileDialog.getSaveFileName(dialog,'Export session report','checkpoint-session.json','JSON (*.json)')
            if path:
                try:Path(path).write_text(json.dumps(self.latest_report,indent=2,allow_nan=False),encoding='utf8')
                except OSError as ex:QMessageBox.warning(dialog,'Export unavailable',str(ex))
        layout.addWidget(button('Export JSON report',save,True));layout.addWidget(button('Close',dialog.accept));dialog.exec()

    def show_history(self):
        dialog=QDialog(self);dialog.setWindowTitle("Local session history");dialog.resize(800,560);root=QVBoxLayout(dialog);root.setContentsMargins(28,28,28,28);root.addWidget(label("Your saved summaries",28,bold=True))
        try:records=self.history.read()
        except Exception as ex:QMessageBox.warning(self,"History unavailable",str(ex));return
        scroll=QScrollArea();scroll.setWidgetResizable(True);content=QWidget();items=QVBoxLayout(content)
        if self.session.reports:
            items.addWidget(label('This session',22,bold=True))
            for report in reversed(self.session.reports):
                row,lay=panel(padding=16);elapsed=int(report['elapsed_seconds']);lay.addWidget(label(FEELINGS[report['feeling']][0],20,bold=True));lay.addWidget(label(f'{elapsed//60:02d}:{elapsed%60:02d} into this session',13,True));items.addWidget(row)
        if not records:items.addWidget(label('No past sessions saved. You can enable history in Settings.',15,True))
        else:items.addWidget(label('Saved sessions',22,bold=True))
        for item in reversed(records):
            box,lay=panel(padding=16);lay.addWidget(label(item.get("game","Session"),20,bold=True));lay.addWidget(label(item.get("started_at","")+" / "+str(round(item.get("duration_seconds",0)/60,1))+" minutes",14,True));lay.addWidget(label("Check-ins: "+", ".join(x["feeling"] for x in item.get("check_ins",[])),16));items.addWidget(box)
        items.addStretch();scroll.setWidget(content);root.addWidget(scroll,1)
        def delete():
            if QMessageBox.question(dialog,"Delete saved summaries?","Delete this app's local derived summaries? Your imported video files will not be changed.")==QMessageBox.StandardButton.Yes:
                self.history.delete();dialog.accept()
        root.addWidget(button("Delete saved summaries",delete));root.addWidget(button("Close",dialog.accept));dialog.exec()

    def edit_context(self):
        dialog=QDialog(self);dialog.setWindowTitle('Game context');dialog.resize(600,460);root=QVBoxLayout(dialog);root.setContentsMargins(24,24,24,24);root.setSpacing(14)
        root.addWidget(label('Your game context',26,bold=True));root.addWidget(label('Add your own context for this session.',14,True));root.addWidget(label('Game',14,bold=True));game=QComboBox();game.setEditable(True);game.addItems(['Getting Over It','Valorant','Counter-Strike 2','Other']);game.setCurrentText(self.session.game);root.addWidget(game)
        root.addWidget(label('Intention',14,bold=True));intention=QComboBox();intention.addItems(['Enjoy the challenge','Practice','Play with friends','Decompress']);intention.setCurrentText(self.session.intention);root.addWidget(intention)
        root.addWidget(label('What is happening?',14,bold=True));entry=QLineEdit(self.session.context);entry.setMaxLength(160);root.addWidget(entry)
        box=QDialogButtonBox(QDialogButtonBox.StandardButton.Save|QDialogButtonBox.StandardButton.Cancel);box.accepted.connect(dialog.accept);box.rejected.connect(dialog.reject);root.addWidget(box)
        if dialog.exec()==QDialog.DialogCode.Accepted:
            self.session.game=game.currentText().strip()[:100] or 'Other';self.session.intention=intention.currentText();self.session.context=entry.text().strip() or 'Manual game context';self.refresh()

    def show_support(self):
        dialog=QDialog(self);dialog.setWindowTitle("Optional support");dialog.resize(640,500);root=QVBoxLayout(dialog);root.setContentsMargins(28,28,28,28);root.setSpacing(16);root.addWidget(label("What would help right now?",28,bold=True))
        for title,copy in [("Technical friction","Check your connection, input or graphics settings when the game allows. Choose any changes yourself."),("Team communication","Consider a quieter channel or use the game's own mute/report controls if you want to. This app never changes them."),("A difficult challenge","Choose a smaller goal, revisit a strategy or pause before the next attempt."),("A short pause","Look away, loosen your grip or get water. You can keep playing without taking any action.")]:root.addWidget(label(title,20,bold=True));root.addWidget(label(copy,15,True))
        root.addWidget(button("Close",dialog.accept));dialog.exec()

    def closeEvent(self,event:QCloseEvent):
        if self.update_dialog is not None and self.update_dialog.request_cancel():
            event.ignore();QTimer.singleShot(300,self.close);return
        if not self.pause():event.ignore();QTimer.singleShot(500,self.close);return
        if not self.stop_game_tracking():event.ignore();QTimer.singleShot(500,self.close);return
        self.overlay.close();self.overlay.deleteLater()
        if self.phone_server is not None:self.phone_server.stop();self.phone_server=None
        self.timer.stop();self.session.end()
        if self.tray is not None:self.tray.hide()
        if not self.saved:
            try:self.history.save(self.session.summary(),consent=self.retain);self.saved=True
            except Exception:self.last_status="Summary could not be saved"
        event.accept()


def create_application(argv=None):
    app=QApplication.instance() or QApplication(argv or []);app.setApplicationName("Checkpoint");app.setOrganizationName("CheckpointResearch");app.setWindowIcon(QIcon(str(ASSETS/"checkpoint.svg")))
    if QFontDatabase.addApplicationFont(str(ASSETS/"DM-Sans.ttf"))<0:raise RuntimeError("Bundled DM Sans font could not be loaded")
    font=QFont("DM Sans");font.setPixelSize(14);app.setFont(font);app.setStyleSheet(STYLE);return app


def main():
    parser=argparse.ArgumentParser();parser.add_argument("--theme",choices=["light","dark"],default="light");parser.add_argument("--feeling",choices=list(FEELINGS));parser.add_argument("--view",type=int,choices=[0,1,2],default=0);parser.add_argument("--video");parser.add_argument("--analyze",action="store_true");parser.add_argument("--no-setup",action="store_true");parser.add_argument("--screenshot");parser.add_argument("--screenshot-delay",type=int,default=1500);args=parser.parse_args()
    app=create_application();window=MainWindow(no_setup=args.no_setup or bool(args.video) or bool(args.screenshot));
    if not args.screenshot:
        screen=app.primaryScreen()
        if screen:
            area=screen.availableGeometry();window.resize(min(1440,max(1000,area.width()-48)),min(940,max(640,area.height()-64)))
    window.show()
    if args.theme=='dark':window.toggle_theme()
    window.change_view(args.view)
    if args.feeling:window.session.check_in(args.feeling);window.refresh()
    if args.video:
        window.session.game="Local video";window.session.intention="Review a recording";window.session.context="No gameplay context inferred"
        QTimer.singleShot(100,lambda:window.start_source(args.video,analyze=args.analyze))
    if args.screenshot:
        def save():
            path=Path(args.screenshot);path.parent.mkdir(parents=True,exist_ok=True)
            window.timer.stop();render=QImage(window.size(),QImage.Format.Format_ARGB32);render.fill(0);window.render(render);render.save(str(path));QTimer.singleShot(200,window.close)
        QTimer.singleShot(args.screenshot_delay,save)
    from checkpoint.updates import signal_update_ready
    QTimer.singleShot(350,lambda:signal_update_ready(Path(__file__).resolve().parents[1]))
    code=app.exec()
    window.deleteLater();app.sendPostedEvents(None,QEvent.Type.DeferredDelete);app.processEvents()
    return code


if __name__=="__main__":raise SystemExit(main())
