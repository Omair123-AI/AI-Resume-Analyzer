import json
import time
from ai.gemini_client import call_gemini


def generate_career_analysis(parsed_resume: dict, ats_result: dict, target_role: str = "") -> dict:
    readiness = calculate_career_readiness(parsed_resume, ats_result)
    gap_analysis = generate_gap_analysis(parsed_resume, target_role)
    roadmap = generate_learning_roadmap(parsed_resume, target_role)
    return {"career_readiness": readiness, "gap_analysis": gap_analysis, "learning_roadmap": roadmap}


def calculate_career_readiness(parsed_resume: dict, ats_result: dict) -> dict:
    ats_score = ats_result.get("total", 0) / 100
    skill_score = min(parsed_resume.get(
        "skills", {}).get("count", 0) / 15, 1.0)
    proj_score = min(parsed_resume.get(
        "projects", {}).get("count", 0) / 4, 1.0)
    exp_years = parsed_resume.get("experience", {}).get("total_years", 0)
    exp_score = min(exp_years / 5, 1.0)
    cert_count = parsed_resume.get("certifications", {}).get("count", 0)
    cert_score = min(cert_count / 3, 1.0)

    weights = {"resume": 0.30, "skills": 0.25, "projects": 0.20,
               "experience": 0.15, "certifications": 0.10}
    breakdown = {
        "resume":         round(ats_score * 100, 1),
        "skills":         round(skill_score * 100, 1),
        "projects":       round(proj_score * 100, 1),
        "experience":     round(exp_score * 100, 1),
        "certifications": round(cert_score * 100, 1),
    }
    total = sum(breakdown[k] * weights[k] for k in weights)
    return {"score": round(total, 1), "label": _readiness_label(total), "breakdown": breakdown, "weights": weights}


def generate_gap_analysis(parsed_resume: dict, target_role: str) -> dict:
    missing_skills = []
    missing_certs = []
    missing_exp = []
    missing_proj = []

    if target_role:
        from ml.missing_skill_detector import detect_missing_skills
        found = [s.lower()
                 for s in parsed_resume.get("skills", {}).get("found", [])]
        gap = detect_missing_skills(found, target_role)
        missing_skills = gap.get("missing_skills", [])

    if parsed_resume.get("certifications", {}).get("count", 0) == 0:
        missing_certs = [
            "No certifications found. Consider AWS, Google, or Microsoft certs."]
    if parsed_resume.get("experience", {}).get("total_years", 0) == 0:
        missing_exp = [
            "No work experience. Add internships, freelance, or volunteer work."]
    if parsed_resume.get("projects", {}).get("count", 0) == 0:
        missing_proj = [
            "No projects listed. Add 2-3 personal or academic projects."]

    return {
        "missing_skills":         missing_skills[:10],
        "missing_certifications": missing_certs,
        "missing_experience":     missing_exp,
        "missing_projects":       missing_proj,
        "total_gaps":             len(missing_skills) + len(missing_certs) + len(missing_exp) + len(missing_proj),
    }


def generate_learning_roadmap(parsed_resume: dict, target_role: str) -> dict:
    if not target_role:
        return _generic_roadmap()

    found_skills = parsed_resume.get("skills", {}).get("found", [])[:10]
    missing = []
    if target_role:
        from ml.missing_skill_detector import detect_missing_skills
        found = [s.lower() for s in found_skills]
        gap = detect_missing_skills(found, target_role)
        missing = gap.get("missing_skills", [])[:6]

    exp_years = parsed_resume.get("experience", {}).get("total_years", 0)

    prompt = f"""Create a specific 5-step learning roadmap for: {target_role}

Current skills: {', '.join(found_skills) if found_skills else 'None'}
Missing skills to learn: {', '.join(missing) if missing else 'None'}
Experience: {exp_years} years

Make each step specific to their missing skills above. Include real resource names.

Return ONLY valid JSON, no markdown:
{{"goal":"{target_role}","estimated_time":"X months","steps":[{{"step":1,"title":"specific title","description":"specific description mentioning actual skills","resources":["Real Resource 1","Real Resource 2"],"duration":"X weeks"}},{{"step":2,"title":"...","description":"...","resources":[...],"duration":"..."}},{{"step":3,"title":"...","description":"...","resources":[...],"duration":"..."}},{{"step":4,"title":"...","description":"...","resources":[...],"duration":"..."}},{{"step":5,"title":"...","description":"...","resources":[...],"duration":"..."}}]}}"""

    # Wait to avoid rate limit collision with suggestion_engine
    time.sleep(6)
    response = call_gemini(prompt)

    if response:
        try:
            clean = response.strip().strip("```json").strip("```").strip()
            # Extract JSON object
            import re
            match = re.search(r'\{.*\}', clean, re.DOTALL)
            if match:
                result = json.loads(match.group(0))
                if result.get("steps"):
                    print("[Roadmap] ✓ Gemini generated personalized roadmap")
                    return result
        except Exception as e:
            print(f"[Roadmap] Parse error: {e}")

    print("[Roadmap] Using generic fallback")
    return _generic_roadmap_for_role(target_role, missing)


