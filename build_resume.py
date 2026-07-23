# -*- coding: utf-8 -*-
"""
Renders Kshitiz Yadav's one-page ATS resume as a .docx.

DATA holds all resume content as a plain dict so a tailored variant (built by hand when
processing a "Tailor My Resume" request -- see CLAUDE.md) can pass a modified copy
(reworded/reordered bullets per a JD) through the same render() without duplicating the
docx layout code. jd_match_score() below scores a tailored variant against a JD.
"""
import os
from docx import Document
from docx.shared import Pt, RGBColor, Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

NAVY = RGBColor(0x1F, 0x38, 0x64)
BLUE = RGBColor(0x2E, 0x5A, 0xAC)
GREY = RGBColor(0x44, 0x44, 0x44)
DGREY = RGBColor(0x33, 0x33, 0x33)
FONT = "Calibri"

# ---- style presets ----
# render() takes a `style` dict controlling the knobs that drive vertical page-fill.
# fit_to_page() (below) picks the loosest preset that keeps the resume on exactly ONE page
# while filling it cleanly (~93-98%), so there's never a big empty gap at the bottom and it
# never spills onto a second page -- for any content volume (base or tailored variant).
# body = base body-font pt; head/name/company scale proportionally off it. line = line spacing.
# gap = space_after (pt) on body paragraphs & bullets; sec_before/sec_after = header spacing;
# sub_before = space before a bold sub-heading.
STYLE_DEFAULT = {
    "body": 9.5, "line": 1.0, "gap": 1.0,
    "sec_before": 5.0, "sec_after": 2.0, "sub_before": 3.0,
}

# Ordered tight -> loose. fit_to_page() walks these and keeps the fullest one that still fits
# on a single page. Fonts stay in the ATS-safe / readable 9.5-11pt band throughout. Steps are
# intentionally fine-grained (font AND line/gap increments interleaved) so a resume whose content
# sits between two font sizes -- where the bigger font overflows to 2 pages but the smaller one
# under-fills -- can still be nudged into the ~93-98% band via line spacing rather than falling
# back to a visibly short page.
STYLE_PRESETS = [
    {"body": 9.5,  "line": 1.00, "gap": 1.0, "sec_before": 5.0, "sec_after": 2.0, "sub_before": 3.0},
    {"body": 9.5,  "line": 1.06, "gap": 2.0, "sec_before": 6.0, "sec_after": 2.5, "sub_before": 3.5},
    {"body": 9.5,  "line": 1.11, "gap": 2.5, "sec_before": 6.5, "sec_after": 2.5, "sub_before": 3.5},
    {"body": 9.5,  "line": 1.16, "gap": 3.0, "sec_before": 7.0, "sec_after": 3.0, "sub_before": 4.0},
    {"body": 9.75, "line": 1.14, "gap": 3.0, "sec_before": 7.0, "sec_after": 3.0, "sub_before": 4.0},
    {"body": 9.5,  "line": 1.22, "gap": 3.5, "sec_before": 7.5, "sec_after": 3.0, "sub_before": 4.0},
    {"body": 10.0, "line": 1.06, "gap": 2.0, "sec_before": 6.0, "sec_after": 2.5, "sub_before": 3.5},
    {"body": 10.0, "line": 1.12, "gap": 3.0, "sec_before": 7.0, "sec_after": 3.0, "sub_before": 4.0},
    {"body": 10.0, "line": 1.18, "gap": 3.5, "sec_before": 7.5, "sec_after": 3.5, "sub_before": 4.5},
    {"body": 10.5, "line": 1.10, "gap": 3.0, "sec_before": 7.0, "sec_after": 3.0, "sub_before": 4.0},
    {"body": 10.5, "line": 1.16, "gap": 4.0, "sec_before": 8.0, "sec_after": 3.5, "sub_before": 4.5},
    {"body": 11.0, "line": 1.15, "gap": 4.0, "sec_before": 8.0, "sec_after": 4.0, "sub_before": 5.0},
    {"body": 11.0, "line": 1.22, "gap": 5.0, "sec_before": 9.0, "sec_after": 4.0, "sub_before": 5.5},
]

DATA = {
    "name": "KSHITIZ YADAV",
    "tagline": "Product Manager  |  Growth & Monetization  |  Consumer & Marketplace Platforms  |  Funnel, Retention & Payments  |  Data-Driven, AI-Enabled",
    "contact": "Gurugram, India  •  +91 8756972501  •  kshitizyadav788@gmail.com  •  linkedin.com/in/kshitizyadav",
    # Keep this SHORT (2-3 lines): positioning only -- who he is, what he owns, how he works, one
    # or two headline numbers. Do NOT restate the metrics that already appear in the bullets below;
    # that duplication was the reason this was rewritten (see CLAUDE.md "Master-resume conventions").
    "summary": (
        "Product Manager with 5+ years owning products end-to-end — from discovery and PRDs through launch, "
        "experimentation, and iteration — across consumer apps, a two-sided marketplace, and internal platform "
        "and CRM systems. Partners closely with engineering, design, and business teams, using data (SQL, Power BI, "
        "GA4) and AI to move core metrics. Track record of driving 20% revenue growth and ₹70L in product-led renewals."
    ),
    "experience": {
        "company_line": "PlanetSpark — Product Manager",
        "meta": "Gurugram · Mar 2021 – Present",
        "intro": "Own the full product suite of a B2C EdTech marketplace -- one of India's largest public speaking & creative writing platforms, connecting students and teachers via a shared LMS: consumer app, student & teacher LMS, sales CRM, product-led growth & renewal engine, and an in-house AI layer.",
        "groups": [
            {"heading": "Growth & Monetization", "bullets": [
                "Built the LPP (Learn, Practice, Perform) module — customized 1:1 sessions, group activities, and performance tasks — driving 20% revenue growth, 25% ARPU expansion (₹35K → ₹45K), and 50% higher revenue per class (₹600 → ₹900).",
                "Designed an in-product renewal engine (nudges, early-bird access, LMS free-trial classes, teacher-initiated renewals) that lowered sales cost and generated ₹70L in renewals in a single month (Jan 2025).",
                "Launched organic acquisition loops surfacing student progress (Sparkline, Word Wisdom, practice classes, workshops) across social channels, bringing 2,000+ organic leads/month at a 7% conversion rate.",
                "Built a counselor-wise P&L tracker computing weekly profitability per sales counselor (Net Revenue − Fixed, Refund, Marketing & Sales cost), giving each counselor the revenue figure needed to turn profitable — putting unit-economics visibility in the hands of the front line.",
            ]},
            {"heading": "Funnel & Platform (0→1)", "bullets": [
                "Re-architected the sign-up → demo → enrolment funnel: single-step OTP sign-in (replacing a two-step create-then-login flow), a preference-capture ranking model that surfaces best-fit courses during the counselor VC, 6 API-integrated payment gateways with pre-filled links, and auto-cleared parent-approval on payment — reducing drop-off across the sign-up, payment, and enrolment stages.",
                "Led the 0→1 launch of the consumer app MVP in 2 months (Feb–Mar 2024: ~1% organic revenue, +10% engagement); built the Student LMS (live classes, feedback reports, PTMs, in-house meeting room), raising course completion 15% and improving NPS.",
            ]},
            {"heading": "AI, Design & Automation", "bullets": [
                "Designed prototypes and MVP interfaces for the app, LMS, and CRM in Figma, Adobe Express, and Canva AI — using Gemini, Claude, ChatGPT, and Codex to accelerate iteration into clickable flows that aligned engineering and stakeholders before build.",
                "Shipped a production GenAI layer (speech/text learning with contextual, age-appropriate responses) and a support chatbot that cut escalations; revamped the Sales CRM (lead navigation, integrated calling, revenue tracking, target-vs-achievement, incentive management), cutting sales-ops workload 80%.",
                "Automated incentive flows and enrolment verification (100% coverage), saving ₹1.6L/month and eliminating fake-revenue reporting.",
            ]},
        ],
    },
    "competencies": "Product Strategy & Roadmapping · Monetization & Unit Economics · Retention & Lifecycle · Funnel & Conversion Optimization · Product Design & Prototyping · A/B Testing & Experimentation · GTM & North-Star Metrics · Consumer & Two-Sided Marketplace Platforms · GenAI Product Development · Stakeholder Management · User Research · Agile/Scrum",
    "skills": [
        ("Data & Analytics", "SQL, GA4, MS Excel (Advanced), Python (basic)"),
        ("Design & Prototyping", "Figma, Adobe Express, Canva AI, wireframing, clickable prototypes"),
        ("Product & Delivery", "JIRA, Confluence, Agile/Scrum, RICE prioritization"),
        ("AI & Integration", "OpenAI / Gemini / Claude APIs, Prompt Engineering, REST APIs, NLP use-cases"),
    ],
    "education": [
        ("BBA — Chandigarh University, Chandigarh", "2019 – 2021"),
        ("Class XII (ISC), St. Thomas High School, Kanpur", "2018"),
    ],
    "certifications": "Product Management Certification — Udemy (2024)    •    JIRA Certification — Udemy (2024)",
}


