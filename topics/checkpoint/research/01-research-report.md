# Gaming frustration: research and design directions

Interaction design module · Rapid secondary research · 2 November 2026

## 1. What this research supports

The strongest project framing is: **help players recognise when challenge has stopped being enjoyable and choose an appropriate response at an appropriate moment.**

Computer vision can help identify visible game events. Camera and audio analysis can provide additional observations. Neither provides direct access to what a player feels or why. CMA supplies a language for describing valence and arousal; it is not an emotion detector or an explanation of the cause.

The product should therefore combine game context, optional player signals, player goals and player correction. It should distinguish technical difficulty, unwanted social behaviour, chosen challenge and an unsatisfying session before deciding what support to offer.

This pack contains secondary research, five provisional personas, an interview guide, synthetic interview rehearsals and proposed directions. **No participants have been recruited, contacted or interviewed. There are no new primary-research findings.**

## 2. Method and evidence boundaries

This was a purposive rapid review, not an exhaustive systematic review. Searches covered academic work on tilt, competence, frustration, emotion inference, interventions and Twitch performance; public Indian gaming discussions; a game-specific community; original game descriptions; and browser/model/publisher documentation.

The retained evidence includes seven research publications or publisher summaries, six opened Reddit discussion threads, game and platform documentation, and a public streamer website. Academic access varied: the 2024 tilt study was available in full; several other papers were assessed through abstracts or publisher summaries. The evidence register records those distinctions.

Indian examples were selected because their authors explicitly described Indian servers, language experiences or their own Indian educational context. Membership in an Indian subreddit alone is not proof of nationality. These are unverified personal accounts, useful for identifying questions and needs, not estimating prevalence.

Direct Twitch pages provided no readable conversational content in the available browser. Day[9]'s own website lists material about losing and toxicity, and published Twitch interview research provides substantive evidence about streaming. No Twitch video was watched or transcribed for this pack. Streamer facial expressions, emotional state and intentions have not been coded from clips.

Four evidence labels apply throughout:

| Label | Meaning |
| --- | --- |
| Published finding | A result reported by cited researchers; its study limitations still apply |
| Public account | What a public poster reports; independently unverified and not representative |
| Design hypothesis | Our interpretation or predicted need, requiring research |
| Proposal | A possible feature, study procedure or implementation, not a validated outcome |

The five personas are evidence-informed composites. Names, product preferences, anticipated behaviours and interview responses are invented for design exploration. They are not biographies of the linked authors or statements made by those authors. No photos, exact ages, salaries or invented diagnoses are attached to them.

## 3. What gaming rage, frustration and tilt mean here

For this project, use the following working distinctions, recognising that players and researchers use the terms differently:

- Frustration: an obstacle interferes with something the player wants to accomplish.
- Rage: an intense angry response, potentially expressed verbally or physically.
- Tilt: negative affect begins to interfere with decisions or performance, potentially creating further mistakes.
- Toxicity: harmful conduct towards others. Frustration and toxicity can coexist, but neither proves the other.
- Productive struggle: difficulty the player still chooses and values.

