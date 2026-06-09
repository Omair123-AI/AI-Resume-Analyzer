"""
upload_routes.py - Resume upload — parses + scores only (NO Gemini on upload)
Suggestions are fetched separately to avoid rate limiting.
"""
import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename

from utils.validators import validate_resume_upload
from utils.helpers import generate_unique_filename
from parsers.resume_parser import parse_resume
from ml.ats_score import calculate_ats_score
from ml.resume_ranker import rank_resume

upload_bp = Blueprint("upload", __name__)


@upload_bp.route("/upload", methods=["POST"])
def upload_resume():
    """
    POST /api/upload
    Fast response — only parses + scores. Does NOT call Gemini.
    Frontend fetches suggestions separately via /api/suggestions.
    """
    valid, error = validate_resume_upload()
    if not valid:
        return jsonify({"error": error}), 400

    file     = request.files["resume"]
    filename = generate_unique_filename(secure_filename(file.filename))
    save_dir = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(save_dir, exist_ok=True)
    filepath = os.path.join(save_dir, filename)
    file.save(filepath)

    try:
        parsed      = parse_resume(filepath)
        ats_result  = calculate_ats_score(parsed)
        rank_result = rank_resume(ats_result["total"], parsed)

        return jsonify({
            "success":  True,
            "file_id":  filename,
            "parsed":   _safe_parsed(parsed),
            "ats":      ats_result,
            "rank":     rank_result,
            # suggestions fetched separately — avoids Gemini rate limit on upload
            "suggestions": None,
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@upload_bp.route("/suggestions", methods=["POST"])
def get_suggestions():
    """
    POST /api/suggestions  { "file_id": "..." }
    Called after upload — fetches AI suggestions separately.
    """
    data    = request.get_json() or {}
    file_id = data.get("file_id", "")
    parsed  = _load_parsed(file_id)
    if "error" in parsed:
        return jsonify(parsed), 404

    from ai.suggestion_engine import generate_suggestions
    ats    = calculate_ats_score(parsed)
    result = generate_suggestions(parsed, ats)
    return jsonify(result), 200


@upload_bp.route("/analyze/<file_id>", methods=["GET"])
def get_analysis(file_id):
    parsed = _load_parsed(file_id)
    if "error" in parsed:
        return jsonify(parsed), 404
    ats  = calculate_ats_score(parsed)
    rank = rank_resume(ats["total"], parsed)
    return jsonify({"parsed": _safe_parsed(parsed), "ats": ats, "rank": rank}), 200


def _safe_parsed(parsed: dict) -> dict:
    return {k: v for k, v in parsed.items() if k != "raw_text"}


def _load_parsed(file_id: str) -> dict:
    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], file_id)
    if not os.path.exists(filepath):
        return {"error": f"File '{file_id}' not found."}
    try:
        return parse_resume(filepath)
    except Exception as e:
        return {"error": str(e)}
