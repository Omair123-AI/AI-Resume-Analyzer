"""
jd_matcher.py - Deep resume vs JD analysis using Sentence Transformers semantic similarity
"""
from ml.job_matcher import match_resume_to_jd


def analyze_resume_vs_jd(resume_text: str, jd_text: str, resume_parsed: dict) -> dict:
    """
    Full resume vs JD analysis combining TF-IDF + semantic + skill overlap.
    """
    base = match_resume_to_jd(resume_text, jd_text)

    # Try sentence-transformer semantic score
    semantic_score = _semantic_similarity(resume_text, jd_text)

    # Blend scores
    if semantic_score > 0:
        final = round(base["match_score"] * 0.5 + semantic_score * 50, 1)
    else:
        final = base["match_score"]

    base["semantic_score"]   = round(semantic_score * 100, 1)
    base["final_match_score"] = final
    base["grade"]             = _grade(final)

    return base


def _semantic_similarity(text1: str, text2: str) -> float:
    try:
        from sentence_transformers import SentenceTransformer, util
        model  = SentenceTransformer("all-MiniLM-L6-v2")
        emb1   = model.encode(text1[:1000], convert_to_tensor=True)
        emb2   = model.encode(text2[:1000], convert_to_tensor=True)
        score  = util.cos_sim(emb1, emb2).item()
        return max(0.0, float(score))
    except Exception:
        return 0.0


def _grade(score: float) -> str:
    if score >= 85: return "Excellent Match"
    if score >= 70: return "Good Match"
    if score >= 50: return "Moderate Match"
    return "Low Match"
