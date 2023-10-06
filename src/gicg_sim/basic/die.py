from typing import NamedTuple


class DieState(NamedTuple):
    pyro: int = 0
    hydro: int = 0
    anemo: int = 0
    electro: int = 0
    dendro: int = 0
    cryo: int = 0
    geo: int = 0
    omni: int = 0
