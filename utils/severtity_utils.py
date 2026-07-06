"""
severity_utils.py
-------------------
This file contains the logic to calculate a severity level
(Low, Medium, High) for a detected civic issue.

The severity is calculated using two simple factors:
1. The type of issue detected (some issues are naturally more serious).
2. The confidence score of the detection (how sure the AI model is).

This is a simple rule-based system, easy for beginners to understand.
"""

# Base severity score for each issue type
# Higher number = more serious issue by default
ISSUE_BASE_SCORE = {
    "pothole": 2,
    "garbage": 1,
    "water_leak": 2,
    "broken_streetlight": 1,
    "damaged_road": 3
}


def calculate_severity(issue_type, confidence_score):
    """
    Calculates the severity level for a civic issue.

    Parameters:
    - issue_type: string, the type of issue detected (e.g. "pothole")
    - confidence_score: float between 0 and 1, how confident the model is

    Returns:
    - severity: string, one of "Low", "Medium", "High"
    """

    # Get the base score for this issue type, default to 1 if unknown
    base_score = ISSUE_BASE_SCORE.get(issue_type.lower(), 1)

    # Convert confidence score (0 to 1) into a confidence weight (0 to 3)
    confidence_weight = confidence_score * 3

    # Add the base score and confidence weight together
    total_score = base_score + confidence_weight

    # Decide the severity level based on the total score
    if total_score <= 2.5:
        severity = "Low"
    elif total_score <= 4.5:
        severity = "Medium"
    else:
        severity = "High"

    return severity
