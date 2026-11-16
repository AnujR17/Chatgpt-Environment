# Next attempt: a useful job for Checkpoint

Research and implementation: 16 November 2026. Isolated branch: `topic/checkpoint-session-20261116`. No release or OTA publication.

## The player and the job

This prototype serves casual and first-time Getting Over It players who want to continue but are repeating a specific mistake. The job is: **help me change one thing on my next attempt, and remember the adjustment that worked for me.** It is not aimed at professional competition, speedrun coaching, diagnosis, or proving that all frustration should be removed.

The previous build made expression recognition carry too much of the product's value. More expressive artwork did not answer what a player could actually do differently. This change adds an actionable practice loop while preserving the native app, own-face preview, Nori and player-reported CMA.

## What the internet evidence supports

These are secondary sources, not interviews with our users. No synthetic persona answers are treated as primary research.

| Source | What we can take from it | Implementation decision |
| --- | --- | --- |
| [Ballou & Deterding, CHI PLAY 2023: need frustration](https://selfdeterminationtheory.org/wp-content/uploads/2024/01/2023_BallouDeterding_IJustWanted.pdf) | Frustration relates to players' expectations and experiences of competence, autonomy and relatedness. A facial category alone does not identify the cause. | Ask the player which problem needs help; preserve choice and dismissal. |
| [Steam Game Recording](https://help.steampowered.com/en/faqs/view/23B7-49AD-4A28-9590) and [Medal clipping support](https://support.medal.tv/support/solutions/articles/48001157618-how-to-make-clips) | Existing tools already preserve/replay gameplay moments. Product documentation establishes features, not our effectiveness. The Steam page's full text was not available through the research reader; search-indexed official documentation supplied the feature description. | Do not build another continuous recording system as the core benefit. Add the missing player decision and practice lesson instead. |
| [SavingOverIt](https://chriskiehl.github.io/SavingOverIt/) | Community software exists specifically for preserving practice progress. This is evidence of a practice-oriented design pattern, not adoption research. | Support practice without modifying game saves or installing mods. |
| [Getting Over It technique guide](https://progameguides.com/getting-over-it-with-bennett-foddy/how-to-beat-getting-over-it/) | Concrete contact/launch techniques offer more actionable material than generic motivational messages. | Original short cue text for hammer placement and launch; source link available on request. |
| [Community tips](https://steamcommunity.com/sharedfiles/filedetails/?id=2913335491), [Orange Hell discussion](https://steamcommunity.com/app/240720/discussions/0/6761670113853118143/), [chimney route guide](https://avidachievers.com/speedruns/getting-over-it-speedrun-guide/) | Players describe local movement problems and alternative techniques. These are suggestions, not validated universal instructions. | Five selectable problems, one cue at a time, and explicit Helped / Still stuck feedback. Only the selected problem's route help appears. |
| [Developer technical FAQ](https://steamcommunity.com/app/240720/discussions/0/1482109512317197080/) | Mouse setups differ; the developer's experience with trackpad tuning conflicts with blanket community recommendations. | Do not silently change sensitivity, acceleration or accessibility settings. |
| [Russell, 1980: CMA](https://doi.org/10.1037/h0077714) | Pleasantness and activation describe affect; they do not prescribe which intervention works or identify a game error. | Use an explicit check-in to change guidance presentation. Keep facial signals separate. |

## Working interaction

1. Open **Next attempt** on the session screen or tray. Select the section/problem yourself. There is no claim that screen recognition identified it.
2. See one technique cue. A recent unpleasant/high-activation check-in starts with a short cue and hides explanation/extra target copy. An unpleasant/low-activation check-in starts with a smaller practice target. Other or unknown states allow the normal explanation. The player can request explanation or a smaller target regardless of CMA.
3. Choose **Try this cue**. Optionally display it beside the transparent, non-focus-taking Nori overlay for 12 seconds. The paired phone also shows the chosen cue above the character, without receiving gameplay or face images. The app does not pause or control the game; switch back to the game as usual.
4. Return through **Review attempt**. Choose **Helped**, **Still stuck**, or dismiss. A note is optional. Still stuck offers a smaller target for another attempt; it does not silently cycle through unrelated advice.
5. Reuse a note previously marked helpful for that same problem. Notes persist across sessions only with the existing saved-summary consent. The CMA PDF includes chosen cues, player verdicts and lessons; there is no invented improvement score.

The five-minute freshness window and routing thresholds are prototype design choices. They are not scientific cut-offs or validated treatment rules. A selected cue stays stable through an attempt; facial motion cannot cause it to flicker or overwrite the user's choice. Mixed, stale and invalid check-ins stay unspecified. Optional later check-ins can accompany feedback; changes are not attributed to the cue.

## Original brief, made concrete

**Sense:** optional face/game/input observations plus the player's own CMA check-in and selected obstacle. **Infer:** distinguish a recent reported state from unknown; do not infer felt emotion from a mouth shape. **Decide:** propose one cue or smaller target on request. **Respond:** desktop help, optional transient Nori cue and paired phone. **Learn:** store the player's verdict and useful adjustment, with retention consent.

This is an offline, curated prototype, not a newly trained coach. It has no LLM call, new ML dependency, always-on recorder, game injection, or global input interception. The existing experimental face model remains; its recognition limitations have not been solved by this feature.

## What is established and what is not

Policy tests and actual native/browser flows cover recent/stale/unknown CMA, stable cue selection, duplicate prevention, feedback, consent-based recall, PDF output, phone updates and disconnected-state handling. Synthetic check-ins do not establish gamer usefulness, technique accuracy on every setup, reduced frustration, or better facial recognition. Physical Windows webcam/gameplay and phone Wi-Fi need device testing.

A short actual-play evaluation should compare a normal stuck attempt with a requested cue: did the player understand the adjustment, try it, rate it useful, and choose to reuse it? Also record interruptions and unwanted spoilers. A smaller task completed or a voluntary helpful rating is more informative here than expression-classification accuracy alone. No research delay is required to try the working prototype.

## Verification and download

[Windows review run 43825458950](https://github.com/AnujR17/Chatgpt-Environment/actions/runs/43825458950) passed for code commit ee3e54616fe70090f9c219f6a24cecd7afa7c227: compilation, 9 support-policy and 8 attempt-policy tests, actual native practice/feedback/recall/PDF flows, compact viewport checks and existing native tracking/model-load fixtures. The portable preview is attached to that run, with no release publication. Local suite: 111 passed, 5 skipped. Both the new cue flow and existing phone expression-rendering flow pass through native app → loopback HTTP → Chromium; physical phone Wi-Fi is not covered. See [the full verification record](NEXT-ATTEMPT-VERIFICATION.json).

The next test is deliberately small: one real Getting Over It session. Does the player find a cue worth keeping? Can they return to play without losing their place? Do they prefer brief or full guidance at the same CMA state? A negative verdict is recorded as such. This is a proposed validation task, not completed primary research or a prerequisite to trying the build.
