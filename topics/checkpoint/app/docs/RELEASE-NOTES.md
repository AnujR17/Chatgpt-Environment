# Checkpoint 0.6 — expressions and game-window tracking

The main character now shows short expression names: Neutral, Happy, Laughing, Angry, Sad, Surprised, Disgusted, Fearful, Smirk and Tense. Diagnostic commentary is hidden from the default Expressions view. The eight-class pretrained model remains unchanged; these names label estimates, not confirmed inner feelings.

Confused? is a new tentative visual configuration, using sustained inner-brow raise plus furrow and lid tightening, with mouth, blink and smile counter-evidence. It works independently of gameplay. It is an authored heuristic, not a newly trained ninth emotion class; effort and other states can look similar. Surprise fallback now requires eye/brow evidence as well as an open mouth. Voluntary and spontaneous expressions cannot reliably be distinguished by this app.

Nori has a new rounded silhouette, softer curved brows, refreshed colours, smooth body/colour changes and a small mitten for hand-to-mouth gestures. Lost or hidden face cues still clear immediately to a flat unknown appearance. Desktop, transparent overlay and phone share the same character treatment; reduced motion remains available.

Track game now turns on process detection AND local Getting Over It screen analysis in one action. Background-motion estimates expose structured climbing/falling/steady/uncertain states, reject zoom and rotation, and count sustained motion runs rather than sampled frames. Mark section stores up to eight named visual views in RAM and recognises their return in the same session. These are visual matches and movement estimates, not guaranteed deaths, restarts, height, menu state or whole-map location. Only the foreground supported game window is captured; other apps are rejected. No raw frames are sent to the phone.

See docs/EXPRESSIONS-AND-GAME-STATE.md for research, evidence and limits. Compatible portable installations can update through Settings > Check for updates > Update and restart. Runtime wheels and bundled models are unchanged; capture starts off after restart.
