import re

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


def get_direct_damage(desc: str) -> (DamagePrototype, str):
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


if __name__ == "__main__":
    with open("output_data.d/effects.yml", "r", encoding="utf-8") as f:
        effects: list[str] = yaml.load(f, Loader=yaml.FullLoader)

    for e in effects:
        damage, remaining = get_direct_damage(e)
        if damage is not None:
            print(damage.model_dump(), remaining)
