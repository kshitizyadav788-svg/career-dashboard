# Career Intelligence Dashboard — project brief for Claude

This repo IS the deployed dashboard for **Kshitiz Yadav** (Product Manager job search).
Any Claude Code session — Windows laptop or Mac — should read this first, then continue.
GitHub is the single source of truth; work from a fresh `git pull` and end with `git push`.

## Who this is for
Kshitiz Yadav — **Product Manager, ~5 yrs**, Gurgaon (open to remote/Bangalore).
Positioning: **general B2C-growth PM first; AI is a skill/force-multiplier, NOT the identity.**
**Location priority: Gurugram first, then Bangalore** — baked into the composite job score
(+8 Gurugram, +5 Bangalore) in both `fetch_jobs.py`'s `score_fit()` and `index.html`'s
client-side `score()`/`locBonus()`, so these cities sort to the top of Job Matches by default.
Signature wins (use these when tailoring resumes): +20% revenue, +25% ARPU (₹35K→₹45K),
₹70L/month product-led renewals, funnel re-architecture (single-step OTP, preference→ranking
model, 6 payment gateways), consumer app MVP in 2 months, Sales CRM revamp (−80% ops), ₹1.6L/mo
automation savings, shipped production GenAI (LLM/ChatGPT). Contact: kshitizyadav788@gmail.com.

## What's here
| File | Purpose |
|------|---------|
| `index.html` | The dashboard. Hosted = loads `jobs.json`; local `file://` = uses baked-in jobs. |
| `jobs.json` | Live job list, **overwritten hourly** by the Action. Don't hand-edit. |
| `seed_jobs.json` | Curated + Naukri roles (no API) always merged into `jobs.json`. Regenerate when re-scraping Naukri. |
| `fetch_jobs.py` | Hourly refresh: JSearch + Adzuna → score → merge with seed → write `jobs.json`. |
| `build_resume.py` | Renders Kshitiz's resume to `.docx` from a `DATA` dict via `render(data, out_path)`. Base for tailoring. |
| `experience_bank.md` | Pool of real projects/skills Kshitiz has done but that don't fit the one-page base resume. Pull from here when a JD needs something `build_resume.DATA` doesn't cover -- never invent. Add to it whenever he mentions something new. |
| `external_resumes.json` | Resumes tailored from JDs Kshitiz pastes directly in chat (not the automated Job Matches feed) -- dashboard's **"External JD Resumes"** tab. Maintain by hand: append `{id, title, co, addedDate, resume, matchScore, why}` (add `coverLetter` if one was made) whenever you tailor one of these. |
| `build_cover_letter.py` | Renders a one-page cover letter `.docx` matching the resume's visual style. Same honesty rules as resumes -- only real, already-verified achievements. |
| `resumes/` | Generated resumes (base + per-JD tailored versions). |
| `.github/workflows/refresh-jobs.yml` | Runs `fetch_jobs.py` hourly, commits `jobs.json`. |
| `.github/ISSUE_TEMPLATE/tailor-resume.yml` | The issue form the dashboard deep-links into — a durable to-do queue, not an automated trigger (see below). |

## How hosting / refresh works (already live)
- Hosted on **GitHub Pages** at `https://kshitizyadav788-svg.github.io/career-dashboard/` (public).
- Hourly **GitHub Action** refreshes jobs in the cloud — no laptop needed.
- Secrets in the repo: `RAPIDAPI_KEY` (JSearch), `ADZUNA_APP_ID`, `ADZUNA_APP_KEY`. (`ANTHROPIC_API_KEY`
  and `GEMINI_API_KEY` are leftover from an abandoned automated-tailoring attempt — see below — and
  are unused; harmless to leave or remove.)
- Source reality: **Adzuna** auto-refreshes; **Indeed/LinkedIn/Glassdoor** only once JSearch's free
  plan is subscribed; **Naukri has no API** → refreshed manually via Claude-in-Chrome.

