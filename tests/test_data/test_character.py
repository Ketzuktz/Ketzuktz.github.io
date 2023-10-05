from gicg_sim.basic.character import CharacterPrototype as CP
from gicg_sim.model.character import Character
from gicg_sim.data import character_data


def test_character_validate():
    for c in character_data:
        assert CP.model_validate(c)


def test_character_load():
    target = 'Diluc'
    
    cps = [cd for cd in character_data if cd['name'] == target]
    assert len(cps) == 1
    cd =  CP.model_validate(cps[0])
    
    c = Character(cd)
    assert c.name == target
    assert c.hp == 10
    