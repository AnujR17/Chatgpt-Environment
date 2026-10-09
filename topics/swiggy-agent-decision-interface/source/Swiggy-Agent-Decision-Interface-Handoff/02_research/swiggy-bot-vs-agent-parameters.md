---
name: swiggy-bot-vs-agent-parameters
description: Splits the 12 refund/blocking parameters (from swiggy-refund-and-blocking-rules-research.md) into what the Help-chat bot uses vs what the human agent sees vs backend-only signals. Inferred classification — read the source doc's Section 4-6 for the underlying evidence. Open question partially resolved 2026-09-29 — see swiggy-secondary-research-crossverification.md.
sources: cowork
---

# Bot vs Agent vs Backend: refund-decision parameters

Companion to `swiggy-refund-and-blocking-rules-research.md`. That doc lists 12 parameters without saying which team sees which one. This doc reconstructs that split from Section 5 (how the decision flows in practice) and flags it as [Inferred] throughout — Swiggy has not published this architecture.

Rendered version with diagram and matrix: https://claude.ai/artifact/VsbFr3LVezLp2BmG7wbjm7

## Handoff sequence [Reported + Official]
1. Customer opens Help chat, picks issue + order -> **Bot** reads issue type, order vertical, payment mode, order stage/timing.
2. Bot offers a coupon or ~20-30% refund. [Anecdotal]
3. Customer taps "talk to an agent" -> full chat history hands off. [Official, engineering blog]
4. **Agent** additionally sees: customer profile, refund total in last 3 months. [Reported]
5. After 2-3 repeat cases, agent escalates to email. [Reported]
6. **Email / Trust & Safety team** does pattern review -> possible "fraud user" flag, restriction. [Reported]

## Bot-layer parameters
- Issue type (customer-selected) — [Official]
- Order vertical: food / Instamart / alcohol / Genie — [Official]
- Payment mode: prepaid vs COD — [Official]
- Order stage/timing vs. policy cutoff — [Official], automation not confirmed
- Merchant permission required before resolution — [Official]
- Evidence request (photo upload) — [Official] for Instamart, [Anecdotal] for food
- Default offer: partial refund or coupon — [Anecdotal]

## Agent-layer parameters (adds to the above on handoff)
- Fault attribution (customer/restaurant/partner/Swiggy) — [Official]
- Refund amount, last 3 months — [Reported]
- Complaint frequency across orders — [Reported]
- Evidence review — [Anecdotal]
- Merchant/delivery-partner permission status — [Official]

## Backend-only (not shown live to bot or agent)
- Customer value tier (high/medium/low) — [Reported]
- "Fraud user" flag — [Reported], set by email team after pattern review
- Device signals (SHIELD fingerprinting) — [Reported], aimed at promo abuse, link to refunds unconfirmed

## Design flag, carried from the research doc
Value tier and fraud flag are customer-intent scores, not checkable facts — surfacing either breaks the project's no-prediction rule. Device-signal data isn't confirmed to touch refunds at all. Objective alternative: show refund count and complaint count as plain dated numbers (agent layer above); no tier, no flag, no score.

## Open question — updated 2026-09-29
This bot/agent/backend split was originally built from one process description (the DEV.to engineering repost), so it was logged as "not confirmed architecture." A teammate's independent secondary-research pass found a second, more recent, independent source: a 2026 Swiggy backend engineering job ad (startup.jobs) listing "CRM (Agent Workbench, Customer Touchpoint Automation, Live Tracking Screen)" as a current team's ownership area.

**Status: partially resolved.** The name "Agent Workbench" and its existence as a live, current internal tool are now corroborated by two independent sources roughly three-plus years apart, rather than a single 2021-era repost. What remains unconfirmed either way: what the Agent Workbench screen actually shows a support agent, whether it includes anything like Uber Eats' named escalation triggers (value ceiling, alcohol orders, first-time customers — see `swiggy-cross-party-evidence-research.md` §4a), and whether restaurant/delivery-partner history (Section "Backend-only" above, and the companion cross-party doc) appears on it at all. The expert interview and any future customer-side chat audit should still test the *content* of the screen, not just whether it exists.

Full comparison against the teammate's research pass: `swiggy-secondary-research-crossverification.md`.
