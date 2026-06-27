# Career Intelligence Dashboard — hosted, auto-refreshing

Put this dashboard online (open it from your Mac, iPad, or phone) and have the job
list refresh **every hour automatically** — for free, using GitHub Pages + GitHub Actions.

## What's in this folder
| File | Purpose |
|------|---------|
| `index.html` | The dashboard. On a hosted URL it loads `jobs.json`; opened locally it uses its built-in jobs. |
| `jobs.json` | The live job list the dashboard reads. Overwritten hourly by the Action. |
| `seed_jobs.json` | Your curated + Naukri roles (no public API) — always merged into `jobs.json`. |
| `fetch_jobs.py` | Pulls fresh Product Manager roles from JSearch + Adzuna, scores, merges, writes `jobs.json`. |
| `.github/workflows/refresh-jobs.yml` | Runs `fetch_jobs.py` hourly and commits the result. |

## One-time setup (~10 min)

### 1. Get two free API keys
- **JSearch** (Indeed + LinkedIn + Glassdoor via Google for Jobs): sign up at
  https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch → copy your **RapidAPI key**.
- **Adzuna** (India coverage + salaries): sign up at https://developer.adzuna.com/ →
  create an app → copy **App ID** and **App Key**.

*(You can start with just one — the script skips any provider whose keys are missing.)*

### 2. Create the GitHub repo
1. Make a new **public** repo on github.com (public = free Pages), e.g. `career-dashboard`.
2. Upload everything in this `site/` folder to the repo root (drag-and-drop in the GitHub UI,
   or `git init && git add . && git commit -m "init" && git push`).
   Make sure `.github/workflows/refresh-jobs.yml` keeps that exact path.

### 3. Add your keys as repo Secrets
Repo → **Settings → Secrets and variables → Actions → New repository secret**, add:
- `RAPIDAPI_KEY`
- `ADZUNA_APP_ID`
- `ADZUNA_APP_KEY`

### 4. Turn on Pages
Repo → **Settings → Pages** → *Build and deployment* → **Deploy from a branch** →
branch `main`, folder `/ (root)` → Save. After a minute your dashboard is live at:
```
https://<your-username>.github.io/career-dashboard/
```
Open that on your Mac / iPad / phone, and bookmark it.

### 5. Kick off the first refresh
Repo → **Actions** tab → enable workflows if prompted → open **“Refresh jobs hourly”**
→ **Run workflow**. It generates a fresh `jobs.json`; after that it runs by itself every hour.

## Good to know
- **Hourly feed covers API sources** (Indeed, LinkedIn, Glassdoor via JSearch; Adzuna India).
  **Naukri has no API**, so your Naukri roles ride along from `seed_jobs.json` — refresh those
  by re-running the dashboard's Chrome pull and regenerating `seed_jobs.json`.
- **Your tracking data** (applications, notes, statuses) is stored **per device** in the
  browser. It does **not** sync across devices on this setup. Want true cross-device sync?
  That's the Supabase add-on — ask and I'll wire it in.
- **Tune the search**: edit `JSEARCH_QUERIES` / `ADZUNA_QUERIES` at the top of `fetch_jobs.py`.
- **Change the cadence**: edit the `cron` line in `.github/workflows/refresh-jobs.yml`
  (`0 * * * *` = hourly; `0 */3 * * *` = every 3 hours).
