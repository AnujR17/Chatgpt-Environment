"""A small native practice desk: one selected problem, one cue, one player verdict."""
from PySide6.QtCore import Qt, QUrl, Signal
from PySide6.QtGui import QDesktopServices, QFont
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                              QListWidget, QLineEdit, QCheckBox, QFrame, QScrollArea, QWidget)
from checkpoint.theme import PALETTES
from checkpoint.ui_graphics import with_icon
from checkpoint.attempts import (TECHNIQUES, BY_KEY, active_attempt, guidance_mode,
                                start_attempt, finish_attempt, saved_lessons)


def text(value, size=14, bold=False):
    w = QLabel(value)
    w.setWordWrap(True)
    w.setTextFormat(Qt.TextFormat.PlainText)
    f = QFont('DM Sans')
    f.setPixelSize(size)
    f.setBold(bold)
    w.setFont(f)
    return w


def action(value, callback, primary=False):
    w = QPushButton(value)
    w.setMinimumHeight(44)
    w.setProperty('primary', primary)
    w.clicked.connect(callback)
    return w


class PracticeDialog(QDialog):
    changed = Signal()

    def __init__(self, window):
        super().__init__(window)
        self.colors = PALETTES[window.theme]
        self.window = window
        self.session = window.session
        self.setWindowTitle('Checkpoint: Next attempt')
        self.resize(960, 700)
        self.setMinimumSize(820, 600)
        self.last_outcome = None
        self.override = None
        self.detail_open = None
        try:
            self.history = window.history.read()
        except (OSError, ValueError):
            self.history = []
        root = QVBoxLayout(self)
        root.setContentsMargins(26, 24, 26, 22)
        root.setSpacing(16)
        head = QHBoxLayout()
        heading = QVBoxLayout()
        heading.addWidget(text('GETTING OVER IT / PRACTICE DESK', 11, True))
        heading.addWidget(text('Make the next attempt different.', 30, True))
        head.addLayout(heading, 1)
        head.addWidget(action('Close', self.reject))
        root.addLayout(head)
        self.cma = text('', 13)
        self.cma.setStyleSheet(f"padding:10px; background:{self.colors['surface_alt']}; color:{self.colors['text']}; border-radius:6px;")
        cma_row = QHBoxLayout()
        cma_row.addWidget(self.cma, 1)
        self.checkin = action('Update my CMA check-in', self.check_in)
        cma_row.addWidget(self.checkin)
        root.addLayout(cma_row)
        body = QHBoxLayout()
        body.setSpacing(26)
        left = QVBoxLayout()
        left.addWidget(text('01  /  WHERE ARE YOU STUCK?', 11, True))
        self.sections = QListWidget()
        self.sections.setMinimumWidth(205)
        self.sections.setMaximumWidth(250)
        self.sections.setAccessibleName('Choose a Getting Over It practice problem')
        self.sections.setWordWrap(True)
        self.sections.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        for t in TECHNIQUES:
            self.sections.addItem(t.section + '\n' + t.problem)
        list_font = QFont('DM Sans'); list_font.setPixelSize(13); self.sections.setFont(list_font)
        self.sections.setStyleSheet('QListWidget{border:0;background:transparent;} QListWidget::item{padding:13px 8px;border-bottom:1px solid '+self.colors['border']+';} QListWidget::item:selected{background:'+self.colors['surface_alt']+';color:'+self.colors['text']+';border-left:3px solid '+self.colors['accent']+';}')
        left.addWidget(self.sections)
        left.addWidget(text('You choose the section.\nScreen tracking does not choose it for you.', 12))
        body.addLayout(left)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        content = QWidget()
        scroll.setWidget(content)
        right = QVBoxLayout(content)
        right.setContentsMargins(0, 0, 8, 4)
        right.setSpacing(14)
        self.eyebrow = text('02  /  CHANGE ONE THING', 11, True)
        right.addWidget(self.eyebrow)
        self.cue = text('', 27, True)
        right.addWidget(self.cue)
        self.target = text('', 16)
        right.addWidget(self.target)
        self.small = action('Give me a smaller target', self.smaller)
        right.addWidget(self.small, alignment=Qt.AlignmentFlag.AlignLeft)
        self.detail_button = action('Why this cue?', self.toggle_detail)
        links = QHBoxLayout()
        links.addWidget(self.detail_button)
        self.source = action('Read the guide', self.open_source)
        links.addWidget(self.source)
        links.addStretch()
        right.addLayout(links)
        self.detail = text('', 14)
        right.addWidget(self.detail)
        self.memory = text('', 14)
        self.memory.setStyleSheet('border-top:1px solid '+self.colors['border']+';padding-top:14px;')
        right.addWidget(self.memory)
        right.addStretch()
        body.addWidget(scroll, 1)
        root.addLayout(body, 1)
        self.status = text('', 13)
        root.addWidget(self.status)
        self.note = QLineEdit()
        self.note.setMaxLength(240)
        self.note.setPlaceholderText('Optional: what would you repeat or change?')
        self.note.setAccessibleName('Your practice lesson, optional')
        root.addWidget(self.note)
        self.pin = QCheckBox('Show the chosen cue beside Nori for 12 seconds')
        root.addWidget(self.pin)
        foot = QHBoxLayout()
        self.dismiss = action('Dismiss attempt', lambda: self.rate('dismissed'))
        foot.addWidget(self.dismiss)
        foot.addStretch()
        self.stuck = action('Still stuck', lambda: self.rate('stuck'))
        self.helped = action('Helped', lambda: self.rate('helped'), True)
        self.try_button = action('Try this cue', self.begin, True)
        self.back = action('Back to game', self.accept, True)
        with_icon(self.try_button,'play',self.colors['on_accent']);with_icon(self.back,'game',self.colors['on_accent']);with_icon(self.checkin,'feeling',self.colors['text']);with_icon(self.source,'help',self.colors['text'])
        for b in (self.stuck, self.helped, self.try_button, self.back):
            foot.addWidget(b)
        root.addLayout(foot)
        pending = active_attempt(self.session)
        index = next((i for i, t in enumerate(TECHNIQUES) if pending and t.key == pending['key']), 0)
        self.sections.setCurrentRow(index)
        self.sections.currentRowChanged.connect(self.selection_changed)
        self.refresh()

    def technique(self):
        pending = active_attempt(self.session)
        return BY_KEY[pending['key']] if pending else TECHNIQUES[max(0, self.sections.currentRow())]

    def selection_changed(self):
        self.override = None
        self.detail_open = None
        self.last_outcome = None
        self.refresh()

    def check_in(self):
        self.window.check_in()
        self.override = None
        self.changed.emit()
        self.refresh()

    def smaller(self):
        self.override = 'small'
        self.refresh()

    def toggle_detail(self):
        self.detail_open = not self.detail.isVisible()
        self.refresh()

    def open_source(self):
        QDesktopServices.openUrl(QUrl(self.technique().source))

    def refresh(self):
        pending = active_attempt(self.session)
        suggested, basis = guidance_mode(self.session)
        mode = pending['mode'] if pending else self.override or suggested
        expanded = self.detail_open if self.detail_open is not None else mode == 'choice'
        t = self.technique()
        self.cma.setText(pending['guidance_basis'] + ' · at cue selection' if pending else basis)
        self.cue.setText(t.target if mode == 'small' else t.cue)
        self.target.setText('Your only target: ' + t.target if mode != 'small' else 'The finish line can wait. Try just this part once.')
        self.target.setVisible(mode != 'brief' or expanded)
        self.eyebrow.setText('02  /  HOW DID THAT ATTEMPT GO?' if pending else '02  /  ONE SMALL TARGET' if mode == 'small' else '02  /  CHANGE ONE THING')
        self.sections.setEnabled(pending is None)
        self.checkin.setEnabled(self.session.active and self.session.break_deadline is None)
        self.small.setVisible(pending is None and mode != 'small')
        self.detail.setText(t.explanation)
        self.detail.setVisible(expanded)
        self.detail_button.setText('Hide explanation' if expanded else 'Why this cue?')
        lessons = saved_lessons(self.history, self.session, t.key)
        self.memory.setText(('YOUR LAST USEFUL ADJUSTMENT\n' + lessons[-1]['lesson'] if lessons else 'YOUR PRACTICE NOTE\nAfter trying, keep one adjustment that worked for you.') +
                            ('\nHistory is off; notes stay in this session.' if not self.window.retain else '\nNotes are retained with your saved session summary.'))
        for b in (self.note, self.dismiss, self.stuck, self.helped, self.back):
            b.setVisible(pending is not None)
        self.try_button.setVisible(pending is None)
        self.pin.setVisible(pending is None)
        self.try_button.setText('Try the smaller target' if mode == 'small' else 'Try this cue')
        self.try_button.setEnabled(self.session.active and self.session.break_deadline is None)
        self.status.setText('Your verdict, not a score. Leave a note if something is worth remembering.' if pending else
                            'Marked helpful. Your note is ready to reuse this session.' if self.last_outcome == 'helped' else
                            'Marked still stuck. Try a smaller target, or choose another problem.' if self.last_outcome == 'stuck' else
                            'No camera needed. Guidance is local; no game files are changed.')

    def begin(self):
        row = start_attempt(self.session, self.technique().key, mode=self.override)
        if row is None:
            return
        if self.pin.isChecked():
            self.window.overlay_enabled = True
            self.window.overlay.set_message(row['target'] if row['mode'] == 'small' else row['cue'], seconds=12)
        self.changed.emit()
        self.accept()

    def rate(self, outcome):
        if finish_attempt(self.session, outcome, self.note.text()):
            self.last_outcome = outcome
            self.note.clear()
            if outcome == 'stuck':
                self.override = 'small'
            self.changed.emit()
            self.refresh()
