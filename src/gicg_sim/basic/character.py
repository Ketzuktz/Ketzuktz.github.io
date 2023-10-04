import typing
from enum import Enum

from pydantic import BaseModel

from gicg_sim.basic.cost import CostType
from gicg_sim.basic.element import ElementType
from gicg_sim.basic.weapon import WeaponType


class SkillType(Enum):
    NormalAttack = "Normal Attack"
    ElementalSkill = "Elemental Skill"
    ElementalBurst = "Elemental Burst"


class SkillPrototype(BaseModel):
    name: str
    type: SkillType
    cost: CostType
    effect: list[typing.Any]
    comment: str | None


class CharacterPrototype(BaseModel):
    name: str
    rarity: int
    element: ElementType
    weapon: WeaponType
    max_HP: int
    max_energy: int
    skills: list[SkillPrototype]
