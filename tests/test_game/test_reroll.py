import unittest
from unittest.mock import MagicMock, call, patch

from gicg_sim.die import DieState, _create_die_state_by_array
from gicg_sim.state import PlayerActionState, PlayerID, State
from gicg_sim.userboard import UserBoard


def roll_n_dies_patch(die_count: int) -> DieState:
    if die_count == 8:
        return _create_die_state_by_array([1, 1, 1, 1, 1, 1, 1, 1])
    else:
        return _create_die_state_by_array(
            [(die_count if i == 0 else 0) for i in range(8)]
        )


class TestReroll(unittest.TestCase):
    def setUp(self) -> None:
        self.state = State()
        self.player_1 = PlayerID.Player_1
        self.player_2 = PlayerID.Player_2
        self.userboard_1 = UserBoard(self.state, self.player_1)
        self.userboard_2 = UserBoard(self.state, self.player_2)

        self.userboard_1.add_character("Diluc")
        self.userboard_2.add_character("Diluc")
        return super().setUp()

    @patch("gicg_sim.state.roll_n_dies", side_effect=roll_n_dies_patch)
    def test_reroll_action(self, mock_func: MagicMock):
        self.assertTrue(self.state.state_all(PlayerActionState.Wait))

        self.state.newturn()
        self.assertTrue(self.state.state_all(PlayerActionState.Set_Reroll_Dies))

        keepdies_1 = _create_die_state_by_array([1, 1, 0, 0, 0, 0, 0, 0])
        keepdies_2 = _create_die_state_by_array([1, 0, 0, 0, 0, 0, 0, 0])

        self.userboard_1.reroll_dies(keepdies_1)
        self.userboard_2.reroll_dies(keepdies_2)

        self.assertEqual(self.userboard_1.die_state.Omni, 7)
        self.assertEqual(self.userboard_1.die_state.Pyro, 1)

        self.assertEqual(self.userboard_2.die_state.Omni, 8)

        self.assertEqual(self.userboard_1.die_state.die_count, 8)
        self.assertEqual(self.userboard_2.die_state.die_count, 8)

        mock_func.assert_has_calls([call(8), call(8), call(6), call(7)])

    @patch("gicg_sim.state.roll_n_dies", side_effect=roll_n_dies_patch)
    def test_reroll_exception(self, mock_func):
        self.state.newturn()
        mock_func.assert_has_calls([call(8), call(8)])

        keepdies_1 = _create_die_state_by_array([2, 1, 0, 0, 0, 0, 0, 0])

        with self.assertRaises(AssertionError):
            self.userboard_1.reroll_dies(keepdies_1)


if __name__ == "__main__":
    unittest.main()
