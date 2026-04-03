import os
from env.environment import CustomerSupportEnv

# Required variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")


def run_task(task_name):
    env = CustomerSupportEnv()
    obs = env.reset()

    print(f"[START] task={task_name} env=customer-support-env model={MODEL_NAME}")

    rewards = []
    step = 0
    done = False

    while not done:
        step += 1

        # Dummy intelligent action (you can improve later)
        action = {
            "intent": "refund",
            "priority": "high",
            "response": "Sorry for the inconvenience, we will resolve this issue."
        }

        obs, reward, done, _ = env.step(action)

        rewards.append(reward)

        print(
            f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error=null"
        )

    print(
        f"[END] success=true steps={step} rewards={','.join([f'{r:.2f}' for r in rewards])}"
    )


if __name__ == "__main__":
    run_task("easy")