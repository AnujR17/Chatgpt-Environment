# Swiggy Support Agent Decision Interface: Full Context File

Compiled: Thu 1 Oct 2026, 1:34 AM IST. Covers chat activity from Sat 26 Sep to Wed 30 Sep 2026.
Purpose: one file that carries everything needed to resume the project cold: the project, your rules, every document and what it is used for, findings, corrections, decisions, open items and all sources.

---

## 1. Project at a glance

- **Project:** Swiggy Support Agent Decision Interface (hypothetical concept, research-led, no access to Swiggy internals)
- **Owner:** Akshat Panchasara, MDes Intelligent User Experience Design, Semester 3, DAU Gandhinagar
- **Deadline:** Tue 6 Oct 2026 (7 days from 29 Sep)
- **Deliverable:** a working dashboard (per-ticket agent screen vs manager-level dashboard still undecided, to be settled by research). Built as an artifact or in Figma Make.
- **Current stage:** 4, Research. Stages 1-3 drafted. Expert interview booked for 29 Sep 2026, transcript not yet received as of this file.
- **Sprint position:** Day 3 of 7 when this file was written.

### Current problem statement (supplied by you, 29 Sep)
Swiggy publicly documents support automation and has disclosed fraud detection, but its current cross-party refund-review workflow is not visible. We propose an order-centred agent panel that brings policy conditions, incident evidence, and appropriately contextualised customer, restaurant, and delivery-partner histories into one review, aiming to reduce investigation effort while protecting genuine claims.

### Design rules in force
- Show facts and policy conditions. No verdicts, no scores, no predictions of customer intent.
- Success is measured by agent decision time and effort, never predicted outcomes.
- Every screen element is labelled as data, insight or decision support.
- Every assumption is labelled as an assumption.
- Policy appears as conditions checked against facts (checklist), plus an order timeline against policy cutoffs.
- Do not surface "value tier" or "fraud user" flags.
- Swiggy already has an Agent Workbench and builds agent recommendations, so this is a hypothetical concept, not a fix for a known flaw.

### Framework
- 13-stage case-study rulebook: Overview, Brief, Problem, Research, Insights, Define, Ideation, Design, Testing, Outcome, Future Scope, Limitations, Learnings.
- Three-layer model (raw data, derived insight, decision) is a Define-stage `[Own]` framework carried through Ideation and Design.
- Outcome, Future Scope and Limitations stay separate stages.
- Empathy Map: out. Affinity diagram: to be made with the interview synthesis.

---

## 2. How you want me to work (from your instructions)

- Think step by step, give relevant docs, references and articles. No jumping to conclusions.
- Short, crisp, to the point. Bullet points with indentation.
- Ask necessary questions before execution (you later said: do not keep asking, answers will be supplied as we go).
- Check the current date and time before answering and keep to the schedule.
- Check skills and use the relevant ones before answering.
- Keep tabs on you with task check-ins.
- Save shared files and links by type (a Behance case study goes to references, class material goes to notes).
- Be blunt and critical. No automatic agreement. Question claims.
- No em-dashes. Metaphors and puns welcome.
- Hard rule: never mention the company named in your saved preference in any output.

---

## 3. Timeline of the chat

- **26 Sep:** Uploaded two research files. I summarised context, pushed back on thin primary research, heavy stages 5-6 and a peer Wizard of Oz test.
- **27 Sep:** You answered: interview not booked, no deadline, Figma Make, Empathy Map out. I pushed back on "as soon as we can" and flagged dashboard vs agent-screen ambiguity.
- **29 Sep:** Dashboard reference search. Agent Workbench visuals search (none public). Deadline set to 6 Oct. Stages 1-3 drafted. Interview guide written. Teammate's cross-party research reviewed. Claims verified against originals. Notion hub created. Deep research launched across eight areas.
- **30 Sep:** Deep research report delivered as an artifact. `/usage` question answered (not available in chat; Settings, then Usage, per third-party guides).
- **1 Oct:** This file.

---

## 4. Files and what each is used for

