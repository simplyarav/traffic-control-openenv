from .models import Observation
from .simulator import TrafficSimulator
from .rewards import compute_reward
from .tasks import TASKS

class TrafficEnv:
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

    def step(self, action):
        self.state_data["signal"] = action.signal
        self.state_data = self.sim.step(self.state_data, action.signal)

        reward = compute_reward(self.state_data, action)
        done = self.state_data["time"] >= self.max_steps

        return self._obs(), reward, done, {}

    def state(self):
        return self.state_data

    def _obs(self):
        return Observation(
            queues=self.state_data["queues"],
            emergency=self.state_data["emergency"],
            time=self.state_data["time"]
        )