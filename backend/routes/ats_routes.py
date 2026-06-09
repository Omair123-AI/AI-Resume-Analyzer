"""
ats_routes.py - ATS score, missing skills, JD matching endpoints
"""
import os
from flask import Blueprint, request, jsonify, current_app
from parsers.resume_parser import parse_resume
from ml.ats_score import calculate_ats_score
from ml.missing_skill_detector import detect_missing_skills, get_all_roles
from ml.jd_matcher import analyze_resume_vs_jd
from utils.validators import validate_jd_input

ats_bp = Blueprint("ats", __name__)


@ats_bp.route("/ats/<file_id>", methods=["GET"])
def get_ats_score(file_id):
    """GET /api/ats/<file_id>"""
    parsed = _load_parsed(file_id)
    if "error" in parsed:
        return jsonify(parsed), 404
    return jsonify(calculate_ats_score(parsed)), 200


@ats_bp.route("/missing-skills", methods=["POST"])
def missing_skills():
    """
    POST /api/missing-skills
    Body: { "file_id": "...", "target_role": "Machine Learning Engineer" }
    """
    data        = request.get_json() or {}
    file_id     = data.get("file_id", "")
    target_role = data.get("target_role", "").strip()

    if not target_role:
        return jsonify({"error": "target_role is required"}), 400

    parsed = _load_parsed(file_id)
    if "error" in parsed:
        return jsonify(parsed), 404

    found_skills = parsed.get("skills", {}).get("found", [])
    result       = detect_missing_skills(found_skills, target_role)
    return jsonify(result), 200


@ats_bp.route("/roles", methods=["GET"])
def list_roles():
    """GET /api/roles - return all available target roles from dataset"""
    return jsonify({"roles": get_all_roles()}), 200


@ats_bp.route("/jd-match", methods=["POST"])
def jd_match():
    """
    POST /api/jd-match
    Body: { "file_id": "...", "job_description": "..." }
    """
    data = request.get_json() or {}
    valid, error = validate_jd_input(data)
    if not valid:
        return jsonify({"error": error}), 400

    file_id = data.get("file_id", "")
    jd_text = data.get("job_description", "")

    parsed = _load_parsed(file_id)
    if "error" in parsed:
        return jsonify(parsed), 404

    result = analyze_resume_vs_jd(parsed["raw_text"], jd_text, parsed)
    return jsonify(result), 200


def _load_parsed(file_id: str) -> dict:
    from flask import current_app
    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], file_id)
    if not os.path.exists(filepath):
        return {"error": f"File '{file_id}' not found. Upload first."}
    try:
        return parse_resume(filepath)
    except Exception as e:
        return {"error": str(e)}
