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
| `tailor_resume.py` | Runs inside the Tailor Resume Action: fetches the JD, calls Claude to tailor `build_resume.DATA`, renders + converts to PDF, writes `resume`/`matchScore` onto the job in `seed_jobs.json`, regenerates `jobs.json`. |
| `resumes/` | Generated resumes (base + per-JD tailored versions). |
| `.github/workflows/refresh-jobs.yml` | Runs `fetch_jobs.py` hourly, commits `jobs.json`. |
| `.github/workflows/tailor-resume.yml` | Runs `tailor_resume.py` when a `tailor-resume`-labeled issue is opened (see below). |
| `.github/ISSUE_TEMPLATE/tailor-resume.yml` | The issue form the dashboard deep-links into to trigger tailoring. |

## How hosting / refresh works (already live)
- Hosted on **GitHub Pages** at `https://kshitizyadav788-svg.github.io/career-dashboard/` (public).
- Hourly **GitHub Action** refreshes jobs in the cloud — no laptop needed.
- Secrets in the repo: `RAPIDAPI_KEY` (JSearch), `ADZUNA_APP_ID`, `ADZUNA_APP_KEY`, `GEMINI_API_KEY` (resume tailoring — free tier, no billing).
- Source reality: **Adzuna** auto-refreshes; **Indeed/LinkedIn/Glassdoor** only once JSearch's free
  plan is subscribed; **Naukri has no API** → refreshed manually via Claude-in-Chrome.

## The resume-tailoring workflow (fully automated, on-demand per job)
The dashboard's **Job Matches** tab has a **"Tailor My Resume"** column. Clicking "✎ Tailor my
Resume" on a job (a) optionally prompts for a pasted JD, (b) saves it to a local
`DB.tailorRequests` queue (per-device, localStorage — shows "Requested" + an instant client-side
estimated match % if a JD was pasted), and (c) opens a **pre-filled GitHub Issue** using the
`tailor-resume.yml` issue form. Kshitiz just clicks **"Submit new issue"** — no typing needed.

That issue (labeled `tailor-resume`) triggers `.github/workflows/tailor-resume.yml`, which runs
`tailor_resume.py`:
1. Parses the issue form fields (job id, role, company, location, JD link, optional pasted JD).
2. If no JD was pasted, fetches the JD link itself (`requests` + BeautifulSoup) — best-effort;
   some job boards block simple fetches, in which case it tailors generically and caps the score.
3. Calls the **Gemini API** (free tier, no billing required — switched from the paid Anthropic API
   for this reason) with `build_resume.DATA` + the JD, instructed to **only reorder/reword existing
   content — never invent achievements or metrics** — and return a tailored
   summary/competencies/experience-bullets JSON plus an honest JD-match score. `tailor_resume.py`'s
   `pick_gemini_model()` **auto-discovers an available "flash" model** at runtime rather than
   hardcoding a name — Gemini model names/availability shift over time and hardcoded names have
   already 404'd once during testing. Set `GEMINI_MODEL` to force a specific one if needed.
4. Renders the tailored `.docx` via `build_resume.render()`, converts to `.pdf` via LibreOffice.
5. Writes `"resume"` (path) and `"matchScore"` fields onto that job's entry in `seed_jobs.json`
   (promoting the job into `seed_jobs.json` first if it was only in the live JSearch/Adzuna feed,
   so it survives the next hourly refresh), then regenerates `jobs.json`.
6. Commits + pushes (with a same-run conflict-reconciliation step if the hourly refresh Action
   raced it — same manual fix pattern as any `jobs.json` merge conflict: keep `seed_jobs.json` as
   authoritative, rebuild `jobs.json` from the remote's fresher live feed).
7. Comments the match score + resume links on the issue and closes it.

**If you're asked to debug or extend this pipeline**, the most likely things to need attention are
(a) JD-fetch reliability for a specific job board's HTML, (b) whether `GEMINI_API_KEY` is set as a
repo secret (get a free one at aistudio.google.com — no card needed), and (c) whether the
`tailor-resume` **label exists on the repo** — GitHub silently drops a label referenced in an issue
template or `?labels=` URL param if that label doesn't already exist; it does not auto-create it.
If a submitted issue's Action run shows `skipped`, check `gh label list` first. (The repo's default
Actions token permission is read-only, but both `tailor-resume.yml` and `refresh-jobs.yml` declare
`permissions: contents: write` explicitly at the workflow level, which overrides that default —
confirmed working since `refresh-jobs.yml` has pushed hourly commits under the same setup. No repo
settings change needed.)

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
