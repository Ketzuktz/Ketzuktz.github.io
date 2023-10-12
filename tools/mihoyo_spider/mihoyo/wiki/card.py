import json
import typing
from typing import TypedDict

from mihoyo.wiki.base import _PageData, get_page


class RawCardInfo(TypedDict):
    id: str
    name: str
    desc: str
    icon_url: str

    infos: typing.Dict[str, typing.Any]


def _page_to_raw_card_info(page: _PageData) -> RawCardInfo:
    infos: typing.Dict[str, typing.Any] = {}

    for module in page["modules"]:
        if len(module["components"]) != 1:
            raise RuntimeError(
                f"Incorrect module components length: {len(module['components'])}"
            )

        module_name = module["name"]

        component = module["components"][0]
        module_id = component["component_id"]

        module_data = json.loads(component["data"])

        info_item = {
            "name": module_name,
            "id": module_id,
            "data": module_data,
        }

        infos[module_name] = infos.get(module_name, []) + [info_item]

    output: RawCardInfo = {
        "id": page["id"],
        "name": page["name"],
        "desc": page["desc"],
        "icon_url": page["icon_url"],
        "infos": infos,
    }

    return output


class _CardBaseInfoAttr(TypedDict):
    element: typing.List[str]
    weapon: typing.List[str]
    faction: typing.List[str]
    energy_count: typing.List[str]
    # 获取方式
    acquisition: typing.List[str]

    # 行动牌
    card_type: typing.List[str]
    tags: typing.List[str]
    cost: typing.List[str]


_CARD_BASE_ATTR_NAME_ZH_TO_EN = {
    "元素": "element",
    "武器": "weapon",
    "阵营": "faction",
    "充能": "energy_count",
    "获取方式": "acquisition",
    "获得方式": "acquisition",
    "获取": "acquisition",
    "类型": "card_type",
    "标签": "tags",
    "花费": "cost",
}


def _refine_card_base_info_attr(
    attrs: typing.List[typing.Dict[str, typing.Any]]
) -> _CardBaseInfoAttr:
    output = {}
    for attr in attrs:
        key = attr["key"].rstrip("：")
        value = [v.lstrip("：") for v in attr["value"]]

        output_key = _CARD_BASE_ATTR_NAME_ZH_TO_EN[key]
        output[output_key] = value

    return output


class _CardBaseInfo(TypedDict, total=False):
    name: str
    common_img: str
    gold_img: str

    life: int
    life_bg: str

    energy: int
    energy_bg: str

    element: typing.List[str]
    weapon: typing.List[str]
    faction: typing.List[str]
    energy_count: typing.List[str]
    # 获取方式
    acquisition: typing.List[str]

    card_type: typing.List[str]
    tags: typing.List[str]
    cost: typing.List[str]


class CostType(TypedDict):
    type: int
    count: int


class _CardSkillInfo(TypedDict):
    name: str
    skill_type: str
    icon: str

    costs: typing.List[CostType]
    desc: str


def _get_card_skill_infos(
    raw_skills_data: typing.List[typing.Dict[str, typing.Any]]
) -> typing.List[_CardSkillInfo]:
    for s in raw_skills_data:
        costs = []
        if s["life"] > 0:
            costs.append(
                {
                    "type": s["life_bg"],
                    "count": s["life"],
                }
            )
        if s["energy"] > 0:
            costs.append(
                {
                    "type": s["energy_bg"],
                    "count": s["energy"],
                }
            )

        valid_desc_key = ["", "技能效果", "召唤物技能", "召唤物效果"]
        assert (
            s["desc"]["key"] in valid_desc_key
        ), f"Invalid desc key: {s['desc']['key']}"

        assert len(s["desc"]["value"]) == 1
        yield {
            "name": s["tab_name"],
            "skill_type": s["skill_type"],
            "icon": s["icon"],
            "costs": costs,
            "desc": s["desc"]["value"][0],
        }


class _CardRichTextInfo(TypedDict):
    rich_text: str


