import typing

from pydantic import BaseModel

from gicg_sim.model.prototype.die import DieCostPrototype


class CostType(BaseModel):
    die: DieCostPrototype
    energy: typing.Optional[int] = None
