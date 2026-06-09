"""
job_matcher.py - Match resume against job description using TF-IDF + Cosine Similarity
"""
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.constants import ALL_SKILLS

STOP_WORDS = {
    "a","an","the","and","or","but","in","on","at","to","for","of","with",
    "by","from","up","about","into","through","during","before","after",
    "above","below","between","out","off","over","under","again","further",
    "then","once","here","there","when","where","why","how","all","both",
    "each","few","more","most","other","some","such","no","nor","not",
    "only","own","same","so","than","too","very","can","will","just",
    "should","now","also","well","even","still","back","any","going",
    "get","make","like","time","year","years","work","using","use","used",
    "etc","via","per","new","good","great","strong","high","large","small",
    "best","real","full","key","able","need","help","build","builds","built",
    "design","designs","bridge","bridges","gap","scalable","production",
    "ready","theoretical","prototypes","intelligent","pipelines","pipeline",
    "applications","application","systems","system","software","between",
    "deploys","deploy","recommendation","recommendations","automated",
    "transforms","transform","engineering","science","models","model",
    "neural","network","between","into","like","they","role","team",
    "experience","years","knowledge","understanding","ability","skills",
}

# Skills that need whole-word boundary matching (short ones get falsely matched)
SHORT_SKILLS = {"r", "go", "c", "c#", "c++", "ml", "ai", "dl", "sql", "js"}


def match_resume_to_jd(resume_text: str, jd_text: str) -> dict:
    tfidf_score      = _tfidf_similarity(resume_text, jd_text)
    skill_analysis   = _skill_overlap(resume_text, jd_text)
    keyword_analysis = _keyword_overlap(resume_text, jd_text)

    final_score = round(
        tfidf_score * 0.40 +
        skill_analysis["overlap_pct"] / 100 * 0.40 +
        keyword_analysis["overlap_pct"] / 100 * 0.20,
        4
    ) * 100

    return {
        "match_score":      round(final_score, 1),
        "tfidf_score":      round(tfidf_score * 100, 1),
        "skill_overlap":    skill_analysis,
        "keyword_overlap":  keyword_analysis,
        "missing_keywords": skill_analysis["missing"][:15],
        "matched_keywords": skill_analysis["matched"][:15],
        "suggestions":      _generate_suggestions(skill_analysis, keyword_analysis, final_score),
    }


def _tfidf_similarity(text1: str, text2: str) -> float:
    try:
        vec   = TfidfVectorizer(stop_words="english", max_features=500)
        tfidf = vec.fit_transform([text1, text2])
        return float(cosine_similarity(tfidf[0], tfidf[1])[0][0])
    except Exception:
        return 0.0


def _skill_match(skill: str, text_lower: str) -> bool:
    """
    Smart skill matching:
    - Short/ambiguous skills (Go, R, C#) require strict word boundaries
    - Long skills use case-insensitive substring match
    """
    skill_lower = skill.lower()

    if skill_lower in SHORT_SKILLS or len(skill_lower) <= 2:
        # Strict: must be surrounded by non-alphanumeric characters
        pattern = r"(?:^|[\s,.()\[\]/+\-])" + re.escape(skill_lower) + r"(?:$|[\s,.()\[\]/+\-])"
        return bool(re.search(pattern, text_lower))
    else:
        # Normal case-insensitive match with word boundary
        pattern = r"(?<![a-z0-9])" + re.escape(skill_lower) + r"(?![a-z0-9])"
        return bool(re.search(pattern, text_lower))


def _skill_overlap(resume_text: str, jd_text: str) -> dict:
    resume_lower = resume_text.lower()
    jd_lower     = jd_text.lower()

    jd_skills     = {s for s in ALL_SKILLS if _skill_match(s, jd_lower)}
    resume_skills = {s for s in ALL_SKILLS if _skill_match(s, resume_lower)}

    matched = jd_skills & resume_skills
    missing = jd_skills - resume_skills
    overlap = round(len(matched) / len(jd_skills) * 100, 1) if jd_skills else 0

    return {
        "jd_skills":   sorted(s.title() for s in jd_skills),
        "matched":     sorted(s.title() for s in matched),
        "missing":     sorted(s.title() for s in missing),
        "overlap_pct": overlap,
    }


def _keyword_overlap(resume_text: str, jd_text: str) -> dict:
    def get_tech_keywords(text: str) -> set:
        tokens = re.findall(r"\b[a-zA-Z][a-zA-Z0-9+#.\-]{3,}\b", text.lower())
        return {t for t in tokens if t not in STOP_WORDS and len(t) >= 4}

    jd_kw     = get_tech_keywords(jd_text)
    resume_kw = get_tech_keywords(resume_text)
    matched   = jd_kw & resume_kw
    missing   = jd_kw - resume_kw
    overlap   = round(len(matched) / len(jd_kw) * 100, 1) if jd_kw else 0

    return {
        "matched":     sorted(matched)[:15],
        "missing":     sorted(missing)[:15],
        "overlap_pct": overlap,
    }


def _generate_suggestions(skill_analysis: dict, kw_analysis: dict, score: float) -> list:
    suggestions = []
    if score < 50:
        suggestions.append("Low alignment with this job. Tailor your resume specifically for this role.")
    if skill_analysis["missing"]:
        top = skill_analysis["missing"][:5]
        suggestions.append(f"Add these missing skills if you have them: {', '.join(top)}.")
    if score >= 80:
        suggestions.append("Strong match! Ensure your resume format is clean and ATS-friendly.")
    if not skill_analysis["jd_skills"]:
        suggestions.append("No specific tech skills detected in JD. Focus on matching job title and responsibilities.")
    return suggestions