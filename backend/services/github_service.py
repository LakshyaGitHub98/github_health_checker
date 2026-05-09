# ==============================
# GitHub Repository Service
# ==============================

import requests

# Import GitHub token
from config import GITHUB_TOKEN


# ==============================
# Extract Repository Information
# ==============================

def extract_repo_details(repo_url):

    """
    Extract owner and repository name
    from GitHub repository URL
    """

    # Remove extra slash
    cleaned_url = repo_url.rstrip("/")

    # Split URL
    parts = cleaned_url.split("/")

    # Extract owner and repo name
    owner = parts[-2]
    repo = parts[-1]

    return owner, repo


# ==============================
# Create GitHub API Headers
# ==============================

def get_github_headers():

    """
    Return GitHub API request headers
    """

    headers = {
        "Accept": "application/vnd.github+json"
    }

    # Add GitHub token if available
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    return headers


# ==============================
# Fetch Main Repository Data
# ==============================

def fetch_repository_data(owner, repo):

    """
    Fetch main repository details
    """

    url = f"https://api.github.com/repos/{owner}/{repo}"

    response = requests.get(
        url,
        headers=get_github_headers()
    )

    data = response.json()

    return data


# ==============================
# Fetch Contributors Count
# ==============================

def fetch_contributors(owner, repo):

    """
    Fetch contributors count
    """

    try:

        url = f"https://api.github.com/repos/{owner}/{repo}/contributors"

        response = requests.get(
            url,
            headers=get_github_headers()
        )

        data = response.json()

        if isinstance(data, list):
            return len(data)

        return 0

    except Exception:
        return 0


# ==============================
# Fetch Releases Count
# ==============================

def fetch_releases(owner, repo):

    """
    Fetch releases count
    """

    try:

        url = f"https://api.github.com/repos/{owner}/{repo}/releases"

        response = requests.get(
            url,
            headers=get_github_headers()
        )

        data = response.json()

        if isinstance(data, list):
            return len(data)

        return 0

    except Exception:
        return 0


# ==============================
# Check README Availability
# ==============================

def check_readme_exists(owner, repo):

    """
    Check if repository has README
    """

    try:

        url = f"https://api.github.com/repos/{owner}/{repo}/readme"

        response = requests.get(
            url,
            headers=get_github_headers()
        )

        # README exists
        if response.status_code == 200:
            return True

        return False

    except Exception:
        return False


# ==============================
# Analyze Repository Metrics
# ==============================

def analyze_repository_metrics(repo_url):

    """
    Analyze repository metrics
    """

    # Extract repository details
    owner, repo = extract_repo_details(repo_url)

    # Fetch repository data
    repo_data = fetch_repository_data(owner, repo)

    # Check repository exists
    if "full_name" not in repo_data:

        raise Exception(
            repo_data.get("message", "Repository not found")
        )

    # Fetch contributors
    contributors_count = fetch_contributors(
        owner,
        repo
    )

    # Fetch releases
    releases_count = fetch_releases(
        owner,
        repo
    )

    # Check README
    has_readme = check_readme_exists(
        owner,
        repo
    )

    # Prepare metrics
    metrics = {

        "name": repo_data.get("full_name"),

        "description": repo_data.get("description"),

        "stars": repo_data.get("stargazers_count"),

        "forks": repo_data.get("forks_count"),

        "watchers": repo_data.get("watchers_count"),

        "open_issues": repo_data.get("open_issues_count"),

        "language": repo_data.get("language"),

        "created_at": repo_data.get("created_at"),

        "updated_at": repo_data.get("updated_at"),

        "last_push": repo_data.get("pushed_at"),

        "contributors": contributors_count,

        "releases": releases_count,

        "has_readme": has_readme
    }

    return metrics