### 4.1 swiggy-case-study-structure.md (you uploaded, 26 Sep)
- **What it is:** the agreed 13-stage structure, decisions, verified vs unverified sources, sprint plan.
- **Use:** the backbone. Read before producing any stage. Holds the stage table and the "one week sprint" plan.
- **Key decisions in it:** 1-week sprint, lead with research, three-layer model at Define, problem stated in full at stage 3, testing measures decision time and effort only, framing as hypothetical because Swiggy already has an Agent Workbench.
- **Open items it lists:** interview questions, read two literature papers before citing, confirm whether the expert can speak to agent tools, Empathy Map decision.

### 4.2 swiggy-refund-and-blocking-rules-research.md (you uploaded, 26 Sep, researched 25 Sep)
- **What it is:** customer-side secondary research on refund and block rules.
- **Use:** source of the policy parameters and the "conditions checklist" design idea. Holds the decision-flow picture, refund rules by situation, parameters table with evidence tiers, blocking ladder, regulation, Zomato comparison, contradictions and gaps.
- **Key points:**
  - Swiggy publishes refund conditions but not thresholds.
  - Fault attribution is the main variable.
  - The Terms of Use and the Refund Policy contradict each other.
  - Customer tier, refund history over 3 months, fraud flag: single anonymised source (Business Standard).
  - Do not surface tier or fraud flags in the interface.

### 4.3 swiggy-cross-party-evidence-research.md (you uploaded, 29 Sep, by a teammate, researched 28 Sep)
- **What it is:** restaurant-side, delivery-partner-side, incident-evidence and precedent research, companion to 4.2.
- **Use:** supports the cross-party panel in the current problem statement.
- **Status:** verified against originals on 29 Sep. See section 6 for corrections. Do not cite it unchecked.
- **Refers to, but I have not seen:** a "refined problem statement" document (you later pasted the statement) and a "Research behaviour rule" (text not supplied).

### 4.4 Deep research report (artifact, generated 30 Sep)
- **Title:** "Swiggy Support Agent Decision Interface: Evidence Base for an Order-Centred, Facts-Not-Verdicts Agent Panel"
- **Use:** the broad research base across eight areas. Holds a parameters table, a 10-type interface typology table, 12 interview questions, and design implications.
- **Caveat:** produced by a research agent. Vendor marketing is flagged inside. Not every figure was independently re-checked by me.

### 4.5 Notion hub (created 29 Sep, private draft)
- **Hub:** Swiggy Case Study: Support Agent Decision Interface. https://app.notion.com/p/3ea4e7cd8fd4810283a8cc6293e6dd00
- **Sub-pages:**
  - Stages 1-3 Drafts: https://app.notion.com/p/3ea4e7cd8fd48145ad9add2d46a4d074
  - Research Log: https://app.notion.com/p/3ea4e7cd8fd4818ea854f35f2bed54be
  - Interview: https://app.notion.com/p/3ea4e7cd8fd4818c81eee9530c04d6f9
  - References: https://app.notion.com/p/3ea4e7cd8fd481349b69fb9dd9bdca8a
- **Not yet in Notion:** the deep research report and the interview transcript and synthesis.
- **Note:** Notion folders cannot hold pages, so this is a hub page with sub-pages.

### 4.6 Memory note
- A project note exists recording deadline, deliverable, Notion preference and stage status.

---

## 5. Stage drafts (as written 29 Sep)

### Stage 1: Overview `[Rec]`
- Project, domain (food delivery support tooling, India), tools (Figma Make or an artifact), context (MDes IUxD Semester 3, 7-day sprint 29 Sep to 6 Oct).
- Role: to confirm (solo or team).
- Provisional research headline: Swiggy publishes refund conditions but not thresholds; fault attribution is the main variable; customer tier and fraud flags rest on single anonymised sources.

### Stage 2: Brief `[Rec]`
- A working dashboard that helps a support agent review a refund claim faster. It shows facts and conditions and does not recommend, score or automate.
- Constraints: no agent access, no Swiggy policy data, illustrative data, no predictions, success measured by decision time and effort.
- Framing: concept tests policy-as-conditions against facts, given that Swiggy already builds agent recommendations.

### Stage 3: Problem
- v1 (customer-side) superseded.
- v2 (current) is the problem statement in section 1.
- `[Rec]` Public sources describe the Workbench in text only.
- `[Assumed]` Agents see restaurant and delivery-partner history at decision time (no public evidence; test in the interview).
- `[Assumed]` Raw dated events are more neutral than flag totals or scores.

---

## 6. Verification pass on the teammate's document (29 Sep)

Checked against the original pages.

