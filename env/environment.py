from typing import Dict, List


class CustomerSupportEnv:
    def __init__(self):
        self.data = []
        self.current_step = 0

    # 🔁 Reset environment
    def reset(self) -> Dict:
        self.data = [
            {
                "message": "I didn't receive my order",
                "customer_type": "regular",
                "correct_intent": "refund",
                "priority": "medium",
                "emotion": "neutral"
            },
            {
                "message": "This is so frustrating! My order is late!",
                "customer_type": "regular",
                "correct_intent": "refund",
                "priority": "high",
                "emotion": "angry"
            },
            {
                "message": "I am a premium customer and this is my second complaint!",
                "customer_type": "premium",
                "correct_intent": "escalate",
                "priority": "high",
                "emotion": "angry"
            }
        ]

        self.current_step = 0
        return self._get_observation()

    # 👀 Get current observation
    def _get_observation(self):
        item = self.data[self.current_step]
        return {
            "message": item["message"],
            "customer_type": item["customer_type"]
        }

    # ⚡ Step function
    def step(self, action: Dict):
        item = self.data[self.current_step]

        reward = 0.0

        # ✅ Intent check
        if action.get("intent") == item["correct_intent"]:
            reward += 0.5
        else:
            reward -= 1.0

        # ✅ Priority check
        if action.get("priority") == item["priority"]:
            reward += 0.3
        else:
            reward -= 0.2

        # ✅ Response tone check (simple)
        response = action.get("response", "").lower()

        if any(word in response for word in ["sorry", "apologize", "understand"]):
            reward += 0.2
        else:
            reward -= 0.2

        # ❗ Premium user penalty
        if item["customer_type"] == "premium" and action.get("priority") != "high":
            reward -= 0.5

        # Move step
        self.current_step += 1
        done = self.current_step >= len(self.data)

        next_obs = None if done else self._get_observation()

        return next_obs, round(reward, 2), done, {}

    # 📊 State info
    def state(self):
        return {
            "current_step": self.current_step,
            "total_steps": len(self.data)
        }