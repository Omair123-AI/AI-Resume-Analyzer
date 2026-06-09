"""
constants.py - Project-wide constants loaded from dataset files
"""
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")

# ── Allowed upload file types ──────────────────────────────────────────────────
ALLOWED_EXTENSIONS = {"pdf", "docx"}

# ── ATS scoring weights ────────────────────────────────────────────────────────
ATS_WEIGHTS = {
    "skills":        0.30,
    "keywords":      0.20,
    "experience":    0.20,
    "education":     0.15,
    "projects":      0.10,
    "formatting":    0.05,
}

# ── Scoring thresholds ─────────────────────────────────────────────────────────
SCORE_LABELS = {
    (85, 100): "Excellent",
    (70,  84): "Good",
    (50,  69): "Average",
    (0,   49): "Poor",
}

# ── Education keywords ─────────────────────────────────────────────────────────
EDUCATION_KEYWORDS = [
    "bachelor", "master", "phd", "doctorate", "b.sc", "m.sc", "b.e", "m.e",
    "b.tech", "m.tech", "mba", "associate", "diploma", "degree", "university",
    "college", "institute", "school", "graduate", "undergraduate",
]

DEGREE_LEVELS = {
    "phd": 5, "doctorate": 5,
    "master": 4, "mba": 4, "m.sc": 4, "m.tech": 4, "m.e": 4,
    "bachelor": 3, "b.sc": 3, "b.tech": 3, "b.e": 3,
    "associate": 2, "diploma": 2,
}

# ── Experience keywords ────────────────────────────────────────────────────────
EXPERIENCE_KEYWORDS = [
    "experience", "work history", "employment", "internship", "job",
    "position", "role", "career", "professional experience",
]

LEADERSHIP_KEYWORDS = [
    "led", "managed", "supervised", "directed", "coordinated", "mentored",
    "oversaw", "headed", "spearheaded", "organized", "guided",
]

# ── Section headers ────────────────────────────────────────────────────────────
SECTION_HEADERS = {
    "education":      ["education", "academic", "qualification", "degree"],
    "experience":     ["experience", "work history", "employment", "career"],
    "skills":         ["skills", "technical skills", "core competencies", "expertise"],
    "projects":       ["projects", "personal projects", "academic projects", "portfolio"],
    "certifications": ["certifications", "certificates", "credentials", "licenses"],
    "summary":        ["summary", "objective", "profile", "about me", "overview"],
    "contact":        ["contact", "personal info", "details"],
}

# ── Dataset loaders (loaded once at startup) ───────────────────────────────────
def _load_skills_set() -> set:
    path = os.path.join(DATASET_DIR, "skills.csv")
    df = pd.read_csv(path)
    return set(df["skill"].str.lower().str.strip())

def _load_hot_skills() -> set:
    path = os.path.join(DATASET_DIR, "skills.csv")
    df = pd.read_csv(path)
    return set(df[df["hot_technology"] == "Y"]["skill"].str.lower().str.strip())

def _load_indemand_skills() -> set:
    path = os.path.join(DATASET_DIR, "skills.csv")
    df = pd.read_csv(path)
    return set(df[df["in_demand"] == "Y"]["skill"].str.lower().str.strip())

def _load_role_skill_map() -> dict:
    path = os.path.join(DATASET_DIR, "role_skill_mapping.csv")
    df = pd.read_csv(path)
    mapping = {}
    for _, row in df.iterrows():
        role = row["role"].strip()
        skills = [s.strip().lower() for s in str(row["skills"]).split(",")]
        mapping[role.lower()] = {"role": role, "skills": skills}
    return mapping

def _load_occupations() -> dict:
    path = os.path.join(DATASET_DIR, "occupations.csv")
    df = pd.read_csv(path)
    return {
        row["soc_code"]: {"role": row["role"], "description": row["description"]}
        for _, row in df.iterrows()
    }

def _load_certifications() -> dict:
    path = os.path.join(DATASET_DIR, "certifications.xlsx")
    df = pd.read_excel(path)
    provider_map = {}
    for _, row in df.iterrows():
        provider = row["Provider"].strip()
        cert = row["Certification"].strip()
        provider_map.setdefault(provider, []).append(cert)
    return provider_map

# ── Module-level globals (loaded once) ────────────────────────────────────────
ALL_SKILLS:       set  = _load_skills_set()
HOT_SKILLS:       set  = _load_hot_skills()
IN_DEMAND_SKILLS: set  = _load_indemand_skills()
ROLE_SKILL_MAP:   dict = _load_role_skill_map()
OCCUPATIONS:      dict = _load_occupations()
CERTIFICATIONS:   dict = _load_certifications()
ALL_ROLES:        list = sorted(ROLE_SKILL_MAP.keys())
ALL_CERT_NAMES:   set  = {
    c.lower()
    for certs in CERTIFICATIONS.values()
    for c in certs
}
