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
    movement: dict | None = None
    source: str = 'expression_estimate'


def expression_display(session, *, max_age=5):
    source='face_movement' if session.face_mapping else 'expression_estimate'
    if not session.experimental_analysis:
        return ExpressionDisplay('Tracking is off', None, 'Enable Track my face, then start your camera.',source=source)
    if not session.camera_active:
        return ExpressionDisplay('Camera paused', None, 'Start your camera or open a local video to track expressions.',source=source)
    cue = session.cue
    if cue is None:
        return ExpressionDisplay('Looking for a face', None, 'Waiting for usable face tracking.',source=source)
    if time.monotonic() - session.cue_received_at > max_age:
        return ExpressionDisplay('Tracking unavailable', None, 'No recent camera result. Pip has returned to a neutral appearance.',source=source)
    if cue.status != 'accepted' or cue.expression not in EXPRESSIONS:
        title='No face detected' if 'no face' in cue.reason.lower() else 'Face tracking unavailable' if session.face_mapping else 'Expression uncertain'
        return ExpressionDisplay(title, None, cue.reason or 'No stable expression estimate is available.',source=source)
    if cue.movement is not None:
        return ExpressionDisplay(cue.mapping_label or 'Facial movement',EXPRESSIONS[cue.expression][1],
            'Your face movements are mapped to Pip. Your feelings remain your check-in.',cue.movement,'face_movement')
    title, artwork = EXPRESSIONS[cue.expression]
    return ExpressionDisplay(title, artwork, 'Experimental face estimate · Your feeling and CMA remain your check-in.')
