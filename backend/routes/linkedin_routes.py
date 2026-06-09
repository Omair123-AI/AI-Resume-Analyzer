"""
linkedin_routes.py - LinkedIn profile analysis endpoint
"""
from flask import Blueprint, request, jsonify
from integrations.linkedin_analyzer import analyze_linkedin
from utils.validators import validate_linkedin_url

linkedin_bp = Blueprint("linkedin", __name__)


@linkedin_bp.route("/linkedin", methods=["POST"])
def analyze_linkedin_profile():
    """
    POST /api/linkedin
    Body: {
        "linkedin_url": "https://linkedin.com/in/username",
        "profile_data": {           ← optional but recommended
            "headline": "...",
            "summary": "...",
            "skills": ["Python", ...],
            "experience_count": 3,
            "recommendations": 2,
            "certifications": 1,
            "projects": 2,
            "education": "BS Computer Science"
        }
    }
    """
    data         = request.get_json() or {}
    url          = data.get("linkedin_url", "").strip()
    profile_data = data.get("profile_data", None)

    if not url:
        return jsonify({"error": "linkedin_url is required"}), 400

    valid, error = validate_linkedin_url(url)
    if not valid:
        return jsonify({"error": error}), 400

    result = analyze_linkedin(url, profile_data)
    return jsonify(result), 200
