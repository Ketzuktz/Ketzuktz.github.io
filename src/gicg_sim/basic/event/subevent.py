from enum import Enum

from gicg_sim.basic.element import ElementType
from gicg_sim.model.prototype.effect import DamageType, TargetType

'''
每个用户操作映射为一个事件，如果这个事件含有其他副作用，则使用
SubEvent 对副作用进行标注。

显然，这里的 SubEvent 和 Effect 高度一致对应。
'''

class SubEventType(Enum):
    damage: str = "damage"
    heal: str = "heal"
    element_gauge: str = "element_gauge"

    lua_plugin: str = "lua_plugin"

    undefined: str = "undefined"


class SubEvent:
    def __init__(self, type: SubEventType = SubEventType.undefined) -> None:
        self.type: SubEventType = type


class SubEventDamage:
    def __init__(self, damage_type: DamageType, target: TargetType, value: int) -> None:
        super(SubEvent, SubEventType.damage)

        self.damage_type = damage_type
        self.target = target
        self.value = value


class SubEventElementGauge:
    def __init__(self, element_type: ElementType, with_damage: bool = False) -> None:
        super(SubEvent, SubEventType.element_gauge)

        self.element_type = element_type
        self.with_damage = with_damage


class SubEventHeal:
    def __init__(self, target: TargetType, value: int) -> None:
        super(SubEvent, SubEventType.heal)

        self.target = target
        self.value = value


class SubEventLuaPlugin:
    def __init__(self, code: str) -> None:
        super(SubEvent, SubEventType.lua_plugin)

        self.code = code
