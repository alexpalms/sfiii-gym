"""Integration test: full environment run similar to examples/run_env.py."""

import numpy as np
import pytest

from sfiii_gym import Environment


@pytest.fixture()
def env():
    """Create a real Environment instance with the actual ROM."""
    environment = Environment(
        "test-env",
        "rom",
        difficulty=6,
        frame_ratio=6,
        render_mode="rgb_array",
    )
    yield environment
    environment.close()


class TestEnvironmentRun:
    """Simulate an episode loop similar to examples/run_env.py."""

    def test_run_episode_loop(self, env: Environment) -> None:
        """Run a short episode loop checking the same flow as run_env.py."""
        _obs, _info = env.reset()

        cumulative_reward = 0.0
        max_steps = 50

        for _ in range(max_steps):
            env.render()
            action = env.action_space.sample()
            _obs, reward, terminated, truncated, _info = env.step(action)
            cumulative_reward += reward

            assert isinstance(reward, float)
            assert isinstance(_info, dict)
            assert "round_done" in _info

            if terminated or truncated:
                _obs, _info = env.reset()
                cumulative_reward = 0.0

    def test_multiple_episodes(self, env: Environment) -> None:
        """Run multiple episodes to ensure reset works correctly between them."""
        for _episode in range(3):
            obs, _info = env.reset()
            assert isinstance(obs, dict)
            assert env.observation_space.contains(obs)

            for _step_num in range(10):
                action = env.action_space.sample()
                obs, _reward, terminated, truncated, _info = env.step(action)
                if terminated or truncated:
                    break

    def test_render_between_steps(self, env: Environment) -> None:
        """Verify render can be called repeatedly between steps."""
        env.reset()

        for _ in range(5):
            frame = env.render()
            assert frame.shape == (224, 384, 3)
            action = env.action_space.sample()
            env.step(action)
            frame = env.render()
            assert frame.shape == (224, 384, 3)

    def test_all_action_types_during_run(self, env: Environment) -> None:
        """Exercise every action type in the action map during a run."""
        env.reset()

        n_actions = len(env.action_map)
        for action_id in range(n_actions):
            obs, _reward, terminated, truncated, _info = env.step(np.intp(action_id))
            assert isinstance(obs, dict)
            if terminated or truncated:
                env.reset()

    def test_stage_observation(self, env: Environment) -> None:
        """Verify the stage observation is present and starts at 1."""
        obs, _info = env.reset()
        assert "stage" in obs
        assert obs["stage"] == np.uint8(1)

        for _ in range(10):
            action = env.action_space.sample()
            obs, _reward, terminated, truncated, _info = env.step(action)
            assert "stage" in obs
            assert 1 <= int(obs["stage"]) <= 10
            if terminated or truncated:
                break
