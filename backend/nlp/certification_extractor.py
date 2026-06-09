"""
certification_extractor.py - Detect certifications using dataset + heuristics
"""
import re
from utils.constants import CERTIFICATIONS, ALL_CERT_NAMES


def extract_certifications(text: str) -> dict:
    found_known   = _match_known_certs(text)
    found_generic = _match_generic_certs(text)

    # Merge, prefer known
    all_certs = {c["name"]: c for c in found_known}
    for c in found_generic:
        if c["name"] not in all_certs:
            all_certs[c["name"]] = c

    entries = list(all_certs.values())
    providers = list({c["provider"] for c in entries if c["provider"] != "Other"})

    return {
        "entries":   entries,
        "count":     len(entries),
        "providers": providers,
    }


def _match_known_certs(text: str) -> list[dict]:
    found = []
    text_lower = text.lower()
    for provider, certs in CERTIFICATIONS.items():
        for cert in certs:
            if cert.lower() in text_lower:
                found.append({"name": cert, "provider": provider, "verified": True})
    return found


def _match_generic_certs(text: str) -> list[dict]:
    """Catch cert-like phrases not in dataset."""
    found = []
    pattern = re.compile(
        r"(certified\s[\w\s]{3,40}|[\w\s]{2,30}certification|[\w\s]{2,20}certificate)",
        re.IGNORECASE
    )
    for m in pattern.finditer(text):
        name = m.group(0).strip()
        if 5 < len(name) < 80:
            found.append({"name": name, "provider": "Other", "verified": False})
    return found
