"""
education_extractor.py - Extract education entries from resume text
"""
import re
from utils.constants import EDUCATION_KEYWORDS, DEGREE_LEVELS


def extract_education(text: str) -> dict:
    """
    Returns:
        {
          "entries": [{"degree": str, "institution": str, "year": str}],
          "highest_degree": str,
          "highest_degree_level": int,   # 1-5 scale
        }
    """
    entries   = _parse_education_entries(text)
    highest   = _get_highest_degree(entries)
    level     = _degree_level(highest)

    return {
        "entries":              entries,
        "highest_degree":       highest,
        "highest_degree_level": level,
    }


def _parse_education_entries(text: str) -> list[dict]:
    lines   = text.split("\n")
    entries = []

    for i, line in enumerate(lines):
        line_lower = line.lower()
        if any(kw in line_lower for kw in EDUCATION_KEYWORDS):
            degree      = _extract_degree(line_lower)
            institution = _extract_institution(line, lines, i)
            year        = _extract_year(line)

            if degree or institution:
                entries.append({
                    "degree":      degree or "Not specified",
                    "institution": institution or "Not specified",
                    "year":        year or "",
                })

    return entries


def _extract_degree(line: str) -> str:
    degree_patterns = [
        r"(ph\.?d\.?|doctorate)",
        r"(master[s]? of [a-z ]+|m\.sc\.?|m\.tech\.?|m\.e\.?|mba)",
        r"(bachelor[s]? of [a-z ]+|b\.sc\.?|b\.tech\.?|b\.e\.?)",
        r"(associate[s]? of [a-z ]+|associate degree)",
        r"(diploma in [a-z ]+|diploma)",
    ]
    for pattern in degree_patterns:
        m = re.search(pattern, line, re.I)
        if m:
            return m.group(0).strip().title()
    return ""


def _extract_institution(line: str, lines: list, idx: int) -> str:
    """Look for 'University', 'College', 'Institute' in nearby lines."""
    context = "\n".join(lines[max(0, idx-1): idx+3])
    m = re.search(
        r"([A-Z][a-zA-Z ]+(University|College|Institute|School|Academy)[a-zA-Z ,]*)",
        context
    )
    return m.group(0).strip() if m else ""


def _extract_year(line: str) -> str:
    # Year range like 2018-2022 or single year 2022
    m = re.search(r"(19|20)\d{2}(\s*[-–]\s*(19|20)\d{2}|present)?", line, re.I)
    return m.group(0).strip() if m else ""


def _get_highest_degree(entries: list[dict]) -> str:
    if not entries:
        return "Not specified"
    best = max(entries, key=lambda e: _degree_level(e["degree"]))
    return best["degree"]


def _degree_level(degree_str: str) -> int:
    lower = degree_str.lower()
    for keyword, level in sorted(DEGREE_LEVELS.items(), key=lambda x: -x[1]):
        if keyword in lower:
            return level
    return 1
