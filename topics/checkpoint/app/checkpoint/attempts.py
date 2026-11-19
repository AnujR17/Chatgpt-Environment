"""Player-requested practice help. No camera-to-CMA or automatic route claims."""
from dataclasses import asdict, dataclass
import math

GUIDE = 'https://progameguides.com/getting-over-it-with-bennett-foddy/how-to-beat-getting-over-it/'
COMMUNITY = 'https://steamcommunity.com/sharedfiles/filedetails/?id=2913335491'


@dataclass(frozen=True)
class Technique:
    key: str
    section: str
    problem: str
    cue: str
    target: str
    explanation: str
    source: str


# Original short practice prompts informed by the linked guides, not copied walkthroughs.
TECHNIQUES = (
    Technique('placement', 'Early climb', 'I keep missing the contact point',
              'Watch the hammer tip. Place it before pulling.',
              'Make one deliberate contact; height is not the target.',
              'The hammer tip is the contact point. Separating placement from the pull gives you one movement to practise before adding speed.', GUIDE),
    Technique('launch', 'Early climb', 'My launch has no control',
              'Set the hammer below the pot before pushing off.',
              'Practise one push from a stable surface.',
              'Build the launch from a settled position. Aim for a reachable contact above you; add the swing after the push becomes repeatable.', GUIDE),
    Technique('chimney', "Devil’s Chimney", 'I cannot make the next hold',
              'Pick the next lamp. Aim the hammer tip there.',
              'Secure the next hold, rather than the whole chimney.',
              'Use the lamps as nearby targets. Work on one reachable hold at a time before chaining the climb. This is a practice prompt, not a guaranteed route.',
              'https://avidachievers.com/speedruns/getting-over-it-speedrun-guide/'),
    Technique('grip', 'Slippery ledges', 'I lose the hold when I rush',
              'Try a shorter reach and a slower pull.',
              'Test one secure contact before trying for more height.',
              'A community guide suggests keeping the hammer closer on slippery sections. Try that as one adjustment; judge it on your own setup rather than changing every mouse setting.', COMMUNITY),
    Technique('orange', 'Orange Hell', 'I overshoot the first reach',
              'Use a smaller hop; slow the swing near contact.',
              'Reach the first hold once, without chasing the next jump.',
              'Community players describe a small table hop followed by slowing the hammer before the rock. Keep the attempt to that first reach; this is route help and may be a spoiler.',
              'https://steamcommunity.com/app/240720/discussions/0/6761670113853118143/'),
)
BY_KEY = {t.key: t for t in TECHNIQUES}


def guidance_mode(session):
    """Use only a recent explicit report. Five minutes is a design expiry, not a finding."""
    if not session.reports:
        return 'choice', 'No recent CMA check-in · choose the amount of help'
    r = session.reports[-1]
    v, a, stamp = r.get('valence'), r.get('arousal'), r.get('elapsed_seconds')
    if not all(isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)
               for x in (v, a, stamp)) or not (-1 <= v <= 1 and -1 <= a <= 1):
        return 'choice', 'CMA not specified · choose the amount of help'
    # Check-in timestamps are rounded to hundredths; a fresh one can lead by 5ms.
    if not -.01 <= session.elapsed() - stamp <= 300:
        return 'choice', 'Earlier check-in · choose what fits now'
    if v < -.18 and a > .4:
        return 'brief', 'Your check-in: unpleasant + high activation · one cue first'
    if v < -.18 and a < -.4:
        return 'small', 'Your check-in: unpleasant + low activation · a smaller target'
    return 'choice', 'Your recent check-in · help stays on your terms'


def active_attempt(session):
    if not session.active or session.break_deadline is not None:
        return None
    return next((x for x in reversed(session.attempts) if x['outcome'] is None and x['game'] == session.game), None)


def recent_cma(session):
    if not session.reports:
        return None
    r = session.reports[-1]
    values = r.get('valence'), r.get('arousal'), r.get('elapsed_seconds')
    if not all(isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) for x in values):
        return None
    v, a, stamp = values
    if -1 <= v <= 1 and -1 <= a <= 1 and 0 <= session.elapsed() - stamp <= 300:
        return {'valence': v, 'arousal': a, 'report_index': len(session.reports)-1}
    return None


def start_attempt(session, key, *, mode=None):
    if (not session.active or session.break_deadline is not None or session.game != 'Getting Over It'
            or active_attempt(session) is not None or key not in BY_KEY):
        return None
    suggested, basis = guidance_mode(session)
    chosen = mode if mode in ('brief', 'small', 'choice') else suggested
    t = BY_KEY[key]
    row = {**asdict(t), 'id': len(session.attempts) + 1, 'game': session.game,
           'mode': chosen, 'guidance_basis': basis + (' · smaller target requested' if mode == 'small' and suggested != 'small' else ''),
           'elapsed_seconds': round(session.elapsed(), 2),
           'report_index': len(session.reports) - 1 if session.reports else None,
           'source_kind': 'player_selected_section', 'outcome': None, 'lesson': '',
           'cma_before': recent_cma(session), 'cma_after': None}
    session.attempts.append(row)
    session.practice_goal = t.target if chosen == 'small' else t.cue
    return row


def finish_attempt(session, outcome, lesson=''):
    row = active_attempt(session)
    if row is None or outcome not in ('helped', 'stuck', 'dismissed'):
        return False
    row.update(outcome=outcome, lesson=str(lesson).strip()[:240],
               finished_seconds=round(session.elapsed(), 2))
    later = recent_cma(session)
    if later and later['report_index'] > (row['report_index'] if row['report_index'] is not None else -1):
        row['cma_after'] = later
    return True


def attempt_summary(session):
    rows = session.attempts
    completed = [r for r in rows if r.get('outcome') in ('helped', 'stuck')]
    return {'started': len(rows), 'rated': len(completed),
            'helped': sum(r['outcome'] == 'helped' for r in completed),
            'still_stuck': sum(r['outcome'] == 'stuck' for r in completed),
            'unrated': sum(r.get('outcome') is None for r in rows),
            'dismissed': sum(r.get('outcome') == 'dismissed' for r in rows),
            'lessons': [{'elapsed_seconds':r['elapsed_seconds'],'section': r['section'], 'cue': r['target'] if r['mode']=='small' else r['cue'],
                         'lesson': r['lesson'], 'outcome': r['outcome'],
                         'cma_before': r.get('cma_before'), 'cma_after': r.get('cma_after')} for r in completed],
            'basis': 'Player-rated usefulness, not measured skill or emotion improvement.'}


def saved_lessons(history, session, key):
    rows = [r for record in history if record.get('game') == session.game
            for r in record.get('attempts', [])]
    rows += session.attempts
    return [r for r in rows if r.get('key') == key and r.get('game', session.game) == session.game
            and r.get('outcome') == 'helped' and r.get('lesson')][-3:]


def phone_attempt(session):
    row = active_attempt(session)
    if not row:
        return None
    return {k: row[k] for k in ('section', 'cue', 'target', 'mode', 'guidance_basis')}
