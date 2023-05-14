import unittest

from gicg_sim.card.character import CharacterCard


class TestCharacter(unittest.TestCase):
    def test_character_load(self):
        character = CharacterCard.create("Diluc")

        self.assertEqual(character.rarity, 5)
        self.assertEqual(character.element, "Pyro")
        # self.assertEqual(character.weapon, )


if __name__ == "__main__":
    unittest.main()
