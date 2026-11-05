"""Product state and local history. Facial cues cannot set a player's CMA report."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import tempfile
import time


from checkpoint.affect import REFERENCES, dimension_words

FEELINGS = {key: (title, *dimension_words(v, a), description)
            for key, (title, v, a, description) in REFERENCES.items()}
FEELINGS['mixed'] = ('Mixed / not sure', 'Not specified', 'Not specified', 'You do not have to choose one feeling.')


@dataclass
class Session:
    game: str = "Getting Over It"
    intention: str = "Enjoy the challenge"
    competitive: bool = False
    started: float = field(default_factory=time.monotonic)
    started_at: str = field(default_factory=lambda:datetime.now(timezone.utc).isoformat())
    active: bool = True
    camera_active: bool = False
    experimental_analysis: bool = False
    face_mapping: bool = True
    face_gain: float = 1.5
    hand_tracking: bool = True
    category_estimates: bool = True
    quiet: bool = True
    source_kind: str | None = None
    cue: object | None = None
    cue_received_at: float = 0.
    report: str | None = None
    valence: float | None = None
    arousal: float | None = None
    reports: list = field(default_factory=list)
    context: str = "Manual game context"
    break_deadline: float | None = None
    ended: float | None = None
    generation: int = 0

    @property
    def affect(self):
        if self.report is None:
            return ("No check-in yet", "Not reported", "Not reported", "Your pleasantness and energy come from your own check-in.")
        title, _, _, description = FEELINGS[self.report]
        if self.valence is None or self.arousal is None:return FEELINGS[self.report]
        if (self.valence,self.arousal) != REFERENCES[self.report][1:3]:description='Your description of this moment.'
        return (title, *dimension_words(self.valence, self.arousal), description)

    def start_capture(self, kind):
        if not self.active: raise ValueError("Start a new session first")
        if self.break_deadline is not None: raise ValueError("Finish the break before resuming capture")
        if kind not in ("camera","video"): raise ValueError("Unsupported capture source")
        self.generation += 1;self.camera_active=True;self.source_kind=kind;self.cue=None
        return self.generation

    def stop_capture(self):
        self.generation+=1;self.camera_active=False;self.source_kind=None;self.cue=None

    def receive_cue(self, cue, generation):
        if not self.active or not self.camera_active or not self.experimental_analysis or generation!=self.generation:
            return False
        self.cue=cue;self.cue_received_at=time.monotonic()
        return True

    def check_in(self, feeling, valence=None, arousal=None):
        if not self.active: raise ValueError("Session has ended")
        if feeling not in FEELINGS: raise ValueError("Unknown check-in")
        if feeling == 'mixed':
            if valence is not None or arousal is not None:raise ValueError('Mixed has no assumed coordinates')
        elif valence is None and arousal is None:
            valence, arousal = REFERENCES[feeling][1:3]
        else:
            import math
            if any(isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) or not -1<=x<=1 for x in (valence,arousal)):
                raise ValueError('Both dimensions must be finite values between -1 and 1')
        self.report=feeling;self.valence=valence;self.arousal=arousal
        self.reports.append({"feeling":feeling,"valence":valence,"arousal":arousal,
                             "elapsed_seconds":round(time.monotonic()-self.started,2),"source":"player_report"})

    def take_break(self, seconds=30, now=None):
        if not self.active: raise ValueError("Session has ended")
        self.stop_capture();self.break_deadline=(time.monotonic() if now is None else now)+seconds

    def finish_break(self):
        self.break_deadline=None
        # Deliberately leave capture off; no automatic resume even when timer reaches zero.

    def end(self):
        self.stop_capture();self.break_deadline=None;self.active=False;self.ended=time.monotonic()

    def elapsed(self):
        return max(0,(self.ended if self.ended is not None else time.monotonic())-self.started)

    def summary(self):
        return {"schema":1,"started_at":self.started_at,"duration_seconds":round(self.elapsed(),2),"game":self.game,
                "intention":self.intention,"check_ins":list(self.reports),"capture_stopped":not self.camera_active}


class History:
    def __init__(self, directory):
        self.directory=Path(directory)
        self.path=self.directory/"history.json"

    def read(self):
        if not self.path.exists():return []
        records=json.loads(self.path.read_text())
        if not isinstance(records,list):raise ValueError("Invalid local history")
        return records

    def save(self, summary, *, consent=False):
        if not consent:return False
        records=(self.read()+[summary])[-100:]
        self.directory.mkdir(parents=True,exist_ok=True)
        with tempfile.NamedTemporaryFile(mode="w",dir=self.directory,delete=False,encoding="utf8") as f:
            json.dump(records,f,indent=2);temporary=f.name
        os.chmod(temporary,0o600);os.replace(temporary,self.path)
        return True

    def delete(self):
        if self.path.exists():self.path.unlink()
