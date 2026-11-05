"""Hand-inked, poster-inspired native emotion cards with original vector paths."""
import math
from checkpoint.vocabulary import CARDS,COMMON
CORE=COMMON
MEANINGS={key:(value['label'],'A player-selected feeling. Add your own pleasantness and energy.') for key,value in CARDS.items()}


def smooth(t):
    t=max(0.,min(1.,t));return t*t*(3-2*t)


def scene(key,t=0.):
    aliases={'relaxed':'calm','content':'contented','tense':'frustrated','low':'sad','engaged':'excited','sleepy':'exhausted'}
    key=aliases.get(key,key)
    if key not in CARDS:
        return [{'kind':'path','commands':[['M',112,139],['C',140,117,191,110,221,139],['C',250,169,257,232,228,253],['C',203,271,132,268,109,250],['C',85,230,87,168,112,139],['Z']],'role':'muted','width':2.4,'fill':None,'opacity':.55,'fill_opacity':0,'stroke_opacity':1}]
    card=CARDS[key];pose=card['pose'];expression=card['expression'];colour='poster_'+card['colour']
    u=(t/(5.2+list(CARDS).index(key)%5*.23))%1
    breath=(smooth(u/.35) if u<.35 else 1-smooth((u-.35)/.65))-.5
    lift=-6*max(0.,math.sin(t*math.pi*.8))**2 if key in ('excited','exhilarated') else -1.5*breath
    lean=(4*math.sin(t*.7) if expression in ('curious','confused') else 0.)
    angle=math.radians(lean);sx=1+.012*breath;sy=1-.018*breath
    items=[]
    def transform(x,y):
        x=(x-180)*sx;y=(y-265)*sy
        return (180+x*math.cos(angle)-y*math.sin(angle),265+x*math.sin(angle)+y*math.cos(angle)+lift)
    def path(commands,role='poster_ink',width=3.5,fill=None,opacity=1,move=True):
        out=[]
        for c in commands:
            values=[]
            for i in range(1,len(c),2):values.extend(transform(c[i],c[i+1]) if move else (c[i],c[i+1]))
            out.append([c[0],*values])
        items.append({'kind':'path','commands':out,'role':role,'width':width,'fill':fill,'opacity':opacity,'fill_opacity':1,'stroke_opacity':1 if width else 0})
    def dot(x,y,r=4.,role='poster_ink'):
        x,y=transform(x,y);items.append({'kind':'dot','x':x,'y':y,'r':r,'role':role,'opacity':1})
    path([['M',90,276],['C',94,266,270,265,275,276],['C',272,286,93,288,90,276],['Z']],'art_shadow',0,'art_shadow',.15,False)
    bodies={
      'tall':[['M',145,91],['C',158,76,182,74,195,87],['C',217,106,227,129,238,152],['C',260,196,269,238,246,257],['C',225,278,130,279,110,258],['C',90,238,104,199,112,172],['C',121,139,127,112,145,91],['Z']],
      'round':[['M',111,132],['C',127,103,160,105,184,112],['C',217,98,251,118,261,147],['C',279,185,282,231,259,253],['C',231,279,129,278,105,252],['C',81,227,87,167,111,132],['Z']],
      'fold':[['M',109,126],['C',120,95,166,97,193,113],['C',225,128,235,152,216,175],['C',247,168,277,192,268,225],['C',262,259,219,273,180,268],['C',137,272,103,257,102,229],['C',101,197,89,160,109,126],['Z']],
      'lean':[['M',128,108],['C',152,85,204,92,215,119],['C',235,113,256,131,252,152],['C',249,177,221,185,221,205],['C',250,225,237,256,212,265],['C',185,278,113,273,100,252],['C',81,223,98,190,106,164],['C',116,141,109,128,128,108],['Z']],
      'puddle':[['M',72,231],['C',95,210,120,181,151,178],['C',177,176,193,201,216,207],['C',243,212,274,224,293,241],['C',309,255,298,267,275,268],['C',211,267,128,276,78,268],['C',48,265,48,247,72,231],['Z']],
      'spark':[['M',119,110],['C',136,90,149,109,164,101],['C',180,92,195,103,210,91],['C',225,80,244,88,240,107],['C',231,139,241,164,247,185],['C',263,221,257,254,229,265],['C',201,277,142,272,123,259],['C',99,242,110,213,109,185],['C',108,157,98,133,119,110],['Z']],
    }
    path(bodies[pose],width=2.7,fill=colour)
    # Facial placement follows posture; puddles keep their face in the upper surface.
    cy=215 if pose=='puddle' else 170
    lx,rx=145,205
    def eyes(kind='dots'):
        if kind=='closed':
            path([['M',lx-12,cy],['Q',lx,cy+13,lx+12,cy]],width=3.4);path([['M',rx-12,cy],['Q',rx,cy+13,rx+12,cy]],width=3.4)
        elif kind=='smile':
            path([['M',lx-12,cy],['Q',lx,cy-14,lx+12,cy]],width=3.5);path([['M',rx-12,cy],['Q',rx,cy-14,rx+12,cy]],width=3.5)
        elif kind=='wide':
            for x in (lx,rx):
                path([['M',x-9,cy],['C',x-9,cy-13,x+9,cy-13,x+9,cy],['C',x+9,cy+13,x-9,cy+13,x-9,cy],['Z']],width=2.5,fill='poster_eye');dot(x+2,cy+2,3.)
        elif kind=='squint':
            path([['M',lx-12,cy-3],['L',lx+10,cy+1]],width=4.);path([['M',rx-10,cy+1],['L',rx+12,cy-3]],width=4.)
        else:dot(lx,cy,4.);dot(rx,cy,4.)
    def mouth(kind='smile'):
        y=cy+43
        if kind=='smile':path([['M',151,y],['C',163,y+25,193,y+25,212,y-1]],width=3.6)
        elif kind=='frown':path([['M',154,y+9],['Q',179,y-13,204,y+9]],width=3.6)
        elif kind=='flat':path([['M',159,y+4],['Q',178,y+1,199,y+4]],width=3.6)
        elif kind=='wavy':path([['M',154,y+4],['C',167,y-6,174,y+16,184,y+4],['Q',196,y-5,207,y+2]],width=3.5)
        elif kind=='open':
            path([['M',155,y-3],['Q',180,y+8,210,y-7],['C',208,y+42,163,y+43,155,y-3],['Z']],width=2.,fill='poster_ink')
            path([['M',168,y+25],['Q',184,y+16,198,y+24]],'poster_tongue',5.)
        elif kind=='o':path([['M',169,y],['C',166,y-17,190,y-19,190,y],['C',190,y+21,169,y+21,169,y],['Z']],width=2.5,fill='poster_ink')
    if expression in ('calm','content'):eyes('closed');mouth('smile')
    elif expression=='smile':eyes();mouth('smile')
    elif expression in ('happy','delight','laugh'):
        eyes('smile');mouth('open' if expression!='happy' else 'smile')
    elif expression in ('shock','awe'):
        eyes('wide');mouth('o')
    elif expression=='confused':
        eyes('wide');path([['M',129,cy-22],['Q',141,cy-34,153,cy-23]],width=2.8);path([['M',196,cy-20],['Q',210,cy-12,222,cy-20]],width=2.8);mouth('wavy')
    elif expression=='curious':eyes();path([['M',128,cy-20],['Q',141,cy-35,155,cy-23]],width=2.8);mouth('flat')
    elif expression in ('angry','frustrated','annoyed'):
        eyes('squint' if expression!='angry' else 'dots');path([['M',128,cy-23],['Q',143,cy-21,157,cy-10]],width=3.5);path([['M',194,cy-10],['Q',207,cy-22,225,cy-23]],width=3.5);mouth('wavy' if expression=='frustrated' else 'flat' if expression=='annoyed' else 'frown')
    elif expression in ('sad','weepy','afraid'):
        eyes('wide' if expression=='afraid' else 'closed');path([['M',132,cy-22],['Q',143,cy-21,155,cy-31]],width=2.8);path([['M',196,cy-30],['Q',209,cy-21,222,cy-23]],width=2.8);mouth('frown')
        if expression=='weepy':dot(219,cy+18,4,'poster_eye')
    elif expression=='disgust':eyes('squint');mouth('wavy')
    elif expression=='yawn':eyes('closed');mouth('o')
    elif expression=='exhausted':
        for x in (lx,rx):path([['M',x-6,cy-4],['L',x+6,cy+5],['M',x+6,cy-4],['L',x-6,cy+5]],width=2.8)
        mouth('flat')
    return items


def svg_path(commands):return ' '.join(c[0]+(' '+' '.join(f'{x:.3f}' for x in c[1:]) if len(c)>1 else '') for c in commands)
