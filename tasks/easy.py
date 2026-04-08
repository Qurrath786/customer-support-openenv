def grader(output):
    if output["intent"] == "refund":
        return 0.8   # ✅ not 1.0
    return 0.2       # ✅ not 0.0