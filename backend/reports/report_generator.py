"""
report_generator.py - Generate polished multi-page PDF report using ReportLab
"""
import os
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# ── Brand Colors ──────────────────────────────────────────────────────────────
PRIMARY = colors.HexColor("#4F46E5")
SECONDARY = colors.HexColor("#7C3AED")
SUCCESS = colors.HexColor("#059669")
WARNING = colors.HexColor("#D97706")
DANGER = colors.HexColor("#DC2626")
LIGHT_BG = colors.HexColor("#F8FAFC")
BORDER = colors.HexColor("#E2E8F0")
DARK_TEXT = colors.HexColor("#1E293B")
GRAY_TEXT = colors.HexColor("#64748B")

# Skill casing fixes
SPECIAL_CASES = {
    "nlp": "NLP", "llm": "LLM", "sql": "SQL", "nosql": "NoSQL",
    "css": "CSS", "html": "HTML", "api": "API", "rest api": "REST API",
    "oop": "OOP", "jwt": "JWT", "aws": "AWS", "gcp": "GCP",
    "ci/cd": "CI/CD", "vs code": "VS Code", "github": "GitHub",
    "gitlab": "GitLab", "node.js": "Node.js", "next.js": "Next.js",
    "vue.js": "Vue.js", "express.js": "Express.js", "mlops": "MLOps",
    "devops": "DevOps", "pytorch": "PyTorch", "tensorflow": "TensorFlow",
    "scikit-learn": "Scikit-learn", "opencv": "OpenCV", "fastapi": "FastAPI",
    "mongodb": "MongoDB", "postgresql": "PostgreSQL", "graphql": "GraphQL",
    "rag": "RAG", "bert": "BERT", "yolo": "YOLO", "cuda": "CUDA",
    "etl": "ETL", "openai api": "OpenAI API", "langchain": "LangChain",
    "numpy": "NumPy", "pandas": "Pandas", "matplotlib": "Matplotlib",
    "docker": "Docker", "kubernetes": "Kubernetes", "firebase": "Firebase",
    "redis": "Redis", "mysql": "MySQL", "sqlite": "SQLite",
    "react native": "React Native", "tailwind css": "Tailwind CSS",
    "power bi": "Power BI", "apache spark": "Apache Spark",
    "hugging face": "Hugging Face", "vector database": "Vector Database",
    "google cloud": "Google Cloud", "spring boot": "Spring Boot",
    "github actions": "GitHub Actions", "figma": "Figma",
    "keras": "Keras", "jupyter": "Jupyter", "react": "React",
    "redux": "Redux", "git": "Git", "linux": "Linux", "nginx": "Nginx",
}


def _fix_case(text: str) -> str:
    return SPECIAL_CASES.get(text.lower().strip(), text.strip().title())


def generate_report(analysis_data: dict, output_path: str) -> str:
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
    )
    styles = _build_styles()
    story = []

    story += _cover_page(analysis_data, styles)
    story.append(PageBreak())
    story += _section_resume_info(analysis_data, styles)
    story.append(Spacer(1, 0.5*cm))
    story += _section_ats_score(analysis_data, styles)
    story.append(Spacer(1, 0.5*cm))
    story += _section_skills(analysis_data, styles)

    if analysis_data.get("missing_skills"):
        story.append(Spacer(1, 0.5*cm))
        story += _section_missing_skills(analysis_data, styles)

    if analysis_data.get("career_readiness"):
        story.append(Spacer(1, 0.5*cm))
        story += _section_career_readiness(analysis_data, styles)

    if analysis_data.get("jd_match"):
        story.append(Spacer(1, 0.5*cm))
        story += _section_jd_match(analysis_data, styles)

    if analysis_data.get("suggestions"):
        story.append(Spacer(1, 0.5*cm))
        story += _section_suggestions(analysis_data, styles)

    if analysis_data.get("learning_roadmap", {}).get("steps"):
        story.append(PageBreak())
        story += _section_roadmap(analysis_data, styles)

    story += _footer_note(styles)
    doc.build(story)
    return output_path


# ── Section builders ───────────────────────────────────────────────────────────

