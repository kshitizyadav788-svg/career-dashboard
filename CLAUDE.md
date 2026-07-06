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
| `build_resume.py` | Builds Kshitiz's one-page ATS resume `.docx` into `resumes/`. Base for tailoring. |
| `resumes/` | Generated resumes (base + per-JD tailored versions). |
| `.github/workflows/refresh-jobs.yml` | Runs `fetch_jobs.py` hourly, commits `jobs.json`. |

## How hosting / refresh works (already live)
- Hosted on **GitHub Pages** at `https://kshitizyadav788-svg.github.io/career-dashboard/` (public).
- Hourly **GitHub Action** refreshes jobs in the cloud — no laptop needed.
- Secrets in the repo: `RAPIDAPI_KEY` (JSearch), `ADZUNA_APP_ID`, `ADZUNA_APP_KEY`.
- Source reality: **Adzuna** auto-refreshes; **Indeed/LinkedIn/Glassdoor** only once JSearch's free
  plan is subscribed; **Naukri has no API** → refreshed manually via Claude-in-Chrome.

## The resume-tailoring workflow (on-demand, per targeted job)
Static site can't write resumes itself — Claude generates them. The dashboard's **Job Matches**
tab has a **"Tailor My Resume"** column: clicking "✎ Tailor my Resume" on a job (a) optionally
prompts for the pasted JD, (b) saves it to a local `DB.tailorRequests` queue (per-device,
localStorage — shows "Requested" + an instant client-side estimated match % if a JD was pasted),
and (c) copies a ready-made request to the clipboard for Kshitiz to paste into a Claude Code chat.
**When you receive that pasted request, do this:**
1. Get the target job's **full JD** (it's usually pasted in the request; otherwise fetch the JD link).
2. Extract the JD's keywords / must-haves.
3. Copy `build_resume.py` → tailor a variant: reorder bullets, mirror their language, front-load
   their requirements. **Aim ATS/JD-match ≥ 85** and keep it recruiter-pleasing (strong top third, quantified).
4. Output to `resumes/<Company>-<Role>.docx` and convert to `.pdf` (see build commands).
5. Add `"resume"` (path, e.g. `"resumes/Acme-Product-Manager.docx"`) and `"matchScore"` (the ATS/JD-match
   number) fields directly onto that job's entry in **`seed_jobs.json`** — this is what makes the
   dashboard's Tailor column show the download + score instead of "Requested". If the job came from
   the live JSearch/Adzuna feed (not already in `seed_jobs.json`), **copy/promote the full job entry
   into `seed_jobs.json` first** (with the new fields added), otherwise the next hourly refresh
   overwrites `jobs.json` from scratch and the tailored-resume link is lost.
6. Regenerate `jobs.json` from `seed_jobs.json` + the live feed (same merge logic as `fetch_jobs.py`'s
   `main()`) so the change shows up without waiting for the next hourly run.
7. `git add resumes/ seed_jobs.json jobs.json && git commit && git push`.

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
