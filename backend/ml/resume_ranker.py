"""
resume_ranker.py - Assign a rank label based on ATS score
"""
from utils.helpers import score_to_label, normalize_score


def rank_resume(ats_score: float, parsed_resume: dict) -> dict:
    label = score_to_label(ats_score)

    strengths   = _identify_strengths(parsed_resume)
    weaknesses  = _identify_weaknesses(parsed_resume)
    percentile  = _estimate_percentile(ats_score)

    return {
        "rank":        label,
        "ats_score":   ats_score,
        "percentile":  percentile,
        "strengths":   strengths,
        "weaknesses":  weaknesses,
        "next_steps":  _next_steps(label),
    }


def _identify_strengths(r: dict) -> list[str]:
    strengths = []
    skills = r.get("skills", {})
    if skills.get("count", 0) >= 10:
        strengths.append(f"Strong skill set with {skills['count']} skills detected.")
    if r.get("experience", {}).get("has_leadership"):
        strengths.append("Leadership experience demonstrated.")
    if r.get("certifications", {}).get("count", 0) > 0:
        strengths.append("Professional certifications present.")
    if r.get("projects", {}).get("count", 0) >= 2:
        strengths.append("Multiple projects showcased.")
    if r.get("education", {}).get("highest_degree_level", 0) >= 4:
        strengths.append("Advanced degree (Master's or higher).")
    return strengths or ["Resume submitted successfully."]


def _identify_weaknesses(r: dict) -> list[str]:
    weaknesses = []
    if r.get("skills", {}).get("count", 0) < 5:
        weaknesses.append("Too few skills listed — add more relevant technical skills.")
    if r.get("experience", {}).get("total_years", 0) == 0:
        weaknesses.append("No work experience detected — add internships or freelance work.")
    if r.get("projects", {}).get("count", 0) == 0:
        weaknesses.append("No projects found — add personal or academic projects.")
    if r.get("certifications", {}).get("count", 0) == 0:
        weaknesses.append("No certifications found — consider adding relevant credentials.")
    if not r.get("education", {}).get("entries"):
        weaknesses.append("Education section is missing or unclear.")
    return weaknesses


def _estimate_percentile(score: float) -> int:
    """Rough percentile estimate based on score distribution."""
    if score >= 90: return 95
    if score >= 80: return 80
    if score >= 70: return 65
    if score >= 60: return 50
    if score >= 50: return 35
    return 20


def _next_steps(label: str) -> list[str]:
    steps = {
        "Excellent": [
            "Apply confidently to your target roles.",
            "Prepare for technical interviews.",
            "Optimize your LinkedIn to match your resume.",
        ],
        "Good": [
            "Add 2-3 more quantified achievements.",
            "Include a professional summary section.",
            "Tailor resume keywords for each job application.",
        ],
        "Average": [
            "Expand your skills section with relevant technologies.",
            "Add more detail to project descriptions.",
            "Earn 1-2 industry certifications.",
        ],
        "Poor": [
            "Rebuild resume structure with clear sections.",
            "Take online courses to add in-demand skills.",
            "Start with internships or personal projects.",
        ],
    }
    return steps.get(label, [])
