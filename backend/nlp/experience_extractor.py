"""
experience_extractor.py - Extract work experience from resume text
Improved to detect more resume formats and Pakistani/student resume styles
"""
import re
import datetime
from utils.constants import EXPERIENCE_KEYWORDS, LEADERSHIP_KEYWORDS, SECTION_HEADERS


def extract_experience(text: str) -> dict:
    entries       = _parse_experience_entries(text)
    total_years   = _estimate_total_years(entries)
    has_intern    = any("intern" in e["title"].lower() for e in entries)
    has_leadership = _check_leadership(text)
    industries    = _infer_industries(entries)

    return {
        "entries":        entries,
        "total_years":    total_years,
        "has_internship": has_intern,
        "has_leadership": has_leadership,
        "industries":     industries,
    }


def _parse_experience_entries(text: str) -> list:
    entries   = []
    lines     = text.split("\n")
    in_exp    = False

    exp_headers = [
        "experience", "work experience", "work history", "employment",
        "professional experience", "internship", "internships",
        "career history", "job history", "positions held",
    ]
    stop_headers = [
        "education", "skills", "certifications", "projects",
        "courses", "publications", "awards", "references",
        "languages", "interests", "hobbies", "volunteer",
    ]

    for i, line in enumerate(lines):
        ll = line.lower().strip()

        # Detect experience section
        if any(ll == h or ll.startswith(h + ":") or ll.startswith(h + " ") for h in exp_headers):
            if len(ll) < 35:
                in_exp = True
                continue

        # Stop at next section
        if in_exp and any(ll == h or ll.startswith(h + ":") for h in stop_headers) and len(ll) < 35:
            in_exp = False

        if not in_exp:
            continue

        title, company, duration = _parse_job_line(line.strip(), lines, i)
        if title:
            entries.append({
                "title":       title,
                "company":     company,
                "duration":    duration,
                "description": _collect_description(lines, i + 1),
            })

    # Fallback: scan whole text for job patterns if nothing found in section
    if not entries:
        entries = _fallback_scan(text)

    return entries


def _parse_job_line(line: str, lines: list, idx: int) -> tuple:
    if not line or len(line) > 100:
        return "", "", ""

    # Pattern 1: "Software Engineer | Google | 2021 - 2023"
    m = re.match(
        r"^([A-Za-z &/,.\-]{5,50})\s*[|@•·]\s*([A-Za-z &,.]+)\s*[|•·]\s*(.+)$",
        line
    )
    if m:
        return m.group(1).strip(), m.group(2).strip(), m.group(3).strip()

    # Pattern 2: "Google – Software Engineer (2021-2023)"
    m = re.match(
        r"^([A-Z][a-zA-Z &,.]+)\s*[-–—]\s*([A-Za-z &/]+)\s*[\(]?((19|20)\d{2}.{0,20})[\)]?$",
        line
    )
    if m:
        return m.group(2).strip(), m.group(1).strip(), m.group(3).strip()

    # Pattern 3: "Software Engineer at Google" with year on next line
    m = re.match(r"^([A-Za-z &/]+)\s+(?:at|@)\s+([A-Za-z &,.]+)$", line, re.I)
    if m:
        year = _find_nearby_year(lines, idx)
        return m.group(1).strip(), m.group(2).strip(), year

    # Pattern 4: Line with job title keywords + a year somewhere nearby
    job_title_words = [
        "engineer", "developer", "intern", "analyst", "designer",
        "manager", "lead", "architect", "consultant", "specialist",
        "coordinator", "assistant", "officer", "researcher", "scientist",
    ]
    ll = line.lower()
    if any(w in ll for w in job_title_words) and len(line) < 80:
        year = _find_nearby_year(lines, idx)
        if year:
            return line.strip(), "", year

    return "", "", ""


def _find_nearby_year(lines: list, idx: int) -> str:
    context = " ".join(lines[max(0, idx-1): idx+3])
    m = re.search(r"(19|20)\d{2}(\s*[-–]\s*((19|20)\d{2}|present|current))?", context, re.I)
    return m.group(0).strip() if m else ""


def _collect_description(lines: list, start: int, max_lines: int = 6) -> str:
    desc = []
    for line in lines[start: start + max_lines]:
        stripped = line.strip()
        if not stripped:
            continue
        ll = stripped.lower()
        # Stop at next section header
        if any(ll.startswith(h) for h in ["education", "skills", "project", "certif"]):
            break
        desc.append(stripped)
    return " ".join(desc)


def _fallback_scan(text: str) -> list:
    """Scan entire text for job-like patterns when no section header found."""
    entries = []
    lines   = text.split("\n")
    job_kws = ["engineer", "developer", "intern", "analyst", "designer",
                "manager", "researcher", "consultant", "officer"]

    for i, line in enumerate(lines):
        ll = line.lower().strip()
        if any(kw in ll for kw in job_kws) and len(line.strip()) < 80:
            year = _find_nearby_year(lines, i)
            if year:
                entries.append({
                    "title":       line.strip(),
                    "company":     "",
                    "duration":    year,
                    "description": _collect_description(lines, i + 1),
                })
    return entries


def _estimate_total_years(entries: list) -> float:
    total = 0.0
    current_year = datetime.datetime.now().year

    for e in entries:
        dur   = e.get("duration", "")
        years = re.findall(r"(19|20)\d{2}", dur)

        if len(years) >= 2:
            try:
                total += int(years[-1]) - int(years[0])
            except ValueError:
                pass
        elif len(years) == 1 and re.search(r"present|current|now", dur, re.I):
            try:
                total += current_year - int(years[0])
            except ValueError:
                pass
        elif len(years) == 1:
            # Single year — assume 1 year duration
            total += 1.0

    return round(total, 1)


def _check_leadership(text: str) -> bool:
    lower = text.lower()
    return any(kw in lower for kw in LEADERSHIP_KEYWORDS)


def _infer_industries(entries: list) -> list:
    industry_keywords = {
        "Technology":   ["software", "engineer", "developer", "tech", "it"],
        "Finance":      ["bank", "finance", "fintech", "investment", "accounting"],
        "Healthcare":   ["health", "medical", "hospital", "clinical", "pharma"],
        "Education":    ["teacher", "professor", "lecturer", "tutor", "education"],
        "Marketing":    ["marketing", "seo", "content", "brand", "digital"],
        "Data/AI":      ["data", "analyst", "machine learning", "ai", "ml"],
    }
    found    = set()
    combined = " ".join(e["title"] + " " + e["company"] for e in entries).lower()
    for industry, keywords in industry_keywords.items():
        if any(kw in combined for kw in keywords):
            found.add(industry)
    return list(found)
