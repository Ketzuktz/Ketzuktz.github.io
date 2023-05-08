from typing import Any, List

from typing_extensions import TypedDict

from .utils.data import cards_data


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


class Character:
    prototype_dict = None

    def build_prototype_dict():
        assert "character" in cards_data, "No character data"
        Character.prototype_dict = dict(
            [(character["name"], character) for character in cards_data["character"]]
        )

    def create(name: str) -> dict:
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
