> Historical continuous-CMA exploration. The current semantic-library direction is in SEMANTIC-EMOTION-LIBRARY.md; this study is retained as evidence and design history.

# Emotion as a continuous form

CMA describes two continuous dimensions: valence (pleasantness) and arousal (activation). It does not specify a total number of emotions, nor a fixed set of discrete types. Russell's 1980 study used 28 feeling words to investigate this structure; those words are not an exhaustive inventory of human emotion. Four broad combinations of the dimensions are regions, not four emotions. Activation is not a frustration-severity score.

This interface uses **12 reference words** to make check-ins manageable. Two feelings can share similar coordinates while differing in meaning, cause and context. The user's word and two independent sliders remain authoritative. The visual represents the reported dimensions, not a diagnosis or a unique emotion fingerprint. “Mixed / not sure” and “not reported” have no assumed coordinates; neither is silently placed at the neutral origin.

## Reference vocabulary

Coordinates below are adjustable product defaults on [-1, 1]. They are **illustrative design choices**, not measured population norms or exact positions established by Russell. A player can disagree with either default. Sleepiness says little about pleasantness, so its zero default must be adjustable. Existing Engaged and Low reports remain readable for compatibility; Engaged is context dependent.

| Feeling | Meaning in this check-in | Pleasantness | Activation | Proposed composition |
|---|---|---:|---:|---|
| Happy | Pleasant moment with some lift | .85 | .20 | Open, rounded contours; moderate dot travel |
| Excited | Pleasant, highly activated | .65 | .80 | Open contours with larger excursions and faster travel |
| Content | Comfortable with the moment | .75 | -.30 | Rounded contours; restrained motion |
| Calm | Pleasant, little activation | .60 | -.65 | Broad smooth contours; slow drift |
| Relaxed | At ease | .65 | -.55 | Similar to calm; slightly more movement |
| Tense | Activated, with discomfort | -.20 | .90 | More constriction, strong excursions and faster travel |
| Angry | Unpleasant, strongly activated | -.75 | .60 | Constricted, corrugated contours; active dots |
| Afraid | Unpleasant, very activated | -.65 | .85 | Similar to anger, with stronger motion |
| Frustrated | Unpleasant, some activation | -.80 | .30 | Constricted contours; moderate motion |
| Sad | Unpleasant, little activation | -.65 | -.55 | Inward contours; slow travel |
| Bored | Unpleasant, underactivated | -.55 | -.65 | Restrained inward form; little movement |
| Sleepy | Very little activation; valence varies | .00 | -.90 | Intermediate curvature; very slow drift |

## Visual grammar

One parameterised renderer produces all reference forms and all slider values between them. Five fixed-topology contours allow smooth transitions. Pleasantness varies curvature and constriction; an additional muted teal-to-clay colour interpolation reinforces it. Activation varies excursion and tempo, from .07 to .26 cycles/second. Both positive excitement and negative tension can move quickly. Dots travel along the same contours. The Form, Lines and Dots views isolate useful parts of this same visual grammar; they do not change the user's report.

Changes blend continuously over 800ms with a smoothstep easing. Ambient motion runs at a capped 30fps only for a visible, known, active report. Pause motion and Reduce motion preserve the same static composition and text. Hidden views, breaks, ended sessions and unknown states stop their animation timers. No flashing, random particle storms, score, “rage meter” or compulsory intervention is introduced.

## Evidence and its limits

- Russell (1980), *A circumplex model of affect*. Basis for a continuous pleasantness/activation space and overlapping feeling words. [Original paper](https://pdodds.w3.uvm.edu/research/papers/others/1980/russell1980a.pdf), DOI [10.1037/h0077714](https://doi.org/10.1037/h0077714).
- Posner, Russell & Peterson (2005), *The circumplex model of affect*. Supports the dimensional account; it does not validate facial-expression-to-mood inference. [PubMed](https://pubmed.ncbi.nlm.nih.gov/16262989/).
- Pacheco, Le Groux & Verschure (2015), *Two dimensional shapes for emotional interfaces*, ACHI, pp.224–228. Manipulated geometry and movement influenced observers' self-reported affect. This is evidence about **elicited affect**, not proof that viewers can decode our proposed shapes correctly. [University research record](https://portalrecerca.uab.cat/en/publications/two-dimensional-shapes-for-emotional-interfaces-assessing-the-inf/).

The CMA dimensions are supported by research. Our geometry-to-dimension encoding is a **design hypothesis**. It has not been validated with players. It is model-consistent because both dimensions vary independently and retain their text labels, not because a particular outline has scientific authority. Facial cues remain a separate, opt-in research feature and cannot set either dimension or trigger an intervention. No model weights were retrained for this design iteration.

## Next primary study — planned, not conducted

Recruit 12–16 adult PC players, including at least six in India; cover varied gender, languages, colour vision, motion sensitivity and competitive/casual play. Obtain consent; do not claim simulated personas are participants. Counterbalance Form/Lines/Dots and state order. Start with short, neutral instructions rather than teaching emotion-shape pairs.

1. With text hidden, ask “Does this feel more pleasant or unpleasant?” and “More or less activated?” on separate scales. Include high-activation positive and negative pairs and low-activation positive and negative pairs. Measure dimensional ordering, not exact emotion-name guessing.
2. Ask “What made you read it that way?” and “Could this same form mean another feeling?”
3. Show labels; ask participants to describe their current game moment using the word and sliders. Ask what the default got wrong.
4. Compare motion, static, grayscale and reduced-motion versions. Record discomfort, interpretation errors and preference.
5. During voluntary gameplay, ask whether the form distracts, whether a manual check-in is practical between rounds, and whether a break feels supportive or intrusive. Do not interrupt a competitive round automatically.

Proposed gates to agree before recruitment: at least 80% correct high-vs-low activation ordering and 75% pleasant-vs-unpleasant ordering on held-out stimuli; no group consistently reverses an axis; no essential information lost in static/grayscale; resolve any motion discomfort before defaulting to animation. These are proposed product targets, not results or established scientific standards. Report individual responses and uncertainty; this sample cannot support population-wide or demographic fairness claims.
