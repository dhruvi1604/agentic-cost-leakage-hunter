def calculate_health_grade(leakage_pct: float):
    """
    Returns financial health grade and explanation
    based on leakage percentage.
    """

    if leakage_pct < 1:
        return {
            "grade": "A",
            "label": "Excellent Control",
            "description": "Leakage is extremely low and well managed."
        }

    elif leakage_pct < 3:
        return {
            "grade": "B+",
            "label": "Healthy Control",
            "description": "Leakage exists but is within manageable limits."
        }

    elif leakage_pct < 6:
        return {
            "grade": "C",
            "label": "Moderate Risk",
            "description": "Leakage is noticeable and requires corrective action."
        }

    else:
        return {
            "grade": "D",
            "label": "High Risk",
            "description": "Leakage level is financially concerning and urgent review is recommended."
        }