def _cover_page(data: dict, styles: dict) -> list:
    elements = []
    elements.append(Spacer(1, 2.5*cm))
    elements.append(Paragraph("AI Resume Analyzer", styles["cover_title"]))
    elements.append(Spacer(1, 0.4*cm))
    elements.append(Paragraph("Career Assessment Report",
                    styles["cover_subtitle"]))
    elements.append(Spacer(1, 0.8*cm))
    elements.append(HRFlowable(width="80%", thickness=2,
                    color=PRIMARY, hAlign="CENTER"))
    elements.append(Spacer(1, 0.8*cm))

    name = data.get("parsed", {}).get("name", "Candidate")
    elements.append(Paragraph(name, styles["cover_name"]))
    elements.append(Spacer(1, 0.4*cm))

    ats = data.get("ats", {}).get("total", 0)
    elements.append(Paragraph(f"ATS Score: {ats}/100", styles["cover_score"]))
    elements.append(Spacer(1, 1.5*cm))
    elements.append(Paragraph(
        f"Generated: {datetime.now().strftime('%B %d, %Y')}",
        styles["cover_date"]
    ))
    return elements


def _section_header(title: str, styles: dict) -> list:
    return [
        Spacer(1, 0.2*cm),
        Paragraph(title, styles["section_header"]),
        HRFlowable(width="100%", thickness=1, color=PRIMARY),
        Spacer(1, 0.3*cm),
    ]


