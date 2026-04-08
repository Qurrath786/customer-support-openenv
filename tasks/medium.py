def grader(output):
    if not isinstance(output, dict):
        return 0.5

    score = 0.0

    if output.get("intent") == "refund":
        score += 0.4
    if output.get("priority") == "high":
        score += 0.4

    # ✅ force safe range
    return max(0.2, min(score, 0.8))