### Corrections needed
- **Telangana association objection is misattributed.** The article reports the group saying ratings, penalties and loss of orders influence delivery behaviour. It is about speed pressure and does not mention the karma score or fault assignment. The fairness concern about karma scoring is our inference, not a cited objection.
- **Uber Eats fraud rule is misread.** The page says the merchant is not charged for the refund when fraud is suspected. It does not say the customer's refund is withheld or that the override is unappealable.
- **Uber Eats categories are not four-way disjoint.** The page has a "merchant may be charged" list and a "merchant not charged" list. Undelivered orders appear on both, split by who delivers. It is a cost rule between merchant and Uber, not a fault taxonomy. It is a UK page (Feb 2024) written for merchants.
- **Uber Direct proof of delivery is configurable.** Options: signature, barcode, picture, ID, pincode (the teammate missed pincode). Merchants choose per delivery or vertical. Picture is automatic only for leave-at-door. Pictures kept 7 days on the dashboard and 30 days via API. Signature images 30 days. The page does not link this to disputes.
- **Quote not found:** "sometimes cannot definitively assign responsibility" appears in none of the three Zomato articles. Use "We can never be fully right" (India News Network) or paraphrase.

### Verified
- Uber flags couriers linked to many reported errors automatically, to protect merchants from those refunds.
- Zomato's karma score uses past records and complaint history on both sides.
- About 5,000 Zomato delivery-partner terminations a month, consistent across three outlets.
- "Fraud is not accidental most of the time" is a Goyal quote in TechStory (single, low-tier source).
- The 50 to 70% figure is framed three ways (refund customer and keep rider; absorb loss because fault is unclear; "take the hit"). Report as roughly half to 70% of disputes, per a podcast, reported inconsistently.

### Not re-checked
- Swiggy Market Intelligence Dashboard page, Uber Eats order accuracy page, Zendesk context panel page, the Management Science paper on two-sided platform disputes (title confirmed, not read).

### Extra finding
- TechStory reports Zomato's karma score also covers customers, with customers of good standing more likely to be believed. This is the prediction layer the interface excludes.

---

## 7. Dashboard and interface references (29 Sep)

### Per-ticket agent workspaces (closest to the concept)
- Kustomer unified agent workspace: complete history plus what the bot already did. Caution: it also predicts sentiment and escalation risk.
- Gorgias ticket sidebar: live order data, shipping and payment details in the ticket (described in a vendor guide).
- Zendesk Agent Workspace: conversation centre plus context panel. Industry baseline.
- Figma Community "AI Agent Workspace" template: split panel with a context sidebar.

### Decision logic
- Fini: logs policy version, data points and amount. Idea to borrow: each decision shows which rule and data it used. Guardrails include a value ceiling and per-customer frequency cap. Show raw counts, not flags.

### Manager-style dashboards (weak fit: KPI cards only)
- UI Bakery support dashboard template, HelpDesk UI kit, Nexchat on Behance.

### Swiggy Agent Workbench: what exists
- No public screens. Text descriptions only.
- Swiggy engineering post: Workbench is the support executive interface for resolving queries and defining assignment and routing rules; chat state carries over from the bot.
- Job posts: Workbench is still active and the team builds smart agent recommendations. The concept must not claim recommendations are missing.
- Customer side only: Mobbin has an 8-screen Swiggy iOS support chat flow.
- Dribbble and Behance "Swiggy dashboards" are designer concepts, not the real tool.

### Ways to get closer to the real screen
- Ask the expert to describe agent tools in words.
- Find ex-Swiggy support staff or Workbench frontend engineers on LinkedIn. Ask for descriptions, not screenshots of internal material.
- Otherwise design from documented facts and label each element as an assumption.

---

## 8. Expert interview

- **Expert:** former American Express design-team lead (a design expert, not a support agent). Label findings as expert recall, not agent behaviour.
- **Booked for:** 29 Sep 2026. **Transcript:** pending.
- **Must-ask five:** screen and tools agents used; walkthrough of a disputed case; how policy was shown; what slowed decisions; what you would refuse to put on the screen.
- **Also ask:** whether agents saw restaurant and delivery-partner history at decision time, and what went wrong when tools showed scores or flags.
- **Hygiene:** ask for stories not opinions, keep Swiggy specifics back until the end, get consent to record, note the date.
- **Next step on receipt:** synthesis, affinity diagram (stage 5), Notion update.

