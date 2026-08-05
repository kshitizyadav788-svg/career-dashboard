# Project Log & Handoff — Career Dashboard

A running record of what has been built and decided, so any future session (or a different AI
platform) can continue with **zero lost context**. Newest at bottom. Read `CLAUDE.md` first for the
operating rules, then this for "what state are we actually in."

---

## 2026-08-05 — BASE RESUME + PORTFOLIO + DASHBOARD RESTRUCTURE (major)

Driven by a multi-round review of the one-page resume (Kshitiz + a second AI reviewer). The base
resume was rebuilt and the change propagated across the whole repo. **This supersedes the single-role
master-resume structure described in the 2026-07-22 snapshot below.**

**What changed (all in one continuous, verified pass):**
- **`build_resume.py`** — `DATA` + `render()` rebuilt to the REAL 3-role progression at PlanetSpark
  shown as dated sub-entries under one company: **Senior Product Analyst (Mar 2021–Aug 2022) →
  Assistant Product Manager (Sep 2022–Aug 2023) → Product Manager (Sep 2023–Present)**. (Full real
  path is Product Analyst → Sr Product Analyst → APM → PM; Kshitiz chose to START at Sr Product
  Analyst — the junior-most rung is intentionally omitted.) Added: compact honest **metrics strip**
  under the header; **Core Competencies moved directly below the summary** (transferable-first for an
  industry switch); **clickable email/LinkedIn hyperlinks**; **"Pricing & Packaging"** competency
  (Kshitiz confirmed he owned the ₹35K→₹45K ARPU move via segment-wise minimum ARPU + phased
  increases). Positioning de-EdTech'd → growth/monetization/payments/workflow-automation.
  `keyword_coverage_score()` updated to read the new `data["roles"]` shape.
- **New verified numbers** (added to base + logged in `experience_bank.md`): CSAT = share of enrolled
  users rating **5/5** rose 10%→25%; **teacher NPS −20→+40** (payout automation + teacher LMS);
  **RAG support chatbot** FRT 4min→<10s, monthly escalations ~300→<50; **advisor P&L tracker** grew
  profitable advisors 50→100 (one month)→125 (next two); scale **150K enrolled / 30K DAU**; leads a
  **squad of 8 engineers + 2 QA** (reported to him early-PM, later remapped under Tech Head); **ships
  minor/mid features via Claude Code** (AI-assisted dev, merges reviewed by eng).
- **Honesty holds:** did NOT add A/B-testing/experimentation (no controlled-experiment experience);
  did NOT cite the funnel "enhanced by 50%" (no clear denominator — open question); kept "production
  GenAI" (real). "Pricing & Packaging" only added because pricing ownership was confirmed real.
- **`index.html`** — `resumeDoc` object + `renderResumeDoc()` rebuilt for the 3-role structure +
  metrics strip; `profile` title/currentRole fixed ("Product Manager"); overview header string and
  the `resume` analysis object (strengths/weaknesses/positioning/keyword note) updated to match.
- **`portfolio.html`** — hero summary (scale + payments), work-slide numbers updated to the verified
  figures (replaced a couple of unverified stats like "80% class conduction/90% on-time" with the
  verified teacher NPS), "counselor"→"advisor" wording, education BBA **2018–2021**, and the journey
  axis fixed **Intern → Sr Product Analyst**.
- Base resume regenerated via `fit_to_page()` → one page, ~95% fill, one-page-full rule intact.

**Deferred (NOT done in this pass):** the **~48 existing tailored resumes** (EXT*/`seed_jobs.json`)
still render with the OLD single-role template and older numbers. Their per-JD source data dicts were
never persisted, so aligning each = a fresh tailoring pass on the new base (honest re-scoring per JD).
Plan: re-tailor onto the new base as each role becomes active / when Kshitiz applies, in tracked
batches — rather than a risky blind mass-regeneration.

---

## Current state snapshot (as of 2026-07-22)

### Dashboard & engine — DONE and live
- Static site on GitHub Pages, hourly job-refresh Action working.
- **Auto-fit resume engine** (`fit_to_page()`) — every resume is one full page (~93–98% fill),
  ATS-clean, never spills to page 2. Toolchain on the Mac: `.venv` (python-docx + pypdf),
  LibreOffice (`soffice`), poppler (`pdftoppm`).
- **Honest scoring** (`keyword_coverage_score()`) — 3 bug-fix iterations; OR-list collapsing;
  word-presence-anywhere matching. Documented in CLAUDE.md.
- **External JD Resumes tab** — PDF+DOCX downloads, cover-letter support, newest-first sort by
  `updatedDate`/`addedDate` (full ISO timestamps for same-day ordering).
