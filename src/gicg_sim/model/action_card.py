
from gicg_sim.basic.group import GroupType
from gicg_sim.model.prototype.action_card import ActionCardPrototype
from gicg_sim.model.prototype.cost import CostType
from gicg_sim.model.prototype.effect import EffectPrototype


class ActionCard:
    @staticmethod
    def load(name: str) -> "ActionCard":
        return ActionCard(ActionCardPrototype.load(name))

    def __init__(self, prototype: ActionCardPrototype) -> None:
        self._prototype = prototype

    @property
    def name(self) -> str:
        return self._prototype.name

    @property
    def group(self) -> list[GroupType]:
        return self._prototype.group

    @property
    def cost(self) -> CostType:
        return self._prototype.cost

    @property
    def effect(self) -> list[EffectPrototype]:
        return self._prototype.effect
