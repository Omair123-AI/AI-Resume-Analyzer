"""
suggestion_engine.py - Robust AI-powered resume suggestions via Gemini.
Features deep cleaning, error logging, and resilient JSON extraction.
"""
import json
import re
import time
import sys
from ai.gemini_client import call_gemini


def generate_suggestions(parsed_resume: dict, ats_result: dict) -> dict:
    """
    Orchestrates prompt generation, makes the API call to Gemini,
    attempts parsing, and returns fallback suggestions if anything fails.
    """
    # Small delay to prevent hitting API rate limits
    time.sleep(1.5)

    prompt = _build_prompt(parsed_resume, ats_result)

    print("[AI Suggestion Engine] Requesting feedback from Gemini API...", file=sys.stderr)
    try:
        response = call_gemini(prompt)
    except Exception as api_err:
        print(
            f"[AI Suggestion Engine] API Call Exception: {api_err}", file=sys.stderr)
        return _fallback_suggestions()

    if response:
        result = _parse_response(response)
        if "error" not in result:
            print(
                "[AI Suggestion Engine] Successfully generated and parsed AI recommendations!", file=sys.stderr)
            return result
        else:
            print(
                f"[AI Suggestion Engine] Failed to parse response. Error type: {result.get('error')}", file=sys.stderr)

    print("[AI Suggestion Engine] Triggering fallback local suggestions.", file=sys.stderr)
    return _fallback_suggestions()


def _build_prompt(r: dict, ats: dict) -> str:
    """
    Assembles structural parameters of the resume into a highly contextual system prompt.
    Includes strict token-saving guidelines to prevent API truncation.
    """
    skills_found = r.get("skills", {}).get("found", [])[:15]
    hot_skills = r.get("skills", {}).get("hot_technology", [])[:5]
    missing_secs = [k for k, v in ats.get("breakdown", {}).items() if v < 60]
    exp_years = r.get("experience", {}).get("total_years", 0)
    proj_count = r.get("projects", {}).get("count", 0)
    certs = r.get("certifications", {}).get("count", 0)
    ats_score = ats.get("total", 0)
    name = r.get("name", "the candidate")

    return f"""You are a professional resume coach. Analyze this resume and provide specific, actionable feedback.

Candidate: {name}
ATS Score: {ats_score}/100
Skills ({len(skills_found)} found): {', '.join(skills_found) if skills_found else 'None detected'}
Hot Technologies: {', '.join(hot_skills) if hot_skills else 'None'}
Experience: {exp_years} years
Projects: {proj_count}
Certifications: {certs}
Weak sections (below 60%): {', '.join(missing_secs) if missing_secs else 'All sections are strong'}

IMPORTANT: Keep all feedback sentences short, direct, and under 15-20 words max. Short responses prevent response truncation.

Return ONLY valid JSON (no markdown block, no conversational text prefix/suffix):
{{
  "overall_feedback": "Short 1-2 sentence assessment of their profile",
  "quick_wins": ["action 1 (max 15 words)", "action 2 (max 15 words)", "action 3 (max 15 words)"],
  "section_tips": {{
    "skills": "Specific skill tip under 15 words",
    "experience": "Specific experience tip under 15 words",
    "projects": "Specific projects tip under 15 words",
    "education": "Specific education tip under 15 words",
    "certifications": "Specific cert recommendation under 15 words"
  }},
  "priority_actions": ["top action (max 15 words)", "second action (max 15 words)", "third action (max 15 words)"]
}}"""


def _parse_response(response: str) -> dict:
    """
    Resilient extraction of JSON from Gemini's response.
    If strict JSON parsing fails due to truncation, shifts automatically to a regex-based recovery parser.
    """
    clean = response.strip()
    print("--- RAW GEMINI RESPONSE ---", file=sys.stderr)
    print(clean, file=sys.stderr)
    print("----------------------------", file=sys.stderr)

    try:
        # Extract everything from the first curly brace '{' to the last curly brace '}'
        start_idx = clean.find('{')
        end_idx = clean.rfind('}')

        if start_idx != -1 and end_idx != -1:
            json_candidate = clean[start_idx:end_idx+1]
        else:
            json_candidate = clean

        # Remove common markdown artifact blocks if they somehow survived boundary extraction
        if "```" in json_candidate:
            json_candidate = re.sub(
                r"^```(?:json)?\s*|\s*```$", "", json_candidate, flags=re.MULTILINE).strip()

        # Parse clean JSON
        return json.loads(json_candidate)
    except Exception as e:
        print(
            f"[AI Suggestion Engine] Standard JSON parsing failed: {e}. Initiating partial recovery...", file=sys.stderr)
        return _regex_parse_truncated(clean)


