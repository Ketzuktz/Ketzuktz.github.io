from gicg_sim.basic.faction import FactionType
from gicg_sim.basic.weapon import WeaponType
from gicg_sim.data import character_mapping
from gicg_sim.model.character import Character
from gicg_sim.model.prototype.character import CharacterPrototype as CP


def test_character_validate():
    for name, c in character_mapping.items():
        assert CP.model_validate(c)


def test_character_create():
    target = "Diluc"

    cp_data = character_mapping[target]
    cp = CP.model_validate(cp_data)

    c = Character(cp)
    assert c.name == target
    assert c.rarity == 5
    assert c.hp == 10
    assert c.energy == 0
    assert c.weapon == WeaponType.Claymore
    assert len(c.faction) == 1 and c.faction[0] == FactionType.Mondstadt
