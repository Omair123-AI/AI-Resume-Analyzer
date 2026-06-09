"""
ats_score.py - Calculate ATS score (0-100) across 6 weighted dimensions
"""
from utils.constants import ATS_WEIGHTS, SECTION_HEADERS
from utils.helpers import normalize_score, score_to_label


def calculate_ats_score(parsed_resume: dict) -> dict:
    """
    Returns full ATS breakdown + total score.
    """
    breakdown = {
        "skills":     _score_skills(parsed_resume),
        "keywords":   _score_keywords(parsed_resume),
        "experience": _score_experience(parsed_resume),
        "education":  _score_education(parsed_resume),
        "projects":   _score_projects(parsed_resume),
        "formatting": _score_formatting(parsed_resume),
    }

    total = sum(breakdown[k] * ATS_WEIGHTS[k] for k in breakdown)
    total = normalize_score(total * 100)

    return {
        "total":     total,
        "label":     score_to_label(total),
        "breakdown": {k: round(v * 100, 1) for k, v in breakdown.items()},
        "weights":   ATS_WEIGHTS,
    }


def _score_skills(r: dict) -> float:
    count = r.get("skills", {}).get("count", 0)
    hot   = len(r.get("skills", {}).get("hot_technology", []))
    # 10+ skills = full marks; bonus for hot-tech skills
    base  = min(count / 10, 1.0)
    bonus = min(hot / 5, 0.2)
    return min(base + bonus, 1.0)


def _score_keywords(r: dict) -> float:
    kw_count = len(r.get("keywords", []))
    return min(kw_count / 20, 1.0)


def _score_experience(r: dict) -> float:
    exp    = r.get("experience", {})
    years  = exp.get("total_years", 0)
    score  = min(years / 5, 0.7)          # 5 years = 70%
    if exp.get("has_internship"):
        score += 0.15
    if exp.get("has_leadership"):
        score += 0.15
    return min(score, 1.0)


def _score_education(r: dict) -> float:
    level = r.get("education", {}).get("highest_degree_level", 0)
    # Level 1-5 → 0.2 … 1.0
    return min(level * 0.2, 1.0)


def _score_projects(r: dict) -> float:
    projects = r.get("projects", {})
    count    = projects.get("count", 0)
    scores   = projects.get("quality_scores", [])
    if not scores:
        return min(count / 3, 0.5)
    avg_quality = sum(s["score"] for s in scores) / len(scores) / 100
    return min((count / 3) * 0.5 + avg_quality * 0.5, 1.0)


def _score_formatting(r: dict) -> float:
    """Check presence of key resume sections."""
    text  = r.get("raw_text", "").lower()
    score = 0.0
    for section, headers in SECTION_HEADERS.items():
        if any(h in text for h in headers):
            score += 1
    # 6 key sections → full marks
    return min(score / 6, 1.0)
