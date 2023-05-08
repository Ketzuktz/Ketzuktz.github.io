import unittest

from gicg_sim.userboard import UserBoard


class TestUserBoard(unittest.TestCase):
    def test_add_character(self):
        userboard = UserBoard()
        userboard.add_character("Diluc")
        self.assertEqual(len(userboard.charaters), 1)
        self.assertEqual(userboard.charaters[0].name, "Diluc")


if __name__ == "__main__":
    unittest.main()