The 2025 qualitative tilt paper describes negative emotions, impaired cognition, behaviour and poorer performance as connected dimensions. Its abstract supports treating tilt as more than a facial expression. It does not validate a detector for our prototype. [A04](https://pubmed.ncbi.nlm.nih.gov/40279257/)

### Does rage happen only in online games?

No. Getting Over It explicitly describes repeated loss of progress as part of its design. A game-community account describes getting stuck, seeking advice and later falling back to the beginning. This establishes that frustrating setbacks exist in single-player play; it does not estimate how frequently players rage. [G01](https://store.steampowered.com/app/240720/Getting_Over_It_with_Bennett_Foddy/), [C05](https://www.reddit.com/r/GettingOverItGame/comments/1jbg8un/)

Online competition adds plausible aggravating conditions: other people's decisions affect the outcome; criticism can be public; team communication can become abusive; rank makes losses consequential; and leaving may harm teammates or incur penalties. A 1,007-player survey found competitive motives associated with greater reported tilt risk. This is an association, not proof that competition causes tilt or that all online players rage. [A02](https://pmc.ncbi.nlm.nih.gov/articles/PMC11082399/)

Viral rage clips cannot tell us whether online games produce more rage than offline games. They are selected for attention, and broadcast behaviour can be performative. A comparative prevalence claim would require matched data across game types and players.

## 4. Why frustration can escalate

| Mechanism | Supporting evidence or status | What to investigate | Candidate response |
| --- | --- | --- | --- |
| Competence is blocked | Seven studies reported that competence-impeding play increased aggression-related outcomes; findings concerned measured outcomes, not a diagnosis of gamers. A01 | Is the player learning or repeating an incomprehensible failure? | Optional explanation or practice support |
| Progress feels erased | Getting Over It's own description makes repeated progress loss explicit. G01 | Was the setback meaningful, expected and still acceptable? | Offer support after recovery, without altering the challenge |
| The activity no longer meets the player's goal | A puzzle-game study with 27 participants connected need satisfaction/frustration with enjoyment and persistence. A03 | Is today's goal improvement, relaxation or social connection? | Tailor choices to that goal |
| Negative emotion affects subsequent play | Qualitative tilt research describes connected emotional, cognitive and behavioural changes. A04 | Does the player recognise rushing, blame or disengagement? | A player-chosen reset at a suitable moment |
| Other players attack or exclude someone | Indian public accounts describe personal abuse, misogyny and language exclusion. C01–C03 | Is support needed against harassment rather than against difficult gameplay? | Help locate mute/report controls; preserve the person's agency |
| The player's circumstances leave little room for play | An Indian college student describes exhaustion, scheduling pressure and gaming feeling obligatory. C04 | Is the session itself wanted? | Support shorter sessions or a satisfying stopping point |
| Performance for an audience complicates observation | Interview research describes emotional labour among women Twitch streamers. A07 | Is the outward reaction performance, distress, both, or unclear? | Private, optional support; ask rather than diagnose |
| Network or frame-rate problems obstruct control | A commenter in an Indian-server discussion reports packet loss when changing servers. C03 | Is there a visible technical problem? | Distinguish troubleshooting from emotion support |

Sources: [A01](https://pubmed.ncbi.nlm.nih.gov/24377357/), [A03](https://journals.sagepub.com/doi/10.1177/15554120211056126), [A04](https://pubmed.ncbi.nlm.nih.gov/40279257/), [A07](https://dl.digra.org/index.php/dl/article/view/1339), [C01](https://www.reddit.com/r/IndianGaming/comments/1f59o4d/), [C02](https://www.reddit.com/r/TwoXIndia/comments/1fgm95e/), [C03](https://www.reddit.com/r/IndianGaming/comments/1lyo1ax/), [C04](https://www.reddit.com/r/IndianGaming/comments/1n9lsf2/).

These are candidate mechanisms, not a formula predicting rage. Losing does not necessarily produce frustration; frustration does not necessarily produce aggression. The same player may enjoy an identical setback on one day and dislike it on another.

### A working escalation sequence to test

The proposed sequence is: the player arrives with a goal and existing state; an obstacle occurs; the player interprets it as manageable, unfair or threatening; attention and decisions may change; subsequent setbacks may reinforce the interpretation; the player continues, disengages, seeks help or stops.

Research should look for counterexamples: a player laughs after a large fall, quietly stops after a win, or feels better after losing a close match. A design that only searches for escalating anger will miss these cases.

## 5. How the proposed games differ

Game mechanics below are sourced descriptions. Expected feelings and intervention opportunities are hypotheses, not fixed CMA assignments.

| Game/context | Relevant mechanics | Frustration hypothesis | What context recognition could look for | Research caution |
| --- | --- | --- | --- | --- |
| Getting Over It | Mouse-controlled climbing with repeated potential progress loss. G01 | A large fall can threaten mastery or waste perceived effort | Relative fall, familiar landmark return, pause/restart | A fall can still be amusing or motivating; do not automatically reduce difficulty |
| Unfair Mario | The inspected site describes hidden traps and reaching a flag. G02 | Unexpected traps can violate expectations; repeating a known trap may feel different | Death/retry/level transition in the exact selected build | Browser versions vary; original authorship and build equivalence were not established |
| Purble Place | Microsoft Press describes cake assembly, matching pairs and feature deduction. G03 | Confusion or repeated mismatch may create mild or substantial frustration | Wrong answer, completion, retry in a specific minigame | Nostalgia and a child-friendly appearance do not make it a validated calming baseline |
| Little Alchemy 2 | Combination discovery with official hint support. G04 | Discovery may feel relaxed; being stuck may become tedious | Repeated combinations, new discovery, hint request | It is a candidate comparison task, not guaranteed positive affect |
| VALORANT | Competitive team context, with documented communication controls and AFK consequences. G05–G06 | Social blame, rank pressure and communication problems may combine | Results screen, round transition and visible technical indicators | Being dead does not necessarily mean being free to disengage; start with post-match support |

Sources: [G01](https://store.steampowered.com/app/240720/Getting_Over_It_with_Bennett_Foddy/), [G02](https://www.unfair-mario.com/), [G03](https://www.oreilly.com/library/view/windows-vistatm-plain/9780735622685/ch06s07.html), [G04](https://hints.littlealchemy2.com/), [G05](https://playvalorant.com/en-us/news/game-updates/valorant-patch-notes-4-11/), [G06](https://playvalorant.com/en-us/news/dev/valorant-behavior-detection-and-penalty-updates/).

If the final project promises to support online toxicity, a study using only offline puzzle and climbing games will leave that promise untested. If the final project focuses on productive versus unwanted struggle, Getting Over It and a contrasting game may provide a more coherent scope than four unrelated games.

## 6. What computer vision would actually do

Separate four technical questions. Each needs its own evidence and evaluation.

### 6.1 Recognise visible game context

Prefer supported game events or an instrumented game when available. Use screen vision where those events are unavailable. A browser can ask the user to share a chosen window through getDisplayMedia, subject to browser and operating-system support. This gives pixels, not game memory, global key presses or reliable knowledge of intent. [T02](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getDisplayMedia)

For one chosen game, the proposed pipeline is:

1. Capture only the selected game surface after explicit permission.
2. Define a small event vocabulary: playing, setback, retry, menu, results and unknown.
3. Annotate example footage for these events. Keep annotations separate from emotional labels.
4. Evaluate simple OCR, template matching or a trained classifier against those annotations. A large general vision model is not automatically necessary.
5. Combine detections over time so a single frame does not trigger a conclusion.
6. Return unknown when the game is unsupported, an overlay obscures the scene or the evidence is ambiguous.

For Getting Over It, camera motion means screen height alone is not a dependable progress measure. Landmark recognition or another game-specific method would need evaluation. For a competitive game, restrict recognition to support timing and visible context; do not extract hidden opponents, offer tactical instructions or automate actions.

### 6.2 Observe the player

MediaPipe Face Landmarker provides landmarks and 52 blendshape coefficients describing facial movement. It does not directly output a validated gaming-frustration score. A separate mapping would need suitable labelled data and testing. [T01](https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker)

Audio could supply changes in vocal activity, volume or pitch. Speaker attribution, room noise and game sound create additional uncertainty. Starting without transcription reduces data collection and avoids pretending an untested language model understands Hindi, Hinglish, Tamil and other code-switched gaming speech equally well.

Mouse/keyboard rhythm can be collected within an instrumented page or supported integration. An ordinary browser page cannot read desktop-game inputs, and merely embedding another site's game does not grant access to its input events. A normal mouse also does not supply meaningful click force. [T03](https://developer.mozilla.org/en-US/docs/Web/API/PointerEvent/pressure), [T04](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy)

### 6.3 Estimate affect and retain uncertainty

A major research review cautions that facial movement does not provide a reliable, specific emotional diagnosis across people and situations. This supports an optional-camera design and a player-correctable estimate. [A06](https://www.psychologicalscience.org/publications/emotional-expressions-reconsidered-challenges-to-inferring-emotion-from-human-facial-movements.html)

Proposed inputs are the current game event, deviation from ordinary play, optional camera/audio observations, the player's session goal and nearby self-reports. A brief resting baseline cannot establish the person's normal gameplay behaviour. Build a tentative baseline during ordinary play, while making clear that this is not enough to train a robust personal emotion model.

A research model could predict valence and arousal from labelled windows. A rule prototype could instead flag a pattern for review. Call it a rule prototype if that is what it is. Do not display invented accuracy percentages or treat a model confidence value as the probability that a person is angry.

### 6.4 Decide whether help would be useful now

CMA needs at least three contextual companions: the player's goal, their interpretation of the problem and an acceptable moment to respond.

| Estimated state | Additional question | Proposed behaviour |
| --- | --- | --- |
| Pleasant, activated | Still enjoying the challenge? | Stay quiet |
| Unpleasant, activated | Technical issue, harassment or unwanted struggle? | Offer a relevant choice at a suitable moment |
| Unpleasant, low activation | Tired, disappointed, bored, or something else? | Ask briefly; offer stopping or changing activity without labelling |
| Pleasant, low activation | Would any intervention improve this? | Usually stay quiet |
| Unknown or conflicting signals | Is there enough evidence to interrupt? | Remain quiet or use a player-requested check-in |

Example: recognising a fall only establishes a setback. A later player check-in might establish whether that setback felt enjoyable, frustrating, embarrassing or irrelevant. An intervention could then offer Keep trying, Optional help, or Take a break. The player chooses.

There is no evidence here for a universal 20-second frustration threshold, a mandatory two-minute baseline or a fixed three-loss rule. Those are configurable study proposals to evaluate, not scientific constants.

### Browser prototype and production constraints

A hosted browser prototype could combine screen sharing, optional camera/audio and a private companion panel. It cannot guarantee an always-on-top overlay in an unrelated desktop game, automatically pause that game, enforce a cooldown in another client or capture all inputs. Some fullscreen modes and protected surfaces may not capture reliably. Test the actual laptop/browser/game combination.

Riot's published policy specifically restricts real-time overlays that immediately alter play to improve performance. Its general policy also calls for product registration and supported data sources. Screen analysis does not establish permission to ship an integration. Use recorded footage or a controlled study while checking the intended production design; do not assume a wellbeing label exempts it. [T05](https://developer.riotgames.com/docs/valorant), [T06](https://developer.riotgames.com/policies/general)

## 7. Five provisional personas

**All five names are fictional. These are design composites built from the public evidence below. Preferences and anticipated behaviour are hypotheses. They have not been interviewed.** The first three are situated in India. The last two have no assigned nationality because the evidence does not support one.

### P1. Rohan: the competitive solo-queue player · India

**Evidence anchor:** A Mumbai-server ranked player describes a loss but explicitly identifies personal abuse, rather than the lost match, as the disturbing experience. Replies discuss how playing with trusted friends changes the experience. [C01](https://www.reddit.com/r/IndianGaming/comments/1f59o4d/)

**Proposed profile:** Plays ranked team games to improve and enjoy competition. Solo queue creates uncertainty about communication and cooperation. This is a segment to recruit, not the source author's reconstructed life.

**Goal:** Finish a session feeling that effort produced learning, even after a loss.

**Possible triggers:** Personal blame, feeling unable to influence the outcome, and immediately pursuing another win after a disappointing match. The last behaviour is a hypothesis, not reported by the linked poster.

**Possible response:** Faster requeueing or sharper communication; neither is a reliable individual marker until observed.

**Design hypothesis:** A post-match choice may be more acceptable than a mid-round interruption. Frame recovery around the player's intention rather than telling them to calm down.

**Potential failure:** The system calls a competitive reaction unhealthy or treats harassment as the target's emotional problem.

**Recruitment probe:** Find a recent ranked player willing to describe both an enjoyable loss and a session they regretted continuing.

### P2. Kavya: the multilingual competitor facing exclusion · India

**Evidence anchor:** A woman on a Mumbai server reports misogynistic abuse and hostility when asking for English communication because she does not speak Hindi. A separate Indian-server account describes abuse after identifying as Tamil-speaking. [C02](https://www.reddit.com/r/TwoXIndia/comments/1fgm95e/), [C03](https://www.reddit.com/r/IndianGaming/comments/1lyo1ax/)

**Proposed profile:** Enjoys competition and wants usable team communication. Being heard can create unwanted attention. The design must support multilingual contexts without assuming Hindi is every Indian player's preferred language.

**Goal:** Keep participating without choosing between silence and abuse.

**Possible triggers:** Gendered comments, language exclusion, being targeted after a mistake, or having to negotiate boundaries while playing.

**Possible response:** Speaking less or withdrawing, as well as anger. Quietness cannot be assumed to mean comfort.

**Design hypothesis:** Fast access to existing communication controls and private follow-up may be useful. Acceptability of any camera or speech analysis remains unknown.

**Potential failure:** A breathing prompt implies the person should adapt to harassment. Automatically muting all teammates also removes useful calls and agency.

**Recruitment probe:** Ask about a specific recent incident without requiring the participant to repeat slurs or revisit material they do not wish to discuss.

### P3. Aman: the time-constrained college gamer · India

**Evidence anchor:** A B.Tech student describes long classes, assignments, exhaustion, having recently obtained a better laptop, and gaming beginning to feel like another obligation. [C04](https://www.reddit.com/r/IndianGaming/comments/1n9lsf2/)

**Proposed profile:** Values gaming but has limited energy and time. This represents an important contrast to the assumption that every dissatisfied gamer is shouting or chasing rank.

**Goal:** Enjoy available leisure without turning game completion into another task.

**Possible triggers:** Slow progress relative to available time, pressure to finish a long game, or an intervention consuming the short session itself.

**Possible response:** Short sessions, indecision, disengagement or quiet disappointment; none should be automatically labelled a clinical condition.

**Design hypothesis:** An optional session intention and a player-defined stopping point may be more useful than continuous mood monitoring.

**Potential failure:** Adding badges, streaks or demanding check-ins makes leisure feel like work. Camera setup adds friction without a demonstrated benefit.

**Recruitment probe:** Include someone who has an unsatisfying session without experiencing overt rage.

### P4. Alex: the mastery-oriented challenge player · Location unspecified

**Evidence anchor:** One Getting Over It player asks for help with controls and later reports progress and a major fall. Another describes eventual completion after repeated attempts, community support and finding an approach that suited them. The first account is mobile, so transfer to a laptop study must be tested. [C05](https://www.reddit.com/r/GettingOverItGame/comments/1jbg8un/), [C06](https://www.reddit.com/r/GettingOverItGame/comments/1si3110/i_beat_the_game/)

**Proposed profile:** Chooses difficult games for mastery and values completing the challenge on their own terms.

**Goal:** Improve while preserving ownership of the achievement.

**Possible triggers:** Unclear mechanics, a large progress loss, intrusive advice or unwanted spoilers.

**Possible response:** Repetition can mean deliberate practice rather than deteriorating self-control.

**Design hypothesis:** Ask whether the challenge is still wanted. Offer opt-in technique help or a reset without changing game difficulty or disclosing a solution automatically.

**Potential failure:** Treating repeated attempts as proof of rage; congratulating endurance when the player actually wants to stop.

**Recruitment probe:** Ask for two similar setbacks that felt different and explore why.

### P5. Morgan: the player who also performs for an audience · Location unspecified

**Evidence anchor:** Guajardo's interviews with eight women Twitch streamers describe emotional labour alongside gameplay. Day[9]'s own site lists content on coping with losing and toxicity; its listing establishes the topics, not specific advice or private feelings. [A07](https://dl.digra.org/index.php/dl/article/view/1339), [M01](https://day9.tv/)

**Proposed profile:** Streams gameplay and manages an audience. This composite does not impersonate Day[9] or any research participant. Audience-size, income and emotional behaviour are deliberately unspecified.

**Goal:** Remain in control of both the gaming experience and what the audience sees.

**Possible triggers:** Audience criticism, backseating, pressure to remain entertaining or a genuine setback occurring during a performance.

**Possible response:** Visible excitement or anger may be performed, felt, or both. This is a problem for inference, not proof that a particular streamer is acting.

**Design hypothesis:** Any emotional summary should be private by default, with an explicit audience/performance context and a manual check-in. Shared-PC and screen-capture behaviour need verification.

**Potential failure:** Broadcasting a mood label creates embarrassment or a new target for chat. Assuming a loud response means distress also disrupts the content the player chose to create.

**Recruitment probe:** Interview a consenting adult streamer about how they distinguish performance from a moment when they actually want support.

## 8. Evidence-led insights and hypotheses

Synthetic interviews are not used as corroborating evidence in this table. They identify assumptions to test.

| Insight or hypothesis | Evidence trail | Design implication | What would challenge it? |
| --- | --- | --- | --- |
| Session goals change what useful support means | A03, C04; goal selection itself is a proposal | Ask whether today's priority is relaxing, improving, socialising or something else | Participants find goal selection burdensome or their goals change frequently |
| A game event does not determine affect | G01, C05, C06, A06 | Keep event labels separate from CMA estimates | Event-only predictions outperform the proposed combination on held-out users; still do not claim direct mind-reading |
| Personal abuse needs a social response | C01–C03 | Offer player-controlled communication/reporting support | Participants prefer a different response; do not reinterpret abuse as their fault |
| Interruption can become another obstacle | G05–G06 and the player-control principle; acceptability untested | Prefer post-match or player-requested support for competition | Observed players prefer a different specific, demonstrably suitable moment |
| Quiet dissatisfaction matters | C04, A04 | Include disengagement and an easy end-session choice | Players say quiet play is normal and the system is overreaching |
| Optional sensing is essential to test | A06, T01 | Compare a minimal-data version with added sensing | Added signals provide a demonstrated benefit acceptable to the participant |
| Public reactions can be misleading | A07 | Treat streaming as a separate context; keep support private | A study finds a reliable alternative indicator, subject to participant validation |
| A universal intervention is poorly justified | A05 identifies varied interventions and evaluation gaps | Evaluate timing, wording and action independently | A simpler option performs as well while creating less burden |

The intervention review identifies 36 systems and a shortage of empirical evaluations. It supports treating our ideas as candidates for testing, not claiming that a particular break length, breathing exercise or AI prompt is proven to solve gaming rage. [A05](https://research-portal.uu.nl/en/publications/how-to-tame-a-toxic-player-a-systematic-literature-review-on-inte/)

## 9. Five possible solution directions

### D1. Post-match recovery and requeue reflection

For competitive players such as P1. Before play, a player may voluntarily choose a reminder condition. At a verified match end, show a private, brief check-in and choices such as Continue, Short reset, or Finish for today. A timer stays in the companion tool; it does not block another game's queue.

**CMA role:** Compare a player-reported change in valence/arousal with whether the next session is still wanted.

**CV role:** Recognise a supported results screen. The MVP can test manual match-end marking first.

**Useful outcome:** The player feels more in control of the decision and does not report additional annoyance. A higher win rate is not a required success measure.

**Trade-off:** Potentially relevant to competition, but real integrations need publisher review. The concept must still function when the player dismisses it.

### D2. Help against unwanted communication

For players such as P2. Let the player quickly access instructions for existing mute/report controls and select what support they want. The tool should not accuse someone of toxicity based only on volume or automatically submit reports.

**CMA role:** Player-reported distress can prompt a choice, while the cause is recorded separately.

**CV role:** Optional identification of a post-match screen; automatic harassment recognition is a separate, substantially harder research problem.

**Useful outcome:** The player can find an appropriate control quickly without losing wanted communication or being blamed for the incident.

**Trade-off:** Clear social relevance, but this cannot replace platform moderation. Speech classification in multilingual and code-switched settings needs evidence we do not yet have.

### D3. Support during chosen single-player challenge

For P4. Recognise a substantial setback in one selected game. At a suitable moment, offer Keep trying, Optional help, or Take a break. Keep tips hidden until requested. A player may switch all prompts off.

**CMA role:** Separate unpleasant-but-wanted struggle from unwanted distress through a direct player correction.

**CV role:** Game-specific setback recognition; evaluate it against annotated footage.

**Useful outcome:** Fewer unwanted interruptions and appropriate player-chosen help. Count an enjoyable repeated attempt as a valid outcome.

**Trade-off:** Strong fit with the current game choices and a controlled laptop study. Generalisation to team harassment would remain untested.

### D4. Support for limited leisure time

For P3. An optional session intention and time budget lead to a reminder at a player-defined stopping point. The tool can suggest ending or changing activity without rewarding longer play.

**CMA role:** Lightweight before/after ratings test whether the session met its intention.

**CV role:** Recognise a menu or completion screen if useful; it may prove unnecessary.

**Useful outcome:** Less reported pressure and a more satisfying choice about continuing.

**Trade-off:** Technically simpler. It tests whether emotion AI is needed at all, which is a legitimate design finding.

### D5. Private support for streamers

For P5. Offer a private check-in on an explicitly chosen surface, with an optional break cue and participant control over what is visible to viewers.

**CMA role:** A private reflection aid, not a public mood score.

**CV role:** Contextualise gameplay, with outward expressions treated cautiously.

**Useful outcome:** The player can request support without unwanted disclosure.

**Trade-off:** Interesting inference challenge, but adds audience, broadcasting and privacy requirements to an already demanding module project.

### Comparison for deciding the next step

This is a qualitative design judgement, not user-tested scoring.

| Direction | Fit with present game study | Potential value | Main dependency |
| --- | --- | --- | --- |
| D1 Post-match recovery | Requires a competitive context or recorded match scenario | Support deliberate continuation | Real player acceptance and publisher compatibility |
| D2 Communication support | Requires multiplayer research | Participation and control during harassment | Useful control access, language coverage and moderation boundaries |
| D3 Chosen challenge support | Strong fit with Getting Over It/Unfair Mario | Preserve challenge while supporting recovery | Reliable event recognition and evidence of acceptable timing |
| D4 Limited leisure | Fits varied games | Reduce obligation and friction | Whether participants actually want session planning |
| D5 Private streamer support | Fits streaming rather than ordinary laptop play | Protect control over public presentation | Access to creators and validated private UI behaviour |

**Provisional recommendation:** If the goal is a coherent module prototype using the present games, D3 is the most direct starting point. If online rage is the priority, D1 is a clearer first scope than a universal live emotion detector. D2 deserves separate investigation if participation and harassment are the main social cause. This recommendation does not select a direction for the user.

## 10. What real primary research should resolve

Recruit five consenting adult participants corresponding to the five behavioural contexts, including three in India. Use the same core interview questions but let their answers contradict the personas. Five participants are suitable for an exploratory qualitative pilot, not population statistics or a validated affect-recognition model.

Ask about recent incidents before showing the concept. Include an enjoyable difficult moment, an unsatisfying session without shouting, a technical problem and a social problem. Do not deliberately provoke harassment or demand that a person become angry.

The separate interview guide supplies screeners, twelve core questions, probes, a session protocol, observation fields and analysis instructions. The synthetic interview file supplies predicted answers only to rehearse that guide. Replace those predictions with real notes rather than treating agreement with the predictions as success.

Evaluate three questions independently:

1. Can the prototype recognise its chosen visible events?
2. Do its affect estimates agree reasonably with nearby player reports, with honest uncertainty?
3. Does an offered response improve perceived control or helpfulness without harming enjoyment or increasing interruptions?

If camera/audio sensing adds little over game context and a brief check-in, remove it. If prompts are not helpful, keep player-requested support or change the intervention. The project should be allowed to discover that less automation is better for this task.

## 11. Status at handoff

Completed: rapid secondary review, source-linked provisional personas, research questions, twelve-question interview guide, synthetic rehearsal answers, candidate directions and implementation constraints.

Not completed: participant recruitment, interviews, observations, model training, event-detection benchmarks, prototype testing or outcome validation.

Next decision: choose a direction and a specific game/context; then recruit the five real participants and revise the personas from their evidence. The attached blank data sheets contain no invented participant responses.
