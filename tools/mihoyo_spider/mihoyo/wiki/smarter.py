import re
from enum import Enum
from html import escape as html_escape

from lxml import etree
from lxml import html as lxml_html
from mihoyo.wiki.card import CardInfo
from mihoyo.wiki.card import _CardBaseInfo as BaseInfo

from gicg_sim.model.prototype.action_card import ActionCardPrototype as AP
from gicg_sim.model.prototype.character import CharacterPrototype as CP
from gicg_sim.model.prototype.cost import CostType
from gicg_sim.model.prototype.die import DieCostPrototype
from gicg_sim.model.prototype.skill import SkillPrototype as SP

SKILL_COMMENT_DICT_ALIAS = {"准备": "准备技能"}


class SmarterContext:
    def __init__(self) -> None:
        self._dictionary = {}
        self._raw_data = {}
        self._effects: set[str] = set()
        pass

    def append_effect(self, effect: str):
        self._effects.add(effect)

    def update_dictionary(self, key: str, value: str, raw_data: str = ""):
        if key in self._dictionary:
            if self._dictionary[key] != value:
                raise RuntimeError(
                    f"Conflict: {key} eq? {self._dictionary[key] == value}"
                    f"\n{repr(self._dictionary[key])}\n and \n{repr(value)}\n"
                )
        self._dictionary[key] = value
        self._raw_data[key] = raw_data

    @property
    def dictionary(self) -> dict:
        return self._dictionary

    @property
    def effects(self) -> list:
        return sorted(list(self._effects))


class CardInfoType(Enum):
    character = "角色牌"
    action = "行动牌"
    monster = "魔物牌"


def _type_count_list_to_dict(type_count_list: list[dict[str, int]]) -> dict[str, int]:
    output = dict()
    for type_count in type_count_list:
        output[type_count["type"]] = type_count["count"]
    return output


def _cost_repr_to_cost(cost_repr: dict[int, int]) -> CostType:
    die_mapping: dict[int, str] = {
        1: "cryo",
        2: "dendro",
        3: "anemo",
        4: "pyro",
        5: "electro",
        6: "hydro",
        7: "geo",
        # 8: 'energy',
        9: "matching",
        10: "unaligned",
        # 12: 'omni',
        12: "matching",
    }

    energy = cost_repr.get(8, 0)
    die_count = {die_mapping[k]: v for k, v in cost_repr.items() if k != 8 and v != 0}

    die_cost: DieCostPrototype = DieCostPrototype.model_validate(die_count)

    output = dict()
    output["die"] = die_cost

    if energy > 0:
        output["energy"] = energy

    return CostType.model_validate(output)


def _life_energy_to_cost(base_info: BaseInfo) -> CostType:
    data = {
        base_info["life_bg"]: base_info["life"],
        base_info["energy_bg"]: base_info["energy"],
    }

    return _cost_repr_to_cost(data)


