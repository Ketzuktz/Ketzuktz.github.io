import typing
from enum import Enum

from pydantic import BaseModel

from gicg_sim.basic.element import ElementType


class DamageType(Enum):
    pyro: str = "pyro"
    hydro: str = "hydro"
    anemo: str = "anemo"
    electro: str = "electro"
    dendro: str = "dendro"
    cryo: str = "cryo"
    geo: str = "geo"
    # 物理伤害
    physical: str = "physical"
    # 穿透伤害
    piercing: str = "piercing"


class SideTargetType(Enum):
    active: str = "active"
    selected: str = "selected"
    all: str = "all"
    backend: str = "backend"
    previous: str = "previous"
    next: str = "next"


class SideType(Enum):
    self: str = "self"
    enemy: str = "enemy"
    all: str = "all"
    undefined: str = "undefined"


class LuaPluginTrigger(Enum):
    on_current_skill_using: str = "on_current_skill_using"
    on_current_skill_used: str = "on_current_skill_used"


class TargetType(BaseModel):
    side: SideType
    target: SideTargetType = SideTargetType.active


class DamagePrototype(BaseModel):
    type: DamageType
    target: TargetType = TargetType(side=SideType.enemy, target=SideTargetType.active)
    value: int = 0


class ElementGaugePrototype(BaseModel):
    type: ElementType
    damage: bool = True


class HealPrototype(BaseModel):
    target: TargetType = TargetType(side=SideType.self, target=SideTargetType.selected)
    value: int = 0


class CharacterBuffGetPrototype(BaseModel):
    target: TargetType = TargetType(side=SideType.self, target=SideTargetType.active)
    name: str


class LuaPluginPrototype(BaseModel):
    name: str
    trigger: LuaPluginTrigger
    implementation: str


# 特殊的，这里的 Effect 只描述无条件发生的效果，即，如果存在特殊条件触发或转换，则在 lua_implement 中实现
class EffectPrototype(BaseModel):
    damage: typing.Optional[DamagePrototype] = None
    heal: typing.Optional[HealPrototype] = None
    energy: typing.Optional[int] = None
    buff_get: typing.Optional[CharacterBuffGetPrototype] = None
    lua_plugin: typing.Optional[LuaPluginPrototype] = None
