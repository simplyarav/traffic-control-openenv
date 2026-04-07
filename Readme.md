Autonomous Traffic Control using OpenEnv

Why I built this?

Traffic congestion at intersections is a common real-world problem. This project simulates a traffic light controller that an AI agent can learn to optimize. The goal was to create a realistic environment where reinforcement learning agents can practice managing traffic efficiently.

What problem it solves?

This environment models a 4-way intersection and allows an AI to:
1) Reduce waiting vehicles
2) Handle emergency traffic
3) Balance traffic flow
4) Avoid congestion buildup

It provides a structured benchmark for evaluating decision-making agents in traffic control scenarios.

How it works?

The environment exposes REST APIs:
- POST /reset : resets simulation
- POST /step : applies signal action
- GET /state : returns current traffic state

How to test?

1: Open /docs endpoint
2: Call /reset
3: Call /step with signal
4: Observe reward and queue changes

Actions:

* NS_GREEN : North/South traffic moves
* EW_GREEN : East/West traffic moves

Expected Output

Example reset response:
{
  "queues": {"N":2,"S":2,"E":2,"W":2},
  "emergency": null,
  "time": 0
}

Example step response:
{
  "observation": {...},
  "reward": -0.12,
  "done": false
}

Demo

Live environment:
https://simplyarav-traffic-control-env.hf.space

Technologies Used

Python, FastAPI, Docker, OpenEnv, Hugging Face Spaces