def _extract_skill_comment_detail(
    detail_text: str, expect_title: str, context: SmarterContext
):
    parsed_detail = lxml_html.fromstring(detail_text)

    raw_contents = [
        s.strip()
        .replace(",", "，")
        .replace(":", "：")
        .replace(";", "；")
        .replace("(", "（")
        .replace(")", "）")
        .replace(" （", "（")
        .replace("「 ", "「")
        .replace("玩素", "元素")
        .replace("元索", "元素")
        .replace("敌方色", "敌方角色")
        .replace("「使用技能」后", "「使用技能后」")
        .replace("此类要", "此类需要")
        .replace("钬伤", "火伤")
        .replace("＋", "+")
        .replace("+ ", "+")
        .replace("够到2次", "最多叠加到2次")
        .replace("[凭依]", "「凭依」")
        .replace("穿透伤害：穿透伤害", "穿透伤害")
        .replace("暨加", "叠加")
        .replace("草/雷伤害", "草元素或雷元素伤害")
        .replace("保护该角色", "保护所附属的角色")
        .replace("1点护盾", "1点「护盾」")
        .replace("根据「凭依」级数，提供效果：", "根据「凭依」级数获得效果：")
        .replace(
            "我方元素骰子总数为偶数时进行的「普通攻击」，视为「重击」。", "我方行动开始前，如果元素骰总数为偶数，则进行的「普通攻击」将被视为「重击」。"
        )
        .replace("万能元素可以视为任何类型的元素", "可以视为任何类型的元素")
        .replace("生成使下3次草元素或雷元素伤害+1", "生成使下2次草元素或雷元素伤害+1")
        .replace("所附属角色进行重击时", "所附属角色进行「重击」时")
        for s in parsed_detail.xpath("//*//text()")
        if len(s.strip(" \n")) > 0
    ]

    if len(raw_contents) == 1 and raw_contents[0][0] == "<":
        return _extract_skill_comment_detail(raw_contents[0], expect_title, context)

    title = raw_contents[0].rstrip("：: ")
    title = SKILL_COMMENT_DICT_ALIAS.get(title, title)
    contents = raw_contents[1:]

    if title != expect_title:
        print(f"title '{title}' !=  expect_title '{expect_title}'")
        contents = raw_contents
        title = expect_title.strip()
        # print('title is {}'.format(title))
        # print('contents is {}'.format(contents))
        # print(f"{title}: {contents} from {detail_text}")

    if expect_title == "断流":
        if contents[-1] != "持续回合：2":
            contents.append("持续回合：2")

    if expect_title == "泷廻鉴花":
        if contents[-1] == "可用次数：2":
            contents[-1] = "可用次数：3"

    if expect_title == "潜行":
        if contents[0] == "注释内容：":
            contents = contents[1:]
        if contents[0] == "潜行：":
            contents = contents[1:]

    if expect_title == "物理伤害":
        contents[0] = contents[0].replace("物理伤害：物理伤害", "物理伤害")

    if expect_title == "绝境狂乱":
        title = expect_title + [v for v in contents if "惟神召符" in v][0][-2:]

    if expect_title == "踏潮":
        contents[1] = contents[1].replace("2点", "3点")

    if expect_title == "璇玑屏":
        if contents[0] == "出战状态":
            title = "璇玑屏（出战状态）"
        else:
            title = "璇玑屏"

    if expect_title == "启途誓使":
        if contents[1] != "结束阶段：":
            contents.insert(1, "结束阶段：")

    if expect_title == "冰元素附魔":
        if contents[-1] != "（持续到回合结束）":
            contents.append("（持续到回合结束）")

    if expect_title == "万能元素":
        if contents[0] == "： .":
            contents = contents[1:]

    if expect_title == "可用次数":
        if contents[0] == "：":
            contents = contents[1:]

        if contents[0] != "此牌效果触发后，会消耗1次可用次数；":
            contents.insert(0, "此牌效果触发后，会消耗1次可用次数；")

    if expect_title == "重华叠霜领域":
        if contents[-1] != "持续回合：2":
            contents.append("持续回合：2")

    if expect_title == "水光破镜":
        contents[-1] = contents[-1].replace("此状态在同一方只能存在一张", "同一方场上最多存在一个此状态")

    content = "\n".join(contents)

    content = (
        content.replace("\n：", "：")
        .replace("[ ", "[")
        .replace("， ", "，")
        .lstrip("：\n")
        .replace("\n\n", "\n")
        .replace("\n[\n", "[\n")
        .replace("1火伤\n害", "1点火伤害")
        .replace("草/雷伤害+1\n的", "草/雷伤害+1的")
        .replace("超导：\n", "超导：")
        .replace("[\n草原核\n]", "[草原核]")
        .replace("草元素或雷元素伤害+1\n的", "草元素或雷元素伤害+1的")
        .replace("[\n激化领域\n]", "[激化领域]")
        .replace("[\n燃烧烈焰\n]", "[燃烧烈焰]")
        .replace("\n持续回合\n", "持续回合")
        .replace(" .\n万能元素", "万能元素")
        .replace("，来支付", "，支付")
    )

    # now, all content has been split

    special_words = [
        "角色",
        "所附属角色",
        "准备",
        "护盾",
        "击倒",
        "免于被击倒",
        "下落攻击",
        "重击",
        "普通攻击",
        "物理伤害",
        "穿透伤害",
        "无色元素",
        "丹火印",
        "岩盔",
        "无法使用技能",
        "可用次数",
        "眩晕",
    ]

    for e in ["水", "火", "风", "冰", "草", "雷", "岩"]:
        special_words.append(f"{e}元素伤害")
        special_words.append(f"{e}元素附着")
        special_words.append(f"{e}元素")

    content = re.sub("(：)\n", r"\1", content)

    for sw in special_words:
        content = re.sub(f"([\u4e00-\u9fa5：])\n{sw}\n", f"\\1「{sw}」", content)
        content = re.sub(f"「\n({sw})\n」", "「\\1」", content)
        content = re.sub(f"([^「])({sw})", "\\1「\\2」", content)
        content = re.sub(f"^({sw})", "「\\1」", content)

    content = re.sub("(」)\n([\u4e00-\u9fa5])", r"\1\2", content)

    context.update_dictionary(title, content, detail_text)


def _extract_skill_comment_single_paragraph_text(
    root: etree.Element, context: SmarterContext
) -> str:
    # 获取包含技能描述的整个字符串，但排除 "[详情]" 部分
    skill_description = "".join(root.xpath("//*[not(self::sup)]/text()")).strip()

    strong_elements = root.xpath(".//u//text()")
    for element in strong_elements:
        # 获取加粗文本
        bold_text = element.strip()

        if bold_text:
            # 检查是否有相邻的 span 元素包含正确的 data-type 和 data-name 属性
            current_element = element

            while current_element is not None:
                if (
                    hasattr(current_element, "getnext")
                    and current_element.getnext() is not None
                    and current_element.getnext().tag == "span"
                ):
                    break

                current_element = current_element.getparent()

            if current_element is None:
                continue

            next_element = current_element.getnext()
            if (
                next_element is not None
                and next_element.tag == "span"
                and next_element.get("data-type") == "详情"
            ):
                # 获取详情文本
                detail_text = next_element.get("data-name")

                _extract_skill_comment_detail(detail_text, bold_text, context)

    return skill_description


def _extract_skill_effect_from_html(html: str, context: SmarterContext) -> str:
    root = etree.fromstring(f"<div>{html}</div>")
    ps = root.xpath('/*')
    output = ""

    for p in ps:
        comment_frag = _extract_skill_comment_single_paragraph_text(p, context)
        output += comment_frag

    output = output.replace("\n", "")
    output = output.replace("  ，", "，")
    output = output.replace("。 （", "。（")

    return output.strip()


def _raw_effect_to_desc(effect: str, context: SmarterContext) -> str:
    try:
        escaped_html_string = re.sub(
            r'="([^"]*)"',
            lambda match: f'="{html_escape(match.group(1))}"',
            effect,
        )
        removed_duplicate_class_string = re.sub(
            '(class=\\"[\\w-]+\\") \\1', "\\1", escaped_html_string
        )
        desc = _extract_skill_effect_from_html(removed_duplicate_class_string, context)
        context.append_effect(desc)
        return desc
    except Exception as e:
        print(escaped_html_string)
        raise e


def _extract_character_data(card: CardInfo, context: SmarterContext) -> CP:
    def card_skill_info_to_SP(skill_info: dict) -> SP:
        skill_effect_desc = _raw_effect_to_desc(skill_info["desc"], context)

        return {
            "name": skill_info["name"],
            "type": skill_info["skill_type"],
            "cost": _cost_repr_to_cost(
                _type_count_list_to_dict(skill_info["costs"])
            ).model_dump(exclude_none=True),
            "effect": skill_effect_desc,
            "comment": skill_effect_desc,
        }

    skills: list[SP] = [card_skill_info_to_SP(s) for s in card["skills"]]

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


def _extract_action_data(card: CardInfo, context: SmarterContext) -> AP:
    effect = _raw_effect_to_desc(card["effect"]["rich_text"], context)

    output: AP = {
        "name": card["name"],
        "group": card["base_info"]["tags"] + card["base_info"]["card_type"],
        "cost": _life_energy_to_cost(card["base_info"]).model_dump(exclude_none=True),
        "effect": effect,
        "comment": card["story"]["rich_text"],
    }
    return output


def card_info_extract_data(card: CardInfo, type: CardInfoType, context: SmarterContext):
    match type:
        case CardInfoType.character:
            return _extract_character_data(card, context)
        case CardInfoType.monster:
            return _extract_character_data(card, context)
        case CardInfoType.action:
            return _extract_action_data(card, context)
