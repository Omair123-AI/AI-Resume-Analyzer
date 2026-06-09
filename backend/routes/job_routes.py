
"""
job_routes.py - Career advisor, gap analysis, roadmap endpoints
"""
import os
from flask import Blueprint, request, jsonify, current_app
from parsers.resume_parser import parse_resume
from ml.ats_score import calculate_ats_score
from ai.career_advisor import generate_career_analysis, calculate_career_readiness
from ai.resume_rewriter import rewrite_resume_bullets, rewrite_single_bullet
from ai.project_analyzer import analyze_projects

job_bp = Blueprint("job", __name__)


@job_bp.route("/career-analysis", methods=["POST"])
def career_analysis():
    """
    POST /api/career-analysis
    Body: { "file_id": "...", "target_role": "..." }
    """
    data        = request.get_json() or {}
    file_id     = data.get("file_id", "")
    target_role = data.get("target_role", "")

    parsed = _load_parsed(file_id)
    if "error" in parsed:
        return jsonify(parsed), 404

    ats    = calculate_ats_score(parsed)
    result = generate_career_analysis(parsed, ats, target_role)
    return jsonify(result), 200


@job_bp.route("/career-readiness", methods=["POST"])
def career_readiness_score():
    """POST /api/career-readiness  Body: { "file_id": "..." }"""
    data    = request.get_json() or {}
    file_id = data.get("file_id", "")
    parsed  = _load_parsed(file_id)
    if "error" in parsed:
        return jsonify(parsed), 404
    ats    = calculate_ats_score(parsed)
    result = calculate_career_readiness(parsed, ats)
    return jsonify(result), 200


@job_bp.route("/rewrite-bullets", methods=["POST"])
def rewrite_bullets():
    """
    POST /api/rewrite-bullets
    Body: { "bullets": ["Built a web app", "Worked on API"] }
    """
    data    = request.get_json() or {}
    bullets = data.get("bullets", [])
    if not bullets:
        return jsonify({"error": "Provide a list of bullet points in 'bullets'"}), 400
    result = rewrite_resume_bullets(bullets)
    return jsonify(result), 200


@job_bp.route("/rewrite-bullet", methods=["POST"])
def rewrite_one_bullet():
    """
    POST /api/rewrite-bullet
    Body: { "text": "Worked on machine learning models" }
    """
    data = request.get_json() or {}
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "Provide bullet text in 'text'"}), 400
    improved = rewrite_single_bullet(text)
    return jsonify({"original": text, "improved": improved}), 200


@job_bp.route("/analyze-projects", methods=["POST"])
def analyze_projects_route():
    """POST /api/analyze-projects  Body: { "file_id": "..." }"""
    data    = request.get_json() or {}
    file_id = data.get("file_id", "")
    parsed  = _load_parsed(file_id)
    if "error" in parsed:
        return jsonify(parsed), 404
    result = analyze_projects(parsed.get("projects", {}))
    return jsonify(result), 200


def _load_parsed(file_id: str) -> dict:
    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], file_id)
    if not os.path.exists(filepath):
        return {"error": f"File '{file_id}' not found. Upload first."}
    try:
        return parse_resume(filepath)
    except Exception as e:
        return {"error": str(e)}
