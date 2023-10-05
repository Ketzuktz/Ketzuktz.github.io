import typing

from pydantic import BaseModel


class DieState(BaseModel):
    pyro: typing.Optional[int] = None
    hydro: typing.Optional[int] = None
    anemo: typing.Optional[int] = None
    electro: typing.Optional[int] = None
    dendro: typing.Optional[int] = None
    cryo: typing.Optional[int] = None
    geo: typing.Optional[int] = None
    omni: typing.Optional[int] = None


class DieCostType(BaseModel):
    pyro: typing.Optional[int] = None
    hydro: typing.Optional[int] = None
    anemo: typing.Optional[int] = None
    electro: typing.Optional[int] = None
    dendro: typing.Optional[int] = None
    cryo: typing.Optional[int] = None
    geo: typing.Optional[int] = None
    # non-specified
    aligned: typing.Optional[int] = None
    unaligned: typing.Optional[int] = None