class CardInfo(TypedDict):
    id: str
    name: str
    desc: str
    icon_url: str

    base_info: _CardBaseInfo
    skills: typing.List[_CardSkillInfo]
    summons: typing.List[_CardSkillInfo]
    effect: _CardRichTextInfo
    story: _CardRichTextInfo


def _refine_card_info(raw_card_info: RawCardInfo) -> CardInfo:
    assert "基础信息" in raw_card_info["infos"] and len(raw_card_info["infos"]["基础信息"]) == 1
    base_info_module = raw_card_info["infos"]["基础信息"][0]
    assert (
        base_info_module["name"] == "基础信息"
        and base_info_module["id"] == "card_base_info"
    )
    base_info_data = base_info_module["data"]

    base_info_raw_attrs = base_info_data["attr"]
    base_info_attrs = _refine_card_base_info_attr(base_info_raw_attrs)

    energy = 0
    if "energy_count" in base_info_attrs:
        energy = int(base_info_attrs["energy_count"][0][:-1])

    base_info: _CardBaseInfo = {
        "name": base_info_data["name"],
        "common_img": base_info_data["common_img"],
        "gold_img": base_info_data["gold_img"],
        "life": base_info_data["life"],
        "life_bg": base_info_data["life_bg"],
        "energy": energy,
        "energy_bg": base_info_data.get("energy_bg", -1),
        "element": base_info_attrs.get("element", []),
        "weapon": base_info_attrs.get("weapon", []),
        "faction": base_info_attrs.get("faction", []),
        "energy_count": base_info_attrs.get("energy_count", []),
        "acquisition": base_info_attrs.get("acquisition", []),
        "card_type": base_info_attrs.get("card_type", []),
        "tags": base_info_attrs.get("tags", []),
        "cost": base_info_attrs.get("cost", []),
    }

    skills: typing.List[_CardSkillInfo] = []

    if "卡牌技能" in raw_card_info["infos"]:
        for skill_module in raw_card_info["infos"]["卡牌技能"]:
            assert skill_module["name"] == "卡牌技能" and skill_module["id"] == "card_skill"
            skills_data_list = skill_module["data"]["list"]

            if skills_data_list is not None:
                skills.extend(_get_card_skill_infos(skills_data_list))

    summons: typing.List[_CardSkillInfo] = []

    if "召唤物" in raw_card_info["infos"]:
        assert len(raw_card_info["infos"]["召唤物"]) == 1
        summon_module = raw_card_info["infos"]["召唤物"][0]
        assert summon_module["name"] == "召唤物" and summon_module["id"] == "card_skill"
        summon_data_list = summon_module["data"]["list"]

        if summon_data_list is not None:
            summons.extend(_get_card_skill_infos(summon_data_list))

    effect_desc_text = ""
    if "效果描述" in raw_card_info["infos"]:
        assert len(raw_card_info["infos"]["效果描述"]) == 1
        effect_desc_module = raw_card_info["infos"]["效果描述"][0]
        assert (
            effect_desc_module["name"] == "效果描述"
            and effect_desc_module["id"] == "collapse_panel"
        )
        effect_desc_data = effect_desc_module["data"]

        effect_desc_text = effect_desc_data["rich_text"]

    story_text = ""

    if "卡牌故事" in raw_card_info["infos"]:
        assert len(raw_card_info["infos"]["卡牌故事"]) == 1
        story_module = raw_card_info["infos"]["卡牌故事"][0]
        assert story_module["name"] == "卡牌故事" and story_module["id"] == "collapse_panel"
        story_data = story_module["data"]

        story_text = story_data["rich_text"]

    output = {
        "id": raw_card_info["id"],
        "name": raw_card_info["name"],
        "desc": raw_card_info["desc"],
        "icon_url": raw_card_info["icon_url"],
        "base_info": base_info,
        "skills": skills,
        "summons": summons,
        "effect": {
            "rich_text": effect_desc_text,
        },
        "story": {
            "rich_text": story_text,
        },
    }

    return output


def get_card(card_id: int) -> CardInfo:
    card_page = get_page(card_id)

    raw_card_info = _page_to_raw_card_info(card_page)

    card_info = _refine_card_info(raw_card_info)

    return card_info
