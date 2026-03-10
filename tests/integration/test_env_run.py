"""Integration test: full environment run similar to examples/run_env.py."""

import pytest

from sfiii_gym.environment import Environment


@pytest.fixture()
def env():
    """Create a real Environment instance with the actual ROM."""
    environment = Environment(
        "test-env",
        "assets/rom",
        difficulty=6,
        frame_ratio=6,
        render_mode="rgb_array",
    )
    yield environment
    environment.close()


class TestEnvironmentRun:
    """Simulate an episode loop similar to examples/run_env.py."""

    def test_run_episode_loop(self, env) -> None:
        """Run a short episode loop checking the same flow as run_env.py."""
        obs, info = env.reset()

        cumulative_reward = 0.0
        max_steps = 50

        for _ in range(max_steps):
            env.render()
            action = env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)
            cumulative_reward += reward

            assert isinstance(reward, float)
            assert isinstance(info, dict)
            assert "round_done" in info

            if terminated or truncated:
                obs, info = env.reset()
                cumulative_reward = 0.0

    def test_multiple_episodes(self, env) -> None:
        """Run multiple episodes to ensure reset works correctly between them."""
        for episode in range(3):
            obs, info = env.reset()
            assert isinstance(obs, dict)
            assert env.observation_space.contains(obs)

            for step_num in range(10):
                action = env.action_space.sample()
                obs, reward, terminated, truncated, info = env.step(action)
                if terminated or truncated:
                    break

    def test_render_between_steps(self, env) -> None:
        """Verify render can be called repeatedly between steps."""
        env.reset()

        for _ in range(5):
            frame = env.render()
            assert frame.shape == (224, 384, 3)
            action = env.action_space.sample()
            env.step(action)
            frame = env.render()
            assert frame.shape == (224, 384, 3)

    def test_all_action_types_during_run(self, env) -> None:
        """Exercise every action type in the action map during a run."""
        env.reset()

        for action_id in range(env.action_space.n):
            obs, reward, terminated, truncated, info = env.step(action_id)
            assert isinstance(obs, dict)
            if terminated or truncated:
                env.reset()
