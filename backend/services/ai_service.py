# ==============================
# AI Repository Analysis Service
# ==============================

import requests

# Import NVIDIA API key
from config import NVIDIA_API_KEY


# ==============================
# Create AI Prompt
# ==============================

def create_analysis_prompt(metrics, health_report):

    """
    Create concise AI analysis prompt
    """

    prompt = f"""
Analyze this GitHub repository.

Repository:
{metrics.get("name")}

Description:
{metrics.get("description")}

Metrics:
- Stars: {metrics.get("stars")}
- Forks: {metrics.get("forks")}
- Contributors: {metrics.get("contributors")}
- Open Issues: {metrics.get("open_issues")}
- Releases: {metrics.get("releases")}
- Language: {metrics.get("language")}

Health Report:
- Health Score: {health_report.get("health_score")}/10
- Activity: {health_report.get("activity_status")}
- Maintenance: {health_report.get("maintenance_status")}
- Community: {health_report.get("community_strength")}

Provide:
1. Repository Summary
2. Strengths
3. Risks
4. Production Readiness
5. Final Recommendation

Keep response concise and clear.
"""

    return prompt


# ==============================
# Generate AI Analysis
# ==============================

def generate_ai_analysis(metrics, health_report):

    """
    Generate AI repository analysis
    """

    try:

        # Create prompt
        prompt = create_analysis_prompt(
            metrics,
            health_report
        )

        # NVIDIA API endpoint
        url = "https://integrate.api.nvidia.com/v1/chat/completions"

        # Headers
        headers = {
            "Authorization": f"Bearer {NVIDIA_API_KEY}",
            "Content-Type": "application/json"
        }

        # Payload
        payload = {

            # Faster model
            "model": "meta/llama-3.1-8b-instruct",

            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            "temperature": 0.4,

            # Increased for complete response
            "max_tokens": 350
        }

        # Send request
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=18
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

        # Extract AI text
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