def _section_resume_info(data: dict, styles: dict) -> list:
    elements = _section_header("Resume Information", styles)
    parsed = data.get("parsed", {})
    rows = [
        ["Name",     parsed.get("name",     "—")],
        ["Email",    parsed.get("email",    "—")],
        ["Phone",    parsed.get("phone",    "—")],
        ["LinkedIn", parsed.get("linkedin", "—") or "—"],
        ["GitHub",   parsed.get("github",   "—") or "—"],
    ]
    t = Table(rows, colWidths=[4*cm, 13*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",     (0, 0), (0, -1), LIGHT_BG),
        ("TEXTCOLOR",      (0, 0), (0, -1), PRIMARY),
        ("FONTNAME",       (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE",       (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, LIGHT_BG]),
        ("GRID",           (0, 0), (-1, -1), 0.5, BORDER),
        ("PADDING",        (0, 0), (-1, -1), 6),
        ("VALIGN",         (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elements.append(t)
    return elements


def _color_hex(color) -> str:
    """Return hex color string for ReportLab paragraph markup."""
    hex_str = color.hexval()  # returns '0x059669'
    return '#' + hex_str[2:]  # strip '0x' prefix → '#059669'


def _section_ats_score(data: dict, styles: dict) -> list:
    elements = _section_header("ATS Score Breakdown", styles)
    ats = data.get("ats", {})
    total = ats.get("total", 0)
    label = ats.get("label", "")
    breakdown = ats.get("breakdown", {})
    weights = ats.get("weights", {})

    color_hex = "059669" if total >= 70 else "D97706" if total >= 50 else "DC2626"
    elements.append(Paragraph(
        f'<font color="#{color_hex}"><b>Total ATS Score: {total}/100 — {label}</b></font>',
        styles["body"]
    ))
    elements.append(Spacer(1, 0.3*cm))

    if breakdown:
        # Header row
        header_row = Table(
            [[
                Paragraph("<b>Category</b>", ParagraphStyle("h1", fontSize=8,
                          fontName="Helvetica-Bold", textColor=colors.white)),
                Paragraph("<b>Score</b>",    ParagraphStyle("h2", fontSize=8,
                          fontName="Helvetica-Bold", textColor=colors.white, alignment=1)),
                Paragraph("<b>Weight</b>",   ParagraphStyle("h3", fontSize=8,
                          fontName="Helvetica-Bold", textColor=colors.white, alignment=1)),
                Paragraph("<b>Progress</b>", ParagraphStyle("h4", fontSize=8,
                          fontName="Helvetica-Bold", textColor=colors.white, alignment=1)),
            ]],
            colWidths=[5*cm, 2*cm, 1.5*cm, 8.5*cm]
        )
        header_row.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), PRIMARY),
            ("PADDING",    (0, 0), (-1, -1), 6),
            ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
        ]))
        elements.append(header_row)
        elements.append(Spacer(1, 0.1*cm))

        for cat, score in breakdown.items():
            score_f = float(score)
            weight = int(weights.get(cat, 0) * 100)
            filled = max(0, min(20, round(score_f / 5)))  # 20 cells = 100%
            empty = 20 - filled

            # Score label
            cat_color = colors.HexColor("#059669") if score_f >= 70 else \
                colors.HexColor("#D97706") if score_f >= 40 else \
                colors.HexColor("#DC2626")

            # Build progress bar using colored table cells
            bar_cells = []
            for i in range(20):
                if i < filled:
                    bar_cells.append("")
                else:
                    bar_cells.append("")

            # Row: category | score | weight | [progress bar as colored table]
            label_row = Table(
                [[
                    Paragraph(f"<b>{cat.title()}</b>", ParagraphStyle("lbl",
                              fontSize=8, fontName="Helvetica-Bold", textColor=DARK_TEXT)),
                    Paragraph(f"<font color='{_color_hex(cat_color)}'><b>{score_f:.0f}%</b></font>",
                              ParagraphStyle("sc", fontSize=8, fontName="Helvetica-Bold", alignment=1)),
                    Paragraph(f"{weight}%", ParagraphStyle(
                        "wt", fontSize=7, textColor=GRAY_TEXT, alignment=1)),
                ]],
                colWidths=[5*cm, 2*cm, 1.5*cm]
            )
            label_row.setStyle(TableStyle(
                [("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))

            # Progress bar table
            bar_data = [bar_cells]
            bar_widths = [0.43*cm] * 20
            bar_table = Table(bar_data, colWidths=bar_widths,
                              rowHeights=[0.35*cm])
            bar_styles = [
                ("GRID",    (0, 0), (-1, -1), 0.3, colors.white),
                ("PADDING", (0, 0), (-1, -1), 0),
                ("VALIGN",  (0, 0), (-1, -1), "MIDDLE"),
            ]
            for i in range(20):
                if i < filled:
                    bar_styles.append(
                        ("BACKGROUND", (i, 0), (i, 0), cat_color))
                else:
                    bar_styles.append(
                        ("BACKGROUND", (i, 0), (i, 0), colors.HexColor("#E2E8F0")))
            bar_table.setStyle(TableStyle(bar_styles))

            # Combine label + bar
            combined = Table(
                [[label_row, bar_table]],
                colWidths=[8.5*cm, 8.5*cm]
            )
            combined.setStyle(TableStyle([
                ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING",  (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING",   (0, 0), (-1, -1), 3),
                ("LINEBELOW", (0, 0), (-1, -1), 0.3, BORDER),
            ]))
            elements.append(combined)

    return elements


def _section_skills(data: dict, styles: dict) -> list:
    elements = _section_header("Extracted Skills", styles)
    skills = data.get("parsed", {}).get("skills", {})
    found = skills.get("found", [])

    if found:
        # Fix casing for all skills
        found_fixed = [_fix_case(s) for s in found]
        chunks = [found_fixed[i:i+5] for i in range(0, len(found_fixed), 5)]
        rows = [["  |  ".join(chunk)] for chunk in chunks]
        t = Table(rows, colWidths=[17*cm])
        t.setStyle(TableStyle([
            ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, LIGHT_BG]),
            ("FONTSIZE",       (0, 0), (-1, -1), 9),
            ("PADDING",        (0, 0), (-1, -1), 5),
            ("GRID",           (0, 0), (-1, -1), 0.5, BORDER),
        ]))
        elements.append(t)
    else:
        elements.append(Paragraph("No skills detected.", styles["body"]))

    hot = skills.get("hot_technology", [])
    if hot:
        hot_fixed = [_fix_case(s) for s in hot]
        elements.append(Spacer(1, 0.3*cm))
        elements.append(Paragraph(
            f"<b>Hot Technologies:</b> {', '.join(hot_fixed)}",
            styles["highlight"]
        ))
    return elements


def _section_missing_skills(data: dict, styles: dict) -> list:
    elements = _section_header("Missing Skills", styles)
    ms = data.get("missing_skills", {})
    role = ms.get("role", "")
    missing = [_fix_case(s) for s in ms.get("missing_skills", [])]
    priority = [_fix_case(s) for s in ms.get("priority_missing", [])]
    match_pct = ms.get("match_percentage", 0)

    if role:
        elements.append(Paragraph(
            f"<b>Target Role:</b> {role}  |  <b>Skill Match:</b> {match_pct}%",
            styles["body"]
        ))
        elements.append(Spacer(1, 0.3*cm))
    if priority:
        elements.append(Paragraph(
            f"<b>Priority Missing (High Demand):</b> {', '.join(priority[:8])}",
            styles["warning_text"]
        ))
    if missing:
        elements.append(Spacer(1, 0.2*cm))
        elements.append(Paragraph(
            f"<b>All Missing Skills:</b> {', '.join(missing[:15])}",
            styles["body"]
        ))
    return elements


def _section_career_readiness(data: dict, styles: dict) -> list:
    elements = _section_header("Career Readiness Score", styles)
    cr = data.get("career_readiness", {})
    score = cr.get("score", 0)
    label = cr.get("label", "")
    breakdown = cr.get("breakdown", {})

    color_hex = "059669" if score >= 70 else "D97706" if score >= 50 else "DC2626"
    elements.append(Paragraph(
        f'<font color="#{color_hex}"><b>Score: {score}/100 — {label}</b></font>',
        styles["body"]
    ))
    elements.append(Spacer(1, 0.3*cm))

    if breakdown:
        rows = [[_fix_case(cat), f"{val}%"] for cat, val in breakdown.items()]
        t = Table(rows, colWidths=[8*cm, 9*cm])
        t.setStyle(TableStyle([
            ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, LIGHT_BG]),
            ("FONTSIZE",       (0, 0), (-1, -1), 9),
            ("GRID",           (0, 0), (-1, -1), 0.5, BORDER),
            ("PADDING",        (0, 0), (-1, -1), 5),
        ]))
        elements.append(t)
    return elements