## The resume-tailoring workflow (manual, Claude-driven, on-demand)
**Why not automated:** we tried wiring "click Tailor My Resume" straight through to an unattended
GitHub Action that called an LLM API and committed the result with zero further input. Anthropic's
API has no free tier and Kshitiz didn't want to pay for it; swapping to Google Gemini's free tier
hit an unresolved account-level `quota=0` restriction across every model tried (not a code bug —
verified by testing 4 different model names, all `limit: 0`). Rather than keep chasing that, the
tailoring step itself is now something **you (Claude) do by hand in a chat**, using the same
quality bar as writing any other tailored resume — the GitHub Issue is just a durable to-do queue,
not a pipeline.

**The flow:**
1. The dashboard's **Job Matches** tab has a **"Tailor My Resume"** column. Clicking "✎ Tailor my
   Resume" on a job (a) optionally prompts for a pasted JD, (b) saves it to a local
   `DB.tailorRequests` queue (per-device, localStorage — shows "Requested" + an instant client-side
   estimated match % if a JD was pasted), and (c) opens a **pre-filled GitHub Issue** using the
   `tailor-resume.yml` issue form. Kshitiz clicks **"Submit new issue"** — that's the only action
   needed on the dashboard side.
2. **When Kshitiz asks you to process the tailor-resume queue**, run:
   `gh issue list --repo kshitizyadav788-svg/career-dashboard --label tailor-resume --state open`
   and handle each one:
   a. Read the issue body for job id, role, company, location, JD link, and (usually) the full
      pasted JD. If no JD was pasted, fetch the JD link yourself.
   b. Extract the JD's keywords/must-haves **as an explicit list** (10-20 specific skill/tool/
      domain terms — e.g. "Agile", "JIRA", "P&L ownership", "cohort analysis" — not generic prose
      words). This list is what step (c)'s score is computed against, so judge it honestly: it
      must reflect the JD's actual must-haves, not be padded with easy terms to inflate the score.
      **Watch for OR-lists in the JD** (e.g. "experience with SaaS, Enterprise Applications, or
      Digital Products") — that's ONE requirement satisfied by ANY of the alternatives, not three
      separate must-haves. A real mistake made once: listing all three as separate keywords
      penalized an honestly-90%+ resume down to 85% for "missing" two alternatives it never
      needed. Collapse an OR-list to whichever single alternative is actually true/covered before
      scoring, don't count the others as gaps.
   c. Tailor a variant of `build_resume.DATA`: reorder/reword bullets, mirror their language,
      front-load their requirements. If the JD needs a skill/tool/domain not covered by the base
      resume, check **`experience_bank.md`** first — it holds real projects Kshitiz has done that
      don't fit the one-page base — and swap in a relevant entry from there instead of a
      less-relevant base bullet. **Never invent achievements, employers, or metrics** — only pull
      from `build_resume.DATA` and `experience_bank.md`.

      **Target: matchScore ≥ 90 — and it must be a real, computed number, never an eyeballed
      guess.** Run `build_resume.keyword_coverage_score(data, keywords)` (in `build_resume.py`)
      against your step-(b) keyword list once you've drafted the tailored `data` — it returns
      `(score, matched, missing)`. This is deliberately keyword-coverage against your curated
      list, not raw full-JD-text word overlap: a naive whole-JD-text version was tried and scored
      a real tailored resume at 33%, because JDs are full of generic connector words ("translate",
      "ensuring", "deliver") no resume would ever contain even when the underlying skill is
      genuinely covered — that's not honest signal, real ATS systems and recruiters key off
      specific terms, not prose glue.
      For anything in `missing`, first check if it's **honestly closeable by rewording only**
      (e.g. writing "Google Analytics (GA4)" instead of just "GA4" is 100% true and closes a
      keyword gap with zero fabrication — this kind of fix is fair game and expected). For
      whatever's still missing after that: **do not force the score to 90 by fabricating or
      stretching the truth.** Report the real computed score to Kshitiz honestly, even if it's
      well under 90, and explain which specific missing terms are the reason. If real experience
      might exist that would close a gap (e.g. he may have used a BI tool, or had informal P&L
      exposure not yet documented), **ask him** — either inline in chat if you're already talking,
      or via the "Needs info" flag below if processing the queue unattended. Only write the
      number `keyword_coverage_score()` actually returned into `"matchScore"`.
      **If the JD needs something genuinely missing from both** (e.g. chatbot automation depth,
      payment API integration specifics, a named tool with no evidence anywhere): **don't block on
      it and don't invent it.** Instead, this is Kshitiz's preferred flow -- flag it and let him
      answer post-hoc, on his own time, rather than needing everything upfront:
        - Comment on the issue with the specific question (e.g. "Can you describe your payment
          API integration work in more detail? Which gateways, what scope?").
        - Add `"tailorNote"` (short version of the ask, e.g. `"Needs: payment API integration
          details"`) and `"tailorIssue"` (the issue number) onto the job in `seed_jobs.json` --
          the dashboard's Tailor column shows this as a "🏳 Needs info" pill instead of a
          finished resume.
        - **Leave the issue open** (don't close it) -- it stays in the queue until answered.
        - Tailor and finish everything else about the resume that doesn't depend on the missing
          piece; only the specific gap blocks completion.
      When Kshitiz answers (on the issue, or in a later chat), add the new fact to
      `experience_bank.md`, finish the tailoring, then continue with steps d-h below.
      **Separately**, if you notice something that would generally strengthen the resume
      (not blocking any specific job, just a good addition) log it under an "Open Questions"
      section in `experience_bank.md` for Kshitiz to answer whenever -- same post-paid principle.
   d. Render via **`build_resume.fit_to_page(data, "resumes/<Company>-<Role>.docx")`** — NOT the
      bare `render()`. `fit_to_page()` renders, converts to PDF via LibreOffice, measures the real
      page count + vertical fill, and auto-selects the loosest font/spacing preset that keeps the
      resume on **exactly one page filled cleanly (~93–98%)** — so there's never a big empty gap at
      the bottom and it never spills to page 2. See "The one-page-full rule" section below for the
      full mechanism and what to do if content is too long/thin. It writes both the `.docx` and
      `.pdf` and returns `(style, pages, fill_pct, pdf_path)`.
   e. Add `"resume"` (path) and `"matchScore"` (your honest JD-match estimate) fields onto that
      job's entry in **`seed_jobs.json`** (promote the job into `seed_jobs.json` first if it's only
      in the live JSearch/Adzuna feed, so it survives the next hourly refresh). Clear any
      `"tailorNote"`/`"tailorIssue"` fields from a prior flag once resolved.
   f. Regenerate `jobs.json` from `seed_jobs.json` + the live feed (same merge logic as
      `fetch_jobs.py`'s `merge_jobs()`/`write_jobs_json()` — import and reuse them, don't reimplement).
   g. `git add resumes/ seed_jobs.json jobs.json && git commit && git push` (pull first; if rejected,
      it's almost always the hourly refresh's `jobs.json` — regenerate from the remote's fresher
      live feed + your `seed_jobs.json`, same fix as any `jobs.json` merge conflict).
   h. `gh issue close <N> --comment "..."` with the match score and resume links (only once
      complete -- skip this for issues still waiting on a flagged answer).

**Gotcha to know about:** GitHub silently drops a label referenced in an issue template's front
matter (or a `?labels=` URL param) if that label doesn't already exist in the repo — it does not
auto-create it. The `tailor-resume` label already exists now (`gh label create` was run once), but
if this ever needs recreating on a fresh repo, create the label first or submitted issues won't
carry it.

## The one-page-full rule (every resume, no exceptions)
Kshitiz's standard: **every resume must be exactly ONE page, filled cleanly with no big empty gap
at the bottom, and stay ATS-friendly** (single column, standard section headings, no tables /
text-boxes / columns / graphics that break parsers). This is enforced mechanically, not eyeballed:

- **Always finish a resume with `build_resume.fit_to_page(data, out_path)`**, never a bare
  `render()`. `fit_to_page()` walks `STYLE_PRESETS` (tight → loose, fonts kept in the ATS-safe
  9.5–11pt band), renders each via LibreOffice, measures the real PDF page count + how far content
  reaches down the page (`measure_pdf()`), and keeps the fullest layout that's still a single page,
  targeting ~93–98% fill. It self-corrects for content volume: a thin tailored variant gets a
  slightly larger font / looser spacing to fill the page; a dense one gets tightened.
- **Why it exists:** the old fixed 9.5pt template left even the *base* resume only ~81% full (≈2"
  of dead space at the bottom); tailored variants with lighter content were worse (~75%). python-docx
  alone can't know page count/fill — only a real layout engine (LibreOffice) can — so this step
  hard-depends on `soffice` being installed.
- **If `fit_to_page()` warns the content is too LONG** (overflows to 2 pages even at the tightest
  preset): trim — shorten the summary, cut/merge a weaker bullet — don't hunt for a smaller font.
- **If it NOTEs the content is too THIN** (best fill still < ~93% at the loosest preset): add a real
  bullet from `experience_bank.md`, don't just inflate spacing to fake fullness.
- Toolchain on this Mac (already set up): a project `.venv` (gitignored) with `python-docx` + `pypdf`
  (`.venv/bin/python build_resume.py`), LibreOffice (`soffice`), and `poppler` (`pdftoppm`, lets the
  Read tool render a resume PDF to an image for a visual check). Windows: has its own python-docx;
  install LibreOffice for `fit_to_page` there too, or fall back to Word for the final page check.
- Existing tailored resumes in `resumes/` were built before auto-fit and may under-fill — re-run
  them through `fit_to_page()` if regenerating.

## Cover letters (optional add-on to tailoring)
`build_cover_letter.py` renders a one-page cover letter (`render(paragraphs, out_path, company,
role)`) matching the resume's visual style (imports `build_resume`'s `NAVY`/`GREY`/`FONT`). Only
make one when Kshitiz asks for it (or the job posting requires one) — not a default step of every
tailoring pass. Same honesty rules as resumes: only real, already-verified achievements. If made,
add a `"coverLetter"` field alongside `"resume"` in `seed_jobs.json`/`external_resumes.json`.

## Scoring methodology gotchas (learned the hard way — read before tailoring)
`keyword_coverage_score()` went through three iterations, each fixing a real false-positive/
false-negative bug found while tailoring real JDs. Know all three before trusting a score:
1. **Naive full-JD-text overlap → 33% on a genuinely strong match.** JDs are full of generic prose
   glue ("translate," "ensuring," "deliver") no resume would ever contain even when the underlying
   skill is fully covered. Fixed by scoring against a curated Required-keyword list (10-20 terms
   judged by hand from the JD), not raw text overlap.
2. **OR-lists split into separate must-haves** (found on Tata 1mg/Velocitai): "SaaS, Enterprise
   Applications, or Digital Products" is ONE requirement satisfiable by any alternative, not three.
   Splitting it penalized an honest 90%+ resume down to 85% for "missing" alternatives it never
   needed. Fix: collapse any OR-list to whichever single true alternative applies before scoring.
3. **Exact-substring matching missed real coverage via word order** (found on boAt): "product
   development" wasn't detected inside "Product Ideation & Development," and "market analysis"
   wasn't detected inside "market research and competitor analysis." Fixed by checking that all
   significant words of a keyword phrase appear anywhere in the resume text, rather than requiring
   them contiguous/in-order. Re-verified this didn't regress already-shipped scores before shipping.

**Separately** — if a bullet's factual framing turns out to be imprecise (e.g. the "Demo Analysis"
AI feature was originally described as recommending courses directly to students; Kshitiz corrected
it to counselor-facing sales enablement), fix the wording in `experience_bank.md` **and** retroactively
in every resume that already used it, then re-verify each affected score is unchanged (a pure
precision fix shouldn't move the number).

## Historical one-off actions (context, not standing rules)
- **Pruned jobs older than 2 weeks** from `seed_jobs.json`/`jobs.json` once. This was a **one-time
  static cleanup**, explicitly **not** a recurring rule — do not build rolling age-based pruning
  into `fetch_jobs.py` or anywhere else unless Kshitiz asks again.

## Externally-found jobs (pasted JD, no dashboard entry)
When Kshitiz pastes a JD directly in chat for a job he found himself (not from the dashboard's
Job Matches feed), just tailor it the same way as above — same honesty rules, same
`keyword_coverage_score()`, same `experience_bank.md`/flagging behavior — but there's no GitHub
Issue involved. When you finish:
1. Render + save the resume as usual.
2. Append an entry to **`external_resumes.json`**: `{id: "EXT<n>", title, co, addedDate
   (today, ISO), resume: "resumes/<file>.docx", matchScore, why}`. `id` just needs to be unique
   within the file — increment from the highest existing `EXT<n>`. The dashboard tab sorts
   **newest-first** by whichever is most recent: `updatedDate` if present, else `addedDate`.
   **If you're refreshing an existing entry** (re-tailoring the same role — don't create a
   duplicate), keep its `addedDate` and set/refresh **`updatedDate`** (today, ISO) so it floats
   back to the top and shows an "updated" pill. Regenerate the resume through `fit_to_page()` and
   re-verify the score honestly (it may move — explain any change in `why`).
