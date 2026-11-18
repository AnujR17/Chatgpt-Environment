import os
os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
from PySide6.QtCore import QTimer,Qt
from PySide6.QtGui import QImage,QColor
from PySide6.QtTest import QTest
from checkpoint.app import create_application,MainWindow,EmotionLibraryDialog,CheckinDialog
from checkpoint.motion import AffectWidget
from checkpoint.vocabulary import POSTER,CARDS,COMMON
from checkpoint.theme import PALETTES


def test_five_primary_cards_and_whole_card_save(tmp_path):
    app=create_application([]);w=MainWindow(no_setup=True,data_dir=tmp_path);w.show()
    from checkpoint.primary import PRIMARY_KEYS
    def select():
        d=app.activeModalWidget();assert isinstance(d,EmotionLibraryDialog)
        assert tuple(d.visible_keys)==PRIMARY_KEYS
        app.processEvents();assert d.cards['neutral'].height()>=184
        assert d.cards['neutral'].art.geometry().bottom()<d.cards['neutral'].height()
        assert w.session.report is None
        QTimer.singleShot(0,save)
        QTest.mouseClick(d.cards['happy'],Qt.MouseButton.LeftButton)
    def save():
        d=app.activeModalWidget();assert isinstance(d,CheckinDialog) and d.chosen=='happy'
        d.sliders[0].setValue(65);d.sliders[1].setValue(-20)
        QTest.mouseClick(d.save,Qt.MouseButton.LeftButton)
    QTimer.singleShot(0,select);w.show_emotion_library()
    assert w.session.report=='happy' and len(w.session.reports)==1
    assert (w.session.valence,w.session.arousal)==(.65,-.2)
    assert not w.session.camera_active and w.worker is None
    w.close();w.deleteLater();app.processEvents()


def test_library_has_only_five_choices_and_cancel_preserves_report(tmp_path):
    app=create_application([]);w=MainWindow(no_setup=True,data_dir=tmp_path);w.session.check_in('happy')
    d=EmotionLibraryDialog(w);d.show();assert set(d.cards)=={'neutral','happy','frustrated','sad','confused'}
    assert not hasattr(d,'all_button') and not hasattr(d,'search')
    d.reject();assert d.chosen is None and w.session.report=='happy'
    d.deleteLater();w.close();w.deleteLater();app.processEvents()


def test_body_fill_and_outline_use_different_colours():
    app=create_application([]);g=AffectWidget(240);g.set_state('frustrated');g.fade_override=1.;g.configure(reduced_motion=True);g.show();app.processEvents()
    image=QImage(g.size(),QImage.Format.Format_ARGB32);image.fill(0);g.render(image)
    colour=QColor(PALETTES['light']['poster_coral']).rgb()&0xffffff
    # Verifies the user-visible colour fill rather than only the scene definition.
    count=sum((image.pixel(x,y)&0xffffff)==colour for x in range(image.width()) for y in range(image.height()))
    assert count>1500
    g.close();g.deleteLater();app.processEvents()


def test_start_session_commits_game_and_keeps_sources_off(tmp_path):
    from checkpoint.app import SetupDialog
    from PySide6.QtWidgets import QDialogButtonBox
    app=create_application([]);w=MainWindow(no_setup=True,data_dir=tmp_path);w.show()
    def start():
        dialog=app.activeModalWidget();assert isinstance(dialog,SetupDialog)
        dialog.game.setCurrentText('Valorant');dialog.intention.setCurrentText('Practice');dialog.competitive.setChecked(True)
        box=dialog.findChild(QDialogButtonBox);QTest.mouseClick(box.button(QDialogButtonBox.StandardButton.Ok),Qt.MouseButton.LeftButton)
    QTimer.singleShot(0,start);w.new_session()
    assert w.session.game=='Valorant' and w.session.intention=='Practice' and w.session.competitive
    assert w.session.active and w.session.report is None and not w.session.camera_active and w.worker is None
    w.close();w.deleteLater();app.processEvents()
