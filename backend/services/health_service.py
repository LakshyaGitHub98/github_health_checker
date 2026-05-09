# ==============================
# Repository Health Service
# ==============================

from datetime import datetime, timezone


# ==============================
# Calculate Days Since Last Push
# ==============================

def calculate_days_since_last_push(last_push_date):

    pushed_date = datetime.strptime(
        last_push_date,
        "%Y-%m-%dT%H:%M:%SZ"
    )

    pushed_date = pushed_date.replace(
        tzinfo=timezone.utc
    )

    current_date = datetime.now(
        timezone.utc
    )

    difference = current_date - pushed_date

    return difference.days


# ==============================
# Get Activity Status
# ==============================

def get_activity_status(days_since_push):

    if days_since_push <= 7:
        return "Highly Active"

    elif days_since_push <= 30:
        return "Active"

    elif days_since_push <= 90:
        return "Moderately Active"

    else:
        return "Inactive"


# ==============================
# Calculate Health Score
# ==============================

def calculate_health_score(metrics):

    score = 0

    stars = metrics.get("stars", 0)

    forks = metrics.get("forks", 0)

    contributors = metrics.get(
        "contributors",
        0
    )

    releases = metrics.get("releases", 0)

    open_issues = metrics.get(
        "open_issues",
        0
    )

    description = metrics.get(
        "description"
    )

    has_readme = metrics.get(
        "has_readme",
        False
    )

    last_push = metrics.get(
        "last_push"
    )

    days_since_push = calculate_days_since_last_push(
        last_push
    )


    # Base Score
    score += 3


    # Activity Score
    if days_since_push <= 7:
        score += 2

    elif days_since_push <= 30:
        score += 1


    # Stars Score
    if stars >= 100000:
        score += 2

    elif stars >= 10000:
        score += 1


    # Forks Score
    if forks >= 10000:
        score += 1


    # Contributors Score
    if contributors >= 20:
        score += 2

    elif contributors >= 5:
        score += 1


    # Releases Score
    if releases >= 5:
        score += 1


    # Description Score
    if description:
        score += 1


    # README Score
    if has_readme:
        score += 1


    # Open Issues Penalty
    if open_issues >= 10000:
        score -= 1


    # Score Limits
    if score < 1:
        score = 1

    if score > 10:
        score = 10

    return score


# ==============================
# Get Maintenance Status
# ==============================

def get_maintenance_status(score):

    if score >= 8:
        return "Well Maintained"

    elif score >= 5:
        return "Moderately Maintained"

    else:
        return "Needs Improvement"


# ==============================
# Get Community Strength
# ==============================

def get_community_strength(metrics):

    stars = metrics.get("stars", 0)

    contributors = metrics.get(
        "contributors",
        0
    )

    if stars >= 50000 and contributors >= 20:
        return "Strong"

    elif stars >= 1000:
        return "Growing"

    else:
        return "Small"


# ==============================
# Generate Health Report
# ==============================

def generate_health_report(metrics):

    days_since_push = calculate_days_since_last_push(
        metrics["last_push"]
    )

    activity_status = get_activity_status(
        days_since_push
    )

    health_score = calculate_health_score(
        metrics
    )

    maintenance_status = get_maintenance_status(
        health_score
    )

    community_strength = get_community_strength(
        metrics
    )

    return {

        "health_score": health_score,

        "activity_status": activity_status,

        "maintenance_status": maintenance_status,

        "community_strength": community_strength,

        "days_since_last_push": days_since_push
    }