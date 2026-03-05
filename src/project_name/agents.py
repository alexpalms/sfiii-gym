"""Agents module."""

from abc import abstractmethod
from typing import Any

from project_name.utils import TypedEnvironment


class Agent:
    """Agent that selects actions.

    Parameters
    ----------
    env : TypedEnvironment
        The environment to use.

    """

    @abstractmethod
    def __init__(self, env: TypedEnvironment) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_action(self, observation: dict[str, Any]) -> list[int]:
        """Get an action from the agent.

        Parameters
        ----------
        observation : dict[str, Any]
            The observation from the environment.

        Returns
        -------
        list[int]
            The action to execute.

        """
        raise NotImplementedError


class RandomAgent(Agent):
    """Agent that selects random actions.

    Args:
        env: TypedEnvironment
        The environment to use.

    """

    def __init__(self, env: TypedEnvironment):
        self.env = env.gymnasium_env

    def get_action(self, observation: dict[str, Any]) -> list[int]:
        """Get an action from the agent.

        Parameters
        ----------
        observation: dict[str, Any]
            The observation from the environment.

        Returns
        -------
        list[int]
            The action to execute.

        """
        actions: list[int] = self.env.action_space.sample()
        return actions
