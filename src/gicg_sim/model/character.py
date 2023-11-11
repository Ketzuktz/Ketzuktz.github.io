from gicg_sim.basic.element import ElementType
from gicg_sim.basic.faction import FactionType
from gicg_sim.basic.weapon import WeaponType
from gicg_sim.model.prototype.character import (CharacterPrototype,
                                                SkillPrototype)


class Character:
    @staticmethod
    def load(name: str) -> "Character":
        return Character(CharacterPrototype.load(name))

    def __init__(self, prototype: CharacterPrototype) -> None:
        self._prototype = prototype
        self.hp: int = self.max_HP
        self.energy: int = 0

        self._skills: list[SkillPrototype] = self._prototype.skills

    @property
    def name(self) -> str:
        return self._prototype.name

    @property
    def rarity(self) -> int:
        return self._prototype.rarity

    @property
    def element(self) -> ElementType:
        return self._prototype.element

    @property
    def weapon(self) -> WeaponType:
        return self._prototype.weapon

    @property
    def max_HP(self) -> int:
        return self._prototype.max_HP

    @property
    def max_energy(self) -> int:
        return self._prototype.max_energy

    @property
    def faction(self) -> list[FactionType]:
        return self._prototype.faction

    @property
    def skills(self) -> list[SkillPrototype]:
        return self._skills
