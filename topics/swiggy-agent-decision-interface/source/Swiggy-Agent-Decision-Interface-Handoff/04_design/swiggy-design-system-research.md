---
name: swiggy-design-system-research
description: What Swiggy publishes about its brand and design system, how peers carry consumer brands into internal and support tools, and the resulting visual-kit options for the agent panel (Stage 8). Researched 2026-10-09.
---

# Swiggy design system research (Stage 8)

## What Swiggy publishes [Official]
Source: Swiggy Brand Book (2026), https://www.swiggy.com/corporate/wp-content/uploads/2026/07/swiggy-brandbook.pdf

**Colour**
- Swiggy Orange **#FF5200** (primary)
- White **#FFFFFF** (secondary)
- Salt **#FFEDE3** (supporting)
- Orange tints: #F58B55, #F8AE88, #FAD2BB, #FDF5EE
- Balance: as much orange as possible, then Salt, then White.

**Type**
- **Gilroy**, in ten weights.
- Headline: ExtraBold, with leading at 1.1× size.
- Subhead: Medium. (The Layout section says Regular instead; the two sections conflict.)
- Body: Light, with leading at 1.4× size.
- Sentence case throughout.

**Layout**
- A rounded "bento" container whose corners match the rounded square behind the logo.

**Not covered:** product UI, internal tools, iconography, tone of voice. The only accessibility point is "maintain contrast" for buttons and calls to action.

**Product design system**
- A shared Figma "foundation library that supports all our business lines" exists (Figma customer story).
- Its contents are not public.

**Agent tool (Agent Workbench)**
- No public visuals, consistent with the Stage 4 findings.

**Could not fetch:** master-brand-guidelines.pdf (fetch error).

## Peer patterns: consumer brand → internal tools [Official, from each company's own publications]
- **Uber, Base Web:** built for "hundreds of internal web applications used by developers, product managers, and operations teams". It has a single place to theme all tokens. https://www.uber.com/blog/introducing-base-web
- **DoorDash, Prism:** one design language with themes for Default, Caviar and Merchant. Teams building tools for support agents previously had to build custom UI. https://careersatdoordash.com/blog/design-language-system-theming/
- **Zomato design system:** green for calls to action, red only for deletion and cancellation, 3 greys, 10 colours in total. All examples are consumer-facing. https://uxdesign.cc/developing-the-zomato-design-system-438357188904
- **Shopify admin:** mostly neutral text. Orange means "pending" or "needs attention"; red is only for blocked or error states; never rely on colour alone. https://shopify.dev/docs/apps/design/visual-design

**Synthesis [Inferred]:** internal tools keep the brand's foundations (type, corner radius, spacing) and use neutral surfaces. They limit the brand colour to identity and actions, and give status colours fixed roles that never rely on colour alone.

## Implications for the agent panel [Inferred]
- **Swiggy Orange vs status colours:** orange is commonly read as "pending" or "warning" in operational UIs, so it must never be used for status. Status uses green (met), red (not met) and neutral grey (unknown), each with an icon and a word.
- **Typeface:** Gilroy is a licensed font. The coded prototype uses stand-ins: Outfit (display), Plus Jakarta Sans (body), IBM Plex Mono (numbers).
- **Body weight:** Gilroy Light is too thin for dense screen text, so body text uses Regular or Medium.
- **Kit options presented 2026-10-09:**
  - Option 1 (recommended): orange for identity, the primary action and the current selection; Salt for selected items.
  - Option 2: neutral charcoal actions, with orange in the logo only.

## Layout change requested by owner (2026-10-09)
- Chat moves to the **centre**.
- A **queue rail** is added on the far left, showing the agent's own pending chats.
- Case information sits on the left and insights plus the decision on the right.
- Proposed queue rule: issue type and wait time only, sorted by wait time, with no priority score or customer label.
- Trade-off: a condition (right) and its evidence (left) are split by the chat. Fix: selecting a condition highlights its evidence, and the condition card shows a thumbnail of that evidence.
