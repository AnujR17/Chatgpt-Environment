"""Semantic native UI tokens. Default warm light theme and optional dark theme."""
PALETTES={
 'light':{'canvas':'#F4F2EC','sidebar':'#FFFEFA','surface':'#FFFEFA','surface_alt':'#EEEEE6','text':'#252D29','secondary':'#626B65','muted':'#7A817B','border':'#DADDD3','accent':'#235C49','on_accent':'#FFFFFF','pleasant':'#28766C','unpleasant':'#B45C4C'},
 'dark':{'canvas':'#151C19','sidebar':'#1B2420','surface':'#1E2823','surface_alt':'#29352E','text':'#EDF1E8','secondary':'#B4BEB4','muted':'#87978B','border':'#3B4C40','accent':'#C7D8A8','on_accent':'#203025','pleasant':'#9CCDC0','unpleasant':'#E7A18E'}
}
# Illustration colours are categorical art direction, not CMA scores.
ART={
 'face_ink':'#34483E','art_shadow':'#7D7968',
 'body_calm':'#B9CFC0','body_frustrated':'#D8B09E',
 'body_bewildered':'#C9C2D4','body_confused':'#D5CBAB',
 'body_happy':'#E6C981','body_excited':'#E3B49A',
 'body_sad':'#B9C9D1','body_angry':'#CBA393',
 'body_frustrated_shade':'#B38A79','body_excited_shade':'#D9927B',
}
ART.update({'poster_ink':'#343C36','poster_eye':'#FFFCF6','poster_tongue':'#E9A599','poster_coral':'#E97460','poster_blue':'#97A8CE','poster_teal':'#92B9B0','poster_ochre':'#E6AE58','poster_yellow':'#D8D85D'})
for palette in PALETTES.values():palette.update(ART)

COLORS=PALETTES['light']

def make_style(theme='light'):
    c=PALETTES[theme]
    return '''
QWidget { font-family:'DM Sans'; color:@text; background:@canvas; }
QMainWindow, QDialog { background:@canvas; }
QLabel { background:transparent; border:0; }
QFrame#nav { background:@sidebar; border:0; border-bottom:1px solid @border; }
QFrame#panel { background:@surface; border:1px solid @border; border-radius:20px; }
QFrame#stateCard { background:@surface_alt; border:0; border-radius:14px; }
QLabel#secondary { color:@secondary; }
QLabel#accent { color:@accent; }
QPushButton { background:@surface; border:1px solid @border; border-radius:10px; padding:10px 18px; min-height:22px; }
QPushButton:hover { background:@surface_alt; }
QPushButton:pressed { background:@border; }
QPushButton:focus { border:2px solid @accent; padding:9px 17px; }
QPushButton:disabled { color:@muted; background:@surface_alt; }
QPushButton[primary="true"] { background:@accent; color:@on_accent; border:1px solid @accent; }
QPushButton[primary="true"]:hover { background:@accent; }
QPushButton#navButton { background:transparent; border:0; text-align:left; }
QLineEdit,QComboBox,QDoubleSpinBox,QListWidget { background:@surface; border:1px solid @border; border-radius:8px; padding:10px; }
QLineEdit:focus,QComboBox:focus,QDoubleSpinBox:focus { border:2px solid @accent; }
QCheckBox { spacing:10px; padding:8px 0; }
QCheckBox::indicator { width:20px; height:20px; border:1px solid @secondary; border-radius:4px; background:@surface; }
QCheckBox::indicator:checked { background:@accent; border:1px solid @accent; }
QToolTip { background:@surface; border:1px solid @secondary; color:@text; }
QScrollArea { background:@canvas; border:0; }
QScrollBar:vertical { background:@surface; width:10px; }
QScrollBar::handle:vertical { background:@border; border-radius:5px; min-height:24px; }
QSlider::groove:horizontal { height:4px; background:@border; border-radius:2px; }
QSlider::sub-page:horizontal { background:@accent; border-radius:2px; }
QSlider::handle:horizontal { background:@accent; width:18px; margin:-7px 0; border-radius:9px; }
'''.replace('@canvas',c['canvas']).replace('@sidebar',c['sidebar']).replace('@surface_alt',c['surface_alt']).replace('@surface',c['surface']).replace('@text',c['text']).replace('@secondary',c['secondary']).replace('@muted',c['muted']).replace('@border',c['border']).replace('@on_accent',c['on_accent']).replace('@accent',c['accent'])

STYLE=make_style()

# Native controls share clear focus and generous hit areas in the card-based UI.
_BASE_MAKE_STYLE=make_style

def make_style(theme='light'):
    c=PALETTES[theme]
    return _BASE_MAKE_STYLE(theme)+f'''
QFrame#artStage {{ background: {'#FFF0DC' if theme=='light' else '#344139'}; border: 0; border-radius: 20px; }}
QPushButton#emotionCard {{ min-height: 208px; min-width: 190px; background: {c['surface']}; border: 1px solid {c['border']}; border-radius: 16px; padding: 0; }}
QPushButton#emotionCard:hover {{ border: 2px solid {c['accent']}; background: {c['surface_alt']}; }}
QPushButton#emotionCard:focus {{ border: 3px solid {c['accent']}; padding: 0; }}
QLineEdit {{ min-height: 22px; }}
'''

STYLE=make_style()
