"""Unit tests for sfiii_gym.actions module."""

from MAMEToolkit.emulator import Action

from sfiii_gym import Actions


class TestActionsEnum:
    """Tests for the Actions enumeration."""

    def test_all_members_are_action_instances(self) -> None:
        for member in Actions:
            assert isinstance(member.value, Action)

    def test_expected_member_count(self) -> None:
        assert len(Actions) == 25

    def test_p1_movement_actions_exist(self) -> None:
        expected = {"P1_UP", "P1_DOWN", "P1_LEFT", "P1_RIGHT"}
        actual = {m.name for m in Actions}
        assert expected.issubset(actual)

    def test_p2_movement_actions_exist(self) -> None:
        expected = {"P2_UP", "P2_DOWN", "P2_LEFT", "P2_RIGHT"}
        actual = {m.name for m in Actions}
        assert expected.issubset(actual)

    def test_p1_attack_actions_exist(self) -> None:
        expected = {
            "P1_JPUNCH",
            "P1_SPUNCH",
            "P1_FPUNCH",
            "P1_SKICK",
            "P1_FKICK",
            "P1_RKICK",
        }
        actual = {m.name for m in Actions}
        assert expected.issubset(actual)

    def test_p2_attack_actions_exist(self) -> None:
        expected = {
            "P2_JPUNCH",
            "P2_SPUNCH",
            "P2_FPUNCH",
            "P2_SKICK",
            "P2_FKICK",
            "P2_RKICK",
        }
        actual = {m.name for m in Actions}
        assert expected.issubset(actual)

    def test_system_actions_exist(self) -> None:
        expected = {"SERVICE", "COIN_P1", "COIN_P2", "P1_START", "P2_START"}
        actual = {m.name for m in Actions}
        assert expected.issubset(actual)

    def test_action_ports(self) -> None:
        inputs_actions = {
            Actions.SERVICE,
            Actions.COIN_P1,
            Actions.COIN_P2,
            Actions.P1_START,
            Actions.P2_START,
            Actions.P1_UP,
            Actions.P1_DOWN,
            Actions.P1_LEFT,
            Actions.P1_RIGHT,
            Actions.P1_JPUNCH,
            Actions.P1_SPUNCH,
            Actions.P1_FPUNCH,
        }
        for action in inputs_actions:
            assert action.value.port == ":INPUTS"

    def test_extra_port_actions(self) -> None:
        extra_actions = {Actions.P1_SKICK, Actions.P1_FKICK}
        for action in extra_actions:
            assert action.value.port == ":EXTRA"

    def test_members_are_unique(self) -> None:
        names = [m.name for m in Actions]
        assert len(names) == len(set(names))
