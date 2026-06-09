from ai.gemini_client import call_gemini
from nlp.project_extractor import _score_project


def analyze_projects(projects: dict) -> dict:
    entries = projects.get("entries", [])
    if not entries:
        return {"message": "No projects found in resume.", "entries": [], "overall_score": 0}

    scored = []
    for proj in entries:
        rule_score  = _score_project(proj)
        ai_feedback = _get_ai_feedback(proj)
        scored.append({**rule_score, "technologies": proj.get("technologies", []), "ai_feedback": ai_feedback})

    overall = round(sum(s["score"] for s in scored) / len(scored), 1)
    return {"entries": scored, "overall_score": overall, "count": len(scored), "summary": _summarize(overall)}


def _get_ai_feedback(project: dict) -> str:
    prompt = f"""Evaluate this resume project and give ONE concise improvement suggestion (max 30 words):
Title: {project.get('title', '')}
Description: {project.get('description', '')[:300]}
Technologies: {', '.join(project.get('technologies', []))}"""

    response = call_gemini(prompt)
    return response.strip() if response else _rule_feedback(project)


def _rule_feedback(project: dict) -> str:
    desc_len = len(project.get("description", "").split())
    if desc_len < 15:
        return "Expand description with technologies used, your role, and the outcome."
    if not project.get("technologies"):
        return "Mention the specific tools and technologies used in this project."
    return "Add quantifiable results (e.g., reduced load time by 40%, served 500+ users)."


def _summarize(score: float) -> str:
    if score >= 75: return "Strong project portfolio with good detail and impact."
    if score >= 50: return "Decent projects. Add metrics and technologies for better impact."
    return "Projects need improvement. Add descriptions, technologies, and outcomes."
