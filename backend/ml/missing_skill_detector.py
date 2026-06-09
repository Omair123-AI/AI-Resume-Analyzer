"""
missing_skill_detector.py - Identify skill gaps for a target role
"""
from utils.constants import ROLE_SKILL_MAP, HOT_SKILLS, IN_DEMAND_SKILLS


def detect_missing_skills(found_skills: list, target_role: str) -> dict:
    """
    Compare resume skills against the role's required skill set.
    Returns missing, matched, and priority skills.
    """
    role_key = target_role.lower().strip()

    # Find closest role match
    role_data = _find_closest_role(role_key)
    if not role_data:
        return {"error": f"Role '{target_role}' not found in database."}

    required  = set(role_data["skills"])
    found_set = set(s.lower() for s in found_skills)

    matched = sorted(required & found_set)
    missing = sorted(required - found_set)

    # Prioritise: hot-tech or in-demand missing skills first
    priority_missing = [s for s in missing if s in HOT_SKILLS or s in IN_DEMAND_SKILLS]
    other_missing    = [s for s in missing if s not in priority_missing]

    match_pct = round(len(matched) / len(required) * 100, 1) if required else 0

    return {
        "role":             role_data["role"],
        "required_skills":  [s.title() for s in sorted(required)],
        "matched_skills":   [s.title() for s in matched],
        "missing_skills":   [s.title() for s in missing],
        "priority_missing": [s.title() for s in priority_missing],
        "other_missing":    [s.title() for s in other_missing],
        "match_percentage": match_pct,
        "total_required":   len(required),
        "total_matched":    len(matched),
        "total_missing":    len(missing),
    }


def _find_closest_role(role_key: str) -> dict | None:
    if role_key in ROLE_SKILL_MAP:
        return ROLE_SKILL_MAP[role_key]
    # Partial match
    for key, data in ROLE_SKILL_MAP.items():
        if role_key in key or key in role_key:
            return data
    return None


def get_all_roles() -> list[str]:
    return sorted(d["role"] for d in ROLE_SKILL_MAP.values())
