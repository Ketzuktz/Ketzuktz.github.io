from enum import Enum

from mihoyo.wiki.card import CardInfo

from gicg_sim.model.prototype.character import CharacterPrototype as CP
from gicg_sim.model.prototype.skill import SkillPrototype as SP


class DictContext:
    def __init__(self) -> None:
        self._dictionary = {}
        pass

    def update(self, key: str, value: str):
        if key in self._dictionary:
            if self._dictionary[key] != value:
                raise RuntimeError(
                    f"Conflict: {key} = {self._dictionary[key]} and {value}"
                )
        self._dictionary[key] = value

    @property
    def data(self) -> dict:
        return self._dictionary


class CardInfoType(Enum):
    character = "角色牌"
    action = "行动牌"
    monster = "魔物牌"


def _extract_character_data(card: CardInfo, context: DictContext) -> CP:
    skills: list[SP] = [
        {
            "name": s["name"],
            "type": s["skill_type"],
            "cost": s["costs"],
            "effect": s["desc"],
            "comment": s["desc"],
        }
        for s in card["skills"]
    ]
    output: CP = {
        "name": card["name"],
        "rariry": -1,
        "element": card["base_info"]["element"],
        "weapon": card["base_info"]["weapon"],
        "max_HP": card["base_info"]["life"],
        "max_energy": card["base_info"]["energy_count"],
        "faction": card["base_info"]["faction"],
        "skills": skills,
    }
    return output


def _extract_action_data(card: CardInfo, context: DictContext):
    pass


def card_info_extract_data(card: CardInfo, type: CardInfoType, context: DictContext):
    match type:
        case CardInfoType.character:
            return _extract_character_data(card, context)
        case CardInfoType.monster:
            return _extract_character_data(card, context)
        case CardInfoType.action:
            return _extract_action_data(card, context)
