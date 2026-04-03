from fastapi import FastAPI
from env.environment import CustomerSupportEnv

def main():
    app = FastAPI()
    env = CustomerSupportEnv()

    @app.get("/")
    def root():
        return {"message": "Customer Support Env Running"}

    @app.post("/reset")
    def reset():
        return {"observation": env.reset()}

    @app.post("/step")
    def step(action: dict):
        obs, reward, done, _ = env.step(action)
        return {"observation": obs, "reward": reward, "done": done}

    @app.get("/state")
    def state():
        return env.state()

    return app


# for uvicorn
app = main()

# 🔥 THIS FIXES YOUR FINAL ERROR
if __name__ == "__main__":
    main()