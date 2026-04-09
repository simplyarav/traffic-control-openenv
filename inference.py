import requests
import os

API_BASE_URL = os.getenv("API_BASE_URL", "https://simplyarav-traffic-control-env.hf.space")
MODEL_NAME = os.getenv("MODEL_NAME", "traffic-baseline")
TASK = "traffic-control"
ENV_NAME = "openenv"

MAX_STEPS = 5

print(f"[START] task={TASK} env={ENV_NAME} model={MODEL_NAME}", flush=True)

res = requests.post(f"{API_BASE_URL}/reset")
state = res.json()

rewards = []
success = False

for step in range(1, MAX_STEPS + 1):
    action = {"signal": "NS_GREEN" if step % 2 == 0 else "EW_GREEN"}

    r = requests.post(f"{API_BASE_URL}/step", json=action)
    data = r.json()

    reward = float(data.get("reward", 0))
    done = bool(data.get("done", False))

    rewards.append(reward)

    print(
        f"[STEP] step={step} action={action['signal']} reward={reward:.2f} done={str(done).lower()} error=null",
        flush=True
    )

    if done:
        success = True
        break

score = max(0.0, min(1.0, sum(rewards) / len(rewards))) if rewards else 0.0

reward_str = ",".join(f"{r:.2f}" for r in rewards)

print(
    f"[END] success={str(success).lower()} steps={len(rewards)} score={score:.2f} rewards={reward_str}",
    flush=True
)