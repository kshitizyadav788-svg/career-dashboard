# Career Intelligence Dashboard — project brief for Claude

This repo IS the deployed dashboard for **Kshitiz Yadav** (Product Manager job search).
Any Claude Code session — Windows laptop or Mac — should read this first, then continue.
GitHub is the single source of truth; work from a fresh `git pull` and end with `git push`.

## Who this is for
Kshitiz Yadav — **Product Manager, ~5 yrs**, Gurgaon (open to remote/Bangalore).
Positioning: **general B2C-growth PM first; AI is a skill/force-multiplier, NOT the identity.**
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
Static site can't write resumes itself — Claude generates them. Steps:
1. Get the target job's **full JD** (user pastes it, or Claude fetches the job's link).
2. Extract the JD's keywords / must-haves.
3. Copy `build_resume.py` → tailor a variant: reorder bullets, mirror their language, front-load
   their requirements. **Aim ATS ≥ 85** and keep it recruiter-pleasing (strong top third, quantified).
4. Output to `resumes/<Company>-<Role>.docx` and convert to `.pdf` (see build commands).
5. Wire it into the dashboard's Resume column + record a JD-match score.
6. `git add resumes/ index.html && git commit && git push`.

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
- [ ] Build the "Tailor my resume?" column + tailored resumes per job.
