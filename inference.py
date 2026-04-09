import requests
import time
import os

API_BASE_URL = os.getenv("API_BASE_URL", "https://simplyarav-traffic-control-env.hf.space")

TASKS = ["easy", "medium", "hard"]

for task in TASKS:

    print(f"[START] task={task}", flush=True)

    res = requests.post(f"{API_BASE_URL}/reset", params={"task": task})
    state = res.json()

    total_reward = 0
    steps = 5

    for step in range(steps):
        action = {"signal": "NS_GREEN" if step % 2 == 0 else "EW_GREEN"}

        r = requests.post(f"{API_BASE_URL}/step", json=action)
        data = r.json()

        reward = data.get("reward", 0)
        total_reward += reward

        print(f"[STEP] task={task} step={step} reward={reward}", flush=True)

        time.sleep(0.2)

    score = max(0, min(1, total_reward / steps))

    print(f"[END] task={task} score={score} steps={steps}", flush=True)