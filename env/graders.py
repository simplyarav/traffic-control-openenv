def grade(env_state: dict) -> float:
    queues = env_state.get("queues", {})
    avg_queue = sum(queues.values()) / len(queues) if queues else 0
    score = 1 - (avg_queue / 25)
    return max(0.0, min(1.0, score))