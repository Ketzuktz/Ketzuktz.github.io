

import typing

from pydantic import BaseModel

from gicg_sim.basic.action_card import ActionCardType
from gicg_sim.model.prototype.cost import CostType
from gicg_sim.model.prototype.effect import EffectPrototype


class Action(BaseModel):
    name: str
    type: ActionCardType
    cost: typing.Optional[CostType]
    effect: list[EffectPrototype]
    comment: typing.Optional[str] = None
