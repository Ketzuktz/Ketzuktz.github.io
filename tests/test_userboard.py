import unittest

from gicg_sim.state import PlayerID, State
from gicg_sim.userboard import UserBoard


class TestUserBoard(unittest.TestCase):
    def setUp(self) -> None:
        self.state = State()
        self.player = PlayerID.Player_1
        self.userboard = UserBoard(self.state, self.player)
        return super().setUp()

    def test_add_character(self):
        self.userboard.add_character("Diluc")
        self.assertEqual(len(self.userboard.characters), 1)
        self.assertEqual(self.userboard.characters[0].name, "Diluc")


if __name__ == "__main__":
    unittest.main()
