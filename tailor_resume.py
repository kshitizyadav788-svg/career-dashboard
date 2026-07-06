#!/usr/bin/env python3
"""
Runs inside the "Tailor Resume" GitHub Action, triggered when a dashboard-
generated issue (label: tailor-resume) is opened.

Fetches the JD, asks Gemini (free API tier -- no billing required) to tailor
Kshitiz's resume against it (reorder/reword only -- never invent achievements),
renders the docx/pdf, and writes the result back onto the job entry in
seed_jobs.json, then regenerates jobs.json so the dashboard picks it up.

Required env vars (set by the workflow from the issue event):
  ISSUE_BODY      -- the raw issue body (GitHub issue-form markdown)
  GEMINI_API_KEY  -- repo secret, a free key from aistudio.google.com
  GEMINI_MODEL    -- optional, defaults to "gemini-2.0-flash"
"""
import os
import re
import sys
import json
import subprocess
import datetime

import requests
from bs4 import BeautifulSoup

import build_resume
from fetch_jobs import merge_jobs, write_jobs_json, score_fit

FIELD_MAP = {
    "job id": "job_id",
    "role / title": "role",
    "company": "company",
    "location": "location",
    "job link (jd url)": "jd_url",
    "full job description (optional, but recommended)": "jd_text",
}


def parse_issue_body(body):
    """GitHub issue forms render as '### Label\\n\\nvalue\\n\\n' blocks."""
    parts = re.split(r"^### (.+)$", body, flags=re.M)
    fields = {}
    for i in range(1, len(parts), 2):
        header = parts[i].strip().lower()
        value = parts[i + 1].strip() if i + 1 < len(parts) else ""
        if value.lower() in ("_no response_", ""):
            value = ""
        key = FIELD_MAP.get(header)
        if key:
            fields[key] = value
    return fields


def fetch_jd_text(url):
    if not url:
        return ""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"}
        r = requests.get(url, headers=headers, timeout=20, allow_redirects=True)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        for tag in soup(["script", "style", "nav", "header", "footer"]):
            tag.decompose()
        text = soup.get_text("\n")
        text = re.sub(r"\n{2,}", "\n", text).strip()
        return text[:12000]
    except Exception as e:
        print(f"JD fetch failed for {url}: {e}", file=sys.stderr)
        return ""


def call_llm(jd_text, role, company):
    """Uses Google Gemini's free API tier (no billing required) to tailor the resume content."""
    import google.generativeai as genai
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    base = build_resume.DATA
    system = (
        "You are tailoring Kshitiz Yadav's one-page Product Manager resume for a specific job. "
        "He is a general B2C-growth Product Manager (~5 yrs) -- AI is a force-multiplier skill, "
        "not his whole identity. Never invent achievements, employers, or metrics; only reorder, "
        "reword, and re-emphasize content that is already in his base resume below so it mirrors "
        "the JD's language and priorities. Return ONLY valid JSON matching exactly this schema: "
        '{"summary": string, "competencies": string, '
        '"groups": [{"heading": string, "bullets": [string, ...]}], '
        '"matchScore": integer 0-100 (honest ATS/JD-keyword-match estimate for the tailored resume), '
        '"matchedKeywords": [string, ...]}'
    )
    user = json.dumps({
        "base_resume": base,
        "target_role": role,
        "target_company": company,
        "job_description": jd_text or ("(JD text not available -- tailor generically for this "
                                        "title/company using the base resume as-is, and cap "
                                        "matchScore at 65 to reflect the missing JD.)"),
    })
    model = genai.GenerativeModel(
        os.environ.get("GEMINI_MODEL", "gemini-2.0-flash"),
        system_instruction=system,
    )
    resp = model.generate_content(
        user,
        generation_config={"response_mime_type": "application/json"},
    )
    text = resp.text
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise ValueError("Gemini did not return JSON: " + text[:500])
    return json.loads(m.group(0))


def slug(s):
    return re.sub(r"(^-+|-+$)", "", re.sub(r"[^a-z0-9]+", "-", (s or "").lower()))


def main():
    body = os.environ["ISSUE_BODY"]
    fields = parse_issue_body(body)
    job_id = fields.get("job_id", "").strip()
    role = fields.get("role", "").strip()
    company = fields.get("company", "").strip()
    location = fields.get("location", "").strip()
    jd_url = fields.get("jd_url", "").strip()
    jd_text = fields.get("jd_text", "").strip()

    if not role or not company:
        print("Missing role/company in issue body -- aborting.", file=sys.stderr)
        sys.exit(1)

    if not jd_text:
        jd_text = fetch_jd_text(jd_url)

    tailored = call_llm(jd_text, role, company)

    data = json.loads(json.dumps(build_resume.DATA))  # deep copy
    data["summary"] = tailored.get("summary") or data["summary"]
    data["competencies"] = tailored.get("competencies") or data["competencies"]
    if tailored.get("groups"):
        data["experience"]["groups"] = tailored["groups"]

    fname = f"{slug(company)}-{slug(role)}"
    docx_path = f"resumes/{fname}.docx"
    build_resume.render(data, docx_path)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", "resumes", docx_path], check=True)
    pdf_path = f"resumes/{fname}.pdf"

    match_score = int(tailored.get("matchScore", 70))

    seed = json.load(open("seed_jobs.json", encoding="utf-8"))
    jobs = seed["jobs"]
    job = next((j for j in jobs if j.get("id") == job_id), None) if job_id else None
    if job is None:
        job = {
            "id": job_id or f"TR_{slug(company)}-{slug(role)}"[:24],
            "src": "Naukri" if "naukri.com" in jd_url else "Web",
            "title": role, "co": company, "loc": location, "url": jd_url,
            "posted": datetime.date.today().isoformat(),
            "fit": score_fit(role, location), "comp": 65, "growth": 70, "prob": 60,
            "why": "Added via the dashboard's Tailor My Resume request.",
        }
        jobs.append(job)
    job["resume"] = docx_path
    job["matchScore"] = match_score
    json.dump(seed, open("seed_jobs.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    try:
        current = json.load(open("jobs.json", encoding="utf-8")).get("jobs", [])
    except Exception:
        current = []
    fresh = [j for j in current if str(j.get("id", "")).startswith(("JS_", "AZ_"))]
    merged = merge_jobs(jobs, fresh)
    write_jobs_json(merged)

    result = {
        "docx": docx_path, "pdf": pdf_path, "matchScore": match_score,
        "matchedKeywords": ", ".join(tailored.get("matchedKeywords", [])),
        "role": role, "company": company, "jdFetched": "true" if jd_text else "false",
    }
    gh_output = os.environ.get("GITHUB_OUTPUT")
    if gh_output:
        # plain key=value lines -- these get interpolated directly into shell
        # commands and JS template strings downstream, so no quoting here.
        with open(gh_output, "a") as f:
            for k, v in result.items():
                f.write(f"{k}={v}\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
