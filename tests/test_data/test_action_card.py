from gicg_sim.basic.group import GroupType
from gicg_sim.data import action_card_mapping
from gicg_sim.model.action_card import ActionCard
from gicg_sim.model.prototype.action_card import ActionCardPrototype as ACP


def test_action_card_validate():
    for name, a in action_card_mapping.items():
        assert ACP.model_validate(a)


def test_food_create():
    target = "Sweet Madame"

    ap_data = action_card_mapping[target]
    ap = ACP.model_validate(ap_data)

    a = ActionCard(ap)
    assert a.name == target
    assert GroupType.Food in a.group
    assert len(a.effect) == 1

    effect = a.effect[0]
    assert effect.heal.target == 1