def _section_jd_match(data: dict, styles: dict) -> list:
    elements = _section_header("Job Description Match", styles)
    jd = data.get("jd_match", {})
    score = jd.get("final_match_score", jd.get("match_score", 0))
    grade = jd.get("grade", "")

    elements.append(
        Paragraph(f"<b>Match Score: {score}% — {grade}</b>", styles["body"]))
    missing_kw = jd.get("missing_keywords", [])
    if missing_kw:
        elements.append(Spacer(1, 0.3*cm))
        elements.append(Paragraph(
            f"<b>Missing Keywords:</b> {', '.join([_fix_case(k) for k in missing_kw[:10]])}",
            styles["warning_text"]
        ))
    return elements


def _section_suggestions(data: dict, styles: dict) -> list:
    elements = _section_header("AI Improvement Suggestions", styles)
    sugg = data.get("suggestions", {})

    feedback = sugg.get("overall_feedback", "")
    if feedback:
        elements.append(Paragraph(feedback, styles["body"]))
        elements.append(Spacer(1, 0.3*cm))

    quick_wins = sugg.get("quick_wins", [])
    if quick_wins:
        elements.append(Paragraph("<b>Quick Wins:</b>", styles["body"]))
        for w in quick_wins:
            elements.append(Paragraph(f"• {w}", styles["bullet"]))

    priority = sugg.get("priority_actions", [])
    if priority:
        elements.append(Spacer(1, 0.3*cm))
        elements.append(Paragraph("<b>Priority Actions:</b>", styles["body"]))
        for i, action in enumerate(priority, 1):
            elements.append(Paragraph(f"{i}. {action}", styles["bullet"]))

    # Section tips — now included in PDF
    section_tips = sugg.get("section_tips", {})
    if section_tips:
        elements.append(Spacer(1, 0.3*cm))
        elements.append(Paragraph("<b>Section Tips:</b>", styles["body"]))
        rows = [[k.title(), v] for k, v in section_tips.items()]
        t = Table(rows, colWidths=[3.5*cm, 13.5*cm])
        t.setStyle(TableStyle([
            ("TEXTCOLOR",      (0, 0), (0, -1), PRIMARY),
            ("FONTNAME",       (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE",       (0, 0), (-1, -1), 8),
            ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, LIGHT_BG]),
            ("GRID",           (0, 0), (-1, -1), 0.5, BORDER),
            ("PADDING",        (0, 0), (-1, -1), 5),
            ("VALIGN",         (0, 0), (-1, -1), "TOP"),
        ]))
        elements.append(t)

    return elements


