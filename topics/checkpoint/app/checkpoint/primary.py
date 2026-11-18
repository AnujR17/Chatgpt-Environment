"""The five presentation states shared by check-in, reflection and companion."""
PRIMARY_KEYS=('neutral','happy','frustrated','sad','confused')
PRIMARY_LABELS={'neutral':'Neutral','happy':'Happy','frustrated':'Frustrated','sad':'Sad','confused':'Confused'}
ALIASES={'composed':'neutral','calm':'neutral','relaxed':'neutral','neutral':'neutral',
 'happiness':'happy','laugh':'happy','laughing':'happy','amused':'happy','excited':'happy','engaged':'happy','content':'happy','contented':'happy','delighted':'happy','satisfied':'happy',
 'anger':'frustrated','angry':'frustrated','tension':'frustrated','tense':'frustrated','annoyed':'frustrated',
 'sadness':'sad','low':'sad','bored':'sad','exhausted':'sad','miserable':'sad','withdrawn':'sad','disappointed':'sad',
 'confusion':'confused','bewildered':'confused','confused?':'confused'}

def primary_key(key):
    key=(key or '').lower()
    return key if key in PRIMARY_KEYS else ALIASES.get(key,'neutral')

def limit_display(display):
    from checkpoint.expression_view import ExpressionDisplay
    if display.artwork is None:return ExpressionDisplay('Neutral',None,display.detail,source=display.source)
    supported=display.artwork in PRIMARY_KEYS or display.artwork in ALIASES
    key=primary_key(display.artwork)
    return ExpressionDisplay(PRIMARY_LABELS[key],key if supported else None,display.detail,display.movement if supported else None,display.source)

def public_estimate(estimate):
    if not estimate:return None
    groups={'neutral':'neutral','happiness':'happy','anger':'frustrated','sadness':'sad'}
    raw=estimate.get('scores',{})
    scores={key:raw[name] for name,key in groups.items() if name in raw}
    key=groups.get(estimate.get('label'))
    return {**estimate,'label':key,'scores':scores,'status':estimate.get('status') if key else 'uncertain'}
