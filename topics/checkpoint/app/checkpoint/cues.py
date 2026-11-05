"""Shared cue values, independent of optional model runtime imports."""
from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class Cue:
    status: str
    expression: str | None = None
    confidence: float | None = None
    probabilities: tuple = ()
    reason: str = ""
    face_box: tuple | None = None
    elapsed_ms: float = 0.
    movement: dict | None = None
    mapping_label: str | None = None

    def to_dict(self):
        return asdict(self)

