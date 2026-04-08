def grader(output):
    if not isinstance(output, dict):
        return 0.5

    if output.get("intent") == "refund":
        return 0.8   # ✅ valid

    return 0.3       # ✅ valid