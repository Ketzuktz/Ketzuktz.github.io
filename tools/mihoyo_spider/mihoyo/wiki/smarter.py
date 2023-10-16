from enum import Enum

from lxml import etree
from mihoyo.wiki.card import CardInfo

from gicg_sim.model.prototype.character import CharacterPrototype as CP
from gicg_sim.model.prototype.skill import SkillPrototype as SP


class DictContext:
    def __init__(self) -> None:
        self._dictionary = {}
        self._raw_data = {}
        pass

    def update(self, key: str, value: str, raw_data: str = ""):
        if key in self._dictionary:
            if self._dictionary[key] != value:
                raise RuntimeError(
                    f"Conflict: {key} = {self._dictionary[key]} and {value}"
                )
        self._dictionary[key] = value
        self._raw_data[key] = raw_data

    @property
    def data(self) -> dict:
        return self._dictionary


class CardInfoType(Enum):
    character = "角色牌"
    action = "行动牌"
    monster = "魔物牌"


def _extract_skill_comment(skill_desc: str, context: DictContext) -> str:
    root = etree.fromstring(skill_desc)

    # 获取包含技能描述的整个字符串，但排除 "[详情]" 部分
    skill_description = "".join(
        root.xpath('//*[not(self::span[@data-type="详情"])]/text()')
    ).strip()

    # 查找所有包含 "strong" 的文本
    strong_elements = root.xpath(".//strong//text()")
    for element in strong_elements:
        # 获取加粗文本
        bold_text = element.strip()
        if bold_text:
            # 检查是否有相邻的 span 元素包含正确的 data-type 和 data-name 属性
            next_element = element.getparent().getparent().getnext()
            if (
                next_element is not None
                and next_element.tag == "span"
                and next_element.get("data-type") == "详情"
            ):
                # 获取详情文本
                detail_text = next_element.get("data-name")
                context.update(bold_text, detail_text, skill_desc)

    return skill_description


def _extract_character_data(card: CardInfo, context: DictContext) -> CP:
    skills: list[SP] = [
        {
            "name": s["name"],
            "type": s["skill_type"],
            "cost": s["costs"],
            "effect": s["desc"],
            "comment": _extract_skill_comment(s["desc"], context),
        }
        for s in card["skills"]
    ]

    assert len(card["base_info"]["element"]) == 1
    assert len(card["base_info"]["weapon"]) == 1
    output: CP = {
        "name": card["name"],
        "rariry": -1,
        "element": card["base_info"]["element"][0],
        "weapon": card["base_info"]["weapon"][0],
        "max_HP": card["base_info"]["life"],
        "max_energy": card["base_info"]["energy"],
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
