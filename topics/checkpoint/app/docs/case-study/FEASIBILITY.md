# Technology and feasibility

## Native desktop

PySide6 supports the Windows session interface, local camera processing and frameless companion. Nori stays click-through during play and can be repositioned. Borderless or windowed play keeps the desktop overlay visible.

## Local sources

- Camera: MediaPipe face and hand features, with optional HSE expression estimates.
- Game: foreground Getting Over It window observations, background-motion estimates and marked-view recognition.
- Input: optional game-focused timing and activity aggregates.
- CMA: the player’s pleasantness and activation check-ins.

## Support during play

Start play support enables game observation and the overlay. A possible fall followed by a settled view can prompt a short next-move reminder, encouragement or optional pause. Automatic invitations are spaced two minutes apart.

I fell requests a response directly. Windows shortcuts provide manual setback marking and mute while support is running. A one-off request preserves the automatic-tip mute preference.

## Recap and phone

The recap relates check-ins, context, choices, later feelings and helpfulness feedback. It is available as a native PDF. A paired phone receives derived state and the report over trusted Wi-Fi.

## Privacy and storage

The player enables each source. Images are processed locally. Saving summaries requires consent; saved history can be deleted. Phone sharing can be stopped from the app.

## Software checks

The application revision passed 124 local tests. [Windows review](https://github.com/AnujR17/Chatgpt-Environment/actions/runs/44271249558) exercised the native session, support/recovery flows, model loading, GDI capture, overlay, shortcut dispatch and loopback phone connection.

The visual case study is checked at desktop and phone widths for navigation, interactive examples, reduced motion, readable research pages and overflow.
