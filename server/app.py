from fastapi import FastAPI
from pydantic import BaseModel
from env.environment import TrafficEnv

app = FastAPI()
env = TrafficEnv()

class ActionModel(BaseModel):
    signal: str

@app.get("/")
def root():
    return {"status": "Traffic Control Env Running"}

@app.post("/reset")
def reset():
    obs = env.reset()
    return obs.dict()

@app.post("/step")
def step(action: ActionModel):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs.dict(),
        "reward": reward,
        "done": done,
        "info": info
    }


@app.get("/state")
def state():
    return env.state()


def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()