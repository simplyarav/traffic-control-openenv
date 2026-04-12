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
        "usage": {
            "reset": "POST /reset?task=easy|medium|hard",
            "step": "POST /step {signal: NS_GREEN | EW_GREEN}",
            "state": "GET /state"
        },
        "metrics": [
            "total_vehicles",
            "avg_waiting_time",
            "traffic_distribution_percent",
            "congestion_level"
        ]
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/metadata")
def metadata():
    return {
        "name": "autonomous-traffic-control",
        "description": "AI agent controls traffic signals at a 4-way intersection to minimize vehicle queues",
        "version": "0.1.0",
        "author": "simplyarav"
    }

@app.get("/schema")
def schema():
    return {
        "action": {
            "type": "object",
            "properties": {
                "signal": {
                    "type": "string",
                    "enum": ["NS_GREEN", "EW_GREEN"],
                    "description": "Traffic signal direction to activate"
                }
            },
            "required": ["signal"]
        },
        "observation": {
            "type": "object",
            "properties": {
                "queues": {"type": "object"},
                "time": {"type": "integer"},
                "task": {"type": "string"},
                "emergency": {"type": "string"}
            }
        },
        "state": {
            "type": "object",
            "properties": {
                "queues": {"type": "object"},
                "time": {"type": "integer"},
                "task": {"type": "string"},
                "emergency": {"type": "string"}
            }
        }
    }

@app.post("/mcp")
def mcp(request: dict = None):
    return {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {
            "name": "autonomous-traffic-control",
            "version": "0.1.0"
        }
    }
@app.get("/tasks")
def list_tasks():
    return {
        "tasks": [
            {
                "name": "easy",
                "description": "Low traffic scenario",
                "grader": "score",
                "pass_threshold": 0.3,
                "graders": [{"type": "score", "pass_threshold": 0.3}]
            },
            {
                "name": "medium",
                "description": "Medium traffic scenario",
                "grader": "score",
                "pass_threshold": 0.5,
                "graders": [{"type": "score", "pass_threshold": 0.5}]
            },
            {
                "name": "hard",
                "description": "Heavy traffic scenario",
                "grader": "score",
                "pass_threshold": 0.7,
                "graders": [{"type": "score", "pass_threshold": 0.7}]
            }
        ]
    }

@app.post("/reset", tags=["Environment"], summary="Reset environment")
def reset(task: str = "easy", action: ActionModel = None):
    global env
    env = TrafficEnv(task=task)
    return env.reset()

@app.post("/step", tags=["Environment"], summary="Take one action step")
def step(action: ActionModel):
    if action.signal not in ["NS_GREEN", "EW_GREEN"]:
        return {
            "error": "Invalid signal",
            "valid_signals": ["NS_GREEN", "EW_GREEN"]
        }

    obs, reward, done, info = env.step(action)
    metrics = compute_metrics(env.state())

    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "metrics": metrics
    }

@app.get("/state", tags=["Environment"], summary="Get current state")
def state():
    state_data = env.state()
    metrics = compute_metrics(state_data)

    return {
        "state": state_data,
        "metrics": metrics
    }

@app.post("/grader")
def grader(task: str = "easy"):
    state_data = env.state()
    queues = state_data.get("queues", {})
    avg_queue = sum(queues.values()) / len(queues) if queues else 0
    score = max(0.0, min(1.0, 1 - (avg_queue / 25)))

    thresholds = {"easy": 0.3, "medium": 0.5, "hard": 0.7}
    passed = score >= thresholds.get(task, 0.3)

    return {
        "task": task,
        "score": score,
        "passed": passed,
        "grader_type": "score",
        "pass_threshold": thresholds.get(task, 0.3)
    }

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()