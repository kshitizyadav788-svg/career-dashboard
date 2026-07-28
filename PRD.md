# PRD — Career Intelligence Dashboard & Resume System

**Owner:** Kshitiz Yadav (Product Manager, ~5 yrs, Gurugram)
**Status:** Live in production. Last major update 2026-07-22.
**Repo:** `kshitizyadav788-svg/career-dashboard` · **Live:** https://kshitizyadav788-svg.github.io/career-dashboard/

---

## 1. Problem
Job hunting as a Product Manager involves three painful, repetitive jobs:
1. **Finding** relevant roles scattered across job boards (Naukri, LinkedIn, Indeed, Adzuna…).
2. **Tailoring** a resume to each job description so it passes ATS keyword screens **and** honestly reflects real experience.
3. **Tracking** applications, matches, skill gaps, and profile hygiene across many platforms.

Doing this by hand is slow, inconsistent, and tempts people to exaggerate. Kshitiz wanted a single system that automates discovery, produces **honestly-scored** tailored resumes, and keeps everything in one place.

## 2. Who it's for
One user: **Kshitiz Yadav**. It is a personal job-search cockpit, not a multi-tenant product. Positioning baked into every output: **general B2C-growth / consumer & marketplace PM first; AI is a force-multiplier, not the identity.** Location priority: **Gurugram first, then Bangalore.**

## 3. Goals
- **G1 — Aggregate jobs automatically** and rank them by fit, with Gurugram/Bangalore sorted to the top.
- **G2 — Produce tailored resumes with a REAL, computed match score** (never a bluffed number) — target ≥90% only when genuinely earned.
- **G3 — Enforce a one-page, ATS-clean, fully-filled resume** every time, mechanically (not by eyeballing).
- **G4 — Never fabricate.** Only draw from verified experience; report honest gaps.
- **G5 — Zero-maintenance hosting** — refreshes itself in the cloud, no laptop needed.
- **G6 — Single source of truth** in Git, usable from any machine (Windows laptop or Mac).

## 4. Non-goals
- Not a product for other users (no auth, no multi-user, no accounts).
- Not an automated apply bot — it prepares; the human applies.
- Not automated LLM tailoring — that was tried and abandoned (no free Anthropic tier; Gemini free-tier `quota=0`). Tailoring is done **by Claude in a chat, by hand**, to keep the honesty bar high.
- No rolling age-based job pruning (a one-time cleanup was done once, explicitly not recurring).

## 5. Features (what the dashboard does)

### Dashboard tabs (`index.html`, a single-file SPA)
| Tab | What it does |
|-----|--------------|
| **Overview** | Snapshot of pipeline, top actions. |
| **My Resume** | The universal/master resume — inline preview + `.docx`/`.pdf` download. Auto-fit to one full page. |
| **Resume Analysis** | ATS score of the master resume, keyword gaps, notes. |
| **Skill Gaps** | Skills to close, sourced from JD patterns. |
| **Job Matches** | Live job feed (`jobs.json`), scored & sorted; per-job "✎ Tailor my Resume" that queues a GitHub Issue. |
| **External JD Resumes** | Resumes tailored from JDs pasted directly in chat (24 so far: boAt → Battery Smart). `.docx`+`.pdf` downloads, cover letters, match score, honest "why". Sorted newest-first. |
| **Applications / Interviews / Networking / Target Companies** | Tracking (per-device localStorage). |

### The two engineering hearts of the system
- **Honest scoring — `keyword_coverage_score()`** (in `build_resume.py`): % of a hand-curated Required-keyword list (10–20 real must-haves judged from the JD) that actually appears in the tailored resume. Deliberately NOT raw full-JD-text overlap (that scored a real match at 33%). Went through 3 bug-fix iterations (see CLAUDE.md "Scoring methodology gotchas"). OR-lists in a JD collapse to the one true alternative before scoring.
- **One-page auto-fit — `fit_to_page()`** (in `build_resume.py`): renders → converts to PDF (LibreOffice) → measures real page count + vertical fill → picks the loosest ATS-safe font/spacing preset (9.5–11pt) that fills exactly one page (~93–98%). Never spills to page 2; never leaves a big empty gap.

## 6. Key workflows
- **Automated jobs:** hourly GitHub Action runs `fetch_jobs.py` → pulls JSearch + Adzuna → scores → merges with `seed_jobs.json` → writes `jobs.json` → commits. Dashboard reads `jobs.json` at runtime.
- **Pasted-JD tailoring (the main flow now):** user pastes a JD in chat → Claude extracts real must-haves → tailors a copy of `build_resume.DATA` (only rewording/reordering real content + `experience_bank.md`) → runs `keyword_coverage_score()` → `fit_to_page()` → appends entry to `external_resumes.json` → commits/pushes → appears in the External JD Resumes tab.
- **Profile renovation:** Claude-in-Chrome updates Naukri, Foundit, iimjobs profiles to match (headline/summary/skills/projects), same honesty rules.

## 7. Success metrics
- Every tailored resume: **1 page, ≥93% fill, real computed score.**
- ≥90% match only when honestly earned; gaps reported plainly otherwise.
- Job feed refreshes hourly with no manual intervention.
- Master resume and all live profiles tell one consistent, honest story.

## 8. Guardrails / principles (non-negotiable)
1. **Never fabricate** achievements, employers, metrics, or scores.
2. **Report the true score** even if <90%; explain which keywords are missing.
3. **Ask** when real experience might close a gap (post-paid: flag & continue, don't block).
4. **One mention of "B2C" max** (it typecasts; broader-but-true framing preferred).
5. **Summary = positioning, not a metrics dump**; metrics live in the bullets.

## 9. Open items / future
- Activate JSearch paid-plan → unlock fresh Indeed/LinkedIn/Glassdoor.
- Align salary figure across Naukri (₹10.75L) / Foundit (₹11L) / iimjobs (₹9L) — user to confirm true current CTC.
- Two experience-bank open questions: formal cohort analysis; the in-house CDP/ops-engine ownership detail (he built both student & teacher sides — needs level confirmation + the 3,500+ teacher figure).
- Optional: private site (Cloudflare Access), cross-device sync of tracking (Supabase).
