# -*- coding: utf-8 -*-
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
add_run(p, "KSHITIZ YADAV", bold=True, size=NAME, color=NAVY)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_after = Pt(0)
add_run(p, "Product Manager  |  B2C Consumer Apps  |  Growth & Monetization  |  Two-Sided Platforms  |  AI-Enabled", size=9.5, color=GREY)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_after = Pt(1)
add_run(p, "Gurugram, India  •  +91 8756972501  •  kshitizyadav788@gmail.com  •  linkedin.com/in/kshitizyadav", size=9.0, color=GREY)

# -------- SUMMARY --------
header_line("Professional Summary")
p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(1)
add_run(p, ("Product Manager with 5+ years owning the full B2C product lifecycle across a consumer app, a two-sided "
            "student/teacher LMS, a sales CRM, and a product-led growth & renewal engine at a high-growth EdTech startup. "
            "Consistent record of moving core metrics — 20% revenue growth, 25% ARPU expansion, ₹70L in product-led "
            "renewals, and 2,000+ organic leads/month at 7% conversion. Pairs monetization and unit-economics thinking "
            "with hands-on data analysis (SQL, GA4), A/B testing, and shipping production GenAI features; works across "
            "engineering, design, marketing, sales, and operations."))

# -------- EXPERIENCE --------
header_line("Professional Experience")
p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(0); right_tab(p)
add_run(p, "PlanetSpark — Product Manager", bold=True, size=10.5); add_run(p, "\tGurugram · Mar 2021 – Present", color=GREY)
p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(1)
add_run(p, "Own the full product suite of a B2C EdTech startup: consumer app, student & teacher LMS, sales CRM, product-led growth & renewal engine, and an in-house AI layer.", italic=True, color=DGREY)

subhead("Growth & Monetization")
bullet("Built the LPP (Learn, Practice, Perform) module — customized 1:1 sessions, group activities, and performance tasks — driving 20% revenue growth, 25% ARPU expansion (₹35K → ₹45K), and 50% higher revenue per class (₹600 → ₹900).")
bullet("Designed an in-product renewal engine (nudges, early-bird access, LMS free-trial classes, teacher-initiated renewals) that lowered sales cost and generated ₹70L in renewals in a single month (Jan 2025).")
bullet("Launched organic acquisition loops surfacing student progress (Sparkline, Word Wisdom, practice classes, workshops) across social channels, bringing 2,000+ organic leads/month at a 7% conversion rate.")

subhead("Funnel & Platform (0→1)")
bullet("Re-architected the sign-up → demo → enrolment funnel: single-step OTP sign-in (replacing a two-step create-then-login flow), a preference-capture ranking model that surfaces best-fit courses during the counselor VC, 6 API-integrated payment gateways with pre-filled links, and auto-cleared parent-approval on payment — reducing drop-off across the sign-up, payment, and enrolment stages.")
bullet("Led the 0→1 launch of the consumer app MVP in 2 months (Feb–Mar 2024: ~1% organic revenue, +10% engagement); built the Student LMS (live classes, feedback reports, PTMs, in-house meeting room), raising course completion 15% and improving NPS.")

subhead("AI, Design & Automation")
bullet("Designed prototypes and MVP interfaces for the app, LMS, and CRM in Figma, Adobe Express, and Canva AI — using Gemini, Claude, ChatGPT, and Codex to accelerate iteration into clickable flows that aligned engineering and stakeholders before build.")
bullet("Shipped a production GenAI layer (speech/text learning with contextual, age-appropriate responses) and a support chatbot that cut escalations; revamped the Sales CRM (lead navigation, integrated calling, revenue tracking, target-vs-achievement, incentive management), cutting sales-ops workload 80%.")
bullet("Automated incentive flows and enrolment verification (100% coverage), saving ₹1.6L/month and eliminating fake-revenue reporting.")

# -------- CORE COMPETENCIES --------
header_line("Core Competencies")
p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(1)
add_run(p, "Product Strategy & Roadmapping · Monetization & Unit Economics · Retention & Lifecycle · Funnel & Conversion Optimization · Product Design & Prototyping · A/B Testing & Experimentation · GTM & North-Star Metrics · B2C & Two-Sided Platforms · GenAI Product Development · Stakeholder Management · User Research · Agile/Scrum")

# -------- TECHNICAL SKILLS --------
header_line("Technical Skills & Tools")
bullet([("Data & Analytics: ", {"bold":True}), ("SQL, GA4, MS Excel (Advanced), Python (basic)", {})])
bullet([("Design & Prototyping: ", {"bold":True}), ("Figma, Adobe Express, Canva AI, wireframing, clickable prototypes", {})])
bullet([("Product & Delivery: ", {"bold":True}), ("JIRA, Confluence, Agile/Scrum, RICE prioritization", {})])
bullet([("AI & Integration: ", {"bold":True}), ("OpenAI / Gemini / Claude APIs, Prompt Engineering, REST APIs, NLP use-cases", {})])

# -------- EDUCATION --------
header_line("Education")
p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(1); right_tab(p)
add_run(p, "BBA — Chandigarh University, Chandigarh", bold=True); add_run(p, "\t2019 – 2021", color=GREY)
p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(1); right_tab(p)
add_run(p, "Class XII (ISC), St. Thomas High School, Kanpur"); add_run(p, "\t2018", color=GREY)

# -------- CERTIFICATIONS --------
header_line("Certifications")
bullet("Product Management Certification — Udemy (2024)    •    JIRA Certification — Udemy (2024)")

# portable: writes next to this script, in ./resumes/  (works on Windows + Mac)
_here = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(_here, "resumes"), exist_ok=True)
out = os.path.join(_here, "resumes", "Kshitiz Yadav - Product Manager Resume.docx")
doc.save(out)
print("saved:", out)
