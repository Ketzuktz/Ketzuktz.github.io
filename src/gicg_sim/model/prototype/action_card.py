

import typing

from pydantic import BaseModel

from gicg_sim.basic.group import GroupType
from gicg_sim.data import action_card_mapping
from gicg_sim.model.prototype.cost import CostType
from gicg_sim.model.prototype.effect import EffectPrototype


class ActionCardPrototype(BaseModel):
    @staticmethod
    def load(name: str) -> "ActionCardPrototype":
        return ActionCardPrototype.model_validate(action_card_mapping[name])

    name: str
    group: list[GroupType]
    cost: CostType
    effect: list[EffectPrototype]
    comment: typing.Optional[str] = None