---

## 9. Deep research report: main findings (30 Sep)

Evidence tiers: Official, Law, Reported, Anecdotal, Inferred.

### Swiggy operations
- Chat stack (Official, older): Webview, Orchestrator, Agent Workbench, decision-tree Bot.
- Databricks LLM agent with CRM "action signals" and human fallback (vendor co-authored). The "100% automated" claim conflicts with its own human-fallback design.
- SHIELD device intelligence for promo abuse and delivery-partner abuse (vendor case study). No source says it feeds agent refund decisions.
- Supr Daily (Swiggy subsidiary) estimated up to 25% of refunds were issued incorrectly, mainly because of poor or missing delivery photos (AWS case study, vendor).
- Refund policy (from search excerpts; page did not render): 100% cancellation charge after placement; penalties where reasons are "not attributable to Swiggy".

### Pressure on Swiggy
- National Consumer Helpline: 10,590 complaints against Swiggy (912 about refunds not received), reported May 2025. CCPA probe; final outcome not found, treat as pending.
- AI-edited evidence photos: an Instamart egg-tray case produced an instant refund of about Rs 245 (Business Today, Nov 2025; Business Standard, Dec 2025).

### Decision parameters
- Strongly evidenced for Swiggy: order stage and timing, fault attribution, address and contactability, item unavailability, payment mode, report before "marked delivered", device signals, delivery photos.
- Reported only for rivals: refund-history score (Zomato karma), high-value and first-time customer escalation (Uber Eats), courier missing-item flag (Uber Eats), 20-minute courier lateness rule (DoorDash).
- Not found for Swiggy: published refund thresholds, OTP as evidence, what the agent screen shows.

### Time per decision
- No human-agent AHT for refund disputes is published for Swiggy.
- Vendor claim: bot-led resolution fell from about 5 minutes to 30-40 seconds (PubNub).
- Industry: US mean service call 442 seconds (ContactBabel 2024). SQM reports AHT up 18% year on year, attributed partly to self-service absorbing easy contacts.
- Screen switching: Salesforce says 58% of agents at underperforming organisations toggle between multiple screens vs 36% at high performers (vendor survey). HBR (2022) reports about 9% of work time lost to toggling.
- Inference: as bots absorb easy cases, human AHT will rise, so AHT alone will misjudge the panel.

### Rivals
- Zomato: karma score, 50:50 refund-sharing with restaurants (paused after backlash), about 5,000 delivery-partner terminations a month.
- Zepto: automated flags plus manual review.
- Uber Eats and DoorDash: published fault and cost rules, photo requirements, escalation criteria.
- Not covered: Blinkit, BigBasket, Amazon, Flipkart, Deliveroo, Grab, Foodpanda, Just Eat, Instacart, Meituan, Rappi, AmbitionBox, Reddit r/swiggy.

### HCI evidence
- Parasuraman and Manzey (2010): automation bias cannot be prevented by training or instructions.
- Brynjolfsson, Li and Raymond (NBER): 14% more resolutions per hour on average, 34% for novices; measured on reply suggestions, not adjudication.
- CX Today, No Jitter: agent-assist can add cognitive load when it is another tab.

### Regulation and other
- Consumer Protection (E-Commerce) Rules 2020: grievance officer acknowledges within 48 hours and resolves within one month.
- Dark Patterns Guidelines 2023; CCPA self-audit advisory June 2025.
- DPDP Act 2023 implications not verified in this pass. Gig-worker state laws not verified.

### Design implications
- Centre on the order, not the person. Three equal party columns with role-limited fields.
- Policy as condition rows, each with its data source. No "approve" badge.
- Timeline of order events against policy cutoffs.
- Evidence panel with provenance (customer upload, delivery-partner photo, GPS trace, restaurant note).
- Cross-party history as dated raw events, not scores.
- Value ceilings routing to an approval queue, with the reason shown.
- Audit trail: conditions shown, data version, agent choice, required reason on deviation.
- Regulatory clock and complaint channel shown.
- One screen, keyboard-first, design for 1366x768.
- Test metrics: time to decision, number of lookups and screens, consistency across agents on the same cases, override and reversal rate, NASA-TLX effort.

---

## 10. Open items and next steps

