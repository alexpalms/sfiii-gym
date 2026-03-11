"""Unit tests for sfiii_gym.steps module."""

import pytest

from sfiii_gym.steps import game_settings, new_game, next_stage


class TestGameSettings:
    """Tests for the game_settings step generator."""

    @pytest.mark.parametrize("frame_ratio", [1, 3, 6])
    def test_returns_list_of_step_dicts(self, frame_ratio: int) -> None:
        steps = game_settings(frame_ratio, difficulty=6)
        assert isinstance(steps, list)
        assert len(steps) > 0

    def test_step_dict_structure(self) -> None:
        steps = game_settings(6, difficulty=6)
        for step in steps:
            assert "wait" in step
            assert "actions" in step
            assert isinstance(step["wait"], int)
            assert isinstance(step["actions"], list)

    @pytest.mark.parametrize("difficulty", range(8))
    def test_all_difficulties(self, difficulty: int) -> None:
        steps = game_settings(6, difficulty)
        assert isinstance(steps, list)
        assert len(steps) > 0

    def test_difficulty_below_3_fewer_than_above(self) -> None:
        # d=1 => 3-1=2 left presses, d=3 => 0 presses
        steps_d1 = game_settings(6, difficulty=1)
        steps_d3 = game_settings(6, difficulty=3)
        assert len(steps_d1) > len(steps_d3)

    def test_difficulty_above_3_adds_right_presses(self) -> None:
        steps_d3 = game_settings(6, difficulty=3)
        steps_d5 = game_settings(6, difficulty=5)
        assert len(steps_d5) > len(steps_d3)

    def test_difficulty_3_no_extra_presses(self) -> None:
        steps_d3 = game_settings(6, difficulty=3)
        steps_d4 = game_settings(6, difficulty=4)
        assert len(steps_d3) < len(steps_d4)

    def test_wait_values_scale_with_frame_ratio(self) -> None:
        steps_r1 = game_settings(1, difficulty=6)
        steps_r6 = game_settings(6, difficulty=6)
        total_wait_r1 = sum(s["wait"] for s in steps_r1)
        total_wait_r6 = sum(s["wait"] for s in steps_r6)
        assert total_wait_r1 >= total_wait_r6


class TestNextStage:
    """Tests for the next_stage step generator."""

    @pytest.mark.parametrize("frame_ratio", [1, 3, 6])
    def test_returns_list_of_step_dicts(self, frame_ratio: int) -> None:
        steps = next_stage(frame_ratio)
        assert isinstance(steps, list)
        assert len(steps) > 0

    def test_step_dict_structure(self) -> None:
        steps = next_stage(6)
        for step in steps:
            assert "wait" in step
            assert "actions" in step

    def test_all_steps_contain_jpunch(self) -> None:
        steps = next_stage(6)
        for step in steps:
            action_names = [a.name for a in step["actions"]]
            assert "P1_JPUNCH" in action_names


class TestNewGame:
    """Tests for the new_game step generator."""

    @pytest.mark.parametrize("frame_ratio", [1, 3, 6])
    def test_returns_list_of_step_dicts(self, frame_ratio: int) -> None:
        steps = new_game(frame_ratio)
        assert isinstance(steps, list)
        assert len(steps) > 0

    def test_step_dict_structure(self) -> None:
        steps = new_game(6)
        for step in steps:
            assert "wait" in step
            assert "actions" in step

    def test_includes_coin_and_start(self) -> None:
        steps = new_game(6)
        all_action_names = [a.name for s in steps for a in s["actions"]]
        assert "COIN_P1" in all_action_names
        assert "P1_START" in all_action_names

    def test_includes_service(self) -> None:
        steps = new_game(6)
        all_action_names = [a.name for s in steps for a in s["actions"]]
        assert "SERVICE" in all_action_names
