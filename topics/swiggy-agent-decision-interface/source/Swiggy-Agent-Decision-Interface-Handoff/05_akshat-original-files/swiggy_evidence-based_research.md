# Swiggy Support Agent Decision Interface: Evidence Base for an Order-Centred, Facts-Not-Verdicts Agent Panel (Research as of 29 Sep 2026)

The evidence supports the case study's premise. Swiggy has publicly described an agent-facing tool (Agent Workbench), a routing layer (Orchestrator), a rule-based and now LLM-based automation stack, and device-level fraud detection. It has never published how a human agent reviews a disputed refund across customer, restaurant and delivery partner. Regulators, restaurants and customers have separately criticised the opaque, score-driven and policy-rigid decisions that such a review screen would need to avoid.

## TL;DR
- **What Swiggy has made public (Official/Reported):** Swiggy documents a chat stack (Webview, Orchestrator, Agent Workbench, decision-tree Bot). It also documents an LLM agent built with Databricks that sends "action signals" to its CRM, and says it uses SHIELD device intelligence to catch promo abuse and delivery-partner abuse. No public source shows the screen a human agent uses to decide a cross-party refund, and I found no public evidence on problems with Swiggy's agent-side tooling. The gap is real, but it is a gap in public information, not proof that the tooling is bad.
- **Where the pressure comes from (Law/Reported):** In 2024 the National Consumer Helpline logged 10,590 complaints against Swiggy, including 912 about refunds not received. That led to a CCPA probe (suo motu from October 2024) into cancellation charges levied even when the platform was at fault. AI-edited evidence photos (for example, the Instamart egg-tray case, where a full refund of about ₹245 was issued; Business Today, 26 Nov 2025) and Zomato's opaque "karma score" and AI refund-sharing model show two risks together: fraud gets through fast chat flows, and parties who are scored cannot see or contest the decision.
- **Design implication (Inferred from HCI evidence):** Automation bias is not cured by training (Parasuraman and Manzey 2010). Agent-assist can add cognitive load when it is bolted on as another tab (CX Today, 2025 to 2026). Generative AI assistance helps novices most (14% more resolutions per hour on average, 34% for novices; Brynjolfsson, Li and Raymond). Build one order-centred screen with policy conditions shown as checkable facts, dated raw events, evidence provenance, value ceilings and an audit trail. Measure time-to-decision and override rates, not just AHT.

## Evidence tier legend
- **Official**: Swiggy or competitor's own site, policy, filing, engineering blog or company-authored post.
- **Law**: statute, rules, regulator direction.
- **Reported**: credible media or vendor case study (vendor content flagged as such).
- **Anecdotal**: individual reviews, social posts, forums.
- **Inferred**: my reasoning from the above; not stated by any source.

---

## 1. Swiggy's existing support and post-order-care operations

