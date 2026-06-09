"""
resume_parser.py - Master parser: dispatches to PDF/DOCX, cleans text,
                   then runs all NLP extractors to build a structured resume dict.
"""
import os
from parsers.pdf_parser import extract_text_from_pdf
from parsers.docx_parser import extract_text_from_docx
from parsers.text_cleaner import clean_resume_text
from utils.helpers import (
    extract_email, extract_phone, extract_linkedin_url, extract_github_url
)
from nlp.skill_extractor import extract_skills
from nlp.keyword_extractor import extract_keywords
from nlp.education_extractor import extract_education
from nlp.experience_extractor import extract_experience
from nlp.project_extractor import extract_projects
from nlp.certification_extractor import extract_certifications


def parse_resume(filepath: str) -> dict:
    """
    Main entry point.
    Returns a fully structured resume dictionary.
    """
    ext = filepath.rsplit(".", 1)[-1].lower()

    # 1. Raw text extraction
    if ext == "pdf":
        raw_text = extract_text_from_pdf(filepath)
    elif ext == "docx":
        raw_text = extract_text_from_docx(filepath)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    # 2. Clean
    clean_text = clean_resume_text(raw_text)

    # 3. Extract structured info
    name     = _extract_name(clean_text)
    email    = extract_email(clean_text)
    phone    = extract_phone(clean_text)
    linkedin = extract_linkedin_url(clean_text)
    github   = extract_github_url(clean_text)

    skills           = extract_skills(clean_text)
    keywords         = extract_keywords(clean_text)
    education        = extract_education(clean_text)
    experience       = extract_experience(clean_text)
    projects         = extract_projects(clean_text)
    certifications   = extract_certifications(clean_text)

    return {
        "raw_text":       clean_text,
        "name":           name,
        "email":          email,
        "phone":          phone,
        "linkedin":       linkedin,
        "github":         github,
        "skills":         skills,
        "keywords":       keywords,
        "education":      education,
        "experience":     experience,
        "projects":       projects,
        "certifications": certifications,
    }


def _extract_name(text: str) -> str:
    """
    Heuristic: the name is typically the first non-empty line of the resume,
    before any contact info appears.  We skip lines that look like headers,
    URLs, or email addresses.
    """
    import re
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    skip_patterns = [
        r"@", r"http", r"\d{3,}", r"resume", r"curriculum",
        r"cv\b", r"linkedin", r"github",
    ]
    for line in lines[:8]:
        if any(re.search(p, line, re.I) for p in skip_patterns):
            continue
        # Looks like a name: 2-4 words, mostly alphabetic
        words = line.split()
        if 1 < len(words) <= 5 and all(re.match(r"[A-Za-z\-'.]+$", w) for w in words):
            return line
    return lines[0] if lines else "Unknown"
