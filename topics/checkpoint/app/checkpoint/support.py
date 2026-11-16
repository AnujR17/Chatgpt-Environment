"""CMA-informed choices at explicit check-ins. Camera signals cannot trigger this policy."""
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class SupportOffer:
    kind: str
    title: str
    detail: str


def support_summary(events):
    decisions = [e for e in events if e.get("type") == "choice"]
    resets = [e for e in decisions if e.get("choice") == "reset"]
    reset_ids = {e["id"] for e in resets}
    votes = {}
    for event in events:
        if event.get("type") == "feedback" and event.get("reset_id") in reset_ids:
            votes[event["reset_id"]] = bool(event.get("helpful"))
    return {
        "resets": len(resets),
        "focus_goals": sum(e.get("choice") == "focus" for e in decisions),
        "kept_playing": sum(e.get("choice") == "continue" for e in decisions),
        "rated_helpful": sum(votes.values()),
        "rated_unhelpful": len(votes) - sum(votes.values()),
        "unrated_resets": len(resets) - len(votes),
        "basis": "Player choices and optional feedback; not inferred effectiveness.",
    }


class SupportController:
    """One inline choice per confirmed check-in; dismissal silences this session."""
    def __init__(self):
        self.token = None
        self.offer = None
        self.suppressed = False
        self.awaiting_reset = None
        self.feedback_reset = None
        self.session_key = None

    def sync(self, session):
        key = (session.started_at, session.started)
        if self.session_key is not None and self.session_key != key:
            self.__init__()
        self.session_key = key
        if not session.active:
            self.offer = None
            self.feedback_reset = None
            return None
        if self.awaiting_reset and session.break_deadline is None:
            self.feedback_reset = self.awaiting_reset
            self.awaiting_reset = None
        if session.break_deadline is not None:
            return None
        token = len(session.reports)
        if token == self.token:
            return self.offer
        self.token = token
        self.offer = None
        if self.suppressed or not session.reports:
            return None
        report = session.reports[-1]
        v, a = report.get("valence"), report.get("arousal")
        if not all(isinstance(x, (int, float)) and not isinstance(x, bool)
                   and math.isfinite(x) and -1 <= x <= 1 for x in (v, a)):
            return None
        # Proposed UI routing thresholds, not measured psychological cut-offs.
        if v < -.18 and a > .4:
            self.offer = SupportOffer("reset", "Want to reset your pace?",
                                      "From your check-in. Keep playing, or take 30 seconds away.")
        elif v < -.18 and a < -.4:
            self.offer = SupportOffer("focus", "A smaller goal for the next attempt?",
                                      "Choose one thing to practise, or keep playing as you are.")
        return self.offer

    def _record(self, session, choice, **extra):
        event = {
            "id": len(session.support_events) + 1, "type": "choice", "choice": choice,
            "elapsed_seconds": round(session.elapsed(), 2), "source": "player_action",
            "report_index": len(session.reports) - 1 if session.reports else None,
            **extra,
        }
        session.support_events.append(event)
        self.offer = None
        return event["id"]

    def keep_going(self, session):
        if not session.active or session.break_deadline is not None:
            return False
        self._record(session, "continue")
        self.suppressed = True
        return True

    def start_reset(self, session):
        if not session.active or session.break_deadline is None:
            return None
        if self.awaiting_reset is not None:
            return self.awaiting_reset
        self.awaiting_reset = self._record(session, "reset")
        self.feedback_reset = None
        return self.awaiting_reset

    def set_focus(self, session, text):
        text = str(text).strip()[:120]
        if not text or not session.active or session.break_deadline is not None:
            return False
        session.practice_goal = text
        self._record(session, "focus", goal=text)
        return True

    def feedback(self, session, helpful=None):
        if self.feedback_reset is None:
            return False
        if helpful is not None:
            session.support_events.append({
                "type": "feedback", "reset_id": self.feedback_reset,
                "helpful": bool(helpful), "elapsed_seconds": round(session.elapsed(), 2),
                "source": "player_feedback",
            })
        self.feedback_reset = None
        return True
