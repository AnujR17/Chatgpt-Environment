# Regen

A gaming companion for your next attempt.

[Open the visual case study](index.html). It includes the product, character, player flow and an interactive CMA example. These are the supporting research and design notes.

## The player problem

Being stuck does not always mean wanting to stop. A player may still enjoy the challenge and need one adjustment, less explanation or a smaller goal.

Regen starts with casual and committed hobby players in Getting Over It. Its immediate job is to offer a useful next step after a setback, without leaving the game. The audience is someone learning a difficult game, including someone who remains calm or laughs when falling. The recap is optional. Better performance, reduced anger and wellbeing remain untested outcomes.

## Empathize

The main case study connects four published findings to explicit design responses. Seven publications, six community threads and game/platform documentation form a rapid secondary review, not a systematic review. Access levels and limits are retained in the [evidence register](RESEARCH-EVIDENCE.md).


The existing secondary review covers published affect and gaming research plus public player accounts. Cregan and colleagues’ survey of 1,007 gamers associates competitive motives with tilt risk. Getting Over It’s premise also makes single-player progress loss relevant. Barrett and colleagues describe limits to inferring felt emotion from facial movement.

Five fictional personas rehearse different situations: Rohan, Kavya and Aman in Indian contexts; Alex as a challenge-oriented player; Morgan as a player/streamer. They are design exercises, not primary interviews or participant quotations.

[Evidence register](../../../research/04-evidence-register.md) · [Interview guide](../../../research/02-interview-guide.md) · [Simulated answers](../../../research/03-simulated-interviews.md)

## Define

After I lose progress, help me find my next step without leaving the game. Falling does not imply anger, and becoming calmer is not the only successful outcome.

Camera estimates describe visible cues. The player reports pleasantness and activation. Optional input timing and game-window observations provide context, not emotional truth.

## Ideate

A full launcher adds library-management scope. A venue platform adds booking, operations and payments. An automatic emotional coach needs evidence this prototype lacks.

The selected direction is a personal companion: opt into play support, notice a possible fall, wait for the game view to settle, and offer one short suggestion. Encouragement, a next-move reminder and an optional pause are selectable styles. The player can ignore or mute support. The layout plan in the visual story describes this revision; it is not a previously tested wireframe.

## Information architecture

The native destinations are Session, Recap, Saved, Tracking and Settings. Check-ins and support live inside Session. Overlay and phone are connected displays. Processing and storage are separate system layers. The hierarchy in the visual case study is adapted from the supplied Claude-export architecture to the actual prototype; it adds no unimplemented microphone, automatic mood inference or four-game study.

## Prototype

The native PySide6 app uses evergreen actions, sage surfaces and conventional icons. Start play support, I fell, check-in and camera controls remain visible at 1024×768. The open layout gives Nori the main stage. Camera is secondary; play support does not require one.

Nori remains the character. Regen is the app. The 43 authored looks are a check-in vocabulary, not 43 trained camera classes.

Automatic responses use a new possible-fall event followed by two seconds of steady or marked-view observations. Optional input idle can also establish a quiet moment. Repeated fall frames do not restart the waiting period. Events expire after 25 seconds; stale, unavailable or unfocused observations cannot initiate a response. Automatic invitations have a two-minute cooldown. These are engineering defaults to test, not validated optimal timings.

Match my check-in uses an explicit report no older than two minutes. Unpleasant/high-activation reports offer a quiet pause; pleasant reports offer encouragement; otherwise the default is a small next move. The thresholds (pleasantness ±0.2 and activation +0.2) are authored interaction rules. Camera estimates never set either CMA dimension or determine the offer. The player can override the style.

I fell is an explicit manual fallback. While play support runs on Windows, Ctrl+Alt+F8 marks a setback and Ctrl+Alt+F9 mutes/unmutes tips. Registration can fail if another app owns the shortcuts. The overlay does not pause, inject input into or control the game. Borderless/windowed play is the initial target.

A player can optionally record context, choose a pause/continue/smaller goal, report a later moment and rate the choice. The CMA recap relates those reported moments without filling gaps or claiming causation. Reports are secondary to help during play. Saved summaries require local-history consent. Technique cues and notes remain an optional deeper path.

## Brand

Regen draws on the gaming idea of regeneration. Evergreen, sage and mint carry the identity; butter and apricot add energy to the case study. DM Sans, an original R mark, native vector characters and a generated papercraft gaming world form the visual system.

The four supplied Behance pages were inaccessible. Their detailed designs and outcomes were not inspected or copied.

## Technology and tools

Windows application, laptop webcam, MediaPipe face/hand features, HSE eight-class estimates, optional game-window capture and aggregate input timing. The phone displays derived state over paired local HTTP; it does not perform recognition.

Codex assisted implementation and writing. Python, PySide6 and QPainter produce the native UI; Playwright/Chromium and GitHub provide software checks; image generation produced the brand illustration. Existing model weights and updater logic remain unchanged.

## Evidence and next step

124 local tests passed, with four missing-video fixtures and one Windows-only check skipped. Native task and phone/PDF flows passed. The interactive case-study example passed at 1440, 390 and 320px, including CMA choices, feedback and reduced motion. Windows run evidence is linked separately and identified by commit.

These are software checks. Actual play, physical camera/phone compatibility, device overhead and participant benefit remain to evaluate. The next useful test labels actual falls and non-falls, measures missed and false invitations plus response delay, then asks target players whether each suggestion helped their next attempt or interrupted it. Continued enjoyment and a useful next choice matter more than forcing calm.

[Project context](PROJECT-CONTEXT.md) · [Feasibility](FEASIBILITY.md) · [Native checks](verification.json) · [Visual interaction checks](visual-case-verification.json)

[Scenario responses](INTERVIEW-REHEARSALS.md) remain synthetic and have no evidential status as primary interviews.

## Sources

- [Cregan, Toth and Campbell, 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11082399/)
- [Russell, 1980: A circumplex model of affect](https://doi.org/10.1037/h0077714)
- [Barrett and colleagues, 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6640856/)
- [Getting Over It on Steam](https://store.steampowered.com/app/240720/Getting_Over_It_with_Bennett_Foddy/)
- [ASC: lighting in Eternal Sunshine](https://theasc.com/article/forget-me-not-eternal-sunshine-of-the-spotless-mind/)
- [Model and video research](../VIDEO-AND-MODEL-RESEARCH.md)
