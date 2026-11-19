# Regen website handoff

Standalone website branch: topic/regen-case-study-site, based on the reviewed Regen design. The generated site is in topics/regen-case-study/site; sync.py refreshes it from the original case-study source. Supporting context, research and feasibility are rendered HTML pages.

Vercel project regen-case-study is separate from chatgpt-environment/job search. Preview deployment dpl_D1YXAQLJewxQQD6YxKzPJv8k18Mk is READY at source commit d0cd2ec9e89b8a366f568cba07ba3131c9bbd8dc. DEPLOYMENT.json contains the link and evidence. Existing team sign-in protection is retained; do not disable it for testing. No native OTA or job-search production setting was changed.

Local Chromium interaction checks pass at1440/390/320, including CMA, feedback, themes and reduced motion. Deployed authenticated HTTP checks pass for root, CSS, JS and all three supporting pages. No separately authenticated live-browser session was performed. The case example is authored, not real emotion inference or participant research.

The shell GH_TOKEN is expired in this environment. Publishing succeeded through connected GitHub Git-data tools, reusing existing binary blob SHAs. A local-branch/remote-branch ambiguity in automatic review was resolved with the remote branches API and ls-remote before creation; no existing remote history was rewound. Future commits can use connected GitHub writes with a branch-head lease. Local fetch still works for this public repository without credentials.

Preserve the sage Regen design, concise titles/descriptions and organic game-focused narrative. No classroom framing. Five persona scenarios remain fictional. Keep runtime/models/native app outside the published site.


Current revision merges app review commit 89792b195a9bc4a9219c15928ec4dccc590af43c. Case study now leads with a player learning a difficult game, support after a possible fall, a settled-view delay and player choice. The recap is secondary. Interactive fall/mute demonstration and CMA follow-up demo pass locally at 1440/390/320. New native play-support and recovery fixtures are included. 124 app tests passed, five skipped. Automatic game-event accuracy and player benefit remain unverified; use the new Windows review run for platform evidence. Refresh DEPLOYMENT.json after the new preview is READY.

Windows review run 44270123364 passed at application commit 89792b195a9bc4a9219c15928ec4dccc590af43c, including the new support and recovery scripts and native shortcut dispatch. Current windows-verification.json records the exact tested code commit.

Updated preview dpl_54e4jJo1EWdHwGigrnQRzBsMyeqA is READY at website source f8787f23e3918a77f4c922ce1489c08c43829629. Authenticated deployed root, CSS, JS, all three supporting HTML pages and play-support/recovery/Windows evidence files returned 200. Generated-site browser interaction passed at 1440/390/320 locally. Existing team sign-in protection remains. See DEPLOYMENT.json.

Final follow-up b10788c47ae9925a64be8c46d6bda519cd886a97 preserves automatic mute during one-off manual help. 124 tests and the native support fixture pass after this correction; Windows run 44271249558 passed at b10788c47ae9925a64be8c46d6bda519cd886a97, including manual-help mute preservation and shortcut dispatch.


## 18 November 2026: authorship, research and information architecture

User supplied a 98-page Claude export and requested its architecture adapted to the actual Regen case study. Extracted page 97 structure, retaining source distinctions: do not add the document’s microphone, four-game study, baseline-based mood/CMA inference or learning claims. The map covers Session, Recap, Saved, Tracking and Settings, plus connected overlay/phone and separate processing/data layers. Hero title is AI for behavior design; author Anuj Rai; subject Interaction design; Professor Anupam Rana, with sentence-case labels. Keep the original papercraft artwork, sage palette, DM Sans and game-first narrative.

Four visible research findings have original source links, stated limits and design responses. Five persona cards expose existing synthetic answers, explicitly not primary interviews. New evidence, scenarios and interview-guide HTML pages retain provenance and readable tables. No native app/model/updater change and no OTA. Browser reflow/interactions and visual PDF export are the applicable checks. Source is on the existing website branch; preserve the job-search Vercel project and protection settings. Topic memory lookup returned cached network failure; no retry.

Browser verification passed at 1440/390/320 with hero author/subject/professor, five-destination IA, source-led findings, expandable scenario answers, existing fall/CMA interactions and readable evidence/scenario/interview-guide pages. All generated links resolve locally. Visual PDF refreshed to 15 pages; cover and architecture inspected.


## Presentation refinement

