from typing import Dict, List, Optional

from typing_extensions import TypedDict

from gicg_sim.basic.cost import DieCost
from gicg_sim.basic.effect import SkillEffect
from gicg_sim.basic.element import ElementType
from gicg_sim.card.base import CardBase
from gicg_sim.utils.data import cards_data


class SkillCost(TypedDict):
    die: Optional[DieCost]
    erengy: Optional[int]


class SkillPrototype(TypedDict):
    name: str
    type: str
    cost: SkillCost
    effect: List[SkillEffect]
    comment: str


class CharacterPrototype(TypedDict):
    name: str
    rarity: int
    element: ElementType
    weapon: str
    max_HP: int
    max_energy: int
    skills: List[SkillPrototype]


class Skill:
    def __init__(self, prototype: SkillPrototype) -> None:
        self.name = prototype["name"]
        self.type = prototype["type"]
        self.cost = prototype["cost"]
        self.effect = prototype["effect"]


def build_character_prototype_dict() -> Dict[str, CharacterPrototype]:
    assert "character" in cards_data, "No character data"
    return dict(
        [(character["name"], character) for character in cards_data["character"]]
    )


class CharacterCard(CardBase):
    prototype_dict: Dict[str, CharacterPrototype] = build_character_prototype_dict()

    @staticmethod
    def create(name: str) -> "CharacterCard":
        assert CharacterCard.prototype_dict, "No character prototype data"
        assert name in CharacterCard.prototype_dict, f"No such character: {name}"
        return CharacterCard(CharacterCard.prototype_dict[name])

    def __init__(self, prototype: CharacterPrototype) -> None:
        self.name = prototype["name"]
        self.rarity = prototype["rarity"]
        self.element = prototype["element"]
        self.weapon = prototype["weapon"]
        self.max_HP = prototype["max_HP"]
        self.max_energy = prototype["max_energy"]
        self.skills = [Skill(skill) for skill in prototype["skills"]]

        self.current_HP = self.max_HP
        self.current_energy = 0

    def get_skill(self, skill_name: str) -> List[Skill]:
        return [skill for skill in self.skills if skill_name == skill.name]
