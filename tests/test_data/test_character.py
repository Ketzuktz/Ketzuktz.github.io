from gicg_sim.data import character_data
from gicg_sim.types.character import CharacterPrototype as CP


def test_character_validate():
    for c in character_data:
        assert CP.model_validate(c)
