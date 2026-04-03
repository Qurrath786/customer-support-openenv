from env.environment import CustomerSupportEnv


def smart_agent(obs):
    message = obs["message"].lower()
    customer_type = obs["customer_type"]

    # 🔧 Normalize text
    message = message.replace("didn't", "did not")

    # 🎯 INTENT DETECTION (STRONG)
    if any(word in message for word in ["not receive", "did not receive", "missing", "late"]):
        intent = "refund"

    elif any(word in message for word in ["wrong", "incorrect", "damaged"]):
        intent = "refund"

    elif any(word in message for word in ["complaint", "second", "again"]):
        intent = "escalate"

    else:
        intent = "refund"

    # ⚡ PRIORITY DETECTION
    if any(word in message for word in ["frustrating", "angry", "issue", "problem"]):
        priority = "high"
    elif customer_type == "premium":
        priority = "high"
    else:
        priority = "medium"

    # 💬 RESPONSE GENERATION
    if any(word in message for word in ["wrong", "damaged"]):
        response = "We sincerely apologize for the issue with your order. We will arrange a replacement or refund immediately."

    elif any(word in message for word in ["not receive", "did not receive", "late", "missing"]):
        response = "We apologize for the inconvenience. We will check your order status and resolve this as soon as possible."

    elif customer_type == "premium":
        response = "We sincerely apologize. As a valued premium customer, your issue will be prioritized and resolved immediately."

    else:
        response = "Sorry for the inconvenience. We understand your concern and will resolve it quickly."

    return {
        "intent": intent,
        "priority": priority,
        "response": response
    }


def run():
    env = CustomerSupportEnv()
    obs = env.reset()

    done = False
    total_reward = 0
    step = 1

    print("[START] Running smart agent")

    while not done:
        action = smart_agent(obs)

        obs, reward, done, _ = env.step(action)

        print(f"[STEP] {step} action={action} reward={reward}")

        total_reward += reward
        step += 1

    print(f"[END] Total Reward = {total_reward}")


if __name__ == "__main__":
    run()