- Receive interview transcript, then affinity diagram and synthesis.
- Put the deep research report, the interview and the synthesis into Notion.
- Rewrite stage 3 after the interview if the expert changes the panel scope.
- Decide: per-ticket agent screen or manager-level dashboard (by research).
- Decide: build in Figma Make or an artifact.
- Confirm role line (solo or team).
- Provide the "Research behaviour rule" text and the "refined problem statement" document, if separate from the pasted statement.
- Read the two literature papers fully before citing any findings.
- Re-verify: Swiggy Market Intelligence page, Uber Eats order accuracy page, Zendesk context panel page.
- Gaps to research next: Reddit r/swiggy, AmbitionBox, Blinkit, Amazon, Flipkart, non-India rivals, Swiggy refund policy full text, CCPA final outcome.
- Sprint plan: Wed 30 Sep transcript synthesis and audit; Thu 1 Oct Define; Fri 2 Oct Ideation; Sat 3 to Sun 4 Oct build; Mon 5 Oct heuristic evaluation and walkthrough; Tue 6 Oct write-up and submission.

---

## 11. Sources

Tiers: Official, Law, Reported, Anecdotal, Vendor. "Verified" means the page was opened and read in this chat. "Excerpt" means read via search snippet only. "Unread" means title confirmed but content not read.

### 11.1 Swiggy and Swiggy-linked
- Chatbots at Swiggy (DEV Community repost of Swiggy engineering post), Official, excerpt: https://dev.to/abeyalex/chatbots-at-swiggy-9bp
- Designing and Scaling Swiggy's Support Chatbot Architecture (Arpit Bhayani), secondary: https://arpitbhayani.me/videos/swiggy-chatbot-system-design
- How Swiggy designed its chatbot (Medium, jayraj_singh), low-tier: https://medium.com/@jayraj_singh/how-swiggy-designed-its-chatbot-and-cut-down-the-costing-effectively-a0ff12577545
- Swiggy's Enterprise-Scale AI Agent with Databricks, Vendor co-authored: https://www.databricks.com/blog/redefining-customer-support-swiggys-enterprise-scale-ai-agent-built-databricks
- Swiggy's Generative AI Journey (Swiggy Bytes): https://bytes.swiggy.com/swiggys-generative-ai-journey-a-peek-into-the-future-2193c7166d9a
- Swiggy blog, generative AI: https://blog.swiggy.com/news/swiggys-generative-ai-journey-a-peek-into-the-future/
- Real-time AI data platform, "vimo" chatbot (Medium), secondary: https://medium.com/@vsanmed/from-billions-of-events-to-milliseconds-of-insight-architecting-swiggys-real-time-ai-data-a43a2697cdee
- Swiggy Market Intelligence Dashboard (Swiggy Catalyst), Official, not re-checked: https://blog.swiggy.com/swiggy-catalyst/stay-ahead-of-the-game-with-swiggys-market-intelligence-dashboard/
- Swiggy Refund and Cancellation policy, Official, excerpt only: https://www.swiggy.com/refund-policy
- Swiggy Terms and Conditions, Official: https://www.swiggy.com/terms-and-conditions
- Instamart Cancellation and Refund Policy, Official: https://instamart.in/instamart-cancellation-refund-policy
- Instamart Terms of Use, Official: https://instamart.in/instamart-terms-of-use
- Swiggy contact page, Official: https://www.swiggy.com/corporate/contact-us/
- Swiggy job post, Frontend (Marketplace Fulfilment), Official via aggregator: https://startup.jobs/software-dev-engineer-i-frontend-reactjs-swiggy_in-1755455
- Swiggy job post, Backend (Agent Workbench in CRM), Official via aggregator, excerpt: https://startup.jobs/software-dev-engineer-i-backend-dev-swiggy_in-1822723
- Swiggy Senior PM, Post-Order Experience, via aggregator: https://freehire.me/jobs/senior-product-manager-swiggy-p6zblx4b
- Swiggy Delivery Partner app listing, Official: https://play.google.com/store/apps/details?id=in.swiggy.deliveryapp&hl=en_US
- PubNub customer story, Vendor: https://www.pubnub.com/customers/swiggy/
- SHIELD x Swiggy case study, Vendor: https://shield.com/case-studies/swiggy
- VARINDIA on SHIELD x Swiggy: https://www.varindia.com/news/SHIELD-to-enhance-Swiggy%E2%80%99s-fraud-prevention-and-detection-capabilities
- AWS Supr Daily case study, Vendor: https://aws.amazon.com/solutions/case-studies/suprdaily-case-study/
- Bacancy, Swiggy CRM case study, Vendor: https://www.bacancytechnology.com/case-study/ruby-on-rails/swiggy
- ZenML, Swiggy neural search and conversational AI, secondary: https://www.zenml.io/llmops-database/neural-search-and-conversational-ai-for-food-delivery-and-restaurant-discovery
- Swiggy CRM slides (SlideShare), low-tier: https://www.slideshare.net/slideshow/swiggy-crm-for-business-growth-customer-satisfaction-pptx/271973386
- Unofficial directory, Swiggy customer service: https://customer-service.wiki/swiggy-customer-service/
- Pathfinder Foundation blog, AI customer service at Swiggy, low-tier, untraced: https://pathfinderfoundation.co.in/blog/ai-centric-customer-service-swiggys-innovative-approach-to-food-delivery
- @SwiggyCares reply (Aug 2025), Official account: https://x.com/SwiggyCares/status/1960745315683700883
- @Swiggy reply (Jan 2025), Official account: https://x.com/Swiggy/status/1878314670081364391
- Storyboard18, Swiggy ordering via ChatGPT, Claude and Gemini: https://www.storyboard18.com/brand-marketing/swiggy-integrates-ai-chatbots-to-enable-ordering-via-chatgpt-claude-and-gemini-88325.htm

