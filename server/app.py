from fastapi import FastAPI
from pydantic import BaseModel
from env.environment import TrafficEnv

app = FastAPI()
env = TrafficEnv()

class ActionModel(BaseModel):
    signal: str

def compute_metrics(state):
    queues = state["queues"]
    total = sum(queues.values())

    if total == 0:
        total = 1

    percentages = {
        d: round((queues[d] / total) * 100, 2)
        for d in queues
    }

    avg_wait = round(total / 4, 2)

    congestion = "LOW"
    if total > 12:
        congestion = "MEDIUM"
    if total > 20:
        congestion = "HIGH"

    return {
        "total_vehicles": total,
        "avg_waiting_time": avg_wait,
        "traffic_distribution_percent": percentages,
        "congestion_level": congestion
    }    

@app.get("/")
def root():
    return {
        "project": "Autonomous Traffic Control OpenEnv",
        "description": "AI-driven traffic signal control simulation",
        "endpoints": {
            "reset": "POST /reset",
            "step": "POST /step {signal: NS_GREEN | EW_GREEN}",
            "state": "GET /state"
        }
    }

@app.post("/reset", tags=["Environment"], summary="Reset environment")
def reset():
    obs = env.reset()
    return obs.dict()

@app.post("/step", tags=["Environment"], summary="Take one action step")
def step(action: ActionModel):
    obs, reward, done, info = env.step(action)

    metrics = compute_metrics(env.state())

    return {
        "observation": obs.dict(),
        "reward": reward,
        "done": done,
        "metrics": metrics
    }


@app.get("/state", tags=["Environment"], summary="Get current state")
def state():
    return env.state()


def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()