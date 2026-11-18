# Regen

A gaming companion for your next attempt.

[Open the visual case study](index.html). It includes the product, character, player flow and an interactive CMA example. These are the supporting research and design notes.

## The player problem

Being stuck does not always mean wanting to stop. A player may still enjoy the challenge and need one adjustment, less explanation or a smaller goal.

Regen starts with casual and committed hobby players in Getting Over It. Its intended benefit is agency over the next choice. Better performance, reduced anger and wellbeing remain untested outcomes.

## Empathize

The existing secondary review covers published affect and gaming research plus public player accounts. Cregan and colleagues’ survey of 1,007 gamers associates competitive motives with tilt risk. Getting Over It’s premise also makes single-player progress loss relevant. Barrett and colleagues describe limits to inferring felt emotion from facial movement.

Five fictional personas rehearse different situations: Rohan, Kavya and Aman in Indian contexts; Alex as a challenge-oriented player; Morgan as a player/streamer. They are design exercises, not primary interviews or participant quotations.

[Evidence register](../../../research/04-evidence-register.md) · [Interview guide](../../../research/02-interview-guide.md) · [Simulated answers](../../../research/03-simulated-interviews.md)

## Define

When I keep missing a section but still want the challenge, help me choose one adjustment without taking over my play.

Camera estimates describe visible cues. The player reports pleasantness and activation. Optional input timing and game-window observations provide context, not emotional truth.

## Ideate

A full launcher adds library-management scope. A venue platform adds booking, operations and payments. An automatic emotional coach needs evidence this prototype lacks.

The selected direction is a personal companion: check in, select a problem, try one cue and keep an adjustment the player found useful. The layout plan in the visual story describes this revision; it is not a previously tested wireframe.

## Prototype

The native PySide6 app uses evergreen actions, sage surfaces and conventional icons. Check-in and camera controls remain visible at 1024×768. Camera is secondary; Get a cue is a direct session action.

Nori remains the character. Regen is the app. The 43 authored looks are a check-in vocabulary, not 43 trained camera classes.

A recent unpleasant/high-activation report starts with one brief cue. An unpleasant/low-activation report suggests a smaller target. Other, mixed, missing or stale reports leave the amount of help open. The player can override the suggestion; an in-flight cue stays stable.

Pleasantness −0.18, activation ±0.4 and a 300-second expiry are authored prototype parameters, not CMA-prescribed thresholds.

Helped or Still stuck records the player’s verdict. Optional notes persist only with local-history consent. The frameless overlay and paired phone can show the chosen cue. The recap shows explicit CMA samples and player-rated usefulness.

## Brand

Regen draws on the gaming idea of regeneration. Evergreen, sage and mint carry the identity; butter and apricot add energy to the case study. DM Sans, an original R mark, native vector characters and a generated papercraft gaming world form the visual system.

The four supplied Behance pages were inaccessible. Their detailed designs and outcomes were not inspected or copied.

## Technology and tools

Windows application, laptop webcam, MediaPipe face/hand features, HSE eight-class estimates, optional game-window capture and aggregate input timing. The phone displays derived state over paired local HTTP; it does not perform recognition.

Codex assisted implementation and writing. Python, PySide6 and QPainter produce the native UI; Playwright/Chromium and GitHub provide software checks; image generation produced the brand illustration. Existing model weights and updater logic remain unchanged.

## Evidence and next step

113 local tests passed, with four missing-video fixtures and one Windows-only check skipped. Native task and phone/PDF flows passed. The interactive case-study example passed at 1440, 390 and 320px, including CMA choices, feedback and reduced motion. Windows run evidence is linked separately and identified by commit.

These are software checks. Actual play, physical camera/phone compatibility, device overhead and participant benefit remain to evaluate. The next useful test asks whether a cue earns the time spent opening the app.

[Project context](PROJECT-CONTEXT.md) · [Feasibility](FEASIBILITY.md) · [Native checks](verification.json) · [Visual interaction checks](visual-case-verification.json)

## Sources

- [Cregan, Toth and Campbell, 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11082399/)
- [Russell, 1980: A circumplex model of affect](https://doi.org/10.1037/h0077714)
- [Barrett and colleagues, 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6640856/)
- [Getting Over It on Steam](https://store.steampowered.com/app/240720/Getting_Over_It_with_Bennett_Foddy/)
- [Model and video research](../VIDEO-AND-MODEL-RESEARCH.md)
