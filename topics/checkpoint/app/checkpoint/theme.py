"""Regen: sage, evergreen and warm neutral native UI tokens."""
PALETTES={
 'light':{'canvas':'#F3F3EA','sidebar':'#243D32','surface':'#FFFEF8','surface_alt':'#E5EADC','text':'#25392E','secondary':'#5B6D60','muted':'#788579','border':'#D4DDCD','accent':'#315D45','on_accent':'#FFFFFF','hover':'#274D38','soft':'#DAE5CD','on_soft':'#294532','pleasant':'#28766C','unpleasant':'#B45C4C'},
 'dark':{'canvas':'#18291F','sidebar':'#20372A','surface':'#233C2D','surface_alt':'#304A37','text':'#F2F4E8','secondary':'#BDCCB9','muted':'#91A18D','border':'#49634A','accent':'#C8DBAD','on_accent':'#223A29','hover':'#D9E8C5','soft':'#3A553D','on_soft':'#E3EDD6','pleasant':'#9CCDC0','unpleasant':'#E7A18E'}
}
# Character colours describe authored expressions, not measured CMA coordinates.
ART={'face_ink':'#34483E','art_shadow':'#7D7968','body_calm':'#B9CFC0','body_frustrated':'#D8B09E','body_bewildered':'#C9C2D4','body_confused':'#D5CBAB','body_happy':'#E6C981','body_excited':'#E3B49A','body_sad':'#B9C9D1','body_angry':'#CBA393','body_frustrated_shade':'#B38A79','body_excited_shade':'#D9927B','poster_ink':'#343C36','poster_eye':'#FFFCF6','poster_tongue':'#E9A599','poster_coral':'#E97460','poster_blue':'#97A8CE','poster_teal':'#92B9B0','poster_ochre':'#E6AE58','poster_yellow':'#D8D85D'}
for palette in PALETTES.values():palette.update(ART)
COLORS=PALETTES['light']