### 11.2 Law and regulation
- Consumer Protection (E-Commerce) Rules 2020 (text): http://thc.nic.in/Central%20Governmental%20Rules/Consumer%20Protection%20%28E-Commerce%29%20Rules%2C%202020.pdf
- E-Commerce Rules summary (Lexology): https://www.lexology.com/library/detail.aspx?g=ea0f67cd-3c27-48e3-bd0b-e8216f9219c8
- E-Commerce Rules summary (Seraphic Advisors): https://www.seraphicadvisors.com/insights/blogs/consumer-protection-ecommerce-rules-2020-6654697d740abe88738c5fdf
- CCPA dark-patterns self-audit advisory (PIB, Jun 2025): https://consumeraffairs.gov.in/public/upload/admin/cmsfiles/pressRelease/Central_Consumer_Protection_Authority_issues_advisory_to_E-Commerce_Platforms_for_self-audit_within_3_months_to_detect_Dark_Patterns_and_ensure_its_resolutionpress_release.pdf
- Amritsar consumer commission order (Indian Express, Jun 2026): https://indianexpress.com/article/legal-news/no-veg-mezze-platter-woman-swiggy-ordered-pay-rs-5000-compensation-10747310
- Deccan Herald, government asks platforms for complaint-redressal plans (2022): https://www.deccanherald.com/business/govt-asks-swiggy-zomato-and-others-to-submit-plans-in-15-days-for-improving-complaint-redressal-1117838.html

