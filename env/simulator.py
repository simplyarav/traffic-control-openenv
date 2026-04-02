import random

class TrafficSimulator:
    def __init__(self, seed=42):
        self.random = random.Random(seed)

    def step(self, state, signal):
        queues = state["queues"]

        if signal == "NS_GREEN":
            queues["N"] = max(0, queues["N"] - 2)
            queues["S"] = max(0, queues["S"] - 2)
        else:
            queues["E"] = max(0, queues["E"] - 2)
            queues["W"] = max(0, queues["W"] - 2)

        for d in queues:
            queues[d] += self.random.randint(0, 2)

        if self.random.random() < 0.15:
            state["emergency"] = self.random.choice(["N","S","E","W"])
        else:
            state["emergency"] = None

        state["time"] += 1
        return state