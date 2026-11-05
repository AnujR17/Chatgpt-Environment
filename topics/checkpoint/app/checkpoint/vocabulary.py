"""Vocabulary transcribed from the user's supplied feelings reference.
Artwork is redrawn as native vector scenes; words do not infer CMA coordinates.
"""
# key, display label, pose, facial expression, colour. Synonyms support search only.
POSTER = [
 ('afraid','Afraid','tall','afraid','yellow'),
 ('amused','Amused','lean','laugh','coral'),
 ('angry','Angry','tall','angry','coral'),
 ('annoyed','Annoyed','fold','annoyed','blue'),
 ('appalled','Appalled','tall','shock','blue'),
 ('astonished','Astonished','tall','delight','blue'),
 ('awe','Awe','lean','awe','teal'),
 ('bored','Bored','tall','yawn','ochre'),
 ('brooding','Brooding','puddle','annoyed','blue'),
 ('combative','Combative','tall','angry','yellow'),
 ('composed','Composed','tall','calm','teal'),
 ('confused','Confused','tall','confused','coral'),
 ('curious','Curious','fold','curious','coral'),
 ('contented','Contented','round','content','coral'),
 ('delighted','Delighted','tall','delight','coral'),
 ('miserable','Miserable','fold','sad','blue'),
 ('determined','Determined','lean','content','teal'),
 ('disappointed','Disappointed','fold','sad','ochre'),
 ('disgust','Disgust','tall','disgust','teal'),
 ('exhausted','Exhausted','puddle','exhausted','yellow'),
 ('exhilarated','Exhilarated','spark','delight','coral'),
 ('grateful','Grateful','round','smile','teal'),
 ('happy','Happy','tall','happy','ochre'),
 ('hate','Hate','tall','angry','teal'),
 ('hysterical','Hysterical','spark','laugh','yellow'),
 ('hopeful','Hopeful','round','smile','yellow'),
 ('indignant','Indignant','fold','angry','coral'),
 ('loathing','Loathing','lean','disgust','teal'),
 ('modest','Modest','round','calm','ochre'),
 ('sad','Sad','tall','sad','blue'),
 ('satisfied','Satisfied','round','content','teal'),
 ('serene','Serene','puddle','calm','ochre'),
 ('shy','Shy','lean','curious','yellow'),
 ('sneaky','Sneaky','lean','content','yellow'),
 ('silly','Silly','fold','laugh','blue'),
 ('surprised','Surprised','tall','shock','blue'),
 ('weepy','Weepy','tall','weepy','yellow'),
 ('withdrawn','Withdrawn','fold','calm','ochre'),
 ('wonder','Wonder','lean','awe','teal'),
]
EXTRA=[
 ('calm','Calm','round','calm','teal'),
 ('frustrated','Frustrated','fold','frustrated','coral'),
 ('excited','Excited','spark','delight','ochre'),
 ('bewildered','Bewildered','lean','confused','blue'),
]
CARDS={row[0]:dict(zip(('key','label','pose','expression','colour'),row)) for row in POSTER+EXTRA}
COMMON=('calm','frustrated','confused','happy','excited','sad','angry','exhausted')
SYNONYMS={'combative':'quarrelsome','grateful':'gratitude thankful','shy':'bashful','miserable':'depressed low','frustrated':'tilt irritated blocked','calm':'composed relaxed','excited':'exhilarated enthusiastic','bewildered':'baffled unsure','exhausted':'tired drained sleepy'}


def search_cards(query='',common=False):
    keys=COMMON if common else tuple(CARDS)
    q=query.strip().casefold()
    return [key for key in keys if not q or q in (CARDS[key]['label']+' '+SYNONYMS.get(key,'')).casefold()]
