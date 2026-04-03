from env.environment import CustomerSupportEnv

def smart_agent(obs):
    message = obs["message"].lower()
    customer_type = obs["customer_type"]

    # 🎯 INTENT DETECTION
    if "not receive" in message or "late" in message or "order" in message:
        intent = "refund"
    elif "complaint" in message or "second" in message:
        intent = "escalate"
    else:
        intent = "refund"

    # ⚡ PRIORITY DETECTION
    if "frustrating" in message or "angry" in message:
        priority = "high"
    elif customer_type == "premium":
        priority = "high"
    else:
        priority = "medium"

    # 💬 RESPONSE GENERATION
    if "angry" in message or "frustrating" in message:
        response = "We sincerely apologize for the inconvenience. We understand your frustration and will resolve this immediately."
    elif customer_type == "premium":
        response = "We value you as a premium customer and will prioritize resolving your issue."
    else:
        response = "Sorry for the inconvenience, we will resolve your issue soon."

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