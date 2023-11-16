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


class DamageAddPrototype(BaseModel):
    target: TargetType = TargetType(side=SideType.self, target=SideTargetType.active)
    value: int = 0


class TokenAddPrototype(BaseModel):
    name: str
    value: int = 1


class TokenCostPrototype(BaseModel):
    name: str
    value: int = 1
    effect: list["EffectPrototype"]


class TokenClearPrototype(BaseModel):
    name: str


class GetCharacterBuffPrototype(BaseModel):
    target: TargetType = TargetType(side=SideType.self, target=SideTargetType.active)
    name: str


class EffectPrototype(BaseModel):
    damage: typing.Optional[DamagePrototype] = None
    energy: typing.Optional[int] = None
    token_add: typing.Optional[TokenAddPrototype] = None
    token_cost: typing.Optional[TokenCostPrototype] = None
    token_clear: typing.Optional[TokenClearPrototype] = None
    damage_add: typing.Optional[DamageAddPrototype] = None
    buff_get: typing.Optional[GetCharacterBuffPrototype] = None
    heal: typing.Optional[HealPrototype] = None
