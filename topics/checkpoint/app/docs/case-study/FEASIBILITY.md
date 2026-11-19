# Technology and feasibility

## Native desktop

PySide6 supports the Windows session interface, local camera processing and frameless companion. Nori shows the current emotion and break countdown. Click for check-in, break and mute controls; drag to reposition. Borderless or windowed play keeps the desktop overlay visible.

## Local sources

- Camera: MediaPipe face and hand features, with optional HSE expression estimates.
- Game: foreground Getting Over It window observations, background-motion estimates and marked-view recognition.
- Input: optional game-focused timing and activity aggregates.
- CMA: the player’s pleasantness and activation check-ins.

## Support during play

Break reminders are off initially and use an independent monotonic timer. Enabling starts a fresh 30 seconds. Session provides interval presets; Settings accepts 30–3600 seconds. Camera and game tracking are optional. Taking a break clears the pending reminder; continuing starts a full interval. Session end stops prompts.

Start play support enables game observation and the overlay. Setback support is separately enabled. A possible fall followed by a settled view can prompt a next move, encouragement or optional pause. Automatic setback suggestions retain their two-minute cooldown.

The mood label and actual break timer have light fills and dark outlines, with no label surface. Nori shows no next-reminder label or countdown. Thought-cloud prompts do not activate the game window or read its pixels. Readability over visually dense motion still needs physical-device evaluation.

I fell requests a response directly. Windows shortcuts provide manual setback marking and mute while support is running. A one-off request preserves the automatic-tip mute preference.

## Recap and phone

The recap relates check-ins, context, choices, later feelings and helpfulness feedback. It is available as a native PDF. A paired phone receives derived state and the report over trusted Wi-Fi.

## Privacy and storage

The player enables each source. Images are processed locally. Saving summaries requires consent; saved history can be deleted. Phone sharing can be stopped from the app.

## Software checks

Automated checks exercise five-state mapping, widget input and break timing. [Windows review](https://github.com/AnujR17/Chatgpt-Environment/actions/runs/44280866344) exercised the native session, support/recovery flows, model loading, GDI capture, overlay, shortcut dispatch and loopback phone connection.

The visual case study is checked at desktop and phone widths for static scenes, straight mockups, visible artwork, readable research pages and overflow.