def make_style(theme='light'):
 c=PALETTES[theme]
 return f'''
QWidget {{ font-family:'DM Sans'; color:{c['text']}; background:{c['canvas']}; }}
QMainWindow,QDialog {{ background:{c['canvas']}; }}
QLabel {{ background:transparent; border:0; }}
QLabel#secondary {{ color:{c['secondary']}; }}
QLabel#accent {{ color:{c['accent']}; }}
QFrame#sidebar {{ background:{c['sidebar']}; border:0; }}
QFrame#sidebar QLabel {{ color:#F3F6E8; }}
QFrame#sidebar QLabel#secondary {{ color:#BDCEB8; }}
QFrame#sidebar QPushButton {{ color:#DDE8D7; background:transparent; border-color:#6F866D; padding:8px; }}
QFrame#sidebar QPushButton#sideNav {{ background:transparent; border:0; text-align:left; padding:10px; font-size:13px; }}
QFrame#sidebar QPushButton#sideNav:hover {{ background:#3B5540; }}
QFrame#sidebar QPushButton#sideNav[selected="true"] {{ background:#D6E4BD; color:#29412C; }}
QFrame#sidebar QPushButton:disabled {{ color:#92A48D; }}
QFrame#sessionHeader QLabel {{ color:#243E2D; }}
QFrame#sessionHeader QLabel#secondary {{ color:#52674D; }}
QFrame#sessionHeader QPushButton {{ background:transparent; color:#2B4733; border:1px solid #8FA684; }}
QFrame#sessionHeader QPushButton[primary="true"] {{ background:#315D45; color:white; border-color:#315D45; }}
QFrame#sessionHeader QPushButton[primary="true"]:disabled {{ background:{c['surface_alt']}; color:{c['muted']}; border-color:{c['border']}; }}
QFrame#sessionHeader QPushButton:disabled {{ background:transparent; color:#718368; border-color:#A7B698; }}
QPushButton[primary="true"]:hover {{ background:#274D38; }}
QFrame#panel,QFrame#cameraPanel {{ background:{c['surface']}; border:1px solid {c['border']}; border-radius:16px; }}
QFrame#companionPanel {{ background:transparent; border:0; }}
QFrame#gamePanel {{ background:{c['surface']}; border:1px solid {c['border']}; border-radius:12px; }}
QFrame#stateCard {{ background:{c['surface']}; border:1px solid {c['border']}; border-radius:12px; }}
QFrame#artStage {{ background:{'#E3EAD5' if theme=='light' else '#35513A'}; border:0; border-radius:20px; }}
QPushButton {{ background:{c['surface']}; border:1px solid {c['border']}; border-radius:9px; padding:10px 16px; min-height:22px; }}
QPushButton:hover {{ background:{c['surface_alt']}; border-color:{c['secondary']}; }}
QPushButton:pressed {{ background:{c['border']}; }}
QPushButton:focus {{ border:2px solid {c['accent']}; padding:9px 15px; }}
QPushButton:disabled {{ color:{c['muted']}; background:{c['surface_alt']}; border-color:{c['border']}; }}
QPushButton[primary="true"] {{ background:{c['accent']}; color:{c['on_accent']}; border:1px solid {c['accent']}; }}
QPushButton[primary="true"]:disabled {{ background:{c['surface_alt']}; color:{c['muted']}; border-color:{c['border']}; }}
QFrame#sessionHeader QPushButton:disabled {{ background:transparent; color:#718368; border-color:#A7B698; }}
QPushButton[primary="true"]:hover {{ background:{c['hover']}; }}
QPushButton[tone="soft"] {{ background:{c['soft']}; color:{c['on_soft']}; border:1px solid {c['border']}; }}
QPushButton[tone="soft"]:hover {{ border-color:{c['accent']}; }}
QPushButton#navButton {{ background:transparent; border:0; text-align:left; }}
QLineEdit,QComboBox,QDoubleSpinBox,QListWidget {{ background:{c['surface']}; border:1px solid {c['border']}; border-radius:8px; padding:10px; }}
QLineEdit {{ min-height:22px; selection-background-color:{c['accent']}; }}
QLineEdit:focus,QComboBox:focus,QDoubleSpinBox:focus {{ border:2px solid {c['accent']}; }}
QCheckBox {{ spacing:10px; padding:8px 0; }}
QCheckBox::indicator {{ width:20px; height:20px; border:1px solid {c['secondary']}; border-radius:5px; background:{c['surface']}; }}
QCheckBox::indicator:checked {{ background:{c['accent']}; border:1px solid {c['accent']}; }}
QToolTip {{ background:{c['surface']}; border:1px solid {c['secondary']}; color:{c['text']}; }}
QScrollArea {{ background:transparent; border:0; }}
QScrollBar:vertical {{ background:{c['canvas']}; width:8px; }}
QScrollBar::handle:vertical {{ background:{c['border']}; border-radius:4px; min-height:24px; }}
QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical {{ height:0; }}
QSlider::groove:horizontal {{ height:4px; background:{c['border']}; border-radius:2px; }}
QSlider::sub-page:horizontal {{ background:{c['accent']}; border-radius:2px; }}
QSlider::handle:horizontal {{ background:{c['accent']}; width:18px; margin:-7px 0; border-radius:9px; }}
QPushButton#emotionCard {{ min-height:208px; min-width:190px; background:{c['surface']}; border:1px solid {c['border']}; border-radius:16px; padding:0; }}
QPushButton#emotionCard:hover {{ border:2px solid {c['accent']}; background:{c['surface_alt']}; }}
QPushButton#emotionCard:focus {{ border:3px solid {c['accent']}; padding:0; }}
QTabBar::tab {{ background:transparent; color:{c['secondary']}; padding:8px 9px; font-size:12px; border:0; margin-right:4px; border-radius:7px; }}
QTabBar::tab:selected {{ background:{c['soft']}; color:{c['on_soft']}; }}
QTabBar::tab:focus {{ border:2px solid {c['accent']}; }}
QTabBar::tear {{ width:0; }}
'''
STYLE=make_style()