### 1.1 Chat platform architecture (Official, older)
- **Source:** "Chatbots at Swiggy", a Swiggy engineering post republished on DEV.to (https://dev.to/abeyalex/chatbots-at-swiggy-9bp, undated; the original Swiggy Bytes URL was not located in this session).
- It describes four components:
  - **Webview:** the customer chat interface.\[1\]
  - **Orchestrator:** "a controller for conversation routing between customers, chatbot, and support executives".\[1\]
  - **Agent Workbench:** "the support executives' interface for resolving customer queries, defining assignment logic and rules".\[1\]
  - **Bot:** "a decision tree parser that connects with multiple systems within Swiggy to validate nodes".\[1\]
- It says "about 70% of our customers prefer to communicate via chat as opposed to calls".\[1\]
- It says executives "were solving similar repetitive complaints every time" (cancellation, order status). Onboarding of delivery-executive and restaurant-partner support onto the chat platform was described as "in progress".\[1\]
- A secondary repost (Medium, jayraj_singh, undated; low-tier) says some customers were cancelling "dozens of orders per day, to claiming 100% refunds for all the orders" and that "Some guard rails had to be put in place to prevent misuse of the system."\[2\] I could not verify this against the original Swiggy post.
- **Agent Workbench is still current (Official, job ad via aggregator):** a Swiggy SDE-I backend job ad (startup.jobs, undated) lists "CRM (Agent Workbench, Customer Touchpoint Automation, Live Tracking Screen)".\[3\]
- **Inferred:** the agent tool sits inside a CRM team that also owns the live-tracking screen. Tracking data is therefore probably available to agents, but how it is shown to them is not public.

### 1.2 Chat automation metrics (Reported, vendor marketing)
- **Source:** PubNub customer case study (https://www.pubnub.com/customers/swiggy/, undated, about 2021 to 2022).
- Swiggy handled "up to 200,000 customer inquiries a day with a peak concurrency of 2,000 users".\[4\]
- It can "automate up to 70% of all customer support inquiries". Resolution time fell "from an average of around five minutes pre-automation to just 30 to 40 seconds now".\[4\]
- On the old phone model, it says "simple requests would turn into multiple questions that would lead to agents needing to navigate through multiple dashboard screens."\[4\]
- **Caveat:** this is bot-led resolution time, not human agent AHT. It is vendor marketing.
- A 2018 Business Wire release (via CB Insights) says Swiggy moved from calls to Layer-powered messaging with "new agent tools" after a "four-fold increase in calls" in 2017 (Reported, vendor press release).\[5\]

### 1.3 Databricks LLM agent and CRM action triggers (Official co-authored, vendor marketing)
- **Source:** "Redefining Customer Support: Swiggy's Enterprise-Scale AI Agent Built with Databricks", Databricks blog, published 21 Oct 2025, modified 27 Aug 2026 (https://www.databricks.com/blog/redefining-customer-support-swiggys-enterprise-scale-ai-agent-built-databricks). \[6\]
- **Stated objectives** include "Reduce reliance on, and costs associated with, human agents by reducing direct human intervention and moving to human-in-the-loop" and "Reduce average handling time (AHT)".\[6\]\[7\] No AHT figure is given.
- **CRM integration:** "Whenever the Agent makes intelligent decisions, the required corresponding actions will be executed in the CRM backend. These decisions are based on dynamic context and business rules and are communicated to the CRM system as action signals."\[6\]\[7\]
- **Safeguards and known failure modes:**
  - The design includes "A graceful fallback to human agents".\[6\]\[7\]
  - Agent assignment done entirely by an LLM "achieved 90% accuracy". This was fixed by adding rule-based routing.\[6\]\[7\]
  - An "Over-reliance on short-term memory" bug returned outdated information until tool calls were made mandatory.\[6\]\[7\]
- **Claimed results:** "100% of customer queries were fully automated without human intervention"; CSAT improved; "reduced resolution times".\[6\]\[7\] No numbers are given. Treat the 100% claim with caution: it contradicts the stated human-in-the-loop design and the human fallback.
- **Inferred:** the rule-based engine came first and still supplies the "business rules". A human review panel would receive the cases the agent escalates. Those are the ambiguous, high-value or contested ones, where facts matter most.

### 1.4 "vimo" chatbot (Reported, secondary)
- **Source:** Medium article (vsanmed, "Architecting Swiggy's Real-Time AI Data Platform", undated; appears to summarise a Databricks conference talk).
- Describes "vimo" as a chatbot that "fully automates responses to common questions like 'Where is my order?'". Agentic apps use LLMs "(e.g., from OpenAI, Gemini)", Redis stores conversation context, and Prometheus handles monitoring.\[8\]
- I did not find a Swiggy-authored primary source for the name "vimo".
- A separate ZenML LLMOps database entry (secondary) says Swiggy worked with a third party on a GPT-4 customer service chatbot and piloted in-house LLMs for restaurant partner support.\[9\]

### 1.5 Automated refund decisions described in media (Reported, low-tier)
- A Pathfinder Foundation blog (education site, low-tier) says Swiggy's AI "checks the rider's location, reviews the order, decides whether a refund is owed, and credits the customer's wallet". It cites resolution "often within 3 to 8 seconds" and Amazon "AgentCore".\[10\]
- I could not trace this to a Swiggy or AWS primary source in this session. Treat it as unverified.

### 1.6 Trust and Safety, SHIELD device intelligence (Official quote plus vendor case study)
- **Sources:** SHIELD case study (https://shield.com/case-studies/swiggy) and press coverage (Business Wire India release dated 20 May 2024; The Week/PTI carries it as "Updated: May 20, 2024"). SHIELD Director Gautam Sehgal is quoted: "SHIELD is proud to support Swiggy in establishing itself as the standard for trust and fairness as well."
- Uses: reducing promo abuse (discounts, sign-up incentives, referrals) and "Delivery Partner Abuse". Signals detected include "app cloners, tampered apps, and GPS spoofers". The device ID identifies "the physical devices used to create multiple fake accounts".\[11\]
- Dolly Sureka (VP, Assurance and Business Advisory, lead for Trust and Safety at Swiggy): "Our partnership with SHIELD has enhanced Swiggy's Fraud Prevention and Detection mechanisms through device-first risk intelligence."\[12\]
- **Not found:** any statement that SHIELD signals are shown to support agents or used in refund decisions. The published uses are promo abuse and delivery-partner abuse.

### 1.7 Image evidence and delivery photos (Reported, vendor case study)
- **Source:** AWS case study on Supr Daily, a Swiggy subsidiary for morning grocery subscriptions (https://aws.amazon.com/solutions/case-studies/suprdaily-case-study/, undated, about 2020 to 2021).
- Delivery partners upload a photo per delivery. Blurry photos "could delay the processing of refunds and lead to unnecessary or fraudulent refund claims".\[13\]
- The company "estimates that as many as 25 percent of refunds were issued incorrectly, primarily due to poor quality or missing delivery photos". It used Amazon Rekognition to check photo quality.\[13\]
- This is the only Swiggy-group source found that ties a figure to evidence quality and refund error. I did not find a published handling-time reduction figure for image verification in this session.

### 1.8 Refund and cancellation policy (Official)
- **Source:** Swiggy Refund and Cancellation page (https://www.swiggy.com/refund-policy). The page body did not render in my fetch, so the text below comes from search-indexed excerpts, accessed 29 Sep 2026.
- **Customer cancellation:** "As a general rule Buyer shall not be entitled to cancel Order once placed." If the buyer cancels, "Swiggy shall have a right to charge 100% of the Order amount for breach of contract terms". It may withhold the refund (prepaid) or recover it from the next order (postpaid) "to compensate the Merchants and Delivery Partners".\[14\]
- **Non-customer cancellation penalties** apply for reasons "not attributable to Swiggy":
  - wrong address or address outside the delivery zone;
  - failure to contact the buyer;
  - failure to deliver due to lack of information or authorisation;
  - unavailability of all items.\[14\]
- A search snippet shows a condition that an issue must be "communicated to Customer Care through the Platform before the Order is marked delivered".\[14\] Its full context was not visible.
- **@SwiggyCares practice (Official account, Anecdotal context):** a reply (about Aug 2025) says "if you cancel your order even one second after it has been placed, you will incur a cancellation fee amounting to 100% of the order value."\[15\] A Jan 2025 @Swiggy reply says "a 100% cancellation fee is applicable post placing the order."\[16\]
- **Critique (Reported):** MediaNama (May 2025) says the policy "does not define what exactly constitutes a breach, nor does it outline how users or restaurant partners can contest these decisions". It also says checkout does not display cancellation terms.\[17\]

### 1.9 Escalation paths (Official/Law, partially verified)
- Verified in this session:
  - support@swiggy.in (Swiggy corporate contact page);\[18\]
  - @SwiggyCares on X;
  - National Consumer Helpline (NCH), the channel behind the CCPA probe.
- The legal duty to have a grievance officer (48-hour acknowledgement, one-month redress, tracking ticket number) comes from the E-Commerce Rules 2020 (Law, see Section 8).\[19\]
- **Partly verified:** Swiggy's own Stakeholder Engagement and Grievance Redressal Policy (swiggy.com PDF, Aug 2025) lists grievances@swiggy.in. Third-party sites give different grievance officer names, so the officer's name is still unverified.
- **Inferred:** the agent panel should show which escalation channel a case came from, plus any regulatory clock (48h/1 month), because an NCH-origin case carries different risk.

### 1.10 Post-order product, BPO and delivery-partner support
- **Post-order product (Official job ad via aggregator):** a "Senior Product Manager - Post-Order Experience" role (freehire.me, 2026) covers the "track screen", "support-linked product surfaces" and "critical moments such as delays, address issues, payment friction, delivery exceptions, and service recovery".\[20\]
- **Chat agent job descriptions (Anecdotal, low-tier job boards):**
  - A work-from-home "Customer Support - Chat Process" role lists tickets for "order status, cancellation, delivery instruction, location issue" and "making outcall to PDPs or stores" (jobvalley.online, Aug 2021).\[21\]
  - A Scribd-hosted job description lists Rs 6,000/month fixed pay plus incentives, 3 weeks of training, and typing-speed tests (undated, low-tier, unverified).\[22\]
  - **Inferred:** agents coordinate across three parties by phone and chat, so cross-party context is already part of the job.
- **Outsourced vendors (Reported, low-tier):** a listicle names Maxicus (Indian BPO) as serving Swiggy (runningremote.com).\[23\] No Swiggy-confirmed vendor list was found.
- **Delivery-partner support (Official):** the Swiggy Delivery Partner app listing on Google Play advertises "24×7 Emergency & Live Order Support" and "₹12 Lakhs Accidental & Medical Insurance".\[24\]
- **Not found this session:** a Market Intelligence Dashboard or other restaurant-facing complaint dashboard, Instamart-specific support tooling, and support KPIs in Swiggy's DRHP or annual report. The subagent found no AHT/FRT figure in investor material but did not read the full FY2025-26 annual report.

### 1.11 AI ordering via MCP (Reported)
- Storyboard18 and others report that Swiggy Food, Instamart and Dineout can be ordered through ChatGPT, Claude and Gemini via Model Context Protocol.\[25\]
- **Inferred:** orders placed by third-party AI assistants create a new evidence-provenance question for disputes (who or what placed and confirmed the order).

---

## 2. Typology of dashboards and agent interfaces

Note: product characterisations below are industry practice drawn from general product knowledge. They were not re-verified against vendor documentation in this session (Inferred/Reported). The HCI findings are sourced in Section 7.

- **Per-ticket agent workspace / unified agent desktop** (Zendesk Agent Workspace, Freshdesk, Gorgias)
  - Shows the conversation, customer profile, order sidebar, macros.
  - Strength: fast for simple tickets.
  - Weakness: ticket-centred, so cross-party context needs extra lookups.
  - Fit: baseline only.
- **Case-management console** (Salesforce Service Console, ServiceNow CSM)
  - Shows case record, related records, SLA timers, approvals.
  - Strength: auditability and workflow.
  - Weakness: tab sprawl and configuration burden.
  - Fit: good model for audit and SLA.
- **Entity/customer-360 timeline** (Kustomer)
  - Shows a chronological event timeline per customer.
  - Strength: history in one place.
  - Weakness: centred on the customer, which invites judgement of the person.
  - Fit: borrow the timeline, but centre it on the order.
- **Order-centred incident view** (food-delivery internal tools; inferred)
  - Shows order timeline, parties, evidence, policy conditions.
  - Strength: matches how disputes happen.
  - Weakness: needs data integration across three parties.
  - Fit: **core pattern for this project.**
- **Supervisor/operations dashboard**
  - Shows queues, AHT, SLA breaches, backlog.
  - Strength: staffing decisions.
  - Weakness: not per-case.
  - Fit: secondary view.
- **QA/analytics dashboard**
  - Shows sampled interactions, scorecards, override rates.
  - Strength: consistency checks.
  - Weakness: after the fact.
  - Fit: needed to measure override rate.
- **Agent-assist copilot sidebar** (Intercom Fin Copilot, Zendesk AI, Salesforce Einstein; Brynjolfsson et al. studied one such tool)
  - Shows suggested replies, knowledge snippets, next-best action.
  - Strength: large gains for novices.
  - Weakness: automation bias, extra cognitive load when it is "another tab", compliance checking burden.
  - Fit: only if limited to fact retrieval, never verdicts.
- **Autonomous AI agent with human escalation** (Sierra, Decagon, Fini; Swiggy's Databricks agent)
  - Shows little UI to the human; escalation summary.
  - Strength: volume.
  - Weakness: the human receives the hardest cases with thin context.
  - Fit: upstream of our panel.
- **Approval/exception queue**
  - Shows items above thresholds awaiting sign-off.
  - Strength: ceilings and four-eyes control.
  - Weakness: queue latency.
  - Fit: use for high-value refunds.
- **Dispute/chargeback review console** (card-network dispute tools; Amex-style; inferred)
  - Shows claim, evidence by type, reason codes, deadlines.
  - Strength: evidence-type discipline and time limits.
  - Weakness: adversarial framing.
  - Fit: **strongest analogue for evidence and provenance.**

---

## 3. Problems with Swiggy's agent decision interface: what is and is not public

### 3.1 Documented facts (Official/Law/Reported)
- **NCH complaint volume (Reported, Business Standard, 21 May 2025, citing Moneycontrol):**
  - Swiggy had 10,590 complaints, including "nearly 4,000 linked to service issues and 912 concerning non-receipt of refunds".\[26\]
  - Zomato had 7,938.\[26\]
  - Storyboard18 dates the suo motu probe to October 2024.\[27\]
  - A source quoted by Storyboard18 said: "Customers are being penalised for platform-related issues such as delays in assigning delivery agents or the actual delivery time exceeding the promised ETA." NewsX quotes a senior official: "There is a clear need to rebalance the policies that shift the liability unfairly onto the customer."
  - The CCPA was expected to ask for software changes to cap cancellation charges and speed refunds.\[27\]
- **Outcome not verified:** I did not find a final CCPA order in this session. Media coverage describes a "likely" direction, so treat the outcome as pending unless confirmed.
- **Cancellation charges up to 90% (Reported, MediaNama May 2025, citing Moneycontrol).**\[17\] This contradicts Swiggy's own "100%" wording. The difference may reflect actual practice versus policy ceiling.
- **Speed over checks (Reported, Business Standard, 1 Dec 2025):** bakery owner Harsh Shah says "Aggregators prefer quick redressal and, in most cases, the entire conversation is done on text, which starts with a chatbot." An Instamart user received an instant full refund of about ₹245 (The Logical Indian) after using Gemini Nano with the prompt "apply more cracks" to produce an image of over 20 cracked eggs; in reality one egg was cracked (first posted by X user @kapilansh; Business Today, 26 Nov 2025).
- **CEO's office escalation (Reported, IANS via Tribune):** in a harassment case, the customer said support did not respond properly until "the escalation team and the CEO's office" contacted her.\[28\] **Inferred:** a separate escalation tier exists.

### 3.2 Anecdotal signals (do not generalise)
- **Glassdoor, Swiggy Customer Support Executive (5 reviews only):**
  - "the only issue is the customers that you receive(fraud ones)";
  - "no priority to customer satisfaction";
  - "Delayed in Salary& not giving enough time for lunch".\[29\]
- **Trustpilot/PissedConsumer:**
  - Instamart agents allegedly sent copy-paste "unable to validate your claim" replies;\[30\]
  - refunds replaced by conditional coupons;
  - orders "marked as delivered without actual receipt".\[31\]
- A Medium post (student author, low-tier) quotes an unnamed Twitter user: "SIX agents gave me six different answers".\[32\] I could not verify it.

### 3.3 What could not be found
- No public source (news, reviews, filings) describes the Swiggy agent screen, its fields, its flags, or agent complaints about it.
- AmbitionBox and Reddit r/swiggy agent threads were not reached within the search budget.
- **Inferred:** the problem statement should frame the tooling gap as "not visible", not "broken".

---

## 4. Decision parameters (details in Table A)
- **Most strongly evidenced for Swiggy:**
  - order stage and timing (cancel after placement);
  - fault attribution (the "not attributable to Swiggy" list);
  - address and contactability;
  - item unavailability;
  - payment mode (prepaid vs postpaid recovery);
  - reporting before "marked delivered";
  - device signals (SHIELD);
  - delivery photos (Supr Daily).
- **Reported for rivals but not Swiggy:**
  - refund history as a score (Zomato karma);
  - high-value, first-time customer and alcohol escalation (Uber Eats);
  - courier missing-item rates (Uber Eats);
  - restaurant 20-minute courier-lateness rule (DoorDash).
- **Published thresholds found:**
  - DoorDash: courier more than 20 minutes after estimated ready time; within seven days; perishables only.\[33\]
  - Zomato (older rejection policy, Deccan Herald): restaurant daily rejection rate above 3% led to suspension the next day; 25% of order value (min Rs 25, up to Rs 200) paid to the customer on rejection.\[34\]
  - Swiggy: no refund thresholds published beyond the 100% cancellation clause.

---

## 5. Time on a decision: AHT and related benchmarks

### 5.1 Swiggy
- **Reported, vendor:** PubNub says average resolution fell from about 5 minutes to 30 to 40 seconds (bot-led).\[4\]
- **Official engineering post:** self-serve cancellation "can be done in 10 seconds" versus "about 5 minutes and multiple phone calls" earlier.\[1\]
- **Official co-authored:** Databricks lists AHT reduction as a goal, with no figure.\[6\]\[7\]
- No human-agent AHT for refund disputes is published.

### 5.2 Industry voice benchmarks
- **ContactBabel US DMG 2024 (independent, RingCentral-sponsored):** mean service call 442 s (7 min 22 s) in 2023, up from 306 s in 2012. Rising length is attributed to "a rise in self-service taking away the easier and shorter calls". Talk time about 53%, wrap-up 13.5%.\[35\]
- **ContactBabel UK DMG 2024 (independent):** service call mean 421 s, median 360 s.\[36\]
- **SQM Group 2024 (benchmarking firm):** AHT "697 seconds, reflecting an 18% increase from the previous year".\[37\]
- **Inferred:** as bots absorb easy contacts (Swiggy's stated strategy), human AHT per case should be expected to rise. AHT alone will then mis-measure the panel.

### 5.3 Chat benchmarks (vendor platform data)
- Comm100 2020 (56M chats): 11 min 47 s average duration at high-CSAT firms versus 8 min 42 s at others.\[38\]
- LiveChat 2022: 10 min 29 s average session, 47 s first response.\[39\]

### 5.4 India and e-commerce
- Only vendor blogs with no stated method:
  - Elision: BFSI AHT 5.5 to 7 min;\[40\]
  - Salesforce India page: retail AHT "about 5 minutes";\[41\]
  - Mindful: e-commerce 3.41 min.\[42\]
- No independent Indian food-delivery benchmark was found.

### 5.5 Lookup and screen switching
- **Salesforce State of Service 6th ed. (vendor survey, 2024):** "58% of agents at underperforming organizations toggle between multiple screens to find what they need — compared to 36% at high performers". Agents spend "just 39% of their time servicing customers".\[43\]\[44\]
- **Verint 2026 (vendor survey of 1,000 agents):** "In 45% of calls, agents spend an average of three minutes searching for answers."\[45\]
- **HBR, 29 Aug 2022 (Murty, Dadlani, Das; log data from 137 users; authors from vendor Soroco):** workers toggled "roughly 1,200 times each day", losing "roughly 9% of their time at work".\[46\]
- **CCW 2024 (via vendor Cresta):** "73% of contact center leaders say agents waste too much time looking up knowledge".\[47\]
- **ContactBabel** reports a figure on the share of call time spent navigating screens (Figure 66),\[35\] but its value could not be extracted.

---

## 6. Rivals

### India
- **Zomato/Eternal:**
  - CEO Deepinder Goyal on Raj Shamani's podcast (reported 7 Jan 2026 by Inshorts, Asianet, CurlyTales) said customers use AI to add insects or hair to photos. He said Zomato tracks genuineness via a "karma score" covering customers and delivery partners, and admitted, per Exchange4media, "This is where the customer karma score and rider karma score kind of blend in, and we can never be fully right"; NewsX and Startuppedia report he said the company "takes the hit 50-70 per cent of the time" in disputed cases.
  - Asianet reports "Low scores mean complaints aren't instantly approved." Goyal also said "We let go of 5,000 every month. Most of it is fraud." (Exchange4media), out of 7 to 8 lakh active delivery partners a month, with fraud including "order being marked as delivered" without delivery and COD misuse (Reported).
  - **50:50 refund-sharing (Reported, Inc42 and MediaNama, May 2025):** Zomato had restaurants share refund costs, decided by "an AI-enabled model that continuously learns". It then paused the programme: "We have temporarily paused the program and will relaunch after incorporating the feedback". Previously restaurants could accept or reject a claim, with Zomato bearing the cost if rejected. MediaNama says restaurants "can't appeal the AI's errors".\[48\]\[49\]
  - Zomato CEO Aditya Mangla (BS, Dec 2025): "We've already rolled out safeguards and early-detection models and are scaling them responsibly."\[50\]
- **Zepto (Reported, BS Dec 2025):** VP Karthic Somalinga says "We use a mix of automated systems and human review", with ML models to "flag suspicious or inconsistent refund activity in real time, supported by periodic manual checks". Zepto is exploring open-source detectors for AI-altered images.\[50\]
- **Blinkit, BigBasket, Amazon India, Flipkart:** no decision-system sources were reached in this session.

### Non-India
- **Uber Eats (Official merchant page, AU/NZ/CA):**
  - "We track customer refund history and block customers who abuse our refund policy".\[51\]
  - "We require photos to be submitted in many cases".\[51\]
  - Escalates to "a trained team" for cases "Not filed in a reasonable time frame", "high-value orders", "alcohol items", "first-time customers".\[51\]
  - Couriers with many missing-item reports "are automatically flagged" and merchants are then not charged.\[51\]
  - Merchant deductions happen "after fraud checks".\[51\]
  - **Inferred:** this is the clearest published example of the three-sided cost allocation our panel must show.
- **DoorDash (Official merchant help):** merchants can issue full or item refunds from the Merchant Portal or Tablet. The "Order Remade Policy" requires the courier to arrive "more than 20 minutes after the estimated order ready time", within seven days, perishables only.\[33\]
  - Anecdotal: customers say refunds are blocked after a "refund limit" and escalated to a "specialist" who may take "up to an hour".\[52\]\[53\]
- **China (Reported, BS citing Chinese media):** AI refund scams around Double 11 led sellers to cancel refund-only options and introduce "credit scores for the users".\[50\]
- **Survey data (Forter, a vendor):** 45% (US) and 52% (UK) of consumers admitted misusing retail policies with AI.\[50\]
- **Deliveroo, Grab, Foodpanda, Just Eat, Instacart, Meituan, Rappi:** not researched in this session due to search budget.

---

## 7. Agentic and agent-assist evidence applicable to the panel

- **Parasuraman and Manzey 2010** (Human Factors 52(3):381 to 410; abstract and partial full text read):
  - Complacency "occurs under conditions of multiple-task load".\[54\]
  - Automation bias produces "both omission and commission errors when decision aids are imperfect".\[54\]
  - It "cannot be prevented by training or instructions" and affects experts and teams.\[54\]
  - A reviewed study found failure detection of 82% with variable-reliability automation versus 33% with constant reliability.\[55\]
  - **Inferred:** a green "refund approved" suggestion, which is right most of the time, will be rubber-stamped under queue pressure.
- **Brynjolfsson, Li and Raymond, "Generative AI at Work"** (NBER WP 31161, Apr 2023, rev. Nov 2023; full working paper text excerpts read):
  - 5,179 agents; 14% more resolutions per hour on average, 34% for novice and low-skilled workers, "minimal impact" on the most experienced.\[56\]
  - "AI assistance may decrease the quality of conversations by the most skilled agents".\[57\]
  - Improves customer sentiment, reduces requests for managerial intervention, improves retention.\[58\]
  - The tool suggested replies; agents were "free to ignore" them.\[58\]
  - **Inferred:** retrieval and summary help BPO novices (Swiggy's likely workforce), but the gain was measured on conversation replies, not adjudication.
- **CX Today / Cyara, "The Hidden Downsides of Contact Center Agent-Assist Technology" (2025; vendor-sponsored piece):**
  - Cites a 2025 study from Chinese universities: transcription freezing, dialect errors, phone number and address errors.\[59\]
  - Names "A Learning Burden", "A Compliance Burden", "A Psychological Burden".\[59\]
- **CX Today (Zendesk-sponsored):** agents "toggling between their CRM, their AI knowledge base, their ticketing system, their phone".\[60\]
- **No Jitter (Forrester's Riccardo Pasto):** "smarter customer service tech, but more cognitive load on the people behind the screens".\[61\]
- **Automation bias systematic review** (Goddard et al., JAMIA 2012, PMC3240751): only a snippet was read; cite only as a pointer.
- **Patterns supported (Inferred from the above plus Uber Eats and DoorDash rules):**
  - policy-as-conditions checklist;
  - order timeline against cutoffs;
  - evidence panel with provenance (customer photo vs delivery-partner photo vs GPS log);
  - dated raw cross-party events;
  - audit trail of rule and data version;
  - value ceilings and approval queue;
  - deliberate "reason required" override.

---

## 8. Other parameters

- **Consumer Protection (E-Commerce) Rules 2020 (Law, in force 23 Jul 2020, via Lexology and others):**
  - A grievance officer must acknowledge complaints within 48 hours and redress them within one month.
  - A ticket number must be provided for tracking.
  - Return and refund information must be displayed.\[19\]\[62\]
- **Dark Patterns Guidelines 2023 (Law):** 13 prohibited practices, including drip pricing and false urgency. On 5 Jun 2025 the CCPA directed platforms to self-audit for dark patterns within three months (MediaNama, Jul 2026).\[63\]
- **CCI (Reported, MediaNama Jul 2026):** dismissed a complaint against Zomato over platform fees and pricing.\[63\]
- **DPDP Act 2023 (Law; provisions not re-verified this session):**
  - purpose limitation and data minimisation apply;
  - showing a delivery partner's or restaurant's history to a customer-support agent needs a defined purpose and the minimum necessary fields.
  - **Inferred:** role-based views and dated events limited to the dispute's relevance.
- **Gig-worker rights (not verified this session):** state platform-worker laws (Rajasthan 2023, Karnataka 2025) and the Code on Social Security contain transparency provisions on automated decisions. Verify the specifics before citing.
- **Restaurant payout deductions:**
  - Zomato's refund-sharing backlash (Reported) and Uber Eats' "order error adjustments" (Official) show cost allocation is contested.\[51\]\[64\]
  - Swiggy's policy says customer cancellation fees compensate "Merchants and Delivery Partners",\[14\] but the split is not published.
- **Fraud typologies (Reported):**
  - AI-edited photos (BS Dec 2025);\[50\]
  - marked-delivered-but-not-delivered and COD abuse (Goyal);\[65\]
  - app cloners, tampered apps, GPS spoofing, multi-account devices (SHIELD);
  - bulk cancellation and 100% refund claims (Swiggy chatbot repost).
- **Metrics:**
  - AHT and resolution time (Swiggy goal);
  - CSAT;
  - repeat contact (Zendesk CX Trends: "74% are frustrated when they have to repeat information", via subagent);\[66\]
  - override rate;
  - false-positive cost (genuine customer denied; restaurant wrongly debited);
  - false-negative cost (fraud paid; the Supr Daily estimate of up to 25% of refunds issued incorrectly).\[13\]
- **Accessibility and ergonomics (Inferred):** agents working 5-hour chat shifts from home (per the job ad) will likely use laptops. Design for 1366x768, keyboard-first actions, WCAG 2.2 AA contrast, and do not rely on colour alone for policy pass/fail.

---

## (a) Parameters table

| Parameter | What is known | Evidence tier | Source (date) |
|---|---|---|---|
| Order stage / time since placement | 100% cancellation charge after placement | Official | Swiggy refund policy (accessed 29 Sep 2026); @SwiggyCares (about Aug 2025) |
| Fault attribution | Penalties when reasons are "not attributable to Swiggy" | Official | Swiggy refund policy |
| Address / contactability | Wrong address, outside zone, unreachable buyer | Official | Swiggy refund policy |
| Item unavailability | Buyer contacted; entitled to cancel | Official | Swiggy refund policy |
| Payment mode | Prepaid refund withheld vs recovery from next postpaid order | Official | Swiggy refund policy |
| Report before "marked delivered" | Condition visible in snippet; full context not seen | Official (partial) | Swiggy refund policy snippet |
| ETA breach / platform delay | Regulator view: no penalty for platform-caused delay | Reported | Business Standard (21 May 2025) |
| Issue type (status, cancellation, location, delivery instruction) | Agent ticket categories | Anecdotal | Job ads (2021) |
| Live tracking / rider location | CRM owns Live Tracking Screen; AI checks rider location | Official / Reported (low-tier) | startup.jobs JD; Pathfinder blog |
| Delivery photo | Poor photos linked to up to 25% incorrect refunds | Reported (vendor) | AWS Supr Daily case study |
| Customer evidence photo | Instant refunds on AI-edited images | Reported | Business Standard (1 Dec 2025) |
| Device signals | App cloners, tampering, GPS spoofing, multi-account devices | Official quote + vendor | SHIELD case study; Business Wire India (20 May 2024) |
| Refund / cancellation frequency | Guardrails after dozens of cancels and 100% refund claims | Reported (secondary) | Medium repost of Swiggy post |
| Behavioural pattern flags | Swiggy: not published. Zepto: ML flags plus manual checks | Reported | Business Standard (Dec 2025) |
| Refund history score | Zomato "karma score" | Reported | Inshorts, Asianet (Jan 2026) |
| Customer value tier | Zomato email: claims mostly from "high-value users" | Reported | MediaNama (May 2025) |
| High-value order / first-time customer / alcohol escalation | Escalated to trained team | Official (Uber Eats) | Uber Eats merchant page |
| Delivery-partner missing-item rate | Auto-flag; merchant not charged | Official (Uber Eats) | Uber Eats merchant page |
| Restaurant permission to accept/reject claim | Zomato previously allowed; removed under 50:50 | Reported | Inc42 (May 2025) |
| Restaurant rejection rate | >3% daily leads to suspension (Zomato, older) | Reported | Deccan Herald |
| Courier lateness at restaurant | >20 min after ready time; within 7 days (DoorDash) | Official (DoorDash) | DoorDash merchant help |
| Escalation channel / regulatory clock | 48 h acknowledge, 1 month redress | Law | E-Commerce Rules 2020 |
| Vertical (Food vs Instamart) | Separate complaints and apps; rules not published | Inferred | Trustpilot; BS |
| OTP / delivery confirmation | Not found in public Swiggy sources this session | Not found | n/a |

## (b) Typology table

| Type | Purpose | Typical info | Strengths | Weaknesses | Fit |
|---|---|---|---|---|---|
| Unified agent desktop | Handle one ticket fast | Chat, profile, macros | Speed, familiarity | Ticket-centric; lookups for other parties | Low to medium |
| Case-management console | Govern multi-step cases | Case, SLA, approvals, related records | Audit, SLA | Tab sprawl | Medium (borrow audit/SLA) |
| Entity 360 timeline | Full history of one entity | Chronological events | Context in one place | Person-centred judgement risk | Medium (borrow timeline) |
| Order-centred incident view | Resolve one disputed order | Order timeline, parties, evidence, policy | Matches dispute structure | Integration effort | **High (core)** |
| Supervisor ops dashboard | Staffing, queues | AHT, backlog, SLA | Macro control | Not case-level | Secondary |
| QA/analytics dashboard | Consistency | Samples, override rate | Measures bias/drift | After the fact | Needed for metrics |
| Copilot sidebar | Assist replies/lookup | Suggestions, KB | Novice gains (+34%) | Automation bias, load | Only fact retrieval |
| Autonomous AI + escalation | Absorb volume | Summary to human | Scale | Humans get hardest cases | Upstream feeder |
| Approval/exception queue | Threshold control | Items over ceiling | Four-eyes control | Latency | For high-value refunds |
| Dispute/chargeback console | Evidence-based adjudication | Claim, evidence by type, deadlines | Evidence discipline | Adversarial framing | **High (evidence model)** |

## (c) Open questions for the expert interview (former American Express design-team lead)
- How did Amex dispute tools show evidence provenance (cardmember statement vs merchant document vs system log), and what reduced reviewer time most?
- Were risk scores ever hidden from reviewers on purpose? What happened to consistency and speed when they were shown vs hidden?
- How were reason codes and policy conditions shown: a checklist, a decision tree, or free text? Which one produced fewer overrides later reversed?
- What value ceilings and approval tiers existed, and how were they shown so they did not anchor the decision?
- How did you measure "effort" beyond AHT (clicks, screens, lookups, reopen rate)?
- How did you design for outsourced or novice reviewers compared with in-house experts?
- What audit-trail detail did compliance require (rule version, data snapshot), and did showing it to reviewers help or distract?
- How did you handle history for repeat claimants without turning it into a label? Did dated raw events work better than counts?
- What design choices reduced rubber-stamping of system suggestions under queue pressure?
- How did regulation (for example, Reg E/Reg Z timelines) shape the on-screen time display, and what is the Indian parallel (48 h / 1 month)?
- In three-party disputes (cardmember, merchant, network), how was cost allocation made visible to the reviewer?
- What would you test first in a 20-minute usability session with support agents?

## (d) Implications for the interface design
- **Centre on the order, not the person (Inferred from Zomato backlash, DPDP).** The header shows order ID, vertical, value, payment mode, stage and time elapsed. Parties appear as three equal columns with role-limited fields.
- **Policy as conditions, not verdicts (Official policy structure).** Each clause is shown as a row, for example:
  - "Cancelled after placement: Yes, 00:03 after placement";
  - "Delay attributable to platform: ETA 30 min, actual 58 min".
  - Each row states its data source. No green "approve" badge.
- **Timeline against cutoffs (Swiggy "before marked delivered"; DoorDash 20-min rule).** A horizontal timeline of placed, accepted, prepared, picked up, marked delivered and complaint raised, with policy cutoffs overlaid.
- **Evidence panel with provenance (Supr Daily 25%; AI-image cases).** Each item is labelled by type and source (customer upload, delivery-partner photo, GPS trace, restaurant note), with capture time and metadata where available. Show "image forensics result: not run / run, output X" as a fact, not a fraud verdict.
- **Cross-party history as dated raw events (Zomato karma critique).** For example: "3 prior claims: 12 Jan missing item, refunded; ...". No aggregate score, colour ranking or "trust tier". Apply the same format to restaurant and delivery-partner history.
- **Guardrails (Uber Eats escalation criteria; Databricks human fallback).** Show the value ceiling and escalation conditions as rules that route to an approval queue. The agent sees why a case was routed ("order value above ceiling").
- **Audit trail (Databricks action signals; E-Commerce Rules).** Record which conditions were shown, which data version, what the agent chose, and a mandatory reason on deviation. This enables override-rate QA.
- **Regulatory clock (E-Commerce Rules).** Show the time since complaint against 48 h and 1 month, and the channel of origin (app, email, X, NCH).
- **Cognitive load (Salesforce 58% toggling; HBR 9%; CX Today).** One screen, no tabs for the core decision, keyboard shortcuts, progressive disclosure for raw logs.
- **Metrics for the prototype test:**
  - time to decision;
  - number of lookups and screens;
  - decision consistency across agents on the same case set;
  - override and reversal rate;
  - agent-reported effort (NASA-TLX).
  - AHT is secondary, because automation shifts harder cases to humans (ContactBabel).

## Caveats
- The search budget prevented coverage of AmbitionBox, Reddit, consumer-commission orders, Blinkit, Amazon and Flipkart, and the non-India rivals beyond Uber Eats and DoorDash. These are gaps in this session, not proof that the evidence is absent.
- The Swiggy refund policy text was read via search excerpts because the page did not render.
- The final CCPA outcome needs verification (the SHIELD announcement is dated 20 May 2024 by Business Wire India).
- Vendor case studies (PubNub, SHIELD, AWS, Databricks) are marketing and may overstate results. The Databricks "100% automated" claim conflicts with its own human-fallback design.
- The dashboard typology product descriptions were not re-verified against vendor documentation in this session.

## Sources

1. [Chatbots at Swiggy - DEV Community](https://dev.to/abeyalex/chatbots-at-swiggy-9bp)
2. [How Swiggy designed its chatbot and cut-down the cost effectively.](https://medium.com/@jayraj_singh/how-swiggy-designed-its-chatbot-and-cut-down-the-costing-effectively-a0ff12577545)
3. [Software Dev Engineer I- Backend Dev at Swiggy](https://startup.jobs/software-dev-engineer-i-backend-dev-swiggy_in-1822723)
4. [Swiggy Is Revolutionizing Delivery](https://www.pubnub.com/customers/swiggy/)
5. [www.cbinsights.com](https://www.cbinsights.com/company/layer-coms/people)
6. [Redefining Customer Support: Swiggy’s Enterprise-Scale AI Agent Built with Databricks](https://www.databricks.com/blog/redefining-customer-support-swiggys-enterprise-scale-ai-agent-built-databricks)
7. [Redefining Customer Support: Swiggy’s Enterprise-Scale AI Agent Built with Databricks](https://databricks.com/blog/redefining-customer-support-swiggys-enterprise-scale-ai-agent-built-databricks)
8. [From Billions of Events to Milliseconds of Insight: Architecting Swiggy’s Real-Time AI Data Platform](https://medium.com/@vsanmed/from-billions-of-events-to-milliseconds-of-insight-architecting-swiggys-real-time-ai-data-a43a2697cdee)
9. [Swiggy: Neural Search and Conversational AI for Food Delivery and Restaurant Discovery - ZenML LLMOps Database](https://www.zenml.io/llmops-database/neural-search-and-conversational-ai-for-food-delivery-and-restaurant-discovery)
10. [AI-CENTRIC CUSTOMER SERVICE: SWIGGY'S INNOVATIVE APPROACH TO FOOD DELIVERY - PRTF Blog](https://pathfinderfoundation.co.in/blog/ai-centric-customer-service-swiggys-innovative-approach-to-food-delivery)
11. [Swiggy Leverages SHIELD’s Device-First Risk Intelligence to Enhance Its Fraud Prevention and Detection Capabilities](https://shield.com/case-studies/swiggy)
12. [SHIELD to Swiggy’s fraud prevention and detection capabilities](https://www.varindia.com/news/SHIELD-to-enhance-Swiggy%E2%80%99s-fraud-prevention-and-detection-capabilities)
13. [suprdaily case study](https://aws.amazon.com/solutions/case-studies/suprdaily-case-study/)
14. [Refund & Cancellation](https://www.swiggy.com/refund-policy)
15. [Swiggy Cares on X: "@Its\_ssshekhawat According to Swiggy's policy, if you cancel your order even one second after it has been placed, you will incur a cancellation fee amounting to 100% of the order value. We cannot refund the cancellation charges. ^Say" / X](https://x.com/SwiggyCares/status/1960745315683700883?lang=en)
16. [Swiggy on X: "@NitinGabrani As mentioned in our cancellation policy - a 100% cancellation fee is applicable post placing the order. As much as we would like to help we'd not be able to process the refund. ^Ansh" / X](https://x.com/Swiggy/status/1878314670081364391)
17. [CCPA Probes Zomato, Swiggy Cancellation and Refund ...](https://www.medianama.com/2025/05/223-ccpa-probes-zomato-swiggy-cancellation-refund-policies/)
18. [Contact Us - Swiggy](https://www.swiggy.com/corporate/contact-us/)
19. [Consumer Protection (E-Commerce) Rules 2020](https://www.seraphicadvisors.com/insights/blogs/consumer-protection-ecommerce-rules-2020-6654697d740abe88738c5fdf)
20. [Senior Product Manager — Swiggy · freehire](https://freehire.me/jobs/senior-product-manager-swiggy-p6zblx4b)
21. [Urgent hiring for swiggy customer Care executive ||](https://www.jobvalley.online/2021/08/urgent-hiring-for-swing-customer-care.html)
22. [Swiggy Chat Process Job Description](https://www.scribd.com/document/571764352/JD-Swiggy)
23. [The 23 Top BPO Companies in the World - Running Remote](https://runningremote.com/bpo-companies/)
24. [Swiggy Delivery Partner App - Apps on Google Play](https://play.google.com/store/apps/details?id=in.swiggy.deliveryapp&hl=en_US)
25. [Swiggy integrates AI chatbots to enable ordering via ChatGPT, Claude and Gemini - Storyboard18](https://www.storyboard18.com/brand-marketing/swiggy-integrates-ai-chatbots-to-enable-ordering-via-chatgpt-claude-and-gemini-88325.htm)
26. [CCPA likely to direct Zomato, Swiggy to revise cancellation, refund policy](https://www.business-standard.com/industry/news/ccpa-zomato-swiggy-cancellation-refund-policy-update-directive-125052101628_1.html)
27. [CCPA may direct Zomato, Swiggy to revise cancellation and refund policies](https://www.storyboard18.com/brand-marketing/ccpa-may-direct-zomato-swiggy-to-revise-cancellation-and-refund-policies-66720.htm)
28. [Add Tribune As Your Trusted Source](https://www.tribuneindia.com/news/nation/miss-you-lot-woman-accuses-swiggy-agent-of-sending-creepy-messages-company-acts-on-her-complaint-405008/amp)
29. [Swiggy Customer Support Executive Reviews](https://www.glassdoor.com/Reviews/Swiggy-Customer-Support-Executive-Reviews-EI_IE952680.0,6_KO7,33.htm)
30. [Swiggy Reviews](https://www.trustpilot.com/review/swiggy.com?page=5)
31. [Swiggy Reviews](https://ca.trustpilot.com/review/swiggy.com)
32. [Reducing Swiggy’s Customer Support Queries: A Product-Led Strategy Backed by Real Data](https://medium.com/@f20231044/reducing-swiggys-customer-support-queries-a-product-led-strategy-backed-by-real-data-f30f23c09424)
33. [How to Resolve Missing Orders on DoorDash](https://help.doordash.com/en-us/merchants/article/what-do-i-do-if-a-customer-reports-an-item-is-missing)
34. [business%2Frestaurant owners slam zomato over rejection policy 973163](https://www.deccanherald.com/amp/story/business%2Frestaurant-owners-slam-zomato-over-rejection-policy-973163.html)
35. <https://assets.ringcentral.com/us/report/us-dmg-2024.pdf>
36. [The UK Contact Centre Decision-Makers’ Guide 2024 (21st edition) Sponsored by](https://www.encoded.co.uk/wp-content/uploads/2024/04/ContactBabel-DMG-Full-Report-2024.pdf)
37. [Call Center FCR Benchmark 2024 Results by Industry](https://www.sqmgroup.com/resources/library/blog/call-center-fcr-benchmark-2024-results-by-industry)
38. [21 Key Live Chat Statistics for Customer Service Teams](https://www.helpscout.com/blog/live-chat-statistics/)
39. [61 Live Chat Stats To Help Build Stronger Customer Connections in 2022](https://getstream.io/blog/live-chat-statistics/)
40. [Indian Banks Are Beating 2026 Contact Center Benchmarks](https://www.elisiontec.com/how-leading-indian-banks-are-outperforming-2026-contact-center-benchmarks/)
41. [11 Top Call Centre Metrics & KPIs to Measure Performance](https://www.salesforce.com/in/service/contact-center/call-center/metrics/)
42. [» Average Handle Time: The Ultimate Guide for Contact Centers](https://getmindful.com/guide/average-handle-time/)
43. [Salesforce Report: Teams Tap AI and Data to Drive Revenue as Service Expectations Rise - Salesforce](https://www.salesforce.com/news/stories/customer-service-statistics-2024/)
44. [Insights from over 5,500 customer service professionals worldwide on](https://www.salesforce.com/content/dam/web/en_us/www/documents/e-books/service/sixth-edition-state-of-service.pdf)
45. [Nearly One-Third of Contact Center Agents Plan to Quit as Agent Experience Falls Short](https://www.verint.com/press-room/2026-press-releases/nearly-one-third-of-contact-center-agents-plan-to-quit-as-agent-experience-falls-short/)
46. [How Much Time and Energy Do We Waste Toggling Between Applications?](https://hbr.org/2022/08/how-much-time-and-energy-do-we-waste-toggling-between-applications)
47. [Reduce Average Hold Time in Contact Centers](https://cresta.com/guides/reduce-average-hold-time-contact-center)
48. [Zomato Pauses Refund-Sharing Policy Amid Partner Backlash](https://www.medianama.com/2025/05/223-zomato-pauses-refund-sharing-policy/)
49. [Exclusive: Zomato Puts 50:50 Refund Sharing With Restaurants On Hold](https://inc42.com/buzz/zomato-puts-5050-refund-sharing-with-restaurants-on-hold/)
50. [Food companies take note of rising AI-generated images for refund](https://www.business-standard.com/industry/news/food-companies-take-note-of-rising-ai-generated-images-for-refund-125120101409_1.html)
51. [Order Errors | Uber Eats](https://merchants.ubereats.com/au/en/order-errors)
52. [Missing items from your DoorDash order? What to do...and what not to do - Ridesharing Driver](https://www.ridesharingdriver.com/doordash-missing-item/)
53. [it.trustpilot.com](https://it.trustpilot.com/review/doordash.com)
54. [Complacency and Bias in Human Use of Automation: An Attentional Integration - Raja Parasuraman, Dietrich H. Manzey, 2010](https://journals.sagepub.com/doi/10.1177/0018720810376055)
55. [(PDF) Complacency and Bias in Human Use of Automation: An Attentional Integration](https://www.researchgate.net/publication/47792928_Complacency_and_Bias_in_Human_Use_of_Automation_An_Attentional_Integration)
56. [Generative AI at Work](https://www.nber.org/papers/w31161)
57. [NBER WORKING PAPER SERIES GENERATIVE AI AT WORK Erik Brynjolfsson Danielle Li](https://www.nber.org/system/files/working_papers/w31161/w31161.pdf)
58. [NBER WORKING PAPER SERIES GENERATIVE AI AT WORK Erik Brynjolfsson Danielle Li](https://mitsloan.mit.edu/shared/ods/documents?PublicationDocumentID=9765)
59. [The Hidden Downsides of Contact Center Agent-Assist Technology - CX Today](https://www.cxtoday.com/contact-center/the-hidden-downsides-of-contact-center-agent-assist-technology-cyara/)
60. [Always‑On Without Always‑Burned‑Out: The Human Cost of AI‑Led CX - CX Today](https://www.cxtoday.com/contact-center/always%E2%80%91on-without-always%E2%80%91burned%E2%80%91out-the-human-cost-of-ai%E2%80%91led-cx-zendesk-cs-0064/)
61. [Smarter systems, tired agents: The hidden cost of AI CX](https://www.nojitter.com/contact-centers/smarter-systems-tired-agents-the-hidden-cost-of-ai-driven-cx)
62. [E-Commerce - Consumer Protection (E-Commerce) Rules, 2020 notified - Lexology](https://www.lexology.com/library/detail.aspx?g=ea0f67cd-3c27-48e3-bd0b-e8216f9219c8)
63. [CCI dismisses Zomato complaint over platform fees, pricing](https://www.medianama.com/2026/07/223-cci-complaint-zomato-fees-pricing/)
64. [How Zomato’s Opaque Ad Model Is Affecting Small Restaurants](https://www.medianama.com/2025/06/223-zomato-opaque-ad-model-small-restaurants-unsustainable-spending/)
65. [Are Zomato Customers Using AI To Claim False Refunds? Here’s What Deepinder Goyal Has To Say](https://curlytales.com/india/trending/are-zomato-customers-using-ai-to-claim-false-refunds-heres-what-deepinder-goyal-has-to-say/)
66. [Contextual Intelligence Becomes the New Standard for Exceptional Customer Experience in 2026](https://www.zendesk.com/newsroom/press-releases/contextual-intelligence-becomes-the-new-standard-for-exceptional-customer-experience-in-2026/)
