# Project context

## AI for behavior design

Designed by Anuj Rai. Subject: Interaction design. Professor: Anupam Rana.

## Subject

Interaction design explores how a player chooses sources, recognises feedback and controls support during a difficult gaming session.

## Theme

AI for Society / Social Cause. The project focuses on agency during challenging play and access to support when the player wants it.

## Framework

The Circumplex Model of Affect describes pleasantness and activation. Player check-ins supply the coordinates; those reports can shape the style of optional support and the session recap.

## Technology and tools

A Windows laptop provides the camera and foreground game window. Local MediaPipe face/hand features, HSE expression estimates, OpenCV observations and aggregate input timing provide separate sources. Python, PySide6 and QPainter produce the native interface. The phone displays derived state over a paired connection.

Codex, GitHub, Playwright and Chromium support implementation and verification. Image generation produced the papercraft brand artwork.

## Core concept

Player input and local analysis inform a native system. The service offers a short response during play and an optional recap afterward. Regen is the product; Nori carries the interaction across desktop and phone.

## Design process

Empathize connects research themes with player needs. Define focuses on the next step after losing progress. Ideate compares ways to provide help alongside the game. Prototype implements the selected flow and checks its behaviour.

## Information architecture

The supplied architecture informed the grouping of Session, Recap, Saved, Tracking and Settings. The Nori overlay and phone extend the same session. Processing and data remain separate system layers.