3. This shows up in the dashboard's **"External JD Resumes"** tab automatically (client fetches
   `external_resumes.json` at runtime, same pattern as `jobs.json`). No `seed_jobs.json` entry
   needed — that file is for the automated Job Matches feed specifically.
4. If Kshitiz later gives you the actual job-board URL for one of these, and he wants it tracked
   in the main Job Matches list too, promote it into `seed_jobs.json` at that point (with the
   real URL — `merge_jobs()` drops entries with no/empty `url`, so don't add it there without one).
5. `git add resumes/ external_resumes.json && git commit && git push`.

## Build / run commands
```bash
# Resume (Mac): use the project venv, which has python-docx + pypdf
.venv/bin/python build_resume.py     # auto-fits the BASE resume to one full page (docx + pdf)
# For a tailored variant, call build_resume.fit_to_page(data, out_path) from a script (see the
# tailoring workflow). fit_to_page() handles docx->pdf conversion + one-page-full verification.
# Needs LibreOffice (soffice) installed for the page measurement; poppler (pdftoppm) lets you
# visually check the pdf. First-time Mac setup:
#   python3 -m venv .venv && .venv/bin/pip install python-docx pypdf
#   brew install --cask libreoffice && brew install poppler
# Windows: python-docx already present; install LibreOffice for fit_to_page, or use Word to check.

# Refresh jobs locally (optional; the cloud Action does this hourly)
pip install requests
RAPIDAPI_KEY=... ADZUNA_APP_ID=... ADZUNA_APP_KEY=... python fetch_jobs.py
```

## Naukri / Foundit profile renovation (external sites, not tracked in this repo)
Kshitiz asked Claude to access his Naukri and Foundit profiles (open in his browser, via
Claude-in-Chrome) and renovate them into stronger PM profiles. Progress so far, as of 2026-07-08
(update this section as work continues — it's the durable cross-device record since these sites
aren't in git):

**Naukri (`https://www.naukri.com/mnjuser/profile`) — in progress:**
- ✅ **Projects section**: renovated, now has 10 real entries (all verified against
  `experience_bank.md`/`build_resume.DATA` before adding, no invented content, no duplicates found
  against existing entries): Demo Analysis (AI sales enablement, Mar-Jun 2026), Counselor-Wise P&L
  Tracker (Jan-Feb 2026), Internal VC Platform (Jan-Mar 2024), In-Product Renewal Engine (Jan
  2024-present), Backend Punching Automation (Dec 2023-Feb 2024), 2:1 Enrolment Automation (Mar-Apr
  2023), Customer Verification Flow (Jan-Feb 2023), Cross-Functional Power BI Dashboards (Jan
  2023-present), Multi-Gateway Payment Integration (Jan 2022-present), LPP Module (Jan-Dec 2022).
- ✅ **Employment section**: the current "Product Manager" role's job-profile text was corrected
  once — Naukri's own "Improve with AI" button (which Kshitiz can click independently of any Claude
  session) had merged two facts inaccurately: attributed "team of 8" to this role (actually from
  his **Assistant Product Manager** role) and causally linked ChatGPT API integration to the 25%
  ARPU growth (actually attributed to the LPP module's session structure). Fixed to separate these
  correctly.
- ⏳ **Not yet saved live** — drafted, verified against the honesty rules, but the actual Naukri
  page edit was not completed before this session ended. Exact text to paste in on a future
  session:

  **Resume Headline:**
  > Product Manager | 5+ yrs | B2C Growth & Monetization | Roadmap, PRD, GTM, A/B Testing | SQL &
  > Power BI | Two-Sided Marketplace | AI-Enabled (LLM/GenAI) | Drove +20% Revenue, +25% ARPU,
  > ₹70L/Month Renewals

  **Profile Summary** (fixes the current live version's "4+ years" typo and an AI-first framing
  that contradicts the established B2C-growth-first/AI-as-differentiator positioning):
  > Product Manager with 5+ years driving B2C growth and monetization for one of India's largest
  > EdTech marketplaces — connecting students and teachers via a shared LMS. Track record of moving
  > core metrics: 20% revenue growth, 25% ARPU expansion (₹35K→₹45K), ₹70L in product-led renewals
  > in a single month, and 2,000+ organic leads/month at 7% conversion. Led end-to-end product
  > delivery across app, LMS, and CRM — funnel re-architecture, multi-gateway payment integration,
  > teacher-facing marketplace tools, and team leadership (trained & led a team of 8). Uses AI
  > (GenAI, LLM APIs, prompt engineering) as a force-multiplier to ship faster — not the whole
  > story. Core strengths: B2C Growth & Monetization | Product Roadmap & GTM | Cross-Functional
  > Leadership | Data-Driven Decisions (SQL, Power BI) | AI-Enabled Product Development

  **Key Skills to add** (keep all existing ones, just add): SQL, Power BI, Payment Gateway
  Integration, Stakeholder Management, Team Leadership, Two-Sided Marketplace, P&L Management.

- **Gotcha**: always re-read the current live Naukri text before assuming a prior Claude draft is
  what's actually saved — Kshitiz can click "Improve with AI" himself at any time and silently
  change it.

**Foundit**: not started at all yet. Same renovation approach once Naukri is finished: read current
live profile fields first, cross-check every claim against `build_resume.DATA` +
`experience_bank.md`, never invent.

## Git workflow (BOTH machines)
```bash
git pull            # ALWAYS first — the hourly Action commits to main constantly
# ...make changes...
git add . && git commit -m "msg" && git push
```
If push is rejected → `git pull` then `git push` again. Never force-push (the Action's commits matter).

## Open items / TODO
- [ ] Activate JSearch (subscribe free plan on RapidAPI) → unlocks fresh Indeed/LinkedIn/Glassdoor.
- [ ] Re-scrape Naukri via Claude-in-Chrome periodically → regenerate `seed_jobs.json`.
- [ ] Save the drafted Naukri **Resume Headline / Profile Summary / Key Skills** live (exact text
      in the "Naukri / Foundit profile renovation" section above) — Projects + Employment already done.
- [ ] Renovate the **Foundit** profile (not started at all yet) — same approach as Naukri.
- [ ] `experience_bank.md`'s "Open Questions" section has two unanswered items (formal cohort
      analysis experience; catalogue/content-listing work detail) — ask Kshitiz when relevant.
- [ ] Optional: make site private (Cloudflare Pages + Access) — currently PUBLIC.
- [ ] Optional: cross-device sync of tracking data (Supabase) — currently per-device localStorage.
