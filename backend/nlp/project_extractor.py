"""
project_extractor.py - Extract project entries from resume text
"""
import re


def extract_projects(text: str) -> dict:
    entries = _parse_project_entries(text)
    return {
        "entries": entries,
        "count":   len(entries),
        "quality_scores": [_score_project(p) for p in entries],
    }


def _parse_project_entries(text: str) -> list[dict]:
    lines   = text.split("\n")
    entries = []
    in_proj = False
    current = None

    project_headers = ["projects", "personal projects", "academic projects",
                       "portfolio", "side projects", "key projects"]
    stop_headers    = ["experience", "education", "skills", "certifications",
                       "work history", "employment", "summary", "objective"]

    for line in lines:
        ll = line.lower().strip()

        if any(ll.startswith(h) for h in project_headers) and len(ll) < 30:
            in_proj = True
            continue

        if in_proj and any(ll.startswith(h) for h in stop_headers) and len(ll) < 30:
            if current:
                entries.append(current)
                current = None
            in_proj = False
            continue

        if not in_proj:
            continue

        # New project: line that starts with a title-cased short phrase
        if line.strip() and len(line.strip()) < 80 and _looks_like_title(line.strip()):
            if current:
                entries.append(current)
            current = {"title": line.strip(), "description": "", "technologies": [], "links": []}
        elif current and line.strip():
            current["description"] += " " + line.strip()
            current["technologies"] += _extract_tech(line)
            current["links"]       += _extract_links(line)

    if current:
        entries.append(current)

    # Deduplicate technologies per project
    for e in entries:
        e["technologies"] = sorted(set(e["technologies"]))

    return entries


def _looks_like_title(line: str) -> bool:
    words = line.split()
    return (1 < len(words) <= 8 and
            words[0][0].isupper() and
            not line.strip().endswith(('.', ',', ';')))


def _extract_tech(line: str) -> list[str]:
    from utils.constants import ALL_SKILLS
    found = []
    ll = line.lower()
    for skill in ALL_SKILLS:
        if re.search(r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])", ll):
            found.append(skill.title())
    return found


def _extract_links(line: str) -> list[str]:
    return re.findall(r"https?://[^\s]+", line)


def _score_project(project: dict) -> dict:
    """Return a quality breakdown for one project (0-100)."""
    score = 0
    feedback = []

    desc_len = len(project.get("description", "").split())
    if desc_len >= 30:
        score += 25
    elif desc_len >= 15:
        score += 15
        feedback.append("Add more detail to the description")
    else:
        score += 5
        feedback.append("Description is too short")

    tech = project.get("technologies", [])
    if len(tech) >= 3:
        score += 25
    elif len(tech) >= 1:
        score += 15
        feedback.append("Mention more technologies used")
    else:
        score += 0
        feedback.append("No technologies mentioned")

    desc_lower = project.get("description", "").lower()
    impact_words = ["improved", "reduced", "increased", "achieved", "built",
                    "deployed", "automated", "optimized", "saved", "grew",
                    "%", "users", "performance"]
    if any(w in desc_lower for w in impact_words):
        score += 25
    else:
        feedback.append("Add metrics / impact statements")

    metric_patterns = [r"\d+%", r"\d+ users", r"\d+x", r"\$\d+"]
    if any(re.search(p, desc_lower) for p in metric_patterns):
        score += 25
    else:
        feedback.append("Add quantifiable achievements")

    return {
        "title":    project.get("title", ""),
        "score":    score,
        "feedback": feedback,
    }
