def grader(action, correct):
    if action["intent"] == correct["intent"]:
        return 1.0
    return 0.0