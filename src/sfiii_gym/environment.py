import hashlib
import logging
from pathlib import Path
from typing import Any

import numpy as np
from gymnasium import Env, spaces
from MAMEToolkit.emulator import Address, Emulator

from sfiii_gym.actions import Actions
from sfiii_gym.steps import new_game, next_stage, set_difficulty, start_game

logger = logging.getLogger(__name__)

_ROM_FILENAME = "sfiii3n.zip"
_ROM_SHA256 = "7239b5eb005488db22ace477501c574e9420c0ab70aeeb0795dfeb474284d416"


# Combines the data of multiple time steps
def add_rewards(old_data, new_data):
    for k in old_data.keys():
        if "rewards" in k:
            for player in old_data[k]:
                new_data[k][player] += old_data[k][player]
    return new_data


# The Street Fighter specific interface for training an agent against the game
class Environment(Env[dict[str, np.ndarray], np.integer]):
    # env_id - the unique identifier of the emulator environment, used to create fifo pipes
    # difficulty - the difficult to be used in story mode gameplay
    # frame_ratio - see Emulator class
    # render, throttle - see Console class
    def __init__(
        self,
        env_id: str,
        roms_path: str,
        difficulty: int = 6,
        frame_ratio: int = 6,
        render: bool = True,
        throttle: bool = False,
    ):

        rom_path = Path(roms_path) / _ROM_FILENAME
        if not rom_path.is_file():
            msg = (
                f"ROM '{_ROM_FILENAME}' not found in '{roms_path}'.\n"
                f"It can be downloaded from: https://wowroms.com/en/roms/mame/download-street-fighter-iii-3rd-strike-fight-for-the-futur-japan-clone/106255.html\n"
                f"DISCLAIMER: Each user is responsible for ensuring they have the legal right to obtain and use this ROM."
            )
            logger.error(msg)
            raise FileNotFoundError(msg)

        actual_sha256 = hashlib.sha256(rom_path.read_bytes()).hexdigest()
        if actual_sha256 != _ROM_SHA256:
            msg = (
                f"ROM '{_ROM_FILENAME}' failed SHA256 checksum verification.\n"
                f"Expected: {_ROM_SHA256}\n"
                f"Got:      {actual_sha256}"
            )
            logger.error(msg)
            raise ValueError(msg)

        self.difficulty = difficulty
        self.frame_ratio = frame_ratio
        self.throttle = throttle

        self.memory_addresses = {
            "fighting": Address("0x02011389", "u8"),
            "winsP1": Address("0x02011383", "u8"),
            "winsP2": Address("0x02011385", "u8"),
            "healthP1": Address("0x02068D0A", "s16"),
            "healthP2": Address("0x020691A2", "s16"),
            "sideP1": Address("0x02016B8E", "u8"),
            "sideP2": Address("0x02068C76", "u8"),
            "characterP1": Address("0x02011387", "u8"),
            "characterP2": Address("0x02011388", "u8"),
        }

        self.emu = Emulator(
            env_id,
            roms_path,
            "sfiii3n",
            self.memory_addresses,
            frame_ratio=frame_ratio,
            render=render,
            throttle=throttle,
            frame_skip=0,
            sound=False,
            debug=False,
            binary_path=None,
        )

        self.action_map = {
            0: [],
            1: [Actions.P1_LEFT],
            2: [Actions.P1_LEFT, Actions.P1_UP],
            3: [Actions.P1_UP],
            4: [Actions.P1_UP, Actions.P1_RIGHT],
            5: [Actions.P1_RIGHT],
            6: [Actions.P1_RIGHT, Actions.P1_DOWN],
            7: [Actions.P1_DOWN],
            8: [Actions.P1_DOWN, Actions.P1_LEFT],
            9: [Actions.P1_JPUNCH],
            10: [Actions.P1_SPUNCH],
            11: [Actions.P1_FPUNCH],
            12: [Actions.P1_SKICK],
            13: [Actions.P1_FKICK],
            14: [Actions.P1_RKICK],
            15: [Actions.P1_SPUNCH, Actions.P1_FKICK],
            16: [Actions.P1_JPUNCH, Actions.P1_SKICK],
            17: [Actions.P1_FPUNCH, Actions.P1_RKICK],
        }

        self.observation_space = spaces.Dict(
            {"frame": spaces.Box(low=0, high=255, shape=(224, 384, 3), dtype=np.uint8)}
        )

        self.action_space = spaces.Discrete(len(self.action_map))

    # Runs a set of action steps over a series of time steps
    # Used for transitioning the emulator through non-learnable gameplay, aka. title screens, character selects
    def _run_steps(self, steps: list[dict[str, int | list[Actions]]]):
        for step in steps:
            for _ in range(step["wait"]):
                self.emu.step([])
            self.emu.step([action.value for action in step["actions"]])

    # Must be called first after creating this class
    # Sends actions to the game until the learnable gameplay starts
    # Returns the first few frames of gameplay
    def _start(self):
        if self.throttle:
            for _ in range(int(250 / self.frame_ratio)):
                self.emu.step([])
        self._run_steps(set_difficulty(self.frame_ratio, self.difficulty))
        self._run_steps(start_game(self.frame_ratio))
        frames = self._wait_for_fight_start()
        self.started = True
        return frames

    # Observes the game and waits for the fight to start
    def _wait_for_fight_start(self):
        data = self.emu.step([])
        while data["fighting"] == 0:
            data = self.emu.step([])
        self.expected_health = {"P1": data["healthP1"], "P2": data["healthP2"]}
        data = self._sub_step([])
        return data["frame"]

    # To be called when a round finishes
    # Performs the necessary steps to take the agent to the next round of gameplay
    def _next_round(self):
        self.round_done = False
        self.expected_health = {"P1": 0, "P2": 0}
        return self._wait_for_fight_start()

    # To be called when a game finishes
    # Performs the necessary steps to take the agent(s) to the next game and resets the necessary book keeping variables
    def _next_stage(self):
        self._wait_for_continue()
        self._run_steps(next_stage(self.frame_ratio))
        self.expected_health = {"P1": 0, "P2": 0}
        self.expected_wins = {"P1": 0, "P2": 0}
        self.round_done = False
        self.stage_done = False
        return self.wait_for_fight_start()

    def _new_game(self):
        self._wait_for_continue()
        self._run_steps(new_game(self.frame_ratio))
        self.expected_health = {"P1": 0, "P2": 0}
        self.expected_wins = {"P1": 0, "P2": 0}
        self.round_done = False
        self.stage_done = False
        self.game_done = False
        self.stage = 1
        return self._wait_for_fight_start()

    # Steps the emulator along until the screen goes black at the very end of a game
    def _wait_for_continue(self):
        data = self.emu.step([])
        while data["frame"].sum() != 0:
            data = self.emu.step([])

    # Steps the emulator along until the round is definitely over
    def _run_till_victor(self, data):
        while (
            self.expected_wins["P1"] == data["winsP1"]
            and self.expected_wins["P2"] == data["winsP2"]
        ):
            data = add_rewards(data, self.sub_step([]))
        self.expected_wins = {"P1": data["winsP1"], "P2": data["winsP2"]}
        return data

    # Checks whether the round or game has finished
    def _check_done(self, data):
        if data["fighting"] == 0:
            data = self.run_till_victor(data)
            self.round_done = True
            if data["winsP1"] == 2:
                self.stage_done = True
                self.stage += 1
            if data["winsP2"] == 2:
                self.game_done = True
        return data

    # Steps the emulator along by one time step and feeds in any actions that require pressing
    # Takes the data returned from the step and updates book keeping variables
    def _sub_step(self, actions):
        data = self.emu.step([action.value for action in actions])

        p1_diff = self.expected_health["P1"] - data["healthP1"]
        p2_diff = self.expected_health["P2"] - data["healthP2"]
        self.expected_health = {"P1": data["healthP1"], "P2": data["healthP2"]}

        data["reward"] = p2_diff - p1_diff
        return data

    def reset(self, *, seed: int | None = None, options: dict | None = None) -> tuple[
        dict[str, np.ndarray], dict[str, Any]
    ]:
        self.started = False
        self.expected_health = {"P1": 0, "P2": 0}
        self.expected_wins = {"P1": 0, "P2": 0}
        self.round_done = False
        self.stage_done = False
        self.game_done = False
        self.stage = 1

    # Steps the emulator along by the requested amount of frames required for the agent to provide actions
    def step(
        self, action: np.integer
    ) -> tuple[dict[str, np.ndarray], float, bool, bool, dict[str, Any]]:
        data = self._sub_step(self.action_map[action])
        data = self._check_done(data)
        terminated = False
        truncated = False
        info = {
            "game_done": self.game_done,
            "stage_done": self.stage_done,
            "round_done": self.round_done,
        }

        if self.game_done:
            terminated = True
        elif self.stage_done:
            self._next_stage()
        elif self.round_done:
            self._next_round()
        return (
            data["frame"],
            data["reward"],
            terminated,
            truncated,
            info,
        )

    # Safely closes emulator
    def close(self):
        self.emu.close()
