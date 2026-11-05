# Distinct emotion gestures — current direction

The user clarified that the library should communicate a feeling through a distinctive composition, rather than require memorising small differences between related contours. This replaces the continuous-contour study as the main UI. The previous study remains on Figma page 08; this revision is on **09 Distinct emotion library**.

## What is represented

There is no fixed total number of emotions in CMA. The current product vocabulary contains eight feeling/experience words, chosen for this prototype: Calm, Frustrated, Bewildered, Confused, Happy, Excited, Sad and Angry. It is not an exhaustive taxonomy. Confusion and bewilderment include cognitive uncertainty and appraisal as well as affect.

| Word | Distinct composition | Main visual material | Motion |
|---|---|---|---|
| Calm | Broad, level wave | One continuous line | Slow, shallow drift |
| Frustrated | Blocked, compressed tangle | One angular path | Small contractions; no shaking or flashing |
| Bewildered | Disrupted, asymmetrical burst and uneven open eyes | Broken lines | Gentle, uneven outward changes |
| Confused | Familiar questioning turn | Curved line and its punctuation dot | Small unresolved hover |
| Happy | Open round silhouette and smile | Soft shape with a familiar expression | Gentle lift |
| Excited | Rounded four-point spark and smile | Expanding shape | A little more lift and expansion |
| Sad | Weighted drop and downturned expression | Drooping shape | Slow downward movement |
| Angry | Compressed angular silhouette and inward brows | Angular shape | Small clench |

The compositions do not all contain lines, shapes and dots. They use familiar visual cues where helpful, and vary in silhouette, density, direction and expression. Labels stay visible. The objective is recognition at a glance, but this has **not yet been established with participants**. In particular, bewilderment may be read as surprise, and calm may be read as quietness. Those are questions to test rather than conceal.

## How CMA remains valid here

The selected word determines the semantic symbol. Separately, the player reports pleasantness and activation through two independent sliders. The main screen presents those dimensions as plain text below the symbol. There is no quadrant or plotted point to interpret.

CMA does not prescribe these shapes or uniquely identify confusion, bewilderment, anger, or any other named emotion. Two experiences can share a CMA position while differing in meaning. A word alone cannot establish a person's coordinates. Current slider starting positions are explicitly **adjustable design suggestions**, not measured emotion norms; saving adopts or adjusts those values as a self-report. This defaulting can introduce anchoring bias and should be tested against an initially unset-slider variant. For confusion and bewilderment especially, either pleasantness or activation can vary with context.

Colour reinforces the selected gesture; it is not a measurement. Facial-expression cues never select the word, either CMA dimension, or a support action. The camera shows the player's own local preview only after an explicit source action.

The basis for continuous valence/activation remains [Russell (1980)](https://doi.org/10.1037/h0077714) and [Posner, Russell & Peterson (2005)](https://pubmed.ncbi.nlm.nih.gov/16262989/). The [Pacheco et al. (2015) study](https://portalrecerca.uab.cat/en/publications/two-dimensional-shapes-for-emotional-interfaces-assessing-the-inf/) concerns affect elicited by geometry/motion; it does not validate decoding these symbols. See EMOTION-MAPPING.md for the earlier dimensional study and source details.

## Primary study to run next — no results claimed

Recruit 12–16 adult players, including players in India and a range of language preferences, motion sensitivity and colour vision. Existing synthetic personas are not research participants. Use voluntary consent; no face recording is required for this symbol study.

1. Show each symbol without its word or colour, in random order. Ask “What does this communicate?” and record the participant's own words before offering choices. Allow “I don't know.”
2. Ask which symbols are easy to confuse. Pay particular attention to frustrated/angry, confused/bewildered, calm/bored and happy/excited. Do not assume that English synonyms distinguish the same way in Hindi, Hinglish or another participant language.
3. Compare static and moving versions. Ask whether movement changes the interpreted feeling or causes distraction/discomfort.
4. Reveal the labels. Ask “Does this fit the word for you? What would you change?”
5. Try actual game check-ins between attempts/rounds. Ask whether the word fits and whether each suggested CMA slider position is right or wrong. Compare suggested versus initially unset sliders.

Report the free-label responses, common confusions, uncertainty and individual differences. Define acceptable synonym groups before scoring. Pre-register any recognition target; software tests and researcher interpretation do not establish recognisability. If players repeatedly cannot separate confusion and bewilderment, merge or revise them instead of requiring memorisation.

## Runtime contract

The native app uses these symbols in its main view and offers the eight-symbol library before the check-in. Selecting a symbol does not commit a report until Save. Cancel preserves the prior native report. Each state has restrained ambient motion; switching symbols uses a 450ms fade with a small settle. Pause and Reduce motion keep the same static semantic composition. Mixed and unreported states stay unassigned. The older CMA contour views remain available only to development/reproduction code, without product view tabs.