User selected existing research and design personas, then explicitly requested no presentation note. Remove repeated limitation callouts and hypothetical wording from all rendered case-study pages. Use source-linked research, normal design personas, a questionnaire and concrete design decisions. Do not claim the author conducted interviews or attribute generated answers to real participants. Canonical research records in topics/checkpoint/research remain intact. Remove simulated-answer presentation copies and diagnostic JSON exports from the website; keep technical verification in source. This is editorial presentation work, with no native model/app or OTA change.


## Static presentation and native release

User requests full, unfaded artwork; straight actual desktop/phone screen mockups; no case-study navigation, sliders, theme switch, simulated gameplay or other demo controls. Keep native application navigation (explicit clarification). The case study now renders authored character poses once and presents static CMA examples. Public presentation omits the previously rejected research labels/notes; canonical research records remain separate.

Native Regen 0.6.2-preview.1 is published from topic/checkpoint at 092935032b2814cdeb6bc5337c140422f15e8007, with 150-second foreground play reminders and existing setback support. Full ZIP and manifest verified after download; Windows run 44280866344 and 129 local tests passed. Case-study source/screens are synchronised to that UI. Preserve the separate hosting project and the job-search project.


## 19 November 2026: five states and widget controls

The shared presentation vocabulary is Neutral, Happy, Frustrated, Sad and Confused. Existing raw eight-category provider outputs remain internal; no new model training or accuracy claim. Check-in choices and public expression payloads show only five states. Unsupported/missing estimates render flat Neutral. Nori is deliberately clickable (not click-through), keeps the emotion name and a 30px m:ss countdown visible, and offers check-in, 30/60/120-second breaks, manual setback and mute controls. Drag to reposition. Break completion waits for Continue playing; capture stays off. Native navigation stays intact.

134 local tests passed, five skipped. Native session/recovery/play/expression/widget scripts and phone bridge/browser checks passed. The case study is static, has no navbar or demo controls, and uses flat screens with unfaded original artwork. Four source-linked findings, five design personas and an interview guide remain; no conducted interviews are claimed. Large visual PDFs are generated in Windows CI and published as release assets rather than Git blobs.


Publication complete: native review 6684749874b88e1a5cbfd9d72beb0c248736ff2e passed Windows run 44392120784. Release checkpoint-v0.6.3-preview.1 targets topic/checkpoint code commit 18d6edab55bfb377affd246e56b0fc31696bb6b2; Windows release run 44392746679 passed all steps, including updater restart/rollback and case PDF export. Downloaded small update (6,170,072 bytes), verified all 92 file hashes and version/five-state/widget code; 0.6.2 discovers 0.6.3. Downloaded case PDF (3,980,342 bytes). Full ZIP hash is dd0a7aadb7514d36da4f479a8799c5a628e6dbf5ea016aa8feaafbc85b408982. Website UI commit 1de8f8cedb35f850e1a4cb8e9eaf673852385ec1 is READY at deployment dpl_GXFn8Jm4GxTd5jqpaA966Hd9hfFD. Authenticated root, CSS, five-state data and research page returned 200. Stable preview alias points to this deployment. Local branch matches published UI tree. Repository main and job-search production are untouched.


## 19 November 2026: open UI and opt-in break reminders

User rejects boxed/capsule labels and a flat cluster of unrelated actions. Native session now groups check-in, breaks/reminder interval, setback support, header session actions and footer display tools through proximity and whitespace. Secondary surfaces and tabs have reduced rounding; selected source uses an underline. Continue playing appears after a response.

Nori mood/countdown labels have transparent backing with white glyphs and a dark outline. A scalloped thought cloud offers “Let’s take a break?” without activating a window or starting a break. No game pixels are sampled for adaptive text; dense-motion readability remains a physical-device check.

Break reminders are a separate explicit opt-in, initially off. The first prompt arrives 30 seconds after enabling, adjustable with Session presets or Settings (30–3600 seconds). Camera/game observation is unnecessary. Taking a break clears the pending reminder; continuing starts a full interval; end stops prompts. Game observation no longer opts into setback support or break reminders. Five primary states are unchanged.

Local verification: 139 tests passed, five fixture/Windows-dependent checks skipped. Actual Qt session/widget/recovery/play-support review scripts passed, including desktop 1440x900 and compact 1024x768, clicked check-in/break controls, phone-payload propagation, interval changes and transparent glyph rendering. Source case study adds concrete UX decisions and refreshed native screenshots. Windows 0.6.4 release and Vercel preview verification are pending publication at this checkpoint. No physical camera/game testing or user outcome claim.
