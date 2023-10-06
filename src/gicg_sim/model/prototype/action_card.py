

import typing

from pydantic import BaseModel

from gicg_sim.basic.group import GroupType
from gicg_sim.model.prototype.cost import CostType
from gicg_sim.model.prototype.effect import EffectPrototype


class ActionCardPrototype(BaseModel):
    name: str
    group: list[GroupType]
    cost: typing.Optional[CostType]
    effect: list[EffectPrototype]
    comment: typing.Optional[str] = None
