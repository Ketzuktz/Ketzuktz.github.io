import typing

from pydantic import BaseModel


class DieCostPrototype(BaseModel):
    pyro: typing.Optional[int] = 0
    hydro: typing.Optional[int] = 0
    anemo: typing.Optional[int] = 0
    electro: typing.Optional[int] = 0
    dendro: typing.Optional[int] = 0
    cryo: typing.Optional[int] = 0
    geo: typing.Optional[int] = 0
    # non-specified
    matching: typing.Optional[int] = 0
    unaligned: typing.Optional[int] = 0
