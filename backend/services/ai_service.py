# ==============================
# AI Repository Analysis Service
# ==============================

import requests

# Import NVIDIA API key
from config import NVIDIA_API_KEY


# ==============================
# Generate AI Prompt
# ==============================

def create_analysis_prompt(metrics, health_report):

    """
    Create AI analysis prompt
    """

    prompt = f"""
You are an expert software engineer and open-source analyst.

Analyze this GitHub repository.

Repository Name:
{metrics.get("name")}

Description:
{metrics.get("description")}

Repository Metrics:
- Stars: {metrics.get("stars")}
- Forks: {metrics.get("forks")}
- Contributors: {metrics.get("contributors")}
- Open Issues: {metrics.get("open_issues")}
- Releases: {metrics.get("releases")}
- Primary Language: {metrics.get("language")}

Health Metrics:
- Health Score: {health_report.get("health_score")}/10
- Activity Status: {health_report.get("activity_status")}
- Maintenance Status: {health_report.get("maintenance_status")}
- Community Strength: {health_report.get("community_strength")}

Provide:
1. Repository Summary
2. Strengths
3. Risks
4. Production Readiness
5. Final Recommendation

Keep the response concise, practical, and professional.
"""

    return prompt


# ==============================
# Generate AI Analysis
# ==============================

def generate_ai_analysis(metrics, health_report):

    """
    Generate AI-powered repository analysis
    """

    try:

        # Create prompt
        prompt = create_analysis_prompt(
            metrics,
            health_report
        )

        # NVIDIA API endpoint
        url = "https://integrate.api.nvidia.com/v1/chat/completions"

        # Request headers
        headers = {
            "Authorization": f"Bearer {NVIDIA_API_KEY}",
            "Content-Type": "application/json"
        }

        # IMPORTANT:
        # Using smaller faster model
        payload = {

            "model": "meta/llama-3.1-8b-instruct",

            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            "temperature": 0.4,

            "max_tokens": 220
        }

        # API request
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=15
        )

        # Convert response
        data = response.json()

        # Validate response
        if "choices" not in data:

            print("NVIDIA API ERROR:", data)

            return {
                "error": True,
                "content": "AI analysis unavailable right now."
            }

        # Extract response text
        ai_response = data["choices"][0]["message"]["content"]

        return {
            "error": False,
            "content": ai_response
        }

    except requests.exceptions.Timeout:

        return {
            "error": True,
            "content": "AI analysis took too long to respond."
        }

    except Exception as error:

        print("AI SERVICE ERROR:", error)

        return {
            "error": True,
            "content": "Unable to generate AI analysis."
        }