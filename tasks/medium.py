def grader(action, correct):
    score = 0.0

    if action["intent"] == correct["intent"]:
        score += 0.5

    if action["priority"] == correct["priority"]:
        score += 0.5

    return score