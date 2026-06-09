"""
linkedin_analyzer.py - Heuristic LinkedIn profile analyzer
(LinkedIn has no public API; we analyze the URL structure + user-provided data)
"""
import re


def analyze_linkedin(profile_url: str, profile_data: dict = None) -> dict:
    """
    profile_data (optional): dict with keys the user can paste in manually:
      headline, summary, skills, experience_count, recommendations,
      certifications, projects, education
    """
    username = _extract_username(profile_url)
    if not username:
        return {"error": "Invalid LinkedIn URL. Expected: https://linkedin.com/in/username"}

    if not profile_data:
        return _url_only_response(username, profile_url)

    score       = _calculate_score(profile_data)
    suggestions = _generate_suggestions(profile_data)

    return {
        "username":    username,
        "profile_url": profile_url,
        "analysis": {
            "headline":         profile_data.get("headline", ""),
            "summary":          bool(profile_data.get("summary")),
            "skills_count":     len(profile_data.get("skills", [])),
            "experience_count": profile_data.get("experience_count", 0),
            "recommendations":  profile_data.get("recommendations", 0),
            "certifications":   profile_data.get("certifications", 0),
            "projects":         profile_data.get("projects", 0),
            "has_education":    bool(profile_data.get("education")),
        },
        "score":       score["total"],
        "breakdown":   score["breakdown"],
        "label":       score["label"],
        "suggestions": suggestions,
    }


def _extract_username(url: str) -> str | None:
    m = re.search(r"linkedin\.com/in/([a-zA-Z0-9\-]+)/?", url)
    return m.group(1) if m else None


def _calculate_score(data: dict) -> dict:
    breakdown = {}

    # Headline (15pts)
    headline = data.get("headline", "")
    breakdown["headline"] = 15 if len(headline) > 20 else (8 if headline else 0)

    # Summary (20pts)
    summary = data.get("summary", "")
    breakdown["summary"] = 20 if len(summary) > 100 else (10 if summary else 0)

    # Skills (20pts)
    skills = data.get("skills", [])
    breakdown["skills"] = min(len(skills) / 10 * 20, 20)

    # Experience (20pts)
    exp = data.get("experience_count", 0)
    breakdown["experience"] = min(exp / 3 * 20, 20)

    # Recommendations (10pts)
    rec = data.get("recommendations", 0)
    breakdown["recommendations"] = min(rec / 3 * 10, 10)

    # Certifications (10pts)
    certs = data.get("certifications", 0)
    breakdown["certifications"] = min(certs / 2 * 10, 10)

    # Projects (5pts)
    projs = data.get("projects", 0)
    breakdown["projects"] = min(projs / 2 * 5, 5)

    total = min(sum(breakdown.values()), 100)
    label = ("Excellent" if total >= 80 else
             "Good"      if total >= 60 else
             "Average"   if total >= 40 else "Needs Work")

    return {
        "total":     round(total, 1),
        "breakdown": {k: round(v, 1) for k, v in breakdown.items()},
        "label":     label,
    }


def _generate_suggestions(data: dict) -> list[str]:
    suggestions = []
    if len(data.get("headline", "")) < 20:
        suggestions.append("Write a compelling headline with your title and value proposition.")
    if len(data.get("summary", "")) < 100:
        suggestions.append("Add a detailed summary (200+ words) showcasing your career story.")
    if len(data.get("skills", [])) < 10:
        suggestions.append("Add at least 10 relevant skills to improve search visibility.")
    if data.get("recommendations", 0) < 2:
        suggestions.append("Request 2-3 recommendations from managers or colleagues.")
    if data.get("certifications", 0) == 0:
        suggestions.append("Add your certifications to boost profile credibility.")
    if data.get("projects", 0) == 0:
        suggestions.append("Showcase projects in the Featured or Projects section.")
    return suggestions or ["Your LinkedIn profile looks strong! Keep it updated."]


def _url_only_response(username: str, profile_url: str) -> dict:
    return {
        "username":    username,
        "profile_url": profile_url,
        "message":     "Provide profile_data for detailed analysis. LinkedIn has no public API.",
        "manual_checklist": [
            "Headline: Does it include your role and value proposition?",
            "Summary: Is it 200+ words and compelling?",
            "Skills: Do you have 10+ relevant skills listed?",
            "Experience: Are all entries detailed with achievements?",
            "Recommendations: Do you have 3+ recommendations?",
            "Certifications: Are all certifications listed?",
            "Projects: Are key projects in the Featured section?",
        ],
    }
