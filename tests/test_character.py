from gicg_sim.card.character import CharacterCard


def test_character_load():
    character = CharacterCard.create("Diluc")

    assert character.rarity == 5
    assert character.element == "Pyro"
    # assert character.weapon == ...
