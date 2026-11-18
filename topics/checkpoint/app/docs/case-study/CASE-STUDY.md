# Research and design decisions

## The player

Regen supports hobby players learning Getting Over It. After losing progress, the player wants a useful next step while remaining in control of the challenge.

## Research

Published research, public gaming discussions and game documentation informed four decisions:

- Competence: offer one manageable action after a setback. [Przybylski and colleagues, 2014](https://pubmed.ncbi.nlm.nih.gov/24377357/).
- Context: keep visible facial movement separate from player-reported feeling. [Barrett and colleagues, 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6640856/).
- Motivation: make encouragement, a next move and a pause available as player choices. [Pusey, Wong and Rappa, 2022](https://doi.org/10.1177/15554120211056126).
- Tilt: include the player’s goal, situation and helpfulness feedback when reviewing a difficult moment. [Cregan, Toth and Campbell, 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11082399/).

[Evidence register](RESEARCH-EVIDENCE.md)

[Interview guide](INTERVIEW-GUIDE.md)

## Design personas

Rohan values competitive progress and respectful communication. Kavya values participation, privacy and control over labels. Aman wants a short session that fits his time and energy. Alex enjoys difficult climbs and wants to preserve discovery. Morgan needs control over what appears during a broadcast.

Together, these profiles focus the design on optional help, suitable timing, private check-ins and the freedom to keep playing.

## Interaction direction

Start play support, then offer a short response after a possible setback or about 2½ minutes of active gaming. The player can continue, pause, mute or request help directly.

A recent CMA check-in can select a support style. Pleasantness and activation come from the player. Camera observations remain a separate source in the interface.

## Information architecture

Session contains the game context, play support, check-in, camera/test view, technique cues and session controls. Recap contains reported CMA moments, choices, helpfulness and PDF export. Saved contains consented summaries and deletion. Tracking describes the sources and their status. Settings contains support, face/hand, overlay, motion, history and update preferences.

The Nori overlay and phone are connected displays. Local processing and session data sit beneath these player-facing destinations.

## Prototype

The native interface gives Nori a large stage, compact source controls, conventional icons and sage-green actions. The transparent overlay brings a brief response into play. The paired phone shows derived state while the game remains in focus.

The recap connects reported feelings, context, choices and later check-ins. The player can rate a choice and save the summary on their own device.

## Visual identity

Regen draws on regeneration and another attempt. Nori carries expressions through soft features, shape and colour. DM Sans, sage surfaces, evergreen actions and the papercraft game world connect the application and case study.

## Technology

Python, PySide6, QPainter, MediaPipe, HSE expression estimates, OpenCV game-window observations and aggregate input timing support the native prototype. Playwright and Chromium verify the visual case-study interactions and responsive layouts.

## Five primary emotions

Neutral, Happy, Frustrated, Sad and Confused form the shared vocabulary across the session, Nori widget, check-in and phone. Laughter sits within Happy; anger and tension cues sit within Frustrated. Player check-ins supply pleasantness and activation.

## Widget interaction

The emotion name and break countdown remain visible. Click Nori to check in, take a timed break, mark a fall or mute reminders. Drag to move the widget. Continue playing ends a completed break.
