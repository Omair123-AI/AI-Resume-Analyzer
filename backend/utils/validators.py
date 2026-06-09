"""
validators.py - Request & input validation
"""
from flask import request
from utils.helpers import allowed_file


def validate_resume_upload() -> tuple[bool, str]:
    """Returns (is_valid, error_message)."""
    if "resume" not in request.files:
        return False, "No file part in request. Use key 'resume'."
    file = request.files["resume"]
    if file.filename == "":
        return False, "No file selected."
    if not allowed_file(file.filename):
        return False, "Invalid file type. Only PDF and DOCX are supported."
    return True, ""


def validate_jd_input(data: dict) -> tuple[bool, str]:
    jd = data.get("job_description", "").strip()
    if not jd:
        return False, "Job description is required."
    if len(jd) < 50:
        return False, "Job description is too short (minimum 50 characters)."
    return True, ""


def validate_github_url(url: str) -> tuple[bool, str]:
    import re
    pattern = r"^https?://(www\.)?github\.com/[\w\-]+/?$"
    if not re.match(pattern, url):
        return False, "Invalid GitHub profile URL."
    return True, ""


def validate_linkedin_url(url: str) -> tuple[bool, str]:
    import re
    pattern = r"^https?://(www\.)?linkedin\.com/in/[\w\-]+/?$"
    if not re.match(pattern, url):
        return False, "Invalid LinkedIn profile URL."
    return True, ""
