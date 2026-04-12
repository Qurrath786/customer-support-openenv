from typing import Dict


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
            },
            {
                "message": "My payment failed but money was deducted",
                "customer_type": "regular",
                "correct_intent": "escalate",
                "priority": "high",
                "emotion": "neutral"
            },
            {
                "message": "Can you update me on my order status?",
                "customer_type": "regular",
                "correct_intent": "inform",
                "priority": "low",
                "emotion": "polite"
            },
            {
                "message": "I have complained before and nothing was done!",
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

    # ⚡ Step function (GRADER LOGIC)
    def step(self, action: Dict):
        item = self.data[self.current_step]

        raw_reward = 0.0

        # ✅ Intent check
        if action.get("intent") == item["correct_intent"]:
            raw_reward += 0.9
        else:
            raw_reward -= 0.8

        # ✅ Priority check
        if action.get("priority") == item["priority"]:
            raw_reward += 0.5
        else:
            raw_reward -= 0.4

        # ✅ Response tone
        response = action.get("response", "").lower()
        if any(word in response for word in ["sorry", "apologize", "understand"]):
            raw_reward += 0.5
        else:
            raw_reward -= 0.4

        # 🔥 Emotion-aware handling
        if item["emotion"] == "angry":
            if any(word in response for word in ["sorry", "apologize"]):
                raw_reward += 0.5
            else:
                raw_reward -= 0.4

        # ❗ Premium customer handling
        if item["customer_type"] == "premium":
            if action.get("priority") == "high":
                raw_reward += 0.5
            else:
                raw_reward -= 0.4

        # 🔥 NORMALIZATION (SAFE)
        normalized = (raw_reward + 3) / 6

        # 🚨 STRICT CLAMP (NO EDGE VALUES)
        if normalized >= 0.95:
            normalized = 0.94
        elif normalized <= 0.05:
            normalized = 0.06

        # Ensure float
        normalized = float(normalized)

        # Move to next step
        self.current_step += 1
        done = self.current_step >= len(self.data)

        # 🚨 Avoid None observation
        if done:
            next_obs = {
                "message": "completed",
                "customer_type": "none"
            }
        else:
            next_obs = self._get_observation()

        return next_obs, normalized, done, {}

    # 📊 State info
    def state(self):
        return {
            "current_step": self.current_step,
            "total_steps": len(self.data)
        }