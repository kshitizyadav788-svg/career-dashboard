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

# ---- tunables (tightened for single page) ----
BODY = 9.5
HEAD = 11.0
NAME = 17.0
LINE = 1.0

DATA = {
    "name": "KSHITIZ YADAV",
    "tagline": "Product Manager  |  B2C Consumer Apps  |  Growth & Monetization  |  Two-Sided Platforms  |  AI-Enabled",
    "contact": "Gurugram, India  •  +91 8756972501  •  kshitizyadav788@gmail.com  •  linkedin.com/in/kshitizyadav",
    "summary": (
        "Product Manager with 5+ years owning the full B2C product lifecycle across a consumer app, a two-sided "
        "student/teacher LMS, a sales CRM, and a product-led growth & renewal engine at a high-growth EdTech startup. "
        "Consistent record of moving core metrics — 20% revenue growth, 25% ARPU expansion, ₹70L in product-led "
        "renewals, and 2,000+ organic leads/month at 7% conversion. Pairs monetization and unit-economics thinking "
        "with hands-on data analysis (SQL, GA4), A/B testing, and shipping production GenAI features; works across "
        "engineering, design, marketing, sales, and operations."
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
    "competencies": "Product Strategy & Roadmapping · Monetization & Unit Economics · Retention & Lifecycle · Funnel & Conversion Optimization · Product Design & Prototyping · A/B Testing & Experimentation · GTM & North-Star Metrics · B2C & Two-Sided Platforms · GenAI Product Development · Stakeholder Management · User Research · Agile/Scrum",
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


def render(data, out_path):
    doc = Document()
    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal.font.size = Pt(BODY)
    normal.paragraph_format.space_after = Pt(1)
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.line_spacing = LINE

    try:
        lb = doc.styles["List Bullet"]
        lb.font.name = FONT; lb.font.size = Pt(BODY)
        lb.paragraph_format.space_after = Pt(1)
        lb.paragraph_format.space_before = Pt(0)
        lb.paragraph_format.line_spacing = LINE
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
        p.paragraph_format.space_before = Pt(5); p.paragraph_format.space_after = Pt(2)
        r = p.add_run(text.upper()); r.bold = True; r.font.size = Pt(HEAD)
        r.font.color.rgb = NAVY; r.font.name = FONT
        set_bottom_border(p)

    def add_run(p, text, bold=False, italic=False, size=BODY, color=None):
        r = p.add_run(text); r.bold = bold; r.italic = italic
        r.font.size = Pt(size); r.font.name = FONT
        if color is not None: r.font.color.rgb = color
        return r

    def bullet(parts):
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(1); p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.line_spacing = LINE
        if isinstance(parts, str): add_run(p, parts)
        else:
            for txt, kw in parts: add_run(p, txt, **kw)

    def subhead(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(3); p.paragraph_format.space_after = Pt(0)
        add_run(p, text, bold=True, italic=True, size=BODY, color=BLUE)

    def right_tab(p):
        cw = sec.page_width - sec.left_margin - sec.right_margin
        p.paragraph_format.tab_stops.add_tab_stop(cw, WD_TAB_ALIGNMENT.RIGHT)

    # -------- HEADER --------
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_after = Pt(0)
    add_run(p, data["name"], bold=True, size=NAME, color=NAVY)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_after = Pt(0)
    add_run(p, data["tagline"], size=9.5, color=GREY)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_after = Pt(1)
    add_run(p, data["contact"], size=9.0, color=GREY)

    # -------- SUMMARY --------
    header_line("Professional Summary")
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(1)
    add_run(p, data["summary"])

    # -------- EXPERIENCE --------
    header_line("Professional Experience")
    exp = data["experience"]
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(0); right_tab(p)
    add_run(p, exp["company_line"], bold=True, size=10.5); add_run(p, "\t" + exp["meta"], color=GREY)
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(1)
    add_run(p, exp["intro"], italic=True, color=DGREY)

    for g in exp["groups"]:
        subhead(g["heading"])
        for b in g["bullets"]:
            bullet(b)

    # -------- CORE COMPETENCIES --------
    header_line("Core Competencies")
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(1)
    add_run(p, data["competencies"])

    # -------- TECHNICAL SKILLS --------
    header_line("Technical Skills & Tools")
    for label, text in data["skills"]:
        bullet([(label + ": ", {"bold": True}), (text, {})])

    # -------- EDUCATION --------
    header_line("Education")
    for school, dates in data["education"]:
        p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(1); right_tab(p)
        add_run(p, school, bold=True); add_run(p, "\t" + dates, color=GREY)

    # -------- CERTIFICATIONS --------
    header_line("Certifications")
    bullet(data["certifications"])

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    doc.save(out_path)
    return out_path


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
    render(DATA, out)
    print("saved:", out)
