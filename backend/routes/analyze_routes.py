# ==============================
# Analyze Routes
# ==============================

from flask import Blueprint, request, jsonify

# Import validators
from utils.validators import is_valid_github_url

# Import GitHub service
from services.github_service import analyze_repository_metrics

# Import health service
from services.health_service import generate_health_report

# Import AI service
from services.ai_service import generate_ai_analysis

# Create Blueprint
analyze_bp = Blueprint("analyze", __name__)


# ==============================
# Analyze Repository Endpoint
# ==============================

@analyze_bp.route("/analyze", methods=["POST"])
def analyze_repository():

    try:

        # Get request JSON data
        data = request.get_json()

        # Extract repository URL
        repo_url = data.get("repo_url")

        # Validate GitHub URL
        if not is_valid_github_url(repo_url):

            return jsonify({
                "success": False,
                "message": "Invalid GitHub repository URL"
            }), 400

        # Fetch repository metrics
        metrics = analyze_repository_metrics(
            repo_url
        )

        # Generate health report
        health_report = generate_health_report(
            metrics
        )

        # Generate AI analysis
        ai_analysis = generate_ai_analysis(
            metrics,
            health_report
        )

        # Return final response
        return jsonify({

            "success": True,

            "repository": metrics,

            "health_report": health_report,

            "ai_analysis": ai_analysis
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500