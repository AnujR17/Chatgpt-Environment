"""Explicitly enabled session reminders, independent of camera and game tracking."""
import math


class BreakReminder:
    MESSAGE = "Let's take a break?"

    def __init__(self):
        self.deadline = None
        self.interval = 30
        self.message_until = 0.

    def reset(self):
        self.deadline = None
        self.message_until = 0.

    def update(self, now, *, enabled, active=True, paused=False, seconds=30):
        seconds = max(30, min(3600, int(seconds)))
        if not enabled or not active or paused:
            self.reset()
            return ''
        if self.deadline is None or seconds != self.interval:
            self.interval = seconds
            self.deadline = now + seconds
            self.message_until = 0.
        elif now >= self.deadline:
            self.deadline = now + seconds
            self.message_until = now + 9
        return self.MESSAGE if now < self.message_until else ''

    def remaining(self, now):
        return max(0, math.ceil(self.deadline - now)) if self.deadline is not None else None
