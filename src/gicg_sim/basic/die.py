import random
from enum import Enum


class DieTypeEnum(Enum):
    pyro = "pyro"
    hydro = "hydro"
    anemo = "anemo"
    electro = "electro"
    dendro = "dendro"
    cryo = "cryo"
    geo = "geo"
    omni = "omni"


class DieState:
    def __init__(self) -> None:
        self._data: dict[DieTypeEnum, int] = {}
        for i in DieTypeEnum:
            self._data[i] = 0

    @staticmethod
    def _map_idx(idx: DieTypeEnum | str) -> DieTypeEnum:
        if isinstance(idx, DieTypeEnum):
            return idx
        elif isinstance(idx, str):
            return DieTypeEnum(idx)
        else:
            raise TypeError(f"Invalid key type {type(idx)}")

    def __getitem__(self, key: DieTypeEnum | str) -> int:
        key_ = DieState._map_idx(key)
        return self._data[key_]

    def __setitem__(self, key: DieTypeEnum | str, value: int) -> None:
        key_ = DieState._map_idx(key)
        self._data[key_] = value

    def clear(self) -> None:
        for i in DieTypeEnum:
            self._data[i] = 0

    @property
    def count(self) -> int:
        return sum(self._data.values())

    @staticmethod
    def roll_n_dies(n: int) -> "DieState":
        ds = DieState()
        for _ in range(n):
            die_type = random.choice(list(DieTypeEnum))
            ds[die_type] += 1
        return ds


DIE_TYPES = ["pyro", "hydro", "anemo", "electro", "dendro", "cryo", "geo", "omni"]


def roll_n_dies(n: int) -> DieState:
    die = DieState()
    for _ in range(n):
        die_type = random.choice(DIE_TYPES)
        die[die_type] += 1  # type: ignore

    return die


def get_empty_die_state() -> DieState:
    return DieState()
