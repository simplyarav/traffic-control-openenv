# Autonomous Traffic Control OpenEnv

## Overview
This project implements an OpenEnv-compatible reinforcement learning environment for autonomous traffic signal control at a four-way intersection.

The goal is to minimize queue length, reduce wait time, and prioritize emergency vehicles.

## Observation Space
{
  queues: {N, S, E, W},
  emergency: null | direction,
  time: int
}

## Action Space
{
  signal: "NS_GREEN" | "EW_GREEN"
}

## Tasks
1. easy — low traffic
2. medium — moderate traffic
3. hard — high traffic with emergencies

## Reward
- negative total queue length
- bonus for clearing emergency vehicle
- penalty for long waiting queues

## API Endpoints
POST /reset
POST /step
GET /state

## Deployment
HuggingFace Space:
https://simplyarav-traffic-control-env.hf.space

## Baseline
Random policy baseline implemented in inference.py

## Docker
Environment runs via Docker container on HuggingFace Spaces.

## Author
Kaushtubh Pandey