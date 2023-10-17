import re
from enum import Enum
from html import escape as html_escape

from lxml import etree
from lxml import html as lxml_html
from mihoyo.wiki.card import CardInfo

from gicg_sim.model.prototype.character import CharacterPrototype as CP
from gicg_sim.model.prototype.skill import SkillPrototype as SP

SKILL_COMMENT_DICT_ALIAS = {"准备": "准备技能"}


class DictContext:
    def __init__(self) -> None:
        self._dictionary = {}
        self._raw_data = {}
        pass

    def update(self, key: str, value: str, raw_data: str = ""):
        if key in self._dictionary:
            if self._dictionary[key] != value:
                raise RuntimeError(
                    f"Conflict: {key} eq? {self._dictionary[key] == value}"
                    f"\n{repr(self._dictionary[key])}\n and \n{repr(value)}\n"
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


def _extract_skill_comment_detail(
    detail_text: str, expect_title: str, context: DictContext
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
        .replace("「使用技能」后", "「使用技能后」")
        .replace("此类要", "此类需要")
        .replace("钬伤", "火伤")
        .replace("＋", "+")
        .replace("+ ", "+")
        .replace("够到2次", "最多叠加到2次")
        .replace("穿透伤害：穿透伤害", "穿透伤害")
        .replace("暨加", "叠加")
        for s in parsed_detail.xpath("//*//text()")
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

    if expect_title == "潜行":
        if contents[0] == "注释内容：":
            contents = contents[1:]
        if contents[0] == "潜行：":
            contents = contents[1:]

    if expect_title == "物理伤害":
        contents[0] = contents[0].replace("物理伤害：物理伤害", "物理伤害")

    if expect_title == "绝境狂乱":
        title = expect_title + [v for v in contents if "惟神召符" in v][0][-2:]

    content = "\n".join(contents)

    content = (
        content.replace("\n：", "：")
        .replace("[ ", "[")
        .replace("， ", "，")
        .lstrip("：\n")
        .replace("\n[\n", "[\n")
        .replace("1火伤\n害", "1点火伤害")
        .replace("草/雷伤害+1\n的", "草/雷伤害+1的")
        .replace("超导：\n", "超导：")
        .replace("[\n草原核\n]", "[草原核]")
        .replace("[\n激化领域\n]", "[激化领域]")
    )

    context.update(title, content, detail_text)


def _extract_skill_comment_single_paragraph_text(
    root: etree.Element, context: DictContext
) -> str:
    # 获取包含技能描述的整个字符串，但排除 "[详情]" 部分
    skill_description = "".join(root.xpath("//*[not(self::sup)]/text()")).strip()

    strong_elements = root.xpath(".//strong//text()")
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


def _extract_skill_comment(skill_desc: str, context: DictContext) -> str:
    root = etree.fromstring(f"<div>{skill_desc}</div>")
    output = ""
    for p in root.xpath("/*"):
        comment_frag = _extract_skill_comment_single_paragraph_text(p, context)
        output += comment_frag + "\n"

    return output.strip()


def _extract_character_data(card: CardInfo, context: DictContext) -> CP:
    def card_skill_info_to_SP(skill_info: dict) -> SP:
        try:
            escaped_html_string = re.sub(
                r'="([^"]*)"',
                lambda match: f'="{html_escape(match.group(1))}"',
                skill_info["desc"],
            )
            skill_comment = _extract_skill_comment(escaped_html_string, context)
        except Exception as e:
            print(escaped_html_string)
            print(skill_info["name"])
            print(skill_info["desc"])
            raise e

        return {
            "name": skill_info["name"],
            "type": skill_info["skill_type"],
            "cost": skill_info["costs"],
            "effect": skill_comment,
            "comment": skill_comment,
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
