def grader(output):
    score = 0

    if output["intent"] == "refund":
        score += 0.4
    if output["priority"] == "high":
        score += 0.4

    return max(0.1, min(score, 0.9))  # ✅ force range