"""
text_cleaner.py - Normalize raw resume text before NLP processing
"""
import re


def clean_resume_text(text: str) -> str:
    """Full cleaning pipeline for raw resume text."""
    text = _remove_urls(text)
    text = _normalize_whitespace(text)
    text = _fix_encoding_artifacts(text)
    text = _remove_page_numbers(text)
    return text.strip()


def _remove_urls(text: str) -> str:
    # Keep domain references (github.com/user) but remove full http links
    text = re.sub(r"https?://[^\s]+", "", text)
    return text


def _normalize_whitespace(text: str) -> str:
    # Collapse multiple spaces / tabs
    text = re.sub(r"[ \t]+", " ", text)
    # Collapse 3+ newlines into 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def _fix_encoding_artifacts(text: str) -> str:
    replacements = {
        "\u2022": "-",  # bullet
        "\u2019": "'",  # right single quote
        "\u2018": "'",  # left single quote
        "\u201c": '"',  # left double quote
        "\u201d": '"',  # right double quote
        "\u2013": "-",  # en dash
        "\u2014": "-",  # em dash
        "\ufb01": "fi",
        "\ufb02": "fl",
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    return text


def _remove_page_numbers(text: str) -> str:
    # Remove standalone numbers that look like page numbers
    text = re.sub(r"(?m)^\s*\d{1,3}\s*$", "", text)
    return text
