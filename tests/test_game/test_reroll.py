from unittest.mock import call, patch

import pytest

from gicg_sim.die import DieState, _create_die_state_by_array
from gicg_sim.state import PlayerID, RoundPhase, State
from gicg_sim.userboard import UserBoard


def roll_n_dies_patch(die_count: int) -> DieState:
    if die_count == 8:
        return _create_die_state_by_array([1, 1, 1, 1, 1, 1, 1, 1])
    else:
        return _create_die_state_by_array(
            [(die_count if i == 0 else 0) for i in range(8)]
        )


@pytest.fixture
def setup_state():
    state = State()
    player_1 = PlayerID.Player_1
    player_2 = PlayerID.Player_2
    userboard_1 = UserBoard(state, player_1)
    userboard_2 = UserBoard(state, player_2)

    userboard_1.add_character("Diluc")
    userboard_2.add_character("Diluc")

    return state, userboard_1, userboard_2


@pytest.fixture
def setup_mock_roll_n_dies():
    with patch(
        "gicg_sim.state.roll_n_dies", side_effect=roll_n_dies_patch
    ) as mock_func:
        yield mock_func


class TestReroll:
    def test_reroll_action(self, setup_state, setup_mock_roll_n_dies):
        state, userboard_1, userboard_2 = setup_state
        mock_func = setup_mock_roll_n_dies

        assert state.round_phase == RoundPhase.END

        state.new_turn()
        assert state.round_phase == RoundPhase.ROLL

        keepdies_1 = _create_die_state_by_array([1, 1, 0, 0, 0, 0, 0, 0])
        keepdies_2 = _create_die_state_by_array([1, 0, 0, 0, 0, 0, 0, 0])

        userboard_1.reroll_dies(keepdies_1)
        userboard_2.reroll_dies(keepdies_2)

        assert state.round_phase == RoundPhase.ACTION

        assert userboard_1.die_state.Omni == 7
        assert userboard_1.die_state.Pyro == 1

        assert userboard_2.die_state.Omni == 8

        assert userboard_1.die_state.die_count == 8
        assert userboard_2.die_state.die_count == 8

        mock_func.assert_has_calls([call(8), call(8), call(6), call(7)])

    def test_reroll_exception(self, setup_state, setup_mock_roll_n_dies):
        state, userboard_1, _ = setup_state
        mock_func = setup_mock_roll_n_dies

        state.new_turn()
        mock_func.assert_has_calls([call(8), call(8)])

        keepdies_1 = _create_die_state_by_array([2, 1, 0, 0, 0, 0, 0, 0])

        with pytest.raises(AssertionError):
            userboard_1.reroll_dies(keepdies_1)
