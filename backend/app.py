# ==============================
# Main Flask Application
# ==============================

from flask import Flask
from flask_cors import CORS

# Import analyze routes
from routes.analyze_routes import analyze_bp

# Create Flask app
app = Flask(__name__)

# Enable CORS
CORS(app)

# Register Blueprint routes
app.register_blueprint(analyze_bp)


# ==============================
# Default Home Route
# ==============================

@app.route("/")
def home():

    return {
        "message": "GitHub Repository Health Checker API"
    }


# ==============================
# Run Flask Server
# ==============================

if __name__ == "__main__":

    app.run(debug=True)