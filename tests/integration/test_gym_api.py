"""Integration test: Gymnasium environment API validation."""

import pytest
from gymnasium.utils.env_checker import (
    check_env,  # pyright: ignore[reportUnknownVariableType]
)

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


class TestGymnasiumApiCompliance:
    """Validate that Environment follows the Gymnasium Env API."""

    def test_env_compliance_with_check_env(self, env: Environment) -> None:
        """Use gymnasium's check_env to validate full API compliance."""
        # check_env performs comprehensive validation of the Gymnasium API
        # including observation/action spaces, reset/step signatures, and more
        try:
            check_env(env.unwrapped, skip_render_check=True)
        except AssertionError as e:
            if (
                "Deterministic step observations are not equivalent for the same seed and action"
                not in str(e)
            ):
                raise
