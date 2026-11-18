"""Optional setback responses. Game events and facial expressions stay separate."""
MODES = ('Match my check-in', 'Next move', 'Encouragement', 'Quiet pause')
MESSAGES = {
    'Next move': 'One secure hold. Then try the next reach.',
    'Encouragement': 'Still in it. Your next try starts here.',
    'Quiet pause': 'A breath before the next try, if you want.',
}


def response_mode(session, preference):
    """Authored support defaults, using only a recent explicit CMA check-in."""
    if preference != 'Match my check-in':return preference
    if not session.reports:return 'Next move'
    report=session.reports[-1]
    if session.elapsed()-report['elapsed_seconds']>120:return 'Next move'
    v,a=report.get('valence'),report.get('arousal')
    if v is None or a is None:return 'Next move'
    if v<-.2 and a>.2:return 'Quiet pause'
    if v>.2:return 'Encouragement'
    return 'Next move'


class PlaySupport:
    COOLDOWN = 120.
    SETTLE = 2.
    EXPIRY = 25.

    def __init__(self):
        self.last_prompt = -1000.
        self.message = ''
        self.message_at = -1000.
        self.last_observation = None
        self.observed_at = -1000.
        self.last_kind = None
        self.last_count = None
        self.pending_at = None
        self.settled_at = None
        self.basis = ''

    def clear(self):
        self.message = ''; self.pending_at = None; self.settled_at = None

    def manual(self, now, mode='Next move'):
        # An explicit player request can bypass the automatic cooldown.
        self.message = MESSAGES.get(mode, MESSAGES['Next move'])
        self.message_at = self.last_prompt = now
        self.pending_at = None; self.basis = 'Player marked a setback'
        return self.message

    def update(self, game, now, *, enabled, active, paused, input_stats=None, mode='Next move'):
        if now - self.message_at >= 9: self.message = ''
        if not active or paused:
            self.clear(); return ''
        if not enabled:
            self.pending_at = None; self.settled_at = None
            # A one-off player request does not opt back into automatic tips.
            if self.basis != 'Player marked a setback': self.message = ''
            return self.message
        if game is not self.last_observation:
            self.last_observation = game; self.observed_at = now
        state = (getattr(game, 'state', None) or {})
        cue = getattr(game, 'cue', '')
        kind = state.get('kind')
        if not kind:  # Compatibility with older observation fixtures.
            kind = 'falling' if cue.startswith('Possible fall') else 'steady' if cue.startswith('No clear vertical') else None
        usable = (getattr(game, 'game', None) == 'Getting Over It'
                  and kind in ('falling', 'climbing', 'steady', 'marked_view', 'uncertain', 'view_changed')
                  and now - self.observed_at <= 3.)
        if not usable:
            self.pending_at = None; self.settled_at = None
            return self.message
        count = state.get('possible_falls')
        new_fall = kind == 'falling' and (self.last_kind != 'falling' if count is None else count != self.last_count)
        if new_fall:
            self.pending_at = now; self.settled_at = None
        if count is not None: self.last_count = count
        self.last_kind = kind
        if kind in ('steady', 'marked_view'):
            if self.settled_at is None: self.settled_at = now
        else: self.settled_at = None
        if self.pending_at is not None:
            age = now - self.pending_at
            idle = (input_stats or {}).get('idle_seconds')
            quiet_input = isinstance(idle, (int, float)) and idle >= 3
            settled = self.settled_at is not None and (now - self.settled_at >= self.SETTLE or quiet_input)
            if age >= self.EXPIRY: self.pending_at = None
            elif age >= 3 and settled and now - self.last_prompt >= self.COOLDOWN:
                self.manual(now, mode)
                self.message = 'Possible fall. ' + self.message
                self.basis = 'Experimental game-window motion estimate'
        return self.message
