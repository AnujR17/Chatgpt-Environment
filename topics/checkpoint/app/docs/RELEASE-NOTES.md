# Checkpoint — Camera and phone connection fix

Fixes Windows camera startup with DirectShow first, Media Foundation/default fallback and warm-up retries. The MSMF hardware-transform path is disabled for this app process. Select the intended camera from the new device control. A tracking-model startup/inference failure no longer shuts down the preview; its error is shown separately. Model loading also handles non-ASCII install folders.

Phone pairing now labels network adapters, prefers active Wi-Fi, reports dashboard connection status and provides a laptop link test. Windows users can explicitly copy a narrowly scoped Private-network/local-subnet firewall rule for this app and its current dashboard port; no firewall changes happen automatically. See docs/CAMERA-AND-PHONE-TROUBLESHOOTING.md.

Extract the full ZIP and run Start Checkpoint.cmd. Tick Track my face and Start camera; Show Pip enables the transparent, frameless, click-through desktop character. Phone dashboard pairs a read-only local dashboard by QR on the same trusted Wi-Fi. Report exports derived observations as JSON. No camera/game images or typed text are sent to the phone.

Pip is one continuous original blob. Neutral and unavailable tracking use a flat mouth and relaxed brows. Default physical mapping uses Google MediaPipe Face Landmarker; optional neutral calibration is in memory and requires no collection of posed emotion photos. HSEmotion is the alternative experimental category model: 62.5% versus the earlier model's 29.8% on the matched 208 acted-video clips, not gamer or personal-webcam accuracy.

Opt-in game-focused mouse/key timing and conservative quiet nudges are included. No key identities or typed text are exported, and the overlay never injects into or controls the game. Windowed/borderless play is recommended; universal fullscreen/anti-cheat compatibility is not claimed. Keep ordinary sharing on a trusted private LAN; HTTP transport is not encrypted.

The gameplay source list and actual limited trailer-training results are included. YouTube downloads were blocked by the workspace proxy. The trained single-trailer scene model failed to generalize an opening view and remains a research artifact; live game cues still use labelled experimental heuristics, not a trained full-game/mood detector.

Automated publication checks cover native Windows launch, overlay focus/style, own-window GDI, input registration, model inference and the loopback phone API. Physical camera, real phone Wi-Fi/firewall access, actual game performance and intervention usefulness remain unverified. This unsigned research preview is not a production affect detector.