def _section_roadmap(data: dict, styles: dict) -> list:
    elements = _section_header("Personalized Learning Roadmap", styles)
    roadmap = data.get("learning_roadmap", {})
    goal = roadmap.get("goal", "")
    est = roadmap.get("estimated_time", "")
    steps = roadmap.get("steps", [])

    if goal:
        elements.append(Paragraph(
            f"<b>Goal:</b> {goal}  |  <b>Estimated Time:</b> {est}",
            styles["body"]
        ))
        elements.append(Spacer(1, 0.4*cm))

    STEP_COLORS = [
        colors.HexColor("#4F46E5"),
        colors.HexColor("#7C3AED"),
        colors.HexColor("#0891B2"),
        colors.HexColor("#059669"),
        colors.HexColor("#D97706"),
    ]

    for i, s in enumerate(steps):
        step_num = str(s.get("step", i + 1))
        title = s.get("title", "")
        desc = s.get("description", "")
        resources = s.get("resources", [])
        duration = s.get("duration", "")
        color = STEP_COLORS[i % len(STEP_COLORS)]

        # Step number circle
        num_cell = Table(
            [[Paragraph(f"<b>{step_num}</b>",
                        ParagraphStyle("num", fontSize=11, fontName="Helvetica-Bold",
                                       textColor=colors.white, alignment=1))]],
            colWidths=[1*cm], rowHeights=[1*cm]
        )
        num_cell.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), color),
            ("PADDING",    (0, 0), (-1, -1), 0),
            ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
            ("ROUNDEDCORNERS", [5]),
        ]))

        # Resources badges
        res_str = "  •  ".join(resources[:4]) if resources else "—"

        # Content cell
        content_inner = Table(
            [
                [Paragraph(f"<b>{title}</b>",
                           ParagraphStyle("stitle", fontSize=10, fontName="Helvetica-Bold",
                                          textColor=DARK_TEXT))],
                [Paragraph(desc,
                           ParagraphStyle("sdesc", fontSize=8, fontName="Helvetica",
                                          textColor=GRAY_TEXT, leading=11))],
                [Paragraph(f"<font color='#{color.hexval()[2:]}'><b>Resources:</b></font> {res_str}  "
                           f"<font color='#D97706'><b>| {duration}</b></font>",
                           ParagraphStyle("sres", fontSize=7, fontName="Helvetica",
                                          textColor=DARK_TEXT))],
            ],
            colWidths=[15.5*cm]
        )
        content_inner.setStyle(TableStyle([
            ("PADDING",      (0, 0), (-1, -1), 2),
            ("TOPPADDING",   (0, 0), (-1, 0), 4),
            ("BOTTOMPADDING", (0, -1), (-1, -1), 4),
        ]))

        # Row: number + content
        row = Table(
            [[num_cell, content_inner]],
            colWidths=[1.2*cm, 15.8*cm]
        )
        row.setStyle(TableStyle([
            ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING",  (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING",   (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("BACKGROUND",   (0, 0), (-1, -1),
             colors.white if i % 2 == 0 else LIGHT_BG),
            ("LINEBELOW",    (0, 0), (-1, -1), 0.5, BORDER),
        ]))
        elements.append(row)

    return elements


def _footer_note(styles: dict) -> list:
    return [
        Spacer(1, 1*cm),
        HRFlowable(width="100%", thickness=0.5, color=BORDER),
        Paragraph(
            "Generated by AI Resume Analyzer • Report is for guidance only",
            styles["footer"]
        ),
    ]


# ── Styles ─────────────────────────────────────────────────────────────────────

def _build_styles() -> dict:
    return {
        "cover_title": ParagraphStyle(
            "cover_title", fontSize=26, textColor=PRIMARY,
            alignment=TA_CENTER, fontName="Helvetica-Bold", spaceAfter=6),
        "cover_subtitle": ParagraphStyle(
            "cover_subtitle", fontSize=15, textColor=SECONDARY,
            alignment=TA_CENTER, fontName="Helvetica", spaceAfter=4),
        "cover_name": ParagraphStyle(
            "cover_name", fontSize=20, textColor=DARK_TEXT,
            alignment=TA_CENTER, fontName="Helvetica-Bold", spaceAfter=4),
        "cover_score": ParagraphStyle(
            "cover_score", fontSize=13, textColor=SUCCESS,
            alignment=TA_CENTER, fontName="Helvetica-Bold"),
        "cover_date": ParagraphStyle(
            "cover_date", fontSize=9, textColor=GRAY_TEXT,
            alignment=TA_CENTER, fontName="Helvetica"),
        "section_header": ParagraphStyle(
            "section_header", fontSize=12, textColor=PRIMARY,
            fontName="Helvetica-Bold", spaceAfter=3, spaceBefore=4),
        "body": ParagraphStyle(
            "body", fontSize=9, textColor=DARK_TEXT,
            fontName="Helvetica", spaceAfter=3, leading=13),
        "bullet": ParagraphStyle(
            "bullet", fontSize=8, textColor=DARK_TEXT,
            fontName="Helvetica", leftIndent=10, spaceAfter=2),
        "highlight": ParagraphStyle(
            "highlight", fontSize=8, textColor=SUCCESS,
            fontName="Helvetica-Bold", spaceAfter=3),
        "warning_text": ParagraphStyle(
            "warning_text", fontSize=8, textColor=WARNING,
            fontName="Helvetica-Bold", spaceAfter=3),
        "footer": ParagraphStyle(
            "footer", fontSize=7, textColor=GRAY_TEXT,
            alignment=TA_CENTER, fontName="Helvetica"),
    }
