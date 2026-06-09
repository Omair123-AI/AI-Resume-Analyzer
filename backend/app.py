"""
app.py - Flask application factory & entry point
"""
import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load .env from project ROOT (one level above backend/)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(ROOT_DIR, ".env"))


def create_app() -> Flask:
    app = Flask(__name__)

    # ── Config ────────────────────────────────────────────────────────────
    app.config["SECRET_KEY"]         = os.getenv("SECRET_KEY", "dev-secret")
    app.config["MAX_CONTENT_LENGTH"] = int(os.getenv("MAX_CONTENT_LENGTH", 16 * 1024 * 1024))
    app.config["UPLOAD_FOLDER"]      = os.path.join(
        os.path.dirname(__file__), os.getenv("UPLOAD_FOLDER", "uploads/resumes"))
    app.config["REPORT_FOLDER"]      = os.path.join(
        os.path.dirname(__file__), os.getenv("REPORT_FOLDER", "uploads/reports"))

    os.makedirs(app.config["UPLOAD_FOLDER"],  exist_ok=True)
    os.makedirs(app.config["REPORT_FOLDER"],  exist_ok=True)

    # ── CORS ──────────────────────────────────────────────────────────────
    CORS(app, resources={r"/api/*": {"origins": [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ]}})

    # ── Register Blueprints ───────────────────────────────────────────────
    from routes.upload_routes   import upload_bp
    from routes.ats_routes      import ats_bp
    from routes.job_routes      import job_bp
    from routes.github_routes   import github_bp
    from routes.linkedin_routes import linkedin_bp
    from routes.report_routes   import report_bp

    for bp in [upload_bp, ats_bp, job_bp, github_bp, linkedin_bp, report_bp]:
        app.register_blueprint(bp, url_prefix="/api")

    # ── Health check ──────────────────────────────────────────────────────
    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok", "service": "AI Resume Analyzer"}), 200

    # ── 404 / 500 handlers ────────────────────────────────────────────────
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Endpoint not found"}), 404

    @app.errorhandler(413)
    def too_large(e):
        return jsonify({"error": "File too large. Maximum size is 16MB."}), 413

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Internal server error"}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=os.getenv("FLASK_DEBUG", "True") == "True",
    )