### 11.3 News and reported sources
- Business Standard, how Swiggy, Blinkit, Zepto rate users (Jul 2025): https://www.business-standard.com/industry/news/swiggy-blinkit-zepto-rate-users-and-delivery-workers-here-s-how-it-works-125071101503_1.html
- Business Standard, CCPA likely to direct revisions (May 2025): https://www.business-standard.com/industry/news/ccpa-zomato-swiggy-cancellation-refund-policy-update-directive-125052101628_1.html
- Business Standard, rising AI-generated images for refunds (Dec 2025): https://www.business-standard.com/industry/news/food-companies-take-note-of-rising-ai-generated-images-for-refund-125120101409_1.html
- Storyboard18, CCPA may direct revisions: https://www.storyboard18.com/brand-marketing/ccpa-may-direct-zomato-swiggy-to-revise-cancellation-and-refund-policies-66720.htm
- MediaNama, CCPA probe (May 2025): https://www.medianama.com/2025/05/223-ccpa-probes-zomato-swiggy-cancellation-refund-policies
- MediaNama, Zomato pauses refund-sharing: https://www.medianama.com/2025/05/223-zomato-pauses-refund-sharing-policy/
- Inc42, Zomato puts 50:50 refund sharing on hold: https://inc42.com/buzz/zomato-puts-5050-refund-sharing-with-restaurants-on-hold/
- MediaNama, CCI dismisses Zomato complaint (Jul 2026): https://www.medianama.com/2026/07/223-cci-complaint-zomato-fees-pricing/
- Outlook Business, Zomato karma score (Jan 2026), Verified: https://www.outlookbusiness.com/news/inside-zomatos-karma-score-what-deepinder-goyal-reveals-about-fraud-refunds
- India News Network, Zomato defends karma system (Jan 2026), Verified: https://www.indianewsnetwork.com/en/zomato-defends-karma-system-amid-scrutiny-gig-worker-practices-20260105
- TechStory, Zomato CEO on churn and fraud (Jan 2026), Verified, low-tier: https://techstory.in/zomato-ceo-lifts-the-lid-on-gig-worker-churn-and-fraud-challenges/
- NDTV, Zomato fraud types (Jan 2026): https://www.ndtv.com/food/deepinder-goyal-reveals-most-common-scams-customers-and-delivery-riders-try-on-zomato-10325357
- CurlyTales, Zomato customers using AI for false refunds: https://curlytales.com/india/trending/are-zomato-customers-using-ai-to-claim-false-refunds-heres-what-deepinder-goyal-has-to-say/
- News18, fake-refund delivery scam (May 2025): https://www.news18.com/viral/new-scam-targets-swiggy-and-zomato-users-with-fake-refunds-and-qr-code-payments-9337429.html
- Tribune India (IANS), Swiggy agent harassment complaint: https://www.tribuneindia.com/news/nation/miss-you-lot-woman-accuses-swiggy-agent-of-sending-creepy-messages-company-acts-on-her-complaint-405008/amp
- Deccan Herald, restaurant owners on Zomato rejection policy: https://www.deccanherald.com/amp/story/business%2Frestaurant-owners-slam-zomato-over-rejection-policy-973163.html
- MediaNama, Zomato's opaque ad model: https://www.medianama.com/2025/06/223-zomato-opaque-ad-model-small-restaurants-unsustainable-spending/
- Wikipedia-level note on Swiggy Genie shutdown, carried in research doc (not re-verified).

### 11.4 Anecdotal
- DesiDime, Swiggy account blocked: https://www.desidime.com/discussions/swiggy-account-blocked-dbb83645-dd2b-4ae4-b33a-e16a14c92ff3
- DesiDime, missing-item refund denied: https://www.desidime.com/discussions/swiggy-not-refunding-money-even-after-having-missing-items
- Reddit r/swiggy threads: https://www.reddit.com/r/swiggy/comments/1jy20ov/swiggy_refused_refund , https://www.reddit.com/r/swiggy/comments/1k24u99/horrible_experience_with_swiggy_customer_support , https://www.reddit.com/r/swiggy/comments/1rqq6vk/no_refund_for_missing_items
- Glassdoor, Swiggy Customer Support Executive reviews: https://www.glassdoor.com/Reviews/Swiggy-Customer-Support-Executive-Reviews-EI_IE952680.0,6_KO7,33.htm
- Trustpilot, Swiggy: https://www.trustpilot.com/review/swiggy.com?page=5
- PissedConsumer, Swiggy Q and A: https://swiggy.pissedconsumer.com/questions-answers.html
- The Emerging India, Instamart refund-scam story (SEO blog, low reliability): https://www.theemergingindia.com/reddit-users-jaw-dropping-expose-on-friends-unethical-hack-highly-unethical-and-risking-bans/
- Job-board Swiggy chat JDs (low-tier): https://www.jobvalley.online/2021/08/urgent-hiring-for-swing-customer-care.html , https://www.scribd.com/document/571764352/JD-Swiggy

