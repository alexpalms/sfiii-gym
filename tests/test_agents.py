# tests/test_agents.py
"""Test the agents module."""

from gymnasium.spaces import MultiDiscrete

from project_name.agents import RandomAgent
from project_name.utils import TypedEnvironment


class DummyEnv:
    """Dummy environment."""

    action_space = MultiDiscrete([2, 2])
    render_mode = None


def test_random_agent() -> None:
    """Test the random agent."""
    env = TypedEnvironment(DummyEnv())
    agent = RandomAgent(env)
    action = agent.get_action({})
    assert action[0] in [0, 1] and action[1] in [0, 1]
