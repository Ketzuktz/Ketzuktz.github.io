from typing import Any, Dict, List

from typing_extensions import TypedDict

from gicg_sim.card.base import CardBase
from gicg_sim.utils.data import cards_data


class SkillPrototype(TypedDict):
    name: str
    type: str
    cost: List[Any]
    effect: List[Any]
    comment: str


class CharacterPrototype(TypedDict):
    name: str
    rarity: int
    element: str
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


class Character(CardBase):
    prototype_dict: Dict[str, CharacterPrototype] = build_character_prototype_dict()

    @staticmethod
    def create(name: str) -> "Character":
        if Character.prototype_dict is None:
            Character.build_prototype_dict()
        assert name in Character.prototype_dict, f"No such character: {name}"
        return Character(Character.prototype_dict[name])

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
