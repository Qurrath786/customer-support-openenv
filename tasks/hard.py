def grader(action, correct):
    score = 0.0

    if action["intent"] == correct["intent"]:
        score += 0.4

    if action["priority"] == correct["priority"]:
        score += 0.3

    if any(word in action["response"].lower() for word in ["sorry", "apologize", "understand"]):
        score += 0.3

    return round(score, 2)