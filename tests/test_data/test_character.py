from gicg_sim.basic.character import CharacterPrototype as CP
from gicg_sim.data import character_data


def test_character_validate():
    for c in character_data:
        assert CP.model_validate(c)
