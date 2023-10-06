import typing

from pydantic import BaseModel


class DamageType(BaseModel):
    pyro: typing.Optional[int] = None
    hydro: typing.Optional[int] = None
    anemo: typing.Optional[int] = None
    electro: typing.Optional[int] = None
    dendro: typing.Optional[int] = None
    cryo: typing.Optional[int] = None
    geo: typing.Optional[int] = None
    physical: typing.Optional[int] = None


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
    damage: typing.Optional[DamageType] = None
    energy: typing.Optional[int] = None
    counter_add: typing.Optional[CounterAddPrototype] = None
    counter_check: typing.Optional[CounterCheckPrototype] = None
    counter_clear: typing.Optional[CounterClearPrototype] = None
    damage_add: typing.Optional[DamageAddPrototype] = None
    get_buff: typing.Optional[GetBuffPrototype] = None
    heal: typing.Optional[HealPrototype] = None