def _generic_roadmap(found_skills: list = None) -> dict:
    return {
        "goal": "General Career Growth",
        "estimated_time": "6 months",
        "steps": [
            {"step": 1, "title": "Strengthen Core Skills",    "description": "Deepen expertise in your primary stack.",
                "resources": ["Coursera", "Udemy", "freeCodeCamp"], "duration": "4 weeks"},
            {"step": 2, "title": "Build Portfolio Projects",  "description": "Create 2-3 end-to-end projects with real impact.",
                "resources": ["GitHub", "Personal Blog"],           "duration": "6 weeks"},
            {"step": 3, "title": "Earn a Certification",      "description": "Pursue an industry-recognized certification.",
                "resources": ["AWS", "Google Cloud", "Microsoft"],  "duration": "6 weeks"},
            {"step": 4, "title": "Network & Apply",           "description": "Optimize LinkedIn and start applying.",
                "resources": ["LinkedIn", "Meetup.com", "GitHub"],  "duration": "Ongoing"},
        ]
    }


def _generic_roadmap_for_role(role: str, missing_skills: list = None) -> dict:
    # Role-specific resources
    role_resources = {
        "machine learning engineer": ["fast.ai", "Kaggle", "Papers With Code", "MLflow Docs"],
        "ai engineer":               ["LangChain Docs", "OpenAI Cookbook", "Hugging Face", "LlamaIndex"],
        "data scientist":            ["Kaggle", "Towards Data Science", "StatQuest", "Mode Analytics"],
        "frontend developer":        ["Frontend Masters", "css-tricks.com", "React Docs", "Scrimba"],
        "backend developer":         ["roadmap.sh", "FastAPI Docs", "PostgreSQL Tutorial", "Redis Docs"],
        "devops engineer":           ["Docker Docs", "Kubernetes.io", "HashiCorp Learn", "Linux Foundation"],
        "full stack developer":      ["The Odin Project", "freeCodeCamp", "roadmap.sh", "Fireship.io"],
    }
    resources = role_resources.get(
        role.lower(), ["Coursera", "Udemy", "Official Docs", "GitHub"])
    missing_str = ', '.join(
        missing_skills[:3]) if missing_skills else "core tools"

    return {
        "goal": role,
        "estimated_time": "6-12 months",
        "steps": [
            {"step": 1, "title": f"Master {missing_str.split(',')[0] if missing_skills else 'Core Concepts'}",
             "description": f"Learn the foundational tools needed: {missing_str}",    "resources": resources[:2],    "duration": "4-6 weeks"},
            {"step": 2, "title": "Build Real Projects",          "description": f"Apply {missing_str} in 2-3 hands-on projects.",
                "resources": ["GitHub", "Kaggle"],             "duration": "4-6 weeks"},
            {"step": 3, "title": "Advanced Tools & Deployment",  "description": "Learn production-level tools and deployment practices.",
                "resources": resources[2:] or ["Docker", "AWS"], "duration": "4-6 weeks"},
            {"step": 4, "title": "Get Certified",                "description": "Earn a recognized certification for your role.",
                "resources": ["AWS", "Google", "Coursera"],    "duration": "4-6 weeks"},
            {"step": 5, "title": "Apply & Interview Prep",       "description": "Optimize resume, apply to roles, practice interviews.",
                "resources": ["LinkedIn", "Glassdoor", "LeetCode"], "duration": "Ongoing"},
        ]
    }


def _readiness_label(score: float) -> str:
    if score >= 80:
        return "Job Ready"
    if score >= 60:
        return "Almost Ready"
    if score >= 40:
        return "In Progress"
    return "Early Stage"