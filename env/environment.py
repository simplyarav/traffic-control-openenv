class TrafficEnv:
    TASKS = ["easy", "medium", "hard"]

    def __init__(self, task="easy"):
        self.task = task
        self.reset()

    def reset(self):
        if self.task == "easy":
            self.queues = {"N": 2, "S": 2, "E": 2, "W": 2}
        elif self.task == "medium":
            self.queues = {"N": 5, "S": 5, "E": 3, "W": 3}
        elif self.task == "hard":
            self.queues = {"N": 8, "S": 8, "E": 6, "W": 6}

        self.time = 0
        self.emergency = None

        return self.state()

    def state(self):
        return {
            "queues": self.queues,
            "time": self.time,
            "task": self.task,
            "emergency": self.emergency
        }

    def step(self, action):
        signal = action.signal

        if signal == "NS_GREEN":
            self.queues["N"] = max(0, self.queues["N"] - 1)
            self.queues["S"] = max(0, self.queues["S"] - 1)
        else:
            self.queues["E"] = max(0, self.queues["E"] - 1)
            self.queues["W"] = max(0, self.queues["W"] - 1)

        self.time += 1

        total_wait = sum(self.queues.values())
        max_wait = 40

        score = 1.0 - (total_wait / max_wait)
        score = max(0.01, min(0.99, score))

        done = self.time >= 20

        return self.state(), score, done, {}