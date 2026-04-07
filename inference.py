import os
import json
from openai import OpenAI
from env.environment import CustomerSupportEnv


# 🔥 Initialize LLM client (MANDATORY for hackathon)
client = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"]
)


# 🧠 LLM DECISION FUNCTION
def llm_decision(message, customer_type):
    prompt = f"""
You are a customer support AI.

Message: {message}
Customer Type: {customer_type}

Decide:
- intent (refund / escalate / inform)
- priority (low / medium / high)
- short response

Return ONLY JSON:
{{"intent": "...", "priority": "...", "response": "..."}}
"""

    try:
        response = client.chat.completions.create(
            model=os.environ["MODEL_NAME"],
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.choices[0].message.content

        return json.loads(text)

    except Exception as e:
        # fallback if LLM fails
        return smart_agent({"message": message, "customer_type": customer_type})


# 🧠 RULE-BASED BACKUP (your original logic)
def smart_agent(obs):
    message = obs["message"].lower()
    customer_type = obs["customer_type"]

    message = message.replace("didn't", "did not")

    # INTENT
    if any(word in message for word in ["not receive", "did not receive", "missing", "late"]):
        intent = "refund"

    elif any(word in message for word in ["wrong", "incorrect", "damaged"]):
        intent = "refund"

    elif any(word in message for word in ["payment", "deducted", "failed"]):
        intent = "escalate"

    elif any(word in message for word in ["status", "update"]):
        intent = "inform"

    elif any(word in message for word in ["complaint", "complained", "second", "again"]):
        intent = "escalate"

    else:
        intent = "refund"

    # PRIORITY
    if any(word in message for word in ["frustrating", "angry"]):
        priority = "high"

    elif any(word in message for word in ["payment", "deducted", "failed"]):
        priority = "high"

    elif customer_type == "premium":
        priority = "high"

    elif any(word in message for word in ["status", "update"]):
        priority = "low"

    else:
        priority = "medium"

    # RESPONSE
    if any(word in message for word in ["wrong", "damaged"]):
        response = "We sincerely apologize for the issue with your order. We will arrange a replacement or refund immediately."

    elif any(word in message for word in ["not receive", "did not receive", "late", "missing"]):
        response = "We apologize for the inconvenience. We will check your order status and resolve this as soon as possible."

    elif any(word in message for word in ["payment", "deducted", "failed"]):
        response = "We sincerely apologize for the payment issue. We will escalate this immediately and resolve it as soon as possible."

    elif any(word in message for word in ["status", "update"]):
        response = "Sure, we will provide you with the latest update on your order status shortly."

    elif customer_type == "premium":
        response = "We sincerely apologize. As a valued premium customer, your issue will be prioritized and resolved immediately."

    else:
        response = "Sorry for the inconvenience. We understand your concern and will resolve it quickly."

    return {
        "intent": intent,
        "priority": priority,
        "response": response
    }


# 🚀 MAIN RUN LOOP
def run():
    env = CustomerSupportEnv()
    obs = env.reset()

    done = False
    total_reward = 0
    step = 1

    print("[START] Running smart agent")

    while not done:
        # 🔥 USE LLM (REQUIRED)
        action = llm_decision(obs["message"], obs["customer_type"])

        obs, reward, done, _ = env.step(action)

        print(f"[STEP] {step} action={action} reward={reward}")

        total_reward += reward
        step += 1

    print(f"[END] Total Reward = {total_reward}")


if __name__ == "__main__":
    run()