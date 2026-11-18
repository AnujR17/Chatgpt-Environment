# Regen feasibility

## Recommended scope

A native companion for casual and committed hobby players, starting with Getting Over It. The first service is support during play: a possible fall, a settled view and one short response. CMA check-ins can adjust its style. A recap is optional.

A launcher, club-booking service or professional coach would add another product problem and infrastructure. Automatic recognition of 43 felt emotions is not a credible promise for this prototype.

## Implemented

- Adjustable CMA check-ins and 43 authored feeling cards.
- Optional next-move, encouragement or quiet-pause responses; recent explicit CMA reports can choose a default.
- Deduplicated possible-fall events, settled-view timing, stale-event rejection and a two-minute cooldown.
- Visible mute, manual I fell fallback and Windows global shortcuts while support runs.
- Five manually selected practice cues, player feedback and consented note recall.
- Native session UI, frameless companion, paired phone and PDF recap.
- Existing face/hand estimates, optional game-window observations and aggregate input timing.

## Limits

Face movement cannot establish a person’s felt emotion. The model remains imperfect; confused appearance is tentative. The existing 62.5% result on 208 acted clips is not gamer mood accuracy.

Game vision estimates background movement and recognises views the player marks. It does not understand the entire route, exact altitude or confirmed deaths. Automatic support uses those uncertain estimates; it must be validated against labelled actual gameplay. It can miss falls that do not move the camera, mistake scene movement for a fall, and fail under occlusion or exclusive fullscreen. Manual I fell remains available.

The phone receives derived state over local HTTP. Physical Wi-Fi, firewall conditions and the laptop remaining open still matter. Exclusive fullscreen can hide a separate desktop overlay.

## Native practicality

PySide6 fits the Windows overlay, local camera and foreground-window features. Native architecture alone does not prove lower power use. Compare game FPS, CPU, memory and update latency with sensing on and off before making a low-overhead claim.

The existing portable distribution is roughly 243 MB compressed. Regen reuses its runtime and models; there is no cloud inference bill for the core flow. Device compatibility and game-specific observation still carry maintenance cost.

The public name changes to Regen. Internal storage, pairing and update identifiers stay compatible with existing installations. This review does not publish an OTA.

## Test in play

Use one consenting target player as a formative check. Let them start support and play without prompting them to feel frustrated. Label falls and non-falls, count false and missed responses, measure event-to-tip delay, and ask whether the tip helped or interrupted the next attempt. Then offer the optional check-in and recap.

Observe interruption, unwanted spoilers, misread expressions and confusion between a face estimate and a CMA report. Start manual-only, then check whether the sensors add value. One session can reveal usability problems; it cannot validate a population-level benefit.

## Verification

124 local checks passed, five skipped. Native flow and the real loopback/Chromium phone/PDF checks passed. The visual case-study interaction passed at desktop, 390px and 320px, including feedback and reduced motion. [Current evidence](verification.json).

[Windows run 44256785585](https://github.com/AnujR17/Chatgpt-Environment/actions/runs/44256785585) passed at the branded application commit `1ead5a783bdc7cfc9b3765a4e17d092f80fefdca`. It covers native practice, model/hand inference, GDI capture, overlay and loopback fixtures. No physical camera/game/phone study or actual-play usefulness result is claimed.
