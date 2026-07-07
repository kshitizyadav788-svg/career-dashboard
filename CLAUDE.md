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
   d. Render via `build_resume.render(data, "resumes/<Company>-<Role>.docx")`, convert to `.pdf`
      (`soffice --headless --convert-to pdf --outdir resumes "resumes/NAME.docx"` — needs
      LibreOffice; `brew install --cask libreoffice` on Mac if missing).
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

## Build / run commands
```bash
# Resume docx  (needs: pip install python-docx)
python build_resume.py            # writes resumes/*.docx

# docx -> pdf
#   Mac / Linux (install LibreOffice):  soffice --headless --convert-to pdf --outdir resumes "resumes/NAME.docx"
#   Windows: LibreOffice same command, OR MS Word COM via PowerShell.

# Refresh jobs locally (optional; the cloud Action does this hourly)
pip install requests
RAPIDAPI_KEY=... ADZUNA_APP_ID=... ADZUNA_APP_KEY=... python fetch_jobs.py
```

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
- [ ] Finish Naukri profile edits (Summary + Employment) — content in the chat history.
- [ ] Optional: make site private (Cloudflare Pages + Access) — currently PUBLIC.
- [ ] Optional: cross-device sync of tracking data (Supabase) — currently per-device localStorage.
