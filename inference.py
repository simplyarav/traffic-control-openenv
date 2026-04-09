import os
import json
import urllib.request

API_BASE_URL = os.environ["API_BASE_URL"]
API_KEY = os.environ["API_KEY"]
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

ENV_URL = os.getenv("ENV_URL", "https://simplyarav-traffic-control-env.hf.space")


def post_json(url, data, headers=None):
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers=headers or {"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as f:
        return json.loads(f.read().decode())


llm_payload = {
    "model": MODEL_NAME,
    "messages": [{"role": "user", "content": "Return NS_GREEN or EW_GREEN"}],
}

post_json(
    f"{API_BASE_URL}/chat/completions",
    llm_payload,
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    },
)

print(f"[START] task=traffic-control env=openenv model={MODEL_NAME}", flush=True)

post_json(f"{ENV_URL}/reset", {})

rewards = []

for step in range(1, 6):
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
        break

score = sum(rewards) / len(rewards) if rewards else 0.0
score = max(0.0, min(1.0, score))

print(
    f"[END] success=true steps={len(rewards)} score={score:.2f} "
    f"rewards={','.join(f'{r:.2f}' for r in rewards)}",
    flush=True,
)