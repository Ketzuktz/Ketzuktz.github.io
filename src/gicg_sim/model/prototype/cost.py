import typing

from pydantic import BaseModel

from gicg_sim.model.prototype.die import DieCostType


class CostType(BaseModel):
    die: DieCostType
    energy: typing.Optional[int] = None