def render(data, out_path, style=None):
    s = dict(STYLE_DEFAULT)
    if style:
        s.update(style)
    body = s["body"]; line = s["line"]; gap = s["gap"]
    sec_before = s["sec_before"]; sec_after = s["sec_after"]; sub_before = s["sub_before"]
    # secondary fonts scale off body so a bump reads proportionally, staying ATS-readable
    head = body + 1.5; name_sz = body + 7.5; company_sz = body + 1.0
    tagline_sz = body; contact_sz = body - 0.5

    doc = Document()
    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal.font.size = Pt(body)
    normal.paragraph_format.space_after = Pt(gap)
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.line_spacing = line

    try:
        lb = doc.styles["List Bullet"]
        lb.font.name = FONT; lb.font.size = Pt(body)
        lb.paragraph_format.space_after = Pt(gap)
        lb.paragraph_format.space_before = Pt(0)
        lb.paragraph_format.line_spacing = line
    except KeyError:
        pass

    sec = doc.sections[0]
    sec.page_width = Mm(210); sec.page_height = Mm(297)        # A4
    sec.top_margin = Mm(9); sec.bottom_margin = Mm(9)
    sec.left_margin = Mm(12); sec.right_margin = Mm(12)

    def set_bottom_border(p):
        pPr = p._p.get_or_add_pPr()
        pbdr = OxmlElement('w:pBdr'); bottom = OxmlElement('w:bottom')
        bottom.set(qn('w:val'), 'single'); bottom.set(qn('w:sz'), '6')
        bottom.set(qn('w:space'), '1'); bottom.set(qn('w:color'), '2E5AAC')
        pbdr.append(bottom); pPr.append(pbdr)

    def header_line(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(sec_before); p.paragraph_format.space_after = Pt(sec_after)
        r = p.add_run(text.upper()); r.bold = True; r.font.size = Pt(head)
        r.font.color.rgb = NAVY; r.font.name = FONT
        set_bottom_border(p)

    def add_run(p, text, bold=False, italic=False, size=None, color=None):
        r = p.add_run(text); r.bold = bold; r.italic = italic
        r.font.size = Pt(size if size is not None else body); r.font.name = FONT
        if color is not None: r.font.color.rgb = color
        return r

    def bullet(parts):
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(gap); p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.line_spacing = line
        if isinstance(parts, str): add_run(p, parts)
        else:
            for txt, kw in parts: add_run(p, txt, **kw)

    def subhead(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(sub_before); p.paragraph_format.space_after = Pt(0)
        add_run(p, text, bold=True, italic=True, size=body, color=BLUE)

    def right_tab(p):
        cw = sec.page_width - sec.left_margin - sec.right_margin
        p.paragraph_format.tab_stops.add_tab_stop(cw, WD_TAB_ALIGNMENT.RIGHT)

    # -------- HEADER --------
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_after = Pt(0)
    add_run(p, data["name"], bold=True, size=name_sz, color=NAVY)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_after = Pt(0)
    add_run(p, data["tagline"], size=tagline_sz, color=GREY)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_after = Pt(gap)
    add_run(p, data["contact"], size=contact_sz, color=GREY)

    # -------- SUMMARY --------
    header_line("Professional Summary")
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(gap)
    add_run(p, data["summary"])

    # -------- EXPERIENCE --------
    header_line("Professional Experience")
    exp = data["experience"]
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(0); right_tab(p)
    add_run(p, exp["company_line"], bold=True, size=company_sz); add_run(p, "\t" + exp["meta"], color=GREY)
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(gap)
    add_run(p, exp["intro"], italic=True, color=DGREY)

    for g in exp["groups"]:
        subhead(g["heading"])
        for b in g["bullets"]:
            bullet(b)

    # -------- CORE COMPETENCIES --------
    header_line("Core Competencies")
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(gap)
    add_run(p, data["competencies"])

    # -------- TECHNICAL SKILLS --------
    header_line("Technical Skills & Tools")
    for label, text in data["skills"]:
        bullet([(label + ": ", {"bold": True}), (text, {})])

    # -------- EDUCATION --------
    header_line("Education")
    for school, dates in data["education"]:
        p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(gap); right_tab(p)
        add_run(p, school, bold=True); add_run(p, "\t" + dates, color=GREY)

    # -------- CERTIFICATIONS --------
    header_line("Certifications")
    bullet(data["certifications"])

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    doc.save(out_path)
    return out_path


def measure_pdf(pdf_path):
    """Return (page_count, fill_pct) for a rendered resume PDF. fill_pct is how far the lowest
    text baseline reaches down the first page as a % of page height -- our proxy for 'how full'."""
    from pypdf import PdfReader
    r = PdfReader(pdf_path)
    pages = len(r.pages)
    pg = r.pages[0]
    h = float(pg.mediabox.height)
    lowest = [h]
    def visitor(text, cm, tm, font, size):
        if text.strip():
            lowest[0] = min(lowest[0], tm[5])
    pg.extract_text(visitor_text=visitor)
    fill_pct = round(100 * (h - lowest[0]) / h, 1)
    return pages, fill_pct


def _render_to_pdf(data, docx_path, style):
    """Render docx with a style, convert to PDF via LibreOffice, return (pages, fill_pct, pdf_path)."""
    import subprocess, shutil
    render(data, docx_path, style=style)
    outdir = os.path.dirname(os.path.abspath(docx_path))
    soffice = shutil.which("soffice") or "/Applications/LibreOffice.app/Contents/MacOS/soffice"
    subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", outdir, docx_path],
                   check=True, capture_output=True)
    pdf_path = os.path.splitext(docx_path)[0] + ".pdf"
    pages, fill = measure_pdf(pdf_path)
    return pages, fill, pdf_path


def fit_to_page(data, out_path, target_lo=93.0, target_hi=98.0, verbose=True):
    """Render `data` at the loosest STYLE preset that still fits on exactly ONE page and fills
    it cleanly (fill% ideally in [target_lo, target_hi]). Requires LibreOffice (soffice) for the
    real page measurement -- there is no pure-Python way to know rendered page count/fill.

    Strategy: walk presets tight -> loose. Track the fullest single-page result seen. Stop early
    once a single-page result lands in the target band. Never returns a 2-page layout if any
    single-page option exists. Returns (chosen_style, pages, fill_pct, pdf_path).

    If even the tightest preset spills to 2 pages, the CONTENT is too long -- trim bullets/summary
    (see CLAUDE.md), don't just shrink further. If the loosest preset still under-fills, the
    content is too thin -- add a real bullet from experience_bank.md rather than bloating spacing."""
    best = None  # (fill, style, pages, pdf) among single-page renders
    for st in STYLE_PRESETS:
        pages, fill, pdf = _render_to_pdf(data, out_path, st)
        if verbose:
            print(f"  body={st['body']:>4} line={st['line']:.2f} gap={st['gap']:.0f} -> pages={pages} fill={fill}%")
        if pages == 1:
            if best is None or fill > best[0]:
                best = (fill, st, pages, pdf)
            if target_lo <= fill <= target_hi:
                break
    if best is None:
        # every preset overflowed: re-render tightest so output is at least the least-bad, and warn
        st = STYLE_PRESETS[0]
        pages, fill, pdf = _render_to_pdf(data, out_path, st)
        print(f"  WARNING: content too long for one page even at tightest preset (pages={pages}). "
              f"Trim content -- see CLAUDE.md.")
        return st, pages, fill, pdf
    fill, st, pages, pdf = best
    if fill < target_lo:
        print(f"  NOTE: best fill only {fill}% (< {target_lo}%). Content is thin -- consider adding "
              f"a real bullet from experience_bank.md rather than relying on spacing.")
    # ensure the on-disk docx matches the chosen style (last render may have been a different preset)
    render(data, out_path, style=st)
    _render_to_pdf(data, out_path, st)
    return st, pages, fill, pdf


def keyword_coverage_score(data, keywords):
    """Deterministic, honest match score: % of an EXPLICIT curated keyword/must-have list
    (extracted by hand from the JD while tailoring -- see CLAUDE.md step (b)) that actually
    appears in the tailored resume text. This is deliberately NOT raw full-JD-text word
    overlap -- a naive version of that scored a real tailored resume at 33% because JDs are
    full of generic connector words ("translate", "ensuring", "deliver") no resume would ever
    contain even when the underlying skill is genuinely covered. Real ATS systems and
    recruiters key off specific skill/tool/domain terms, not prose glue -- so should this.

    A multi-word keyword phrase matches if ALL of its significant words appear somewhere in the
    resume (not necessarily adjacent) -- exact contiguous substring matching was tried first and
    produced false negatives: "product development" didn't match "Product Ideation & Development"
    (words not adjacent), "market analysis" didn't match "market research and competitor analysis"
    (same concept, different word order/filler). Single-word keywords still match as substrings.

    `keywords` must be the actual must-have terms judged from reading the JD, not padded to
    inflate the score; the resulting number is only honest if that list is honest. Returns
    (score, matched, missing) so the gaps are visible, not just a bare percentage."""
    _filler = {"and", "the", "of", "a", "an", "for", "to", "in", "&"}
    bullets = " ".join(b for g in data["experience"]["groups"] for b in g["bullets"])
    resume_text = " ".join([
        data.get("summary", ""), data.get("competencies", ""),
        " ".join(t for _, t in data.get("skills", [])),
        bullets,
    ]).lower()

    def is_match(keyword):
        words = [w for w in keyword.lower().split() if w not in _filler]
        return all(w in resume_text for w in words) if words else False

    matched = [k for k in keywords if is_match(k)]
    missing = [k for k in keywords if not is_match(k)]
    score = round(100 * len(matched) / len(keywords)) if keywords else None
    return score, matched, missing


if __name__ == "__main__":
    _here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(_here, "resumes", "Kshitiz Yadav - Product Manager Resume.docx")
    print("Auto-fitting base resume to one full page...")
    style, pages, fill, pdf = fit_to_page(DATA, out)
    print(f"saved: {out}")
    print(f"       {pdf}")
    print(f"final: pages={pages}, fill={fill}%, style body={style['body']}pt line={style['line']}")
