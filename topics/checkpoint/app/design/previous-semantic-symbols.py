"""Distinct semantic emotion gestures. Design hypotheses, not CMA-derived icons.
Every scene uses a 360px viewbox and can be rendered by Qt or editable Figma vectors.
"""
import math

CORE=('calm','frustrated','bewildered','confused','happy','excited','sad','angry')
MEANINGS={
 'calm':('Settled wave','A wide, level line; very slow movement.'),
 'frustrated':('Compressed tangle','A blocked, tightly knotted path; small restrained contractions.'),
 'bewildered':('Disrupted burst','Uneven outward directions; a disoriented, off-centre composition.'),
 'confused':('Unresolved question','A familiar questioning turn; an open, unresolved route.'),
 'happy':('Open smile','A soft, open round form with an immediately familiar smile.'),
 'excited':('Lifted spark','A rounded spark that lifts and expands; energetic and positive.'),
 'sad':('Drooping drop','A lowered, weighted silhouette and a downturned expression.'),
 'angry':('Clenched form','A compressed angular silhouette with inward-sloping brows.'),
}


def scene(key,t=0.):
    # Returned commands are native paths, not screenshots or a graph.
    items=[]
    def path(commands,role='text',width=4,fill=None,opacity=1):
        items.append({'kind':'path','commands':commands,'role':role,'width':width,'fill':fill,'opacity':1 if fill else opacity,'fill_opacity':opacity if fill else 0,'stroke_opacity':.65 if fill else 1})
    def dot(x,y,r=5,role='text',opacity=1):items.append({'kind':'dot','x':x,'y':y,'r':r,'role':role,'opacity':opacity})
    phase=t*2*math.pi
    if key in ('calm','relaxed','content'):
        lift=3*math.sin(phase*.10)
        path([['M',54,184],['C',96,184,110,168+lift,146,176],['C',182,184-lift,190,194,222,186],['C',252,178,274,184,306,184]],'pleasant',5)
        # A relaxed, almost level wave. One line; no particle code to learn.
    elif key in ('frustrated','tense','low'):
        squeeze=1+.018*math.sin(phase*.28)
        raw=[(83,174),(212,128),(133,227),(225,187),(111,139),(189,239),(231,151),(103,205),(174,122),(220,223),(98,167),(214,169),(139,223),(180,130),(243,202),(128,191),(203,147),(170,230),(104,185),(252,171)]
        points=[((x-180)*squeeze+180,(y-180)/squeeze+180) for x,y in raw]
        # Rounded joins keep the frustration mark expressive without a strobe or shake.
        commands=[['M',*points[0]]]+[['L',*p] for p in points[1:]]
        path(commands,'unpleasant',4)
    elif key=='confused':
        dy=2*math.sin(phase*.13)
        path([['M',132,137+dy],['C',134,101+dy,210,94+dy,226,132+dy],['C',246,179+dy,176,179+dy,176,211+dy]],'text',5)
        dot(176,242+dy,5,'text')
    elif key=='bewildered':
        # Broken asymmetrical burst: surprise + disorientation, distinct from a question.
        for i,(angle,start,length) in enumerate([(-92,58,49),(-45,56,36),(2,63,49),(48,56,29),(91,62,44),(143,55,41),(188,60,32),(228,58,47)]):
            a=math.radians(angle);j=2*math.sin(phase*.19+i);cx,cy=180,179
            path([['M',cx+start*math.cos(a),cy+start*math.sin(a)],['L',cx+(start+length+j)*math.cos(a),cy+(start+length+j)*math.sin(a)]],'secondary',4)
        path([['M',149,173],['C',148,153,167,150,167,172],['C',167,195,148,193,149,173],['Z']],'text',3)
        path([['M',196,163],['C',195,145,216,146,217,165],['C',219,187,196,186,196,163],['Z']],'text',3)
        path([['M',176,217],['Q',188,208,201,218]],'text',3)
    elif key in ('happy','engaged'):
        dy=-3*math.sin(phase*.18);s=2*math.sin(phase*.18)
        path([['M',180,83+dy],['C',238+s,83+dy,282,123,278,183+dy],['C',275,242,233,282,178,278+dy],['C',117,276,78,232,82,175+dy],['C',86,119,125,82,180,83+dy],['Z']],'pleasant',3,'pleasant',.12)
        dot(143,164+dy,5,'pleasant');dot(217,164+dy,5,'pleasant')
        path([['M',133,196+dy],['C',151,231+dy,208,232+dy,228,194+dy]],'pleasant',5)
    elif key=='excited':
        s=1+.025*math.sin(phase*.27)
        raw=[['M',180,64],['C',192,123,232,155,291,180],['C',231,190,198,231,180,294],['C',163,231,129,197,66,180],['C',130,163,164,125,180,64],['Z']]
        transformed=[[c[0]]+[(v-180)*s+180 for v in c[1:]] for c in raw]
        path(transformed,'pleasant',3,'pleasant',.12);dot(154,174,4,'pleasant');dot(205,174,4,'pleasant');path([['M',153,198],['Q',180,225,207,198]],'pleasant',4)
    elif key=='sad':
        dy=2*math.sin(phase*.08)
        path([['M',180,69+dy],['C',161,120,105,166,112,217+dy],['C',119,284,245,288,248,214+dy],['C',250,166,196,119,180,69+dy],['Z']],'unpleasant',3,'unpleasant',.10)
        path([['M',145,193+dy],['Q',155,202+dy,164,194+dy]],'unpleasant',3)
        path([['M',198,194+dy],['Q',208,202+dy,218,192+dy]],'unpleasant',3)
        path([['M',159,237+dy],['Q',183,216+dy,208,237+dy]],'unpleasant',4)
    elif key=='angry':
        clench=2*math.sin(phase*.21)
        path([['M',111,99],['L',248,106],['L',283,179],['L',247,261],['L',112,258],['L',78,181],['Z']],'unpleasant',3,'unpleasant',.10)
        path([['M',122,155],['L',162,172+clench]],'unpleasant',6)
        path([['M',239,154],['L',200,172+clench]],'unpleasant',6)
        path([['M',147,221],['L',212,221]],'unpleasant',5)
    elif key=='sleepy':
        path([['M',102,160],['Q',129,183,154,160]],'secondary',4);path([['M',205,160],['Q',232,183,257,160]],'secondary',4);path([['M',163,220],['Q',180,230,197,220]],'secondary',4)
    elif key=='afraid':
        path([['M',112,133],['Q',132,105,153,126]],'unpleasant',4);path([['M',207,126],['Q',231,102,252,132]],'unpleasant',4);dot(140,164,6,'unpleasant');dot(223,164,6,'unpleasant');path([['M',165,225],['C',163,195,201,194,199,226],['Z']],'unpleasant',4)
    elif key=='bored':
        for x in [123,180,237]:dot(x,180,6,'secondary')
    else:
        path([['M',120,190],['C',120,111,245,104,246,184]],'muted',3,opacity=.6)
    return items


def svg_path(commands):
    return ' '.join(c[0]+(' '+' '.join(f'{x:.3f}' for x in c[1:]) if len(c)>1 else '') for c in commands)
