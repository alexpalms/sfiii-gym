#!/usr/bin/env python3
"""Vizdoom run script."""

import argparse
import logging

import gymnasium
from vizdoom import (  # type: ignore[import-untyped]
    gymnasium_wrapper,  # pyright: ignore # noqa: F401
)

from project_name.agents import RandomAgent
from project_name.utils import TypedEnvironment

logging.basicConfig(level=logging.INFO)


def run_vizdoom(
    agent_type: str,
) -> None:
    """Run the Vizdoom environment.

    Parameters
    ----------
        agent_type : str
            The type of agent to use.

    """
    env = TypedEnvironment(
        gymnasium.make(  # pyright: ignore
            "VizdoomHealthGatheringSupreme-v0", render_mode="human", frame_skip=4
        )
    )

    if agent_type == "random":
        agent = RandomAgent(env)
    else:
        raise ValueError(f"Invalid agent type: {agent_type}")

    observation, _ = env.reset()

    while True:
        action = agent.get_action(observation)
        logging.info("Action: %s", action)
        observation, _, terminated, truncated, _ = env.step(action)

        if terminated or truncated:
            observation, _ = env.reset()
            break

    # Close the environment
    env.close()


def main() -> None:
    """Run the CLI."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent-type", type=str, default="random")
    args = parser.parse_args()

    while True:
        logging.info("Running Vizdoom")
        run_vizdoom(args.agent_type)
        continue_answer = input("New episode? (y/[n]): ")
        if continue_answer.lower() != "y":
            break


if __name__ == "__main__":
    main()
