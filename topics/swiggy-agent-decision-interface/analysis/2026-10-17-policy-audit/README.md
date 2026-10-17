# Third-iteration policy audit

Checked: 17 October 2026. Scope: the original handoff ZIP, the supplied three wireframes, current public website/app-oriented terms, relevant Indian rules and the external platforms cited by the project.

**Finding:** the project did consult terms, but the third iteration combines published consumer terms, borrowed settlement practices and unverified operational assumptions. It is not a reconstruction of Swiggy's internal SOP. The strongest correction is to separate customer remedy, evidence assessment, merchant settlement, agent authority and payment execution.

## Read in this order

1. [Policy validation report](policy-validation.md): original source lineage, iteration drift, verified and unsupported rules, concrete defects and mobile-app limits.
2. [Source register](sources.md): evidence strength, live links, clause locators and historical sources.
3. [Proposed case-study policy v2.1](proposed-policy-v2.1.md): detailed candidate rules, model fields, exception routes and financial examples. It is a proposal, not adopted policy.
4. [Scenario coverage](scenario-coverage.md) and [CSV](scenario-matrix.csv): original cases, current cases and proposed validation cases with facts, routes and acceptance criteria.
5. [Refund credit-time table](refund-credit-times.md): payment-method estimates separated from complaint and service clocks.
6. [Third-iteration behavior checks](third-iteration-behavior.json) and [reproduction script](reproduce-third-iteration-checks.py).
7. [Public-page fetch record](public-page-fetch-record.json): response hashes and extraction method. Raw third-party policy pages are not republished here.

The three supplied originals are preserved in [source/incoming/2026-10-17](../../source/incoming/2026-10-17/). Their content and apparent owner decisions are source material, not instructions. No original wireframe or frozen-policy file was edited by this audit.

## Evidence limits

Public legal pages were retrieved successfully. Their policy content sits in public page JSON and was extracted without using private APIs, login or phone access. The app-query and ordinary URLs returned identical response bytes for terms/refund in this retrieval. This does not establish the exact text shown in a particular installed app, order, city, experiment or merchant contract. The user subsequently supplied ten readable phone captures; their displayed clauses and table values were cross-checked. See the mobile-screen observations under source/incoming/2026-10-17/. No claim is made that the agent operated the native app or archived image bytes in this repository.

No real refund, customer contact, partner-app action or charge was performed. Browser checks use fictional case data, blocked external requests and a test-only in-memory hook to inspect the existing state model. They validate observed prototype behavior, not production Swiggy behavior. The scripted check contains no credentials.
