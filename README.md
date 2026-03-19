<p align="center">
    <img src="https://raw.githubusercontent.com/alexpalms/sfiii-gym/main/img/sfiii3n.jpg" alt="SFIII Gym" width="30%"/>
</p>

<p align="center">
<a href="https://github.com/alexpalms/sfiii-gym/tags"><img src="https://img.shields.io/github/v/tag/alexpalms/sfiii-gym?label=latest%20tag&logo=github" alt="Latest Tag"/></a>
<a href="https://pypi.org/project/sfiii-gym/"><img src="https://img.shields.io/pypi/v/sfiii-gym?logo=pypi" alt="Pypi version"/></a>
</p>

<p align="center">
<a href="https://github.com/alexpalms/sfiii-gym/actions/workflows/code-checks.yaml"><img src="https://img.shields.io/github/actions/workflow/status/alexpalms/sfiii-gym/code-checks.yaml?label=code%20checks%20(ruff%20%26%20pyright)&logo=github" alt="Code Checks"/></a>
<a href="https://github.com/alexpalms/sfiii-gym/actions/workflows/pytest.yaml"><img src="https://img.shields.io/github/actions/workflow/status/alexpalms/sfiii-gym/pytest.yaml?label=tests%20(pytest)&logo=github" alt="Pytest"/></a>
</p>

<p align="center">
<img src="https://img.shields.io/badge/supported%20os-linux-blue" alt="Supported OS"/>
<img src="https://img.shields.io/badge/python-%3E%3D3.12-blue?logo=python" alt="Python Version"/>
<img src="https://img.shields.io/github/last-commit/alexpalms/sfiii-gym/main?label=repo%20latest%20update&logo=readthedocs" alt="Latest Repo Update"/>
</p>
<p align="center">
<img src="https://img.shields.io/github/license/alexpalms/sfiii-gym?cacheBust=1" alt="License"/>
</p>

# SFIII Gym

A [Gymnasium](https://gymnasium.farama.org/) environment for **Street Fighter III: 3rd Strike** using the [MAME](https://www.mamedev.org/) emulator. Train reinforcement learning agents to play one of the most iconic fighting games ever made.

<p align="center">
    <img src="https://raw.githubusercontent.com/alexpalms/sfiii-gym/main/img/sfiii-gym.gif" alt="SFIII Gym" width="100%"/>
</p>

## Features

- **Gymnasium-compatible** — standard `reset()` / `step()` / `render()` API
- **Rich observations** — game frame (224×384 RGB), player healths, sides, opponent character, and current stage
- **15 discrete actions** — movement (8 directions + idle) and attacks (6 punch/kick buttons)
- **Configurable difficulty** — 8 difficulty levels (1–8)
- **Render modes** — `"human"` for live playback, `"rgb_array"` for headless training

## Prerequisites

- **Python ≥ 3.12**
- **Linux** (MAME emulator requirement)
- **Street Fighter III: 3rd Strike ROM** (`sfiii3n.zip`) — you must legally obtain this ROM and place it in a local directory (e.g. `./rom/`)

## Installation

```bash
pip install sfiii-gym
```

Or with [uv](https://github.com/astral-sh/uv):

```bash
uv add sfiii-gym
```

For development:

```bash
git clone https://github.com/alexpalms/sfiii-gym.git
cd sfiii-gym
uv sync
```

## Getting Started

```python
from sfiii_gym import Environment

# Create the environment
env = Environment("env1", "./rom", render_mode="human", throttle=False)
obs, info = env.reset()

cumulative_reward = 0
while True:
    env.render()
    action = env.action_space.sample()  # Replace with your agent's action
    obs, reward, terminated, truncated, info = env.step(action)
    cumulative_reward += reward

    if terminated or truncated:
        print(f"Episode finished — Cumulative Reward: {cumulative_reward}")
        obs, info = env.reset()
        cumulative_reward = 0
```

### Observation Space

| Key            | Space                              | Description               |
|----------------|------------------------------------|---------------------------|
| `frame`        | `Box(0, 255, (224, 384, 3), uint8)` | Raw game screen (RGB)   |
| `healthP1`     | `Box(-1, 160, int16)`             | Player 1 health           |
| `healthP2`     | `Box(-1, 160, int16)`             | Player 2 (opponent) health|
| `sideP1`       | `MultiBinary(1)`                   | Player 1 side             |
| `sideP2`       | `MultiBinary(1)`                   | Player 2 side             |
| `characterP2`  | `Discrete(20)`                     | Opponent character ID     |
| `stage`        | `Box(1, 10, uint8)`                | Current stage (1–10)      |

### Action Space

`Discrete(15)` — 0: no-op, 1–8: movement directions, 9–14: attacks (jab, strong, fierce, short, forward, roundhouse).

## Configuration

| Parameter      | Type   | Default       | Description                           |
|----------------|--------|---------------|---------------------------------------|
| `env_id`       | `str`  | —             | Unique environment identifier         |
| `roms_path`    | `str`  | —             | Path to directory containing the ROM  |
| `difficulty`   | `int`  | `6`           | CPU difficulty level (1–8)            |
| `frame_ratio`  | `int`  | `6`           | Frames per step (higher = faster)     |
| `render_mode`  | `str`  | `"rgb_array"` | `"human"` or `"rgb_array"`            |
| `throttle`     | `bool` | `False`       | Throttle to real-time speed           |

## Repository Structure

```
sfiii-gym/
├── src/sfiii_gym/          # Main package
│   ├── __init__.py         # Package exports
│   ├── environment.py      # Gymnasium environment implementation
│   ├── actions.py          # Action definitions and mappings
│   ├── steps.py            # Step/observation processing logic
│   └── py.typed            # PEP 561 typing marker
├── tests/
│   ├── unit/               # Unit tests (actions, steps)
│   └── integration/        # Integration tests (env run, Gym API compliance)
├── stubs/MAMEToolkit/      # Type stubs for the MAME emulator toolkit
├── examples/
│   └── run_env.py          # Example script to run the environment
├── rom/                    # ROM directory (not distributed)
└── pyproject.toml          # Project metadata and dependencies
```

## License

This project is licensed under the [MIT License](LICENSE).
