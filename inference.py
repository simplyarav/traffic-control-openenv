import json
import os
import urllib.request

API_BASE_URL = os.getenv("API_BASE_URL", "https://simplyarav-traffic-control-env.hf.space")
MODEL_NAME = os.getenv("MODEL_NAME", "traffic-baseline")
TASK = "traffic-control"
ENV_NAME = "openenv"

MAX_STEPS = 5


def post(url, data=None):
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8") if data else None,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req) as f:
        return json.loads(f.read().decode())


print(f"[START] task={TASK} env={ENV_NAME} model={MODEL_NAME}", flush=True)

state = post(f"{API_BASE_URL}/reset")

rewards = []
success = False

for step in range(1, MAX_STEPS + 1):
    action = {"signal": "NS_GREEN" if step % 2 == 0 else "EW_GREEN"}

    data = post(f"{API_BASE_URL}/step", action)

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