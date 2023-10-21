import typing
from enum import Enum

from pydantic import BaseModel


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


class TargetType(BaseModel):
    side: SideType
    target: SideTargetType = SideTargetType.active


class DamagePrototype(BaseModel):
    type: DamageType
    target: TargetType
    value: int = 0


class DamageAddPrototype(BaseModel):
    pyro: typing.Optional[int] = None
    hydro: typing.Optional[int] = None
    anemo: typing.Optional[int] = None
    electro: typing.Optional[int] = None
    dendro: typing.Optional[int] = None
    cryo: typing.Optional[int] = None
    geo: typing.Optional[int] = None
    physical: typing.Optional[int] = None


class CounterAddPrototype(BaseModel):
    name: str
    value: int = 1


class CounterCheckPrototype(BaseModel):
    name: str
    value: int = 1
    effect: list["EffectPrototype"]


class CounterClearPrototype(BaseModel):
    name: str


class GetBuffPrototype(BaseModel):
    name: str


class HealPrototype(BaseModel):
    target: typing.Optional[int] = None


class EffectPrototype(BaseModel):
    damage: typing.Optional[DamagePrototype] = None
    energy: typing.Optional[int] = None
    counter_add: typing.Optional[CounterAddPrototype] = None
    counter_check: typing.Optional[CounterCheckPrototype] = None
    counter_clear: typing.Optional[CounterClearPrototype] = None
    damage_add: typing.Optional[DamageAddPrototype] = None
    get_buff: typing.Optional[GetBuffPrototype] = None
    heal: typing.Optional[HealPrototype] = None
