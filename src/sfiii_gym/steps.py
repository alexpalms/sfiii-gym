from typing import TypedDict

from sfiii_gym.actions import Actions


class Step(TypedDict):
    wait: int
    actions: list[Actions]


def game_settings(frame_ratio: int, difficulty: int) -> list[Step]:
    steps: list[Step] = [
        {"wait": 0, "actions": [Actions.SERVICE]},
        {"wait": int(10 / frame_ratio), "actions": [Actions.P1_UP]},
        {"wait": int(10 / frame_ratio), "actions": [Actions.P1_UP]},
        {"wait": int(10 / frame_ratio), "actions": [Actions.P1_UP]},
        {"wait": int(10 / frame_ratio), "actions": [Actions.P1_UP]},
        {"wait": int(10 / frame_ratio), "actions": [Actions.P1_JPUNCH]},
        {
            "wait": int(10 / frame_ratio),
            "actions": [Actions.P1_DOWN],
        },  # Resetting to factory settings (mainly to deactivate bonus stage)
        {"wait": int(10 / frame_ratio), "actions": [Actions.P1_DOWN]},
        {
            "wait": int(10 / frame_ratio),
            "actions": [Actions.P1_JPUNCH, Actions.P1_FPUNCH],
        },
        {"wait": int(10 / frame_ratio), "actions": [Actions.P1_UP]},
        {"wait": int(10 / frame_ratio), "actions": [Actions.P1_JPUNCH]},
    ]
    if (difficulty % 8) < 3:
        steps.extend(
            Step(wait=int(10 / frame_ratio), actions=[Actions.P1_LEFT])
            for _ in range(3 - (difficulty % 8))
        )
    else:
        steps.extend(
            Step(wait=int(10 / frame_ratio), actions=[Actions.P1_RIGHT])
            for _ in range((difficulty % 8) - 3)
        )
    steps.extend(
        [
            {"wait": int(10 / frame_ratio), "actions": [Actions.P1_DOWN]},
            {"wait": int(10 / frame_ratio), "actions": [Actions.P1_DOWN]},
            {"wait": int(10 / frame_ratio), "actions": [Actions.P1_DOWN]},
            {"wait": int(10 / frame_ratio), "actions": [Actions.P1_DOWN]},
            {"wait": int(10 / frame_ratio), "actions": [Actions.P1_DOWN]},
            {"wait": int(10 / frame_ratio), "actions": [Actions.P1_DOWN]},
            {"wait": int(10 / frame_ratio), "actions": [Actions.P1_JPUNCH]},
            {"wait": int(10 / frame_ratio), "actions": [Actions.P1_DOWN]},
            {"wait": int(10 / frame_ratio), "actions": [Actions.P1_JPUNCH]},
            {"wait": int(10 / frame_ratio), "actions": [Actions.P1_DOWN]},
            {"wait": int(10 / frame_ratio), "actions": [Actions.P1_DOWN]},
            {"wait": int(10 / frame_ratio), "actions": [Actions.P1_JPUNCH]},
            {"wait": int(10 / frame_ratio), "actions": [Actions.P1_DOWN]},
            {"wait": int(10 / frame_ratio), "actions": [Actions.P1_DOWN]},
            {"wait": int(10 / frame_ratio), "actions": [Actions.P1_DOWN]},
            {"wait": int(10 / frame_ratio), "actions": [Actions.P1_JPUNCH]},
        ]
    )
    return steps


def next_stage(frame_ratio: int) -> list[Step]:
    steps: list[Step] = [Step(wait=int(60 / frame_ratio), actions=[Actions.P1_JPUNCH])]
    steps.extend(
        Step(wait=0, actions=[Actions.P1_JPUNCH]) for _ in range(int(180 / frame_ratio))
    )
    steps.append(Step(wait=int(60 / frame_ratio), actions=[Actions.P1_JPUNCH]))
    return steps


def new_game(frame_ratio: int) -> list[Step]:
    return [
        {"wait": 0, "actions": [Actions.SERVICE]},
        {"wait": int(30 / frame_ratio), "actions": [Actions.P1_UP]},
        {"wait": int(30 / frame_ratio), "actions": [Actions.P1_JPUNCH]},
        {"wait": int(300 / frame_ratio), "actions": [Actions.COIN_P1]},
        {"wait": int(10 / frame_ratio), "actions": [Actions.COIN_P1]},
        {"wait": int(60 / frame_ratio), "actions": [Actions.P1_START]},
        {"wait": int(80 / frame_ratio), "actions": [Actions.P1_LEFT]},
        {"wait": int(80 / frame_ratio), "actions": [Actions.P1_LEFT]},
        {"wait": int(80 / frame_ratio), "actions": [Actions.P1_LEFT]},
        {"wait": int(80 / frame_ratio), "actions": [Actions.P1_LEFT]},
        {
            "wait": int(80 / frame_ratio),
            "actions": [Actions.P1_LEFT, Actions.P1_JPUNCH],
        },
        {"wait": int(60 / frame_ratio), "actions": [Actions.P1_JPUNCH]},
        {"wait": int(60 / frame_ratio), "actions": [Actions.P1_JPUNCH]},
    ]
