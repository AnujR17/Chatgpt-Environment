# Live expressions and Getting Over It observation

## What changed in preview 2

Previously the expression worker displayed only a small research cue; the large card always read a player report. The live expression card now changes with stable, accepted model outputs. Source loss, no-face, uncertain or stale results clear the live artwork. Your chosen feeling and two CMA dimensions remain independent and are never overwritten by expression or game signals.

## Use the face tracker

1. Download preview 2 and extract the entire ZIP; launch Start Checkpoint.cmd.
2. Tick **Track expressions (experimental)** beside your camera, then click **Start camera**. You can also open a local face video.
3. The card source switches to **Live expression**. Three agreeing accepted samples are required; default analysis is twice per second. Low confidence, an unsuitable frame or no face produces an uncertain state instead of a guessed emotion.
4. Choose **Your check-in** from the card-source menu to view your own report. The CMA readouts always describe that report, even while the live expression card is selected.

The model has eight facial-expression outputs, not 43 feelings. Illustrations borrow the card family; their shape/colour and fixed animation parameters are presentation choices, not estimated valence/arousal. Neutral does not mean calm and an anger-like expression does not establish frustration. The experimental model's held-out image accuracy is 77.1%; external acted-video clip accuracy is 29.8%. These numbers are different tasks, not webcam or gamer-mood accuracy. Existing model weights, confidence calibration and failed production gates are unchanged.

## Use Getting Over It observation

1. In **Settings**, enable **Observe the Getting Over It game window**, then Save. This also enables foreground-game detection.
2. Return to the game. Windows process identity recognises GettingOverIt.exe. Only that supported foreground game's client area is sampled, up to 640 pixels wide, twice per second. A different app or a different game does not get screen analysis.
3. The context line reports possible climbing/falling from sustained background motion. The method assumes a camera following the player; it cannot distinguish every intentional descent, camera movement, jump, fall or menu transition. It is not a trained fall classifier and does not estimate height, completion percentage, cause of frustration or a player's feeling.
4. Optionally click **Mark start view**, then switch to the game at your chosen start location. The next usable game frame provides a reference held only in memory. A later match is labelled **Marked start view visible**, not a confirmed restart or death. Stop tracking clears that reference.
5. Use **Stop game tracking** to stop both process observation and screen sampling. Break, session completion and closing also stop it. Camera tracking is independent.

Process detection also recognises CS2 and Valorant, but their screen events are unsupported. Borderless/windowed mode may be needed: some fullscreen render paths return blank frames. Blank, unavailable or changed-size frames reset motion evidence and return an unknown state. Tracking never reads game memory, injects game input, or displays gameplay in place of the face preview. Raw screen frames and camera video are not saved or uploaded in normal use.

To inspect an explicit local gameplay recording offline:

```sh
python -m checkpoint.gameplay --video path/to/getting-over-it.mp4
```

This prints timestamped experimental cues; it does not record or alter the source. The live app still uses the selected foreground game window rather than silently opening a gameplay file.

## Evidence and remaining work

34 software checks pass in Linux with the separately sourced face-video fixture; one Windows-only GDI test is skipped. These cover actual recorded face inference, automatic card updates, manual-report isolation, stale/uncertain/source-loss clearing, and synthetic game motion/cuts/start-view matching. A Windows build additionally runs native card and GDI capture fixture checks against its own Qt window. Such a fixture is not a running game, a real camera or a gameplay accuracy test.

No real Getting Over It recording has been evaluated for climb/fall accuracy. Required next evidence is a labelled recording with ordinary climbing, stationary hammer movement, intentional descent, falls, menus and returning to the marked view, followed by a live Windows camera/game-performance check. Do not present the heuristic as validated game understanding or claim frustration detection. No data were invented or model retraining performed for this update.
