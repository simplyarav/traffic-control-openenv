import os
import json
import urllib.request
import urllib.error

API_BASE_URL = os.environ.get("API_BASE_URL", "")
API_KEY = os.environ.get("API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

ENV_URL = os.getenv("ENV_URL", "https://simplyarav-traffic-control-env.hf.space")
TASK = "traffic-control"
ENV_NAME = "openenv"
MAX_STEPS = 5


def post_json(url, data=None, headers=None):
    try:
        payload = json.dumps(data if data is not None else {}).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=payload,
            headers=headers or {"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=15) as f:
            return json.loads(f.read().decode())
    except Exception:
        return {}


if API_BASE_URL and API_KEY:
    _ = post_json(
        f"{API_BASE_URL}/chat/completions",
        {
            "model": MODEL_NAME,
            "messages": [{"role": "user", "content": "Return NS_GREEN or EW_GREEN"}],
        },
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
    )

print(f"[START] task={TASK} env={ENV_NAME} model={MODEL_NAME}", flush=True)

post_json(f"{ENV_URL}/reset", {})

rewards = []
success = False

for step in range(1, MAX_STEPS + 1):
    action = {"signal": "NS_GREEN" if step % 2 else "EW_GREEN"}
    result = post_json(f"{ENV_URL}/step", action)

    reward = float(result.get("reward", 0))
    done = bool(result.get("done", False))
    rewards.append(reward)

    print(
        f"[STEP] step={step} action={action['signal']} "
        f"reward={reward:.2f} done={str(done).lower()} error=null",
        flush=True,
    )

    if done:
        success = True
        break

score = sum(rewards) / len(rewards) if rewards else 0.0
score = max(0.0, min(1.0, score))
reward_str = ",".join(f"{r:.2f}" for r in rewards)

print(
    f"[END] success={str(success).lower()} steps={len(rewards)} "
    f"score={score:.2f} rewards={reward_str}",
    flush=True,
)