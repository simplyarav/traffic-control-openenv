def compute_reward(state, action):
    queues = state["queues"]

    total = sum(queues.values())
    reward = -total * 0.02

    emergency = state.get("emergency")
    if emergency:
        if emergency in ["N","S"] and action.signal == "NS_GREEN":
            reward += 0.5
        elif emergency in ["E","W"] and action.signal == "EW_GREEN":
            reward += 0.5
        else:
            reward -= 0.3

    if max(queues.values()) > 15:
        reward -= 1.0

    return reward