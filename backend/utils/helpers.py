"""
helpers.py - Reusable utility functions
"""
import os
import re
import uuid
from datetime import datetime


def allowed_file(filename: str) -> bool:
    from utils.constants import ALLOWED_EXTENSIONS
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_unique_filename(original_filename: str) -> str:
    ext = original_filename.rsplit(".", 1)[1].lower()
    return f"{uuid.uuid4().hex}.{ext}"


def clean_text(text: str) -> str:
    """Remove excessive whitespace and non-printable chars."""
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\x20-\x7E\n]", " ", text)
    return text.strip()


def extract_email(text: str) -> str | None:
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    match = re.search(pattern, text)
    return match.group(0) if match else None


def extract_phone(text: str) -> str | None:
    pattern = r"(\+?\d[\d\s\-().]{7,15}\d)"
    match = re.search(pattern, text)
    return match.group(0).strip() if match else None


def extract_linkedin_url(text: str) -> str | None:
    pattern = r"linkedin\.com/in/[\w\-]+"
    match = re.search(pattern, text, re.IGNORECASE)
    return f"https://{match.group(0)}" if match else None


def extract_github_url(text: str) -> str | None:
    pattern = r"github\.com/[\w\-]+"
    match = re.search(pattern, text, re.IGNORECASE)
    return f"https://{match.group(0)}" if match else None


def score_to_label(score: float) -> str:
    from utils.constants import SCORE_LABELS
    for (low, high), label in SCORE_LABELS.items():
        if low <= score <= high:
            return label
    return "Poor"


def normalize_score(value: float, min_val: float = 0, max_val: float = 100) -> float:
    return round(max(min_val, min(max_val, value)), 2)


def timestamp_now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    return round(numerator / denominator, 4) if denominator else default