- **My Resume tab** — the universal master resume, download path fixed (`resumes/` prefix).

### Master resume — REVAMPED 2026-07-22 (per Kshitiz's line-by-line review)
- "B2C" cut from 4 mentions to 1 (kept only in the experience intro).
- Summary shortened from 6 lines to 3 (positioning only, no metric duplication).
- Added a differentiated bullet: **counselor-wise P&L tracker** (unit-economics ownership).
- Tagline broadened: "Growth & Monetization | Consumer & Marketplace Platforms | Funnel, Retention
  & Payments | Data-Driven, AI-Enabled".
- These are now standing conventions in CLAUDE.md → apply to EVERY future resume.

### Tailored resumes — 24 in `external_resumes.json` (EXT1–EXT24)
boAt, INDmoney (Growth), Policybazaar, MakeMyTrip*, Tata 1mg, BlackRock, Payoneer(+cover letter),
Oracle, OLX, Airtel Financial (Platform), Barclays, Amex, Airtel Fintech (APM), Nat Habit,
INDmoney (US Stocks), PhysicsWallah, Noon, Zippee, D.E. Shaw, dunnhumby(+cover letter),
Credgenics, Blitz, Battery Smart. (*MakeMyTrip was refreshed.)
Each has a REAL computed score and an honest "why" including gaps. Strongest real fits so far:
**PhysicsWallah 96%, Nat Habit 96%, MakeMyTrip 96%, Battery Smart 96% (Gurugram), OLX 92%.**

### Profiles renovated via Claude-in-Chrome
- **Naukri** — headline, summary (B2C-growth-first, 138K+ enrolled learners), key skills, 10
  projects, employment. GOTCHA: ₹ saves as "?" → always use "Rs"; key skills are dropdown-restricted.
- **Foundit** — summary, 8 added skills, current-PM-role Amazon-style description, 6 projects added.
  Parked: APM-role description (Foundit requires a salary for it — not invented).
- **iimjobs** — fixed experience 4→5 yrs, rewrote "About" (was wrongly "business ops exec, 1+ yr"),
  swapped 2 weak skills for Power BI + Monetization. GOTCHA: "About" field disallows "/" and "<";
  form_input didn't trigger validation → had to type. Audio/Video profile left (only he can record).

### Verified experience unlocked this session (now safe to use)
- **Content catalogue / CMS**: grade- & course-wise content, then AI-automated content generation.
- **Attribution**: UTM + tracking cookies in a centralized CRM.
- **Audience segmentation**: by grade; professionals by industry + seniority; keyword targeting.
- **Performance-marketing collaboration** with Marketing/Sales.
- **Real platform scale**: 138,216 enrolled (paying) learners (use for scale questions; NOT a 1M+
  MAU product — answer honestly).
- Expanded vendor list: Daily.co, 100ms, Convin, Servetel (on top of payments/Gupshup/Exotel).

### Parked (needs Kshitiz's input before use)
- **Salary — CONFIRMED 2026-07-22: true current CTC = Rs 10.75 LPA** (Naukri already correct). Still
  to align: iimjobs (shows 9L → 10.75L) and Foundit (shows 11L → 10.75L) — both need a quick
  Claude-in-Chrome edit.
- **In-house CDP + ops engine** — DROPPED 2026-07-22: Kshitiz chose to leave it out; not pursuing.
- **Formal cohort analysis**: still open (Demo Analysis is individual-behaviour, not cohort).

---

## Standing decisions (the "why" behind how we work)
1. **Tailoring is manual (Claude-in-chat), not automated.** Full automation was tried and abandoned
   (no free Anthropic tier; Gemini free-tier `quota=0`). Manual keeps the honesty bar high.
2. **Honesty over score.** Report the real number even if <90%; never fabricate; flag gaps; ask
   about closable gaps. A bluffed resume collapses in the interview.
3. **One-page-full, always**, via `fit_to_page()` — never a bare `render()`.
4. **Git is the single source of truth.** Always `git pull` first (the hourly Action commits
   constantly), end with `git push`. Never force-push.
5. **Location priority**: Gurugram > Bangalore, baked into scoring.

## How to continue on a new platform / session
1. Read `CLAUDE.md` (rules) → this file (state) → `PRD.md` (what/why) → `ARCHITECTURE.md` (how).
2. To tailor a new JD: follow CLAUDE.md "Externally-found jobs" section. Use `build_resume.DATA` +
   `experience_bank.md` only; never invent. Score with `keyword_coverage_score()`; render with
   `fit_to_page()`; append to `external_resumes.json`; commit + push.
3. Interview/form answers: draw from `experience_bank.md` + the base resume; pick the project that
   best matches the JD's emphasis; keep numbers defensible.
