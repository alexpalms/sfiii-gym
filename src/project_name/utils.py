"""Utils module."""

from typing import Any


class TypedEnvironment:
    """Environment that selects actions.

    Parameters
    ----------
    env : Any
        The environment to use.

    """

    def __init__(self, env: Any):
        self.gymnasium_env = env

    def reset(self) -> tuple[dict[str, Any], dict[str, Any]]:
        """Reset the environment.

        Returns
        -------
        observation : dict[str, Any]
            The observation.
        info : dict[str, Any]
            The info.

        """
        observation, info = self.gymnasium_env.reset()
        return observation, info

    def step(
        self, action: list[int]
    ) -> tuple[dict[str, Any], float, bool, bool, dict[str, Any]]:
        """Step the environment.

        Parameters
        ----------
        action : list[int]
            action: The action to execute.

        Returns
        -------
        observation : dict[str, Any]
            The observation.
        reward : float
            The reward.
        terminated : bool
            Whether the episode has terminated.
        truncated : bool
            Whether the episode has truncated.
        info : dict[str, Any]
            The info.

        """
        observation, reward, terminated, truncated, info = self.gymnasium_env.step(
            action
        )
        return observation, reward, terminated, truncated, info

    def render(self) -> Any:
        """Render the environment."""
        return self.gymnasium_env.render()

    def close(self) -> None:
        """Close the environment."""
        self.gymnasium_env.close()
