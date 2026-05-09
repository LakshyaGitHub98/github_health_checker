# ==============================
# Validate GitHub Repository URL
# ==============================

def is_valid_github_url(url):

    """
    Check if provided URL is a valid GitHub repository URL
    """

    # Check empty URL
    if not url:
        return False

    # Check GitHub domain
    if "github.com" not in url:
        return False

    return True