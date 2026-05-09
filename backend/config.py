# ==============================
# Load Environment Variables
# ==============================

from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# GitHub API token
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# NVIDIA API key
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")