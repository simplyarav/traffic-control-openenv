import random
from env.environment import TrafficEnv
from env.models import Action

env = TrafficEnv(task="easy")
obs = env.reset()

done = False

while not done:
    action = Action(signal=random.choice(["NS_GREEN","EW_GREEN"]))
    obs, reward, done, _ = env.step(action)
    print(obs, reward)