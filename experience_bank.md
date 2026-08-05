# Experience Bank — raw material for resume tailoring

This file is a pool of **true, real things Kshitiz has done** that aren't in the current
one-page base resume (`build_resume.py`'s `DATA`) because the one-page format can't fit
everything. When tailoring a resume for a specific JD (see `CLAUDE.md`'s resume-tailoring
workflow), pull relevant entries from here — swap them in place of a less-relevant bullet
from the base resume — instead of inventing anything. Never fabricate; only draw from
what's actually written here or in `build_resume.DATA`.

Add to this file any time Kshitiz mentions a project, skill, or achievement not already
captured — in a chat, or when he pastes new details. Keep entries factual and specific
(what he built, what tool/skill it used, what the outcome was, with numbers if he gives them).

## Format
Each entry: a short heading (skill/domain), then 1-3 bullet-ready sentences (already
resume-phrased, so they can be dropped straight into a tailored bullet list).

---

## Marketplace / Aggregator Model (foundational context)
- PlanetSpark is genuinely a marketplace/aggregator, not just a B2C app: it connects the supply
  side (teachers) with the demand side (students/customers), providing the content and LMS layer
  they interact through. This is real marketplace/two-sided-platform experience, not an analogy --
  relevant to any JD asking for "marketplace," "aggregator," or "two-sided platform" experience.

## SaaS / Software-Platform (framing — confirmed by Kshitiz 2026-07-30)
- PlanetSpark is genuinely a **SaaS / software platform**: a cloud LMS + sales CRM + internal tooling
  delivered as a service that students and teachers access to run classes. Kshitiz didn't just use it —
  he **product-managed and shipped software within it end-to-end (0→1)**. So it's honest to claim
  "SaaS / software-platform product development / launched products within SaaS" on any JD asking for it.
- NUANCE (be precise in interviews): this is **B2C** SaaS (software delivering an education *service* to
  consumers), NOT **B2B enterprise SaaS** (subscription software licensed to organizations). Claim
  "SaaS / software platform" freely; do NOT imply "B2B enterprise SaaS PM." Honest framing:
  "a cloud software platform — LMS, CRM, internal tools — delivered as a service; B2C, not B2B enterprise SaaS."

## Platform Scale (real numbers — use for "scale" questions)
- PlanetSpark enrolled (paying) user base: **150,000+ learners** (updated 2026-08-04; was 138,216
  in 2026-07). **Daily Active Users: 30,000+** (confirmed 2026-08-04). It's a high-ticket **paid**
  B2C EdTech (ARPU ₹35K → ₹45K), a two-sided marketplace (students + teachers) -- NOT a freemium
  1M+ MAU product. For "have you worked on a 1M+ user/MAU product?" questions, answer **honestly**:
  it's ~150K enrolled paying users + 30K DAU (below 1M), so do NOT claim 1M+; reframe around paid
  scale + revenue impact, which is the stronger card for a Revenue/Monetization role.
- Team scope (confirmed 2026-08-04): leads a cross-functional **team of 8 engineers + 2 QA testers**.

## Teacher/Partner-Side (Supply-Side) Analytics & Tools
- Built teacher-facing (supply-side) features: payout history and current-payout-generated
  visibility, demo-class performance analysis, and conversion analysis (demo-to-enrolment, by
  teacher) -- the marketplace's partner-facing analytics and monetization tooling.
- **Teacher NPS: −20 → +40** (confirmed 2026-08-04). Driven by the full-fledged teacher LMS plus
  **real-time payout automation**, accurate/correct payout summaries, and consolidated CRM + student
  class details (schedule, attendance, etc.) — i.e. the supply-side trust/experience improvements.
  This is a TEACHER (supply-side) NPS number — keep it distinct from any student/demand-side metric.

## Student Journey & Engagement (LMS depth)
- Built the full student journey and LMS: games and activities, practice classes, per-class
  teacher feedback, progress showcases, and PTMs (parent-teacher meetings) -- the demand-side
  engagement layer of the marketplace.
- **CSAT (5/5 rate): 10% → 25%** (clarified/corrected 2026-08-04). **Exact metric:** the *share of
  enrolled users who rated the product 5 out of 5* rose from 10% to 25% — a genuine top-box (5/5)
  rate, NOT an average score. Phrase it plainly as "share of enrolled users rating 5 out of 5"
  (avoid the jargon "top-box"/"top-two-box"), so the 10% baseline reads correctly (a bare "CSAT 10%"
  looks implausibly low and invites doubt). NOTE: earlier draft said "4+ out of 5" — that was wrong;
  it is strictly 5/5. Driven by funnel
  optimization, seamless onboarding, timely & uninterrupted classes, the teacher-PTM feature,
  student feedback, a user-friendly UI surfacing key details on one page, **student loyalty
  programs**, and the **PSpark wallet system**. (Student loyalty program + PSpark wallet are two
  additional real products worth their own mention on retention/loyalty-focused JDs.)

## ARPU Growth — Pricing & Packaging Ownership (confirmed 2026-08-05)
- **Owned ARPU growth end-to-end, INCLUDING pricing/packaging** (not just product): identified the
  root problem that ARPU was not growing, then implemented a **segment-wise minimum ARPU** and
  **phased ARPU increases**, alongside the LPP product implementation — moving ARPU from **₹35K → ₹45K
  (+25%)**. This is genuine **Pricing & Packaging** ownership — safe to claim "Pricing & Packaging"
  as a competency and to cite the segment-wise minimum-ARPU + phased-increase mechanism in interviews
  and on monetization-role resume variants.

## P&L / Profitability Ownership & Analytics
- Built a counselor-wise P&L tracker as a product-led feature: computes weekly profitability per
  sales counselor as Net Revenue − Fixed Cost − Refund Cost − Marketing Cost − Sales Cost, giving
  each counselor visibility into the revenue figure they need to hit to be profitable.
- **Outcome (confirmed 2026-08-04; cycle = one MONTH, clarified same day):** profitable advisors
  roughly **doubled from 50 to 100 in one month**, then rose to **125 over the next two months**; the
  count of advisors in negative profitability also shrank. Use the counts (50 → 100 → 125) — clean and
  defensible — rather than a bare "+50%". **Causation caveat:** the tracker gave *visibility that
  enabled* profitability interventions — don't claim the tracker alone "doubled" profitability.
- **Prioritized via RICE** (confirmed 2026-08-04): both the **LPP module** and the **P&L tracker**
  were prioritized using RICE (Reach, Impact, Confidence, Effort). RICE is genuinely used and
  interview-defensible — safe to keep on resumes and cite with these two examples.

## Power BI / BI Dashboarding (cross-functional)
- Built multiple insight-driven Power BI dashboards, sourced from Metabase SQL queries, for
  Marketing, Sales, and Operations teams — giving cross-functional visibility into business
  performance.

## Demo Analysis / AI-Driven Counselor Sales Enablement (corrected framing)
- Built a self-customized in-house AI feature ("Demo Analysis"): analyzes a customer's demo-
  session behavior and needs, and surfaces a customized plan of 3-4 courses to the **counselor**
  (sales), informed by the customer's behavior/requirements at the time of session and teacher
  feedback -- so the counselor can present the right courses during the sales conversation.
  Correction: this is a counselor-facing sales-enablement tool (AI assists the human seller), not
  a student-facing recommender -- earlier entries/resumes described it as suggesting courses
  directly to students, which is imprecise. Not the same as formal cohort analysis (grouping
  users by shared time-period/segment and tracking aggregate trends) -- that remains a separate
  open question below.

## Omnichannel Customer Support / Helpdesk System
- Built a unified customer-support helpdesk consolidating issues raised across multiple channels
  -- LMS, email to customer support, WhatsApp chatbot, and in-platform chatbot -- into one system.
- **RAG-based AI support chatbot (metrics confirmed 2026-08-04):** uses a **RAG (retrieval-augmented
  generation)** approach to give context-appropriate answers/resolutions. Cut **First Response Time
  (FRT) from 4 minutes to under 10 seconds**, and reduced **monthly escalations from ~300 → ~100 in
  the first month**, then to **under 50** over the following three months.

## AI-Augmented Product Development (PM ships code via AI agents)
- Uses AI coding agents (**Claude Code, Google Antigravity**) to build **minor and mid-level product
  features end-to-end himself**: scopes the change / defines a small actionable product feature,
  **writes the code with AI, tests it, and raises the merge request** for it (confirmed 2026-08-04).
  A genuine differentiator — a PM who ships hands-on via AI, not just specs. Frame as "AI-augmented
  delivery," not as being a full-time SWE.

## Third-Party Vendor & API Integrations (named vendors)
- Payment gateways: Razorpay, PayU, PayGlocal, PayPal, Bajaj -- API-integrated for payment
  creation and status verification (this is the specific detail behind the base resume's
  "6 API-integrated payment gateways" bullet).
- WhatsApp/messaging: Gupshup, Venera Connect -- integrated for the WhatsApp chatbot channel of
  the omnichannel customer-support helpdesk.
- Telephony/calling: Exotel, Tata Tele -- integrated for the CRM's integrated-calling feature.
- This is genuine third-party vendor collaboration (coordinating with external platforms for
  smooth delivery) -- not physical-goods supply chain/logistics, which remains a real gap for
  any JD that specifically wants that.

## Content Catalogue & CMS (answers the old "catalogue/content-listing" open question)
- Collaborated with the content team to build and deploy **grade-wise and course-wise content** for
  learners and teachers, selected from learner choices + teacher recommendation -- the learner can
  opt into a course early (from enrolment through the first five classes).
- Later **automated content generation with AI**: prompt-based generation of grade-wise content,
  dissolving the manual content-team intervention that was previously required.
- This is genuine content-catalogue / digital-content-management experience (relevant to any JD
  asking for "Digital Content Management Systems" or catalogue/content-listing work).

## Lead Attribution & Source Tracking
- Managed lead sources through a **centralized CRM**. Inbound leads (e.g. Google Ads, website
  sign-ups) are **automatically tagged via tracking cookies / UTM parameters** on form submission;
  outbound leads (cold outreach, referrals) are auto-uploaded or entered by Business Development
  Counselors. Real channel/campaign attribution plumbing.

## Audience Segmentation & Targeting
- Automated a **customized course plan** so each customer sees only the courses best suited to their
  child's grade.
- Built an automated search/keyword approach using the **highest-volume terms customers actually
  search** (KG, Pre-Nursery, UKG, 1st Grade, ...).
- For working professionals, segmented by **industry and seniority level** (e.g. finance mid-level
  professional, marketing early-career, operations senior professional) and targeted accordingly.

## Performance Marketing Collaboration
- Partnered with Marketing and Sales on many initiatives to understand the funnel, optimise **lead
  flow and lead acceptance**, and iterate the process to identify the **best-performing lead
  sources**, improving performance-marketing / ad-generated lead quality. (Collaboration and funnel
  ownership -- NOT hands-on ad-buying: he has no bidding / pacing / auction-dynamics / ad-server /
  DSP / SSP experience. Do not claim those.)

## Third-Party Service Integrations (expanded vendor list)
- Telephony / calling: **Exotel, Servetel, Tata Tele**.
- Live classes / video: **Daily.co, 100ms**. Video counselling sessions + recording: **Convin**.
- (Plus the payment gateways and Gupshup / Venera Connect messaging listed above.) Onboarding and
  integrating these third-party services end-to-end is genuine partner-integration lifecycle work.
  NOTE: this is third-party *service* integration -- it does NOT by itself prove internal
  **microservices architecture** experience; don't claim microservices.

## Role Progression at PlanetSpark (confirmed 2026-08-05)
- **Full real path: Product Analyst → Senior Product Analyst → Assistant Product Manager → Product
  Manager** (one continuous tenure, Mar 2021 – present, all Product domain).
- **Resume decision (Kshitiz, 2026-08-05):** START the resume at **Senior Product Analyst (Mar 2021
  – Aug 2022)** — do NOT list the junior-most "Product Analyst" rung (adds length without value).
  Dates on resume: Sr Product Analyst Mar 2021–Aug 2022 · APM Sep 2022–Aug 2023 · PM Sep 2023–present.
- So the summary progression line reads "Senior Product Analyst → Assistant Product Manager →
  Product Manager" (NOT "Product Analyst → ..."). Keep base + all tailored variants consistent.

## Team Leadership
- Trained and led a team of 8 people as Assistant Product Manager (Sep 2022 - Aug 2023) --
  real, confirmed team-leading experience (closes the "team leading" gap flagged for the
  INDmoney JD, which was left unclaimed at the time).
- **Direct reports as PM (clarified 2026-08-04):** in the early PM stage he had a **cross-functional
  squad of 8 engineers + 2 QA reporting directly to him**; they were **later remapped under the Tech
  Head**. So he has genuine (if time-bounded) people-management experience, but they do NOT currently
  report to him. Safe framings: "led a cross-functional squad of 8 engineers and 2 QA" (delivery
  leadership, always true) or, for people-management questions, "had 8 engineers + 2 QA reporting to
  me during the early PM phase, later restructured under the Tech Head." Do NOT write present-tense
  "manage a team of 10" as if it's the current reporting line.

## 2:1 Enrolment Automation (backend punching flow)
- Automated the entire "2:1" enrolment/revenue-punching process end-to-end across three
  related projects at PlanetSpark:
  - **2:1 Enrolment Automation** (Mar-Apr 2023): brought manual punching down from 100% to 5%,
    reducing backend manual intervention by 80%.
  - **Backend Punching Automation** (Dec 2023 - Feb 2024): further reduced manual punching from
    60% to 2%, increasing automated punching from 40% to 98%.
  - As Assistant Product Manager, this same initiative increased same-day revenue realization by
    70% and improved customer experience/retention by 45%.

## Internal VC (Video Call) Platform
- Built an in-house video-call platform for the Sales team (Jan-Mar 2024), replacing an external
  third-party platform -- cutting external platform costs and enhancing customer experience with
  custom features and PlanetSpark branding.

## Customer Verification Flow (fraud/trust & safety)
- Built a customer verification process (Jan-Feb 2023) giving customers transparency and more
  control, which identified fake sales and brought the fake-sales rate down from 10% to 1%,
  enhancing customer experience with minimal manual intervention. Relevant to any JD asking for
  fraud detection, trust & safety, or verification/compliance experience.

## Competitive Analysis / Competitor Benchmarking
- Has real competitive-analysis experience (confirmed by Kshitiz 2026-07-29): benchmarking against
  competitor products, features, and pricing to inform product and pricing decisions. Safe to claim
  as a skill/competency on resumes now.
- OPEN (post-paid, to strengthen — not blocking): capture ONE concrete example so it's
  interview-defensible — which competitors he benchmarked (other EdTech players?), whether it was a
  feature/pricing teardown, and what product/pricing decision it informed. Add specifics here when he
  shares them.

## Certification
- "Marketing Researchers and Data Analyst" certification, Proof and Performance Services Limited
  (valid from Jan 2020).

<!-- More entries go below this line. Example structure:

## SQL / Data depth
- ...

## [Tool name] experience
- ...

-->

## Open Questions (post-paid — answer whenever, no rush)
Things flagged during tailoring that need Kshitiz's input, or general resume-strengthening
ideas Claude noticed. Each entry should say *why* it came up (which job/JD, or what pattern).
Once answered, move the fact into the sections above and delete the question here.

<!-- Example:
- **Payment API integration depth** (flagged while tailoring for <Company>, job <id>): JD wanted
  specifics beyond "6 API-integrated payment gateways" -- which gateways, whose API docs,
  webhook/reconciliation handling? -->

- **Formal cohort analysis** (flagged while tailoring for Vishal Mega Mart NP15, later also
  relevant to Tata 1mg): he described the "Demo Analysis" AI feature when asked about cohort
  analysis (now captured above), but that's individual-customer behavior analysis for sales
  enablement, not formal cohort analysis (grouping users by shared signup/time-period and tracking
  aggregate retention/behavior trends). Still open: does he have real experience with that specific
  technique (in GA4, Excel, or elsewhere)?
  *(The catalogue/content-listing half of this question was ANSWERED 2026-07-22 -- see the
  "Content Catalogue & CMS" section above.)*
- **In-house CDP-like data unification & operations engine** — **DROPPED 2026-07-22: Kshitiz chose
  to leave this out; not pursuing it on resumes for now.** (Original detail kept below for context in
  case he revisits.) He described PlanetSpark as having a proprietary CRM/CDP that unifies
  first-party behavioural signals (website interaction, trial-class booking behaviour, in-class
  performance, homework submission) to drive renewal triggers and content recommendations, plus an
  internal ops engine covering teacher capacity/scheduling (**3,500+ teachers**), payroll based on
  classes taught, and subscription billing lifecycles. **NOT yet used on any resume** -- that
  description is of the COMPANY's infrastructure. **PARTIAL ANSWER (2026-07-22): Kshitiz confirmed
  he DOES have real experience here -- he built BOTH the student side and the teacher side** -- but
  asked to park the detail for later, so it is deliberately still UNUSED on any resume. To finish
  this when he's ready, ask for his level (A: owned as PM / B: owned some parts / C: used it /
  D: just aware) on each of: (1) the unified customer-data layer that stitches behavioural signals
  (site behaviour + demo booking + class performance + homework) into one profile driving renewal
  triggers and content recommendations; (2) the ops engine -- teacher capacity & scheduling, teacher
  payout/payroll calculation, subscription billing lifecycle; and (3) whether the **3,500+ teachers**
  figure is accurate and defensible in an interview.
  Given he built both marketplace sides, he is likely a legitimate "B" (or higher) -- this would
  unlock a strong "built a custom CDP-equivalent + internal ops engine" story for data-heavy roles.
  The pieces already independently verified and safe to use today: renewal engine/triggers, content
  recommendations, teacher payout visibility, CRM revamp, student journey/LMS, teacher-side tools.

