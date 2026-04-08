def grader(output):
    score = 0

    if output["intent"] == "escalate":
        score += 0.4
    if output["priority"] == "high":
        score += 0.3
    if "sorry" in output["response"].lower():
        score += 0.2

    return max(0.1, min(score, 0.9))  # ✅ always safe