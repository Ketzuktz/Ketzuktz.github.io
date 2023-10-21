import re
import typing

import yaml

from gicg_sim.model.prototype.effect import (DamagePrototype, DamageType,
                                             GetCharacterBuffPrototype,
                                             HealPrototype, SideTargetType,
                                             SideType, TargetType)

TARGET_ALIASES = {
    "自身": "我方出战角色",
    "此角色": "我方出战角色",
    "本角色": "我方出战角色",
    "我方出战角色": "我方出战角色",
    "所有我方角色": "我方所有角色",
}

TARGET_TRANSLATOR = {
    None: (SideTargetType.active, SideType.enemy),
    "我方出战角色": (SideTargetType.active, SideType.self),
    "我方所有角色": (SideTargetType.all, SideType.self),
    "目标角色": (SideTargetType.selected, SideType.undefined),
}

DAMAGE_TYPE_TRANSLATOR = {
    "火": DamageType.pyro,
    "水": DamageType.hydro,
    "风": DamageType.anemo,
    "雷": DamageType.electro,
    "草": DamageType.dendro,
    "冰": DamageType.cryo,
    "岩": DamageType.geo,
    "物理": DamageType.physical,
    "穿透": DamageType.piercing,
}


def get_direct_damage(desc: str) -> typing.Tuple[DamagePrototype, str]:
    matched = re.match(
        r"^(?:对(?P<target>[\u4e00-\u9fa5]+?))?造成(?P<value>\d+)点(?:的?)(?P<type>[\u4e00-\u9fa5]+?)(?:元素)伤害(?:。|，|；)",
        desc,
    )

    if matched:
        target = matched["target"]
        target_v, side_v = TARGET_TRANSLATOR.get(target, None)
        assert target_v is not None, f"Unknown target: {target} from {desc}"

        value_v = int(matched["value"])

        type_v = DAMAGE_TYPE_TRANSLATOR.get(matched["type"], None)
        assert type_v is not None, f"Unknown type: {matched['type']} from {desc}"

        remaining_string = desc[matched.end() :]

        return (
            DamagePrototype(
                type=type_v,
                target=TargetType(side=side_v, target=target_v),
                value=value_v,
            ),
            remaining_string,
        )

    return None, desc


def get_heal_effect(desc: str) -> typing.Tuple[HealPrototype, str]:
    matched = re.match(
        r"^(?:治疗)(?P<target>[\u4e00-\u9fa5]+?)(?P<value>\d+)(?:点)(?:。|，|；)", desc
    )

    if matched:
        target = matched["target"]
        target_name = TARGET_ALIASES.get(target, target)
        target_v, side_v = TARGET_TRANSLATOR.get(target_name, (None, None))

        assert target_v is not None, f"Unknown target: {target} from {desc}"
        if side_v == SideType.undefined:
            side_v = SideType.self

        assert side_v == SideType.self, f"Unknown side: {side_v} from {desc}"

        remaining_string = desc[matched.end() :]

        value_v = int(matched["value"])

        return (
            HealPrototype(
                target=TargetType(side=side_v, target=target_v), value=value_v
            ),
            remaining_string,
        )

    return None, desc


def get_character_buff(desc: str) -> typing.Tuple[GetCharacterBuffPrototype, str]:
    matched = re.match(
        r"^(?P<init>初始)?(?P<target>[\u4e00-\u9fa5]+?)?(?:附属)(?P<buff>[\u4e00-\u9fa5·]+?)(?:。|，|；)",
        desc,
    )

    if matched:
        target = matched["target"]
        buff = matched["buff"]

        target_name = TARGET_ALIASES.get(target, target)
        target_v, side_v = TARGET_TRANSLATOR.get(target_name, (None, None))

        assert target_v is not None, f"Unknown target: {target} from {desc}"

        remaining_string = desc[matched.end() :]

        return (
            GetCharacterBuffPrototype(
                target=TargetType(side=side_v, target=target_v), name=buff
            ),
            remaining_string,
        )

    return None, desc


def get_phase_condition(desc: str) -> typing.Tuple[str, str]:
    matched = re.match(
        r"^(?P<target>(战斗开始时)|(结束阶段)|(本回合中)|(下回合行动阶段开始时))(?:(:|，)?)", desc
    )

    if matched:
        target = matched["target"]
        remaining_string = desc[matched.end() :]
        return target, remaining_string

    return None, desc


def get_lose_buff_condition(desc: str) -> typing.Tuple[str, str]:
    matched = re.match(
        r"^(?P<target>[\u4e00-\u9fa5]+?)(?:所附属的)(?P<buff_name>[\u4e00-\u9fa5]+?)效果结束时(?:，?)",
        desc
    )

    if matched:
        target = matched["target"]
        buff_name = matched["buff_name"]

        remaining_string = desc[matched.end() :]
        return f"{target} {buff_name}", remaining_string

    return None, desc


def get_special_condition(desc: str) -> typing.Tuple[str, str]:
    matched = re.match(
        r"^(?P<target>[^\u4e00-\u9fa5]+?)(?P<condition>(使用技能后))(?:，?)", desc
    )

    if matched:
        target = matched["target"]
        condition = matched["condition"]

        buff_condition = matched["buff_condition"]
        buff_name = matched["buff_name"]

        remaining_string = desc[matched.end() :]
        return f"{target} {condition} {buff_condition} {buff_name}", remaining_string

    return None, desc


def get_whether_passive(desc: str) -> typing.Tuple[bool, str]:
    matched = re.match(r"^【被动】", desc)

    if matched:
        remaining_string = desc[matched.end() :]
        return True, remaining_string

    return False, desc


def get_summon(desc: str) -> typing.Tuple[str, str]:
    matched = re.match(
        r"^(?:召唤|召唤出)(?P<name>[\u4e00-\u9fa5]+?)(?:。|，|；)",
        desc,
    )

    if matched:
        name_v = matched["name"]
        remaining_string = desc[matched.end() :]

        return name_v, remaining_string

    return None, desc


if __name__ == "__main__":
    with open("output_data.d/effects.yml", "r", encoding="utf-8") as f:
        effects: list[str] = yaml.load(f, Loader=yaml.FullLoader)

    for e_ in effects:
        e = e_
        output = {}
        passive, e = get_whether_passive(e)
        if passive:
            output["passive"] = True
        phase_c, e = get_phase_condition(e)
        if phase_c:
            output["phase_condition"] = phase_c
        character_buff, e = get_character_buff(e)
        if character_buff:
            output["character_buff"] = character_buff.model_dump(exclude_none=True)

        lose_buff_condition, e = get_lose_buff_condition(e)
        if lose_buff_condition:
            output["lose_buff_condition"] = lose_buff_condition

        special_c, e = get_special_condition(e)
        if special_c:
            output["special_condition"] = special_c
        damage, e = get_direct_damage(e)
        if damage:
            output["damage"] = damage.model_dump(exclude_none=True)
        heal, e = get_heal_effect(e)
        if heal:
            output["heal"] = heal.model_dump(exclude_none=True)
        summon_name, e = get_summon(e)
        if summon_name:
            output["summon_name"] = summon_name

        print(output, e)

        # if character_buff and character_buff.name == "远程状态":
        #     print(special_buff_c)
        #     exit(-1)
