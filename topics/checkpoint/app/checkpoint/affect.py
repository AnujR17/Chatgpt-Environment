"""CMA reference vocabulary and deterministic procedural motion.
Coordinates and graphical encodings are design defaults, not measured norms.
"""
import math

# label, pleasantness, activation, description. No inference from facial cues.
ANCHORS = {
    'confused': ('Confused', .0, .0, 'A moment of uncertainty; pleasantness and activation can vary.'),
    'bewildered': ('Bewildered', -.20, .70, 'Surprised and disoriented; adjust both dimensions for yourself.'),
    'happy': ('Happy', .85, .20, 'A pleasant moment with some lift.'),
    'excited': ('Excited', .65, .80, 'Pleasant and highly activated.'),
    'content': ('Content', .75, -.30, 'Comfortable with how this moment feels.'),
    'calm': ('Calm', .60, -.65, 'Pleasant, with little activation.'),
    'relaxed': ('Relaxed', .65, -.55, 'At ease, with room to slow down.'),
    'tense': ('Tense', -.20, .90, 'Activated, with some discomfort.'),
    'angry': ('Angry', -.75, .60, 'Unpleasant and strongly activated.'),
    'afraid': ('Afraid', -.65, .85, 'Unpleasant, alert and highly activated.'),
    'frustrated': ('Frustrated', -.80, .30, 'Unpleasant, with some activation.'),
    'sad': ('Sad', -.65, -.55, 'Unpleasant, with little activation.'),
    'bored': ('Bored', -.55, -.65, 'Unpleasant and underactivated.'),
    'sleepy': ('Sleepy', .0, -.90, 'Very little activation; pleasantness can vary.'),
}
LEGACY = {
    'engaged': ('Engaged', .55, .65, 'The challenge still feels enjoyable.'),
    'low': ('Low', -.55, -.60, 'This moment feels flat or tiring.'),
}
REFERENCES = {**ANCHORS, **LEGACY}

# Extended words are optional vocabulary, with adjustable illustrative defaults.
# No categorical word or facial cue establishes either dimension for a person.
from checkpoint.vocabulary import CARDS
from checkpoint.cma_defaults import DEFAULTS
for _key,_card in CARDS.items():
    if _key not in REFERENCES:
        _v,_a=DEFAULTS.get(_key,(0.,0.))
        REFERENCES[_key]=(_card['label'],_v,_a,'Your word for this moment. Adjust the balance to fit how it feels.')


def dimension_words(valence, arousal):
    def value(v, low, mid, high, threshold=.18):
        return low if v < -threshold else high if v > threshold else mid
    return (value(valence, 'Unpleasant', 'In between', 'Pleasant'),
            value(arousal, 'Low activation', 'Moderate activation', 'High activation', .4))


def contours(valence, arousal, phase=0., count=5, samples=96):
    """Fixed topology supports continuous morphs. Points are normalised to [-1,1].
    Valence shapes curvature/openness; activation shapes excursion and tempo.
    No unique emotion can be recovered from this geometry.
    """
    v=max(-1.,min(1.,valence)); a=(max(-1.,min(1.,arousal))+1)/2
    openness=(v+1)/2
    result=[]
    for j in range(count):
        points=[];layer=j/(count-1)
        for i in range(samples):
            t=2*math.pi*i/samples
            wave=(.015+.18*a)*math.sin(3*t+phase+layer*.7)
            pinch=(1-openness)*.19*math.cos(4*t-phase*.4+layer*.35)
            ripple=(1-openness)*a*.045*math.sin(9*t+phase*.6)
            r=(.48+layer*.115)*(1+wave+pinch+ripple)
            twist=.13*math.sin(2*t+phase*.5)*(1-openness)
            x=r*math.cos(t+twist)*( .82+.15*openness )
            y=r*math.sin(t+twist)*( .88-.10*openness )
            x+=.018*a*math.sin(phase+layer)
            y+=.025*a*math.cos(phase*.8+layer)
            points.append((x,y))
        result.append(points)
    return result


def svg_path(points, size=360):
    # Catmull-Rom -> cubic Beziers, same path as native QPainter renderer.
    p=[((x+1)*size/2,(y+1)*size/2) for x,y in points];n=len(p)
    chunks=[f'M {p[0][0]:.3f} {p[0][1]:.3f}']
    for i in range(n):
        p0,p1,p2,p3=p[(i-1)%n],p[i],p[(i+1)%n],p[(i+2)%n]
        c1=(p1[0]+(p2[0]-p0[0])/6,p1[1]+(p2[1]-p0[1])/6)
        c2=(p2[0]-(p3[0]-p1[0])/6,p2[1]-(p3[1]-p1[1])/6)
        chunks.append(f'C {c1[0]:.3f} {c1[1]:.3f} {c2[0]:.3f} {c2[1]:.3f} {p2[0]:.3f} {p2[1]:.3f}')
    return ' '.join(chunks)+' Z'
