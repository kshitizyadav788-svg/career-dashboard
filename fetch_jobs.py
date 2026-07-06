#!/usr/bin/env python3
"""
Hourly job refresh for the Career Intelligence Dashboard.

Pulls live Product Manager listings from:
  - JSearch  (Google-for-Jobs aggregator: Indeed, LinkedIn, Glassdoor, ZipRecruiter ...)
  - Adzuna   (India job aggregator + salary data)

Merges them with seed_jobs.json (the hand-curated + Naukri roles, which have no
public API and can't be auto-fetched), de-duplicates, scores each for a ~5-yr
general Product Manager, and writes jobs.json for the dashboard to load.

Runs in GitHub Actions. Required environment variables (set as repo Secrets):
  RAPIDAPI_KEY     -> JSearch key from rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
  ADZUNA_APP_ID    -> from developer.adzuna.com
  ADZUNA_APP_KEY   -> from developer.adzuna.com
Any provider whose keys are missing is skipped, so it still works with just one.
"""
import os, json, re, datetime, sys

try:
    import requests
except ImportError:
    sys.exit("Run: pip install requests")

# ---- what to search for (tweak freely) ----
JSEARCH_QUERIES = [
    "Product Manager in Gurgaon, India",
    "Product Manager in Bangalore, India",
    "Product Manager India remote",
]
ADZUNA_QUERIES = [("product manager", "Gurgaon"), ("product manager", "Bangalore"),
                  ("product manager", "")]  # "" = all India

TODAY = datetime.date.today()


def days_old(iso):
    if not iso:
        return 999
    try:
        d = datetime.date.fromisoformat(iso[:10])
        return max(0, (TODAY - d).days)
    except Exception:
        return 999


def score_fit(title, loc, exp_years=None):
    """Heuristic fit for a ~5-yr general PM (B2C growth, Gurgaon, open to remote)."""
    t = (title or "").lower()
    f = 72
    if any(k in t for k in ["product manager", "product owner"]):
        f += 4
    if any(k in t for k in ["senior", "sr.", "staff", "lead", "principal", "head", "director", "group"]):
        f -= 4          # senior — reachable at 5 yrs but a slight stretch
    if "junior" in t or "associate" in t or "apm" in t:
        f -= 8          # below level
    L = (loc or "").lower()
    if any(c in L for c in ["gurgaon", "gurugram"]):
        f += 8          # top priority: home base
    elif any(c in L for c in ["bangalore", "bengaluru"]):
        f += 5          # second priority
    elif any(c in L for c in ["delhi", "noida", "remote"]):
        f += 2
    if any(k in t for k in ["growth", "monetization", "consumer", "b2c", "platform"]):
        f += 3
    return max(50, min(90, f))


def norm_jsearch(j):
    title = j.get("job_title", "")
    url = j.get("job_apply_link") or j.get("job_google_link") or ""
    src = (j.get("job_publisher") or "Web")
    # collapse JSearch publishers to clean tags the dashboard colours
    sl = src.lower()
    if "linkedin" in sl: src = "LinkedIn"
    elif "indeed" in sl: src = "Indeed"
    elif "glassdoor" in sl: src = "Glassdoor"
    elif "ziprecruiter" in sl: src = "ZipRecruiter"
    loc = ", ".join(x for x in [j.get("job_city"), j.get("job_state")] if x) or (
        "Remote" if j.get("job_is_remote") else j.get("job_country", ""))
    posted = (j.get("job_posted_at_datetime_utc") or "")[:10]
    fit = score_fit(title, loc)
    return {"id": "JS_" + str(abs(hash(url)) % 10**8), "src": src, "title": title,
            "co": j.get("employer_name", ""), "loc": loc, "url": url, "posted": posted,
            "fit": fit, "comp": 68, "growth": 72, "prob": 70 if fit >= 78 else 58,
            "why": f"{src} via JSearch" + (" · remote" if j.get('job_is_remote') else "")}


def norm_adzuna(j):
    title = j.get("title", "")
    url = j.get("redirect_url", "")
    loc = (j.get("location", {}) or {}).get("display_name", "")
    posted = (j.get("created") or "")[:10]
    sal = j.get("salary_max")
    comp = min(90, 50 + int(sal / 100000)) if sal else 62
    fit = score_fit(title, loc)
    return {"id": "AZ_" + str(j.get("id", abs(hash(url)) % 10**8)), "src": "Adzuna",
            "title": title, "co": (j.get("company", {}) or {}).get("display_name", ""),
            "loc": loc, "url": url, "posted": posted, "fit": fit, "comp": comp,
            "growth": 70, "prob": 70 if fit >= 78 else 58, "why": "Adzuna (India)"}


def fetch_jsearch():
    key = os.environ.get("RAPIDAPI_KEY")
    if not key:
        print("· JSearch: no RAPIDAPI_KEY, skipping"); return []
    out = []
    headers = {"X-RapidAPI-Key": key, "X-RapidAPI-Host": "jsearch.p.rapidapi.com"}
    for q in JSEARCH_QUERIES:
        try:
            r = requests.get("https://jsearch.p.rapidapi.com/search",
                             headers=headers,
                             params={"query": q, "page": "1", "num_pages": "1", "date_posted": "month"},
                             timeout=30)
            r.raise_for_status()
            data = r.json().get("data", []) or []
            out += [norm_jsearch(j) for j in data]
            print(f"· JSearch '{q}': {len(data)}")
        except Exception as e:
            print(f"· JSearch '{q}' failed: {e}")
    return out


def fetch_adzuna():
    app_id, app_key = os.environ.get("ADZUNA_APP_ID"), os.environ.get("ADZUNA_APP_KEY")
    if not (app_id and app_key):
        print("· Adzuna: no keys, skipping"); return []
    out = []
    for what, where in ADZUNA_QUERIES:
        try:
            r = requests.get("https://api.adzuna.com/v1/api/jobs/in/search/1",
                             params={"app_id": app_id, "app_key": app_key, "what": what,
                                     "where": where, "results_per_page": 25,
                                     "max_days_old": 30, "content-type": "application/json"},
                             timeout=30)
            r.raise_for_status()
            res = r.json().get("results", []) or []
            out += [norm_adzuna(j) for j in res]
            print(f"· Adzuna '{what}/{where or 'India'}': {len(res)}")
        except Exception as e:
            print(f"· Adzuna '{what}/{where}' failed: {e}")
    return out


def main():
    base = []
    try:
        base = json.load(open("seed_jobs.json", encoding="utf-8")).get("jobs", [])
    except Exception:
        pass
    fresh = fetch_jsearch() + fetch_adzuna()

    # de-dupe by (title + company), keep the curated/seed version first
    seen, merged = set(), []
    for j in base + fresh:
        k = (j.get("title", "").strip().lower(), j.get("co", "").strip().lower())
        if k in seen or not j.get("url"):
            continue
        seen.add(k); merged.append(j)

    merged.sort(key=lambda j: round(j["fit"] * .4 + j["comp"] * .2 + j["growth"] * .2 + j["prob"] * .2),
                reverse=True)
    out = {"updated": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
           "source": "live", "count": len(merged), "jobs": merged}
    json.dump(out, open("jobs.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"Wrote jobs.json: {len(base)} seed + {len(fresh)} fresh = {len(merged)} unique")


if __name__ == "__main__":
    main()
