from enum import Enum

from pydantic import BaseModel

from gicg_sim.model.prototype.cost import CostType
from gicg_sim.model.prototype.effect import EffectPrototype


class SkillType(Enum):
    NormalAttack = "Normal Attack"
    ElementalSkill = "Elemental Skill"
    ElementalBurst = "Elemental Burst"


class SkillPrototype(BaseModel):
    name: str
    type: SkillType
    cost: CostType
    effect: list[EffectPrototype]
    comment: str | None
