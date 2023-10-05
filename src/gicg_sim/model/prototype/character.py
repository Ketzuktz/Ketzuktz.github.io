
from pydantic import BaseModel

from gicg_sim.basic.element import ElementType
from gicg_sim.basic.weapon import WeaponType
from gicg_sim.model.prototype.skill import SkillPrototype


class CharacterPrototype(BaseModel):
    name: str
    rarity: int
    element: ElementType
    weapon: WeaponType
    max_HP: int
    max_energy: int
    skills: list[SkillPrototype]
