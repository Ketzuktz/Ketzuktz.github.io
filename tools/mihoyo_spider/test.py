import re
import typing

import yaml

from gicg_sim.model.prototype.effect import (DamagePrototype, DamageType,
                                             SideTargetType, SideType,
                                             TargetType)

TARGET_TRANSLATOR = {
    None: SideTargetType.active,
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
        r"^(?:对(?P<target>.+?))?造成(?P<value>\d+)点(?:的?)(?P<type>.+?)(?:元素)伤害(?:。|，|；)",
        desc,
    )

    if matched:
        target = matched["target"]
        target_v = TARGET_TRANSLATOR.get(target, None)
        assert target_v is not None, f"Unknown target: {target} from {desc}"
        side_v = SideType.enemy

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


def get_phase_condition(desc: str) -> typing.Tuple[str, str]:
    matched = re.match(r"^(?P<target>战斗开始时)(?:，?)", desc)

    if matched:
        target = matched["target"]
        remaining_string = desc[matched.end() :]
        return target, remaining_string

    return None, desc


def get_whether_passive(desc: str) -> typing.Tuple[bool, str]:
    matched = re.match(r"^【被动】", desc)

    if matched:
        remaining_string = desc[matched.end() :]
        return True, remaining_string

    return False, desc


def get_apply_status(desc: str) -> typing.Tuple[str, str]:
    matched = re.match(r"^(?P<init>初始)?附属(?P<status>.+?)(?:。|，|；)", desc)

    if matched:
        matched["init"]
        status = matched["status"]
        remaining_string = desc[matched.end() :]
        return status, remaining_string

    return None, desc


def get_summon(desc: str) -> typing.Tuple[str, str]:
    matched = re.match(
        r"^(?:召唤|召唤出)(?P<name>.+?)(?:。|，|；)",
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
        status, e = get_apply_status(e)
        if status:
            output["apply_status"] = status
        damage, e = get_direct_damage(e)
        if damage:
            output["damage"] = damage.model_dump(exclude_none=True)
        summon_name, e = get_summon(e)
        if summon_name:
            output["summon_name"] = summon_name

        print(output, e)
