from .models import Observation
from .simulator import TrafficSimulator
from .rewards import compute_reward
from .tasks import TASKS

class TrafficEnv:

    def __init__(self, task="easy"):
        self.task = task
        self.config = TASKS[task]
        self.sim = TrafficSimulator(seed=42)
        self.reset()

    def reset(self):
        self.state_data = {
            "queues": self.config["initial"].copy(),
            "signal": "NS_GREEN",
            "emergency": None,
            "time": 0
        }
        self.max_steps = self.config["max_steps"]
        return self._obs()

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