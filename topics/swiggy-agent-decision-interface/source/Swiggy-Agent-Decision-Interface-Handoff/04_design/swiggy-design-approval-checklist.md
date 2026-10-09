---
name: swiggy-design-approval-checklist
description: Checklist of visual-design decisions the project owner must approve before the wireframe and prototype (Stage 8). Each item lists the options, the current recommendation, and what reference to find. Created 2026-10-09.
status: open, waiting on the owner's references
---

# Stage 8: Design approval checklist

**How to use this:** tick an item once you've chosen. Wherever it says **Find**, collect 2–3 screenshots or links and share them with me. I'll check each against the project rules (no verdicts, no scores, never colour alone) before anything is built.

**Already approved:**
- [x] Reference set (Zendesk, Intercom, Gorgias, Salesforce, GitHub status checks, Stripe disputes, Uber Eats; Zomato karma score as the anti-reference)
- [x] Queue rule: only the agent's own pending chats, showing issue type and wait time, sorted by wait time, with no priority score or customer label

---

## A. Frame and theme

- [ ] **A1. Desktop frame size.** Every layout will be shown inside this fixed frame from now on.
  - 1440 × 900 (16:10) · *recommended: a common laptop size that leaves room for 4 columns*
  - 1920 × 1080 (16:9) · a full-HD monitor
  - 1366 × 768 · a budget laptop *(assumption: possibly common in support centres; not verified)*
  - **Find:** whether you know what screens Swiggy agents use (unlikely to be public).

- [ ] **A2. Theme.**
  - **What's proposed now:** the reference board follows your device's light or dark setting, but the visual kit was **designed light-first** (warm neutrals), with dark values defined as a secondary version.
  - Options:
    - Light only
    - Light by default, with a dark mode *(recommended: long shifts and night shifts)*
    - Dark by default
  - **Find:** agent tools you like in each theme.

- [ ] **A3. Density.**
  - Comfortable (more spacing)
  - Compact (more rows on screen) · *recommended for 4 columns at 1440 wide*

## B. Layout (flagged, waiting on your references)

- [ ] **B1. Column order.**
  - Proposed: queue rail → case info → chat (centre) → insights and decision.
  - Alternative: insights on the left and case info on the right.
- [ ] **B2. Column widths at the A1 frame size.**
  - Proposed: queue 150 · case 330 · chat 480 · insights 360, plus gutters.
- [ ] **B3. Linking a condition to its evidence across the chat.**
  - Proposed: selecting a condition highlights its evidence, and the condition card shows a small thumbnail of that evidence.
- [ ] **B4. Where the status strip sits.**
  - Proposed: top of the insights column.
  - Alternative: full-width header across all columns.
- **Find:** support or ops dashboards with 3–4 columns where the chat is in the centre.

## C. Colour tokens

- [ ] **C1. Primary action colour.**
  - Option 1: Swiggy Orange #FF5200 for actions *(recommended)*
  - Option 2: neutral charcoal, with orange in the logo only
- [ ] **C2. Neutrals.**
  - Warm (matches Salt #FFEDE3) *(recommended)*
  - Cool grey
- [ ] **C3. Status colours.** Each always comes with an icon and a word.
  - Met: green
  - Not met: red
  - Unknown: neutral grey, never orange or amber
- [ ] **C4. Insight tint.** A pale cool tint that marks insight lines apart from raw data.
- [ ] **C5. Selection and keyboard-focus colour.**
  - Salt background with an orange edge *(Option 1)*, or an ink edge *(Option 2)*
- [ ] **C6. Review-trigger chip style.**
  - Proposed: neutral outline with source text, so it doesn't look like an alarm.
- **Find:**
  - **Swiggy Partner app** (restaurant) and **Swiggy Delivery Partner app** screenshots (Play Store / App Store). These are the closest public examples of how Swiggy styles *working* tools rather than consumer screens.
  - Also the consumer Swiggy app, for brand feel.

## D. Typography

- [ ] **D1. Typeface.**
  - Gilroy (Swiggy's official font; needs a licence)
  - Stand-ins: Outfit for display, Plus Jakarta Sans for body *(recommended for the coded prototype)*
- [ ] **D2. Font for numbers.**
  - IBM Plex Mono for times, amounts and counts *(recommended)*
  - Same font as the body text, with numbers set to equal width
- [ ] **D3. Type scale.**
  - Proposed: 12 · 13 · 15 · 18 · 22.
  - Body text at 13–15 in Regular or Medium; Light is too thin on screen.
- **Find:** your preference among the stand-ins, or confirm whether you have a Gilroy licence.

## E. Shape, spacing, elevation

- [ ] **E1. Corner radius.**
  - Proposed: rounded corners that echo the brand book's "bento" (about 10–12 px on cards, 8 px on chips and buttons).
- [ ] **E2. Spacing scale.**
  - Proposed: 4-pt base (4 · 8 · 12 · 16 · 24 · 32).
- [ ] **E3. Separating sections.**
  - Borders only *(recommended for dense tools)*
  - Soft shadows
- **Find:** examples of cards you like.

## F. Components (one reference each is enough)

- [ ] F1. Queue item
- [ ] F2. Bot-handover card
- [ ] F3. Chat bubbles and reply box with templates
- [ ] F4. Evidence tile (type, supplied by, origin, times)
- [ ] F5. Party-records row ("3 / 7 orders · 90 days")
- [ ] F6. Restaurant-permission status
- [ ] F7. Status strip (clocks, triggers, permission)
- [ ] F8. Policy-condition card (status chip, fact, source, evidence thumbnail)
- [ ] F9. Similar-cases drawer (cards labelled "Past case, not a recommendation")
- [ ] F10. Decision buttons: Full / Partial / Deny / Review, with equal weight
- [ ] F11. Case log / audit view
- **Find:** anything close for F4, F8 and F10. These three carry the project's core idea.

## G. Icons

- [ ] **G1. Icon set.**
  - Lucide (outline, neutral) *(recommended)*
  - Phosphor
  - Material Symbols
- **Find:** Swiggy app icons, to match their line weight.

## H. Motion and feedback

- [ ] **H1. Minimal motion.**
  - Proposed: a short highlight when a condition is selected, a gentle pulse when a clock nears its limit, and nothing decorative.
  - Respects the "reduce motion" setting.

## I. Accessibility

- [ ] **I1. Contrast target.**
  - WCAG AA (4.5:1 for body text) *(recommended)*
- [ ] **I2. Keyboard shortcuts** for common actions (next chat, link evidence, decide).
- [ ] **I3. Never colour alone.** Icons and words are on every state. *(Locked by project rule.)*

---

## Notes
- **Brand facts used:** Swiggy Brand Book (2026): Orange #FF5200, Salt #FFEDE3, White, Gilroy. The brand book has no product-UI or internal-tool guidance, so every agent-tool token here is **our proposal**, not Swiggy's actual system. See `swiggy-design-system-research.md`.
- **What happens next:** once your references arrive, I'll update the reference board, lock the tokens, and then build the content and layer map plus the wireframe for scenario S2, inside the A1 frame.
