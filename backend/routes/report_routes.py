"""
report_routes.py - PDF report generation & download endpoint
"""
import os
from flask import Blueprint, request, jsonify, send_file, current_app
from parsers.resume_parser import parse_resume
from ml.ats_score import calculate_ats_score
from ml.resume_ranker import rank_resume
from ml.missing_skill_detector import detect_missing_skills
from ai.suggestion_engine import generate_suggestions
from ai.career_advisor import generate_career_analysis
from reports.report_generator import generate_report
from utils.helpers import timestamp_now

report_bp = Blueprint("report", __name__)


@report_bp.route("/report/generate", methods=["POST"])
def generate_pdf_report():
    """
    POST /api/report/generate
    Body: {
        "file_id": "...",
        "target_role": "...",      ← optional
        "jd_text": "..."           ← optional
    }
    Returns: { "report_id": "filename.pdf", "download_url": "/api/report/download/filename.pdf" }
    """
    data        = request.get_json() or {}
    file_id     = data.get("file_id", "")
    target_role = data.get("target_role", "")
    jd_text     = data.get("jd_text", "")

    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], file_id)
    if not os.path.exists(filepath):
        return jsonify({"error": f"File '{file_id}' not found"}), 404

    try:
        parsed  = parse_resume(filepath)
        ats     = calculate_ats_score(parsed)
        rank    = rank_resume(ats["total"], parsed)
        sugg    = generate_suggestions(parsed, ats)
        career  = generate_career_analysis(parsed, ats, target_role)

        missing_skills = {}
        if target_role:
            found = [s.lower() for s in parsed.get("skills", {}).get("found", [])]
            missing_skills = detect_missing_skills(found, target_role)

        jd_match = {}
        if jd_text:
            from ml.jd_matcher import analyze_resume_vs_jd
            jd_match = analyze_resume_vs_jd(parsed["raw_text"], jd_text, parsed)

        analysis_data = {
            "parsed":           {k: v for k, v in parsed.items() if k != "raw_text"},
            "ats":              ats,
            "rank":             rank,
            "suggestions":      sugg,
            "career_readiness": career.get("career_readiness", {}),
            "gap_analysis":     career.get("gap_analysis", {}),
            "learning_roadmap": career.get("learning_roadmap", {}),
            "missing_skills":   missing_skills,
            "jd_match":         jd_match,
        }

        # Save to reports folder
        report_dir = current_app.config["REPORT_FOLDER"]
        os.makedirs(report_dir, exist_ok=True)
        report_name = f"report_{file_id.replace('.', '_')}_{timestamp_now().replace(' ','_').replace(':','-')}.pdf"
        report_path = os.path.join(report_dir, report_name)

        generate_report(analysis_data, report_path)

        return jsonify({
            "success":      True,
            "report_id":    report_name,
            "download_url": f"/api/report/download/{report_name}",
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@report_bp.route("/report/download/<report_id>", methods=["GET"])
def download_report(report_id):
    """GET /api/report/download/<report_id>"""
    report_path = os.path.join(current_app.config["REPORT_FOLDER"], report_id)
    if not os.path.exists(report_path):
        return jsonify({"error": "Report not found. Generate it first."}), 404
    return send_file(report_path, as_attachment=True, download_name=report_id)
