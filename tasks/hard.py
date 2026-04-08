def grader(output):
    if not isinstance(output, dict):
        return 0.5

    score = 0.0

    if output.get("intent") == "escalate":
        score += 0.4
    if output.get("priority") == "high":
        score += 0.3
    if "sorry" in output.get("response", "").lower():
        score += 0.2

    return max(0.2, min(score, 0.8))