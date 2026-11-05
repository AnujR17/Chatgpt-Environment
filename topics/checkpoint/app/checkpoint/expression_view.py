"""Presentation of observed expression categories, separate from player-reported CMA."""
from dataclasses import dataclass
import time

# Illustration bindings do not define valence/arousal or additional model classes.
EXPRESSIONS = {
    'neutral': ('Neutral expression', 'composed'),
    'happiness': ('Happy expression', 'happy'),
    'surprise': ('Surprised expression', 'surprised'),
    'sadness': ('Sad expression', 'sad'),
    'anger': ('Angry expression', 'angry'),
    'disgust': ('Disgust-like expression', 'disgust'),
    'fear': ('Fear-like expression', 'afraid'),
    'contempt': ('Contempt-like expression', 'annoyed'),
}


@dataclass(frozen=True)
class ExpressionDisplay:
    title: str
    artwork: str | None
    detail: str


def expression_display(session, *, max_age=5):
    if not session.experimental_analysis:
        return ExpressionDisplay('Tracking is off', None, 'Enable Track expressions, then start your camera.')
    if not session.camera_active:
        return ExpressionDisplay('Camera paused', None, 'Start your camera or open a local video to track expressions.')
    cue = session.cue
    if cue is None:
        return ExpressionDisplay('Looking for a face', None, 'Waiting for a stable expression. This is an experimental estimate.')
    if time.monotonic() - session.cue_received_at > max_age:
        return ExpressionDisplay('Expression unavailable', None, 'No recent camera result. The previous expression has been cleared.')
    if cue.status != 'accepted' or cue.expression not in EXPRESSIONS:
        return ExpressionDisplay('Expression uncertain', None, cue.reason or 'No stable expression estimate is available.')
    title, artwork = EXPRESSIONS[cue.expression]
    return ExpressionDisplay(title, artwork, 'Experimental face estimate · Your feeling and CMA remain your check-in.')