### 11.5 Rivals and industry practice
- Uber Eats, Order Error Adjustments (UK, Feb 2024), Verified: https://www.uber.com/gb/en/blog/order-error-adjustments-best-practices/
- Uber Eats, Order Errors (AU): https://merchants.ubereats.com/au/en/order-errors
- Uber Eats, order accuracy guide, not re-checked: https://www.uber.com/en-GB/blog/your-guide-to-monitor-your-order-accuracy-on-uber-eats
- Uber Direct, Proof of Delivery, Verified: https://developer.uber.com/docs/deliveries/guides/proof-of-delivery
- DoorDash, missing items (merchant help): https://help.doordash.com/en-us/merchants/article/what-do-i-do-if-a-customer-reports-an-item-is-missing
- Zendesk Agent Workspace: https://support.zendesk.com/hc/en-us/articles/4408821259930-About-the-Zendesk-Agent-Workspace
- Zendesk context panel, not re-checked: https://support.zendesk.com/hc/en-us/articles/4408836526362-Using-the-context-panel-in-the-Zendesk-Agent-Workspace
- Kustomer unified agent workspace, Vendor: https://www.kustomer.com/resources/blog/unified-agent-workspace/
- Fini refund and dispute ops guides, Vendor: https://www.usefini.com/guides/ai-platforms-refund-dispute-operations , https://www.usefini.com/blog/top-10-ai-agents-for-handling-refunds-returns-cancellations-automatically
- UI Bakery, case management and support dashboard template: https://uibakery.io/blog/best-case-management-software , https://uibakery.io/templates/customer-support-dashboard
- Figma Community, AI Agent Workspace template: https://www.figma.com/community/file/1653308101284510808/ai-agent-workspace-ui-template-customer-support-dashboard
- Figma Community, Customer Support Dashboard UI Kit: https://www.figma.com/community/file/1502557663697104018/customer-support-dashboard-ui-kit
- Behance, AI Agent Customer Service Dashboard (Nexchat): https://www.behance.net/gallery/237704797/AI-Agent-Customer-Service-Dashboard-UIUX-Design
- Behance, Swiggy re-design and admin dashboard (concept): https://www.behance.net/gallery/110468233/SWIGGY-RE-DESIGN-ADMIN-DASHBOARD-DESIGN
- Dribbble, Swiggy Dashboard (concept): https://dribbble.com/shots/17588606-Swiggy-Dashboard
- Mobbin, Swiggy iOS support chat flow: https://mobbin.com/explore/flows/26a11940-a254-4bea-87f2-282357efe932

### 11.6 Benchmarks and HCI research
- ContactBabel US Decision-Makers Guide 2024: https://assets.ringcentral.com/us/report/us-dmg-2024.pdf
- ContactBabel UK 2024: https://www.encoded.co.uk/wp-content/uploads/2024/04/ContactBabel-DMG-Full-Report-2024.pdf
- SQM Group, call centre benchmark 2024: https://www.sqmgroup.com/resources/library/blog/call-center-fcr-benchmark-2024-results-by-industry
- Salesforce State of Service, 6th edition (vendor survey): https://www.salesforce.com/content/dam/web/en_us/www/documents/e-books/service/sixth-edition-state-of-service.pdf
- Verint 2026 agent survey (vendor): https://www.verint.com/press-room/2026-press-releases/nearly-one-third-of-contact-center-agents-plan-to-quit-as-agent-experience-falls-short/
- HBR, toggling between applications (2022): https://hbr.org/2022/08/how-much-time-and-energy-do-we-waste-toggling-between-applications
- Parasuraman and Manzey (2010), Human Factors, abstract and partial text read: https://journals.sagepub.com/doi/10.1177/0018720810376055
- Brynjolfsson, Li and Raymond, Generative AI at Work (NBER w31161), excerpts read: https://www.nber.org/papers/w31161
- CX Today, hidden downsides of agent-assist (vendor-sponsored): https://www.cxtoday.com/contact-center/the-hidden-downsides-of-contact-center-agent-assist-technology-cyara/
- No Jitter, smarter systems, tired agents: https://www.nojitter.com/contact-centers/smarter-systems-tired-agents-the-hidden-cost-of-ai-driven-cx
- Management Science, "Improving Dispute Resolution in Two-Sided Platforms: The Case of Review Blackmail" (2022), Unread: https://pubsonline.informs.org/doi/10.1287/mnsc.2022.4655

### 11.7 Usage question (30 Sep)
- Third-party guides on checking Claude usage (not official): https://tokensforgood.ai/how-to-check-your-claude-usage , https://continuumcode.ai/guides/how-to-check-claude-usage-limit/

---

## 12. Quick-start prompt for a new chat

"Read swiggy-case-study-context.md. We are on Day N of a 7-day sprint ending 6 Oct 2026. Resume at stage 4 (Research). I will paste the interview transcript next. Rules: be blunt, bullet points, no em-dashes, check the date and time, tag every claim with an evidence tier, no scores or verdicts in the interface."
