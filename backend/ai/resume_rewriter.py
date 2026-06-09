import json
import re
from ai.gemini_client import call_gemini


def rewrite_resume_bullets(bullets: list) -> dict:
    if not bullets:
        return {"error": "No bullets provided"}
    prompt   = _build_rewrite_prompt(bullets)
    response = call_gemini(prompt)
    return _parse_response(response, bullets)


def rewrite_single_bullet(text: str) -> str:
    prompt = f"""You are an expert resume writer. Rewrite this weak resume bullet point into a strong,
impactful one using action verbs, specific technologies, and quantifiable impact.

Weak: "{text}"

Return ONLY the improved bullet point, nothing else. No quotes, no explanation."""
    response = call_gemini(prompt)
    return response.strip() if response else _rule_based_improve(text)


def _build_rewrite_prompt(bullets: list) -> str:
    bullets_str = "\n".join(f"{i+1}. {b}" for i, b in enumerate(bullets))
    return f"""You are an expert resume writer. Rewrite each bullet point to be impactful,
specific, and ATS-optimized. Use strong action verbs and add realistic metrics.

Original bullets:
{bullets_str}

Return ONLY a JSON array of improved bullets in the same order. No markdown, no explanation:
["improved bullet 1", "improved bullet 2", ...]"""


def _parse_response(response: str, originals: list) -> dict:
    if not response:
        return {"original": originals, "improved": [_rule_based_improve(b) for b in originals], "count": len(originals)}
    try:
        clean    = response.strip().strip("```json").strip("```").strip()
        improved = json.loads(clean)
        if isinstance(improved, list):
            return {"original": originals, "improved": improved, "count": len(improved)}
    except Exception:
        pass
    return {"original": originals, "improved": [_rule_based_improve(b) for b in originals], "count": len(originals)}


def _rule_based_improve(text: str) -> str:
    ACTION_VERBS = ["Developed", "Built", "Implemented", "Designed", "Optimized",
                    "Delivered", "Engineered", "Created", "Deployed", "Automated",
                    "Architected", "Streamlined", "Improved", "Established", "Launched"]
    text = text.strip().rstrip(".")
    weak = r"^(worked on|helped with|assisted in|was responsible for|i |did |made |built a|created a)"
    if re.match(weak, text, re.I):
        verb = ACTION_VERBS[hash(text) % len(ACTION_VERBS)]
        text = re.sub(weak, verb + " ", text, flags=re.I)
    text = text[0].upper() + text[1:] if text else text
    return text + ", resulting in measurable performance improvements and enhanced team productivity."
