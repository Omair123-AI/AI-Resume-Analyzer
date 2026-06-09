"""
github_routes.py - GitHub profile analysis endpoint
"""
from flask import Blueprint, request, jsonify
from integrations.github_analyzer import analyze_github
from utils.validators import validate_github_url

github_bp = Blueprint("github", __name__)


@github_bp.route("/github", methods=["POST"])
def analyze_github_profile():
    """
    POST /api/github
    Body: { "github_url": "https://github.com/username" }
    """
    data = request.get_json() or {}
    url  = data.get("github_url", "").strip()

    if not url:
        return jsonify({"error": "github_url is required"}), 400

    valid, error = validate_github_url(url)
    if not valid:
        return jsonify({"error": error}), 400

    result = analyze_github(url)
    if "error" in result:
        return jsonify(result), 404

    return jsonify(result), 200