def _regex_parse_truncated(raw_text: str) -> dict:
    """
    Scans truncated/cut-off responses using regular expressions to recover any successfully 
    written JSON fragments, falling back only for fields that were completely lost.
    """
    # Base our results on standard fallbacks so keys are never missing
    data = _fallback_suggestions()
    recovered_keys = []

    # 1. Recover overall feedback
    of_match = re.search(r'"overall_feedback"\s*:\s*"([^"]+)"', raw_text)
    if of_match:
        data["overall_feedback"] = of_match.group(1)
        recovered_keys.append("overall_feedback")

    # 2. Recover quick wins
    qw_match = re.search(r'"quick_wins"\s*:\s*\[(.*?)\]', raw_text, re.DOTALL)
    if qw_match:
        wins = re.findall(r'"([^"]+)"', qw_match.group(1))
        if wins:
            data["quick_wins"] = wins
            recovered_keys.append("quick_wins")

    # 3. Recover section tips individually (very robust against sectional dropouts)
    for key in ["skills", "experience", "projects", "education", "certifications"]:
        tip_match = re.search(rf'"{key}"\s*:\s*"([^"]+)"', raw_text)
        if tip_match:
            data["section_tips"][key] = tip_match.group(1)
            recovered_keys.append(f"section_tips.{key}")

    # 4. Recover priority actions (even if truncated mid-bracket)
    pa_match = re.search(
        r'"priority_actions"\s*:\s*\[(.*?)\]', raw_text, re.DOTALL)
    if pa_match:
        actions = re.findall(r'"([^"]+)"', pa_match.group(1))
        if actions:
            data["priority_actions"] = actions
            recovered_keys.append("priority_actions")
    else:
        # If it was truncated inside priority_actions, extract whatever complete strings we can find before EOF
        truncated_pa = re.search(
            r'"priority_actions"\s*:\s*\[(.*)$', raw_text, re.DOTALL)
        if truncated_pa:
            items = re.findall(r'"([^"]+)"', truncated_pa.group(1))
            # If the last item does not end with a double quote, it was cut off mid-sentence; discard only that one.
            if items and not truncated_pa.group(1).strip().endswith('"'):
                items = items[:-1]
            if items:
                data["priority_actions"] = items
                recovered_keys.append("priority_actions (partial)")

    if recovered_keys:
        print(
            f"[AI Suggestion Engine] Successfully recovered fields: {', '.join(recovered_keys)}", file=sys.stderr)
        # Return recovered data (without standard "error" flag)
        return data

    return {"error": "recovery_failed"}


def _fallback_suggestions() -> dict:
    """
    Returns generic fallback tips in case both standard parsing and regex recovery fail.
    """
    return {
        "overall_feedback": "Your resume has been analyzed. Focus on adding quantified achievements and relevant technical skills to boost your ATS score.",
        "quick_wins": [
            "Add numbers and metrics to your experience bullets (e.g. 'improved performance by 30%')",
            "Include a professional summary section at the top of your resume",
            "List more relevant technical skills matching your target role"
        ],
        "section_tips": {
            "skills":         "Add industry-relevant tools and technologies specific to your target role",
            "experience":     "Use strong action verbs and quantify your impact in each role",
            "projects":       "Describe technologies used, your specific role, and measurable outcomes",
            "education":      "Mention relevant coursework, GPA if strong, or academic achievements",
            "certifications": "Add vendor certifications (AWS, Google Cloud, Microsoft) relevant to your stack"
        },
        "priority_actions": [
            "Tailor your resume keywords for each specific job application",
            "Add 2-3 portfolio projects with measurable results and GitHub links",
            "Earn one industry-recognized certification in your primary tech stack"
        ]
    }
