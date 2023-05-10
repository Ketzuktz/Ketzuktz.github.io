import random
from typing import List

from typing_extensions import TypedDict

element_names = ["Omni", "Pyro", "Hydro", "Anemo", "Electro", "Dendro", "Cryo", "Geo"]
element_count = len(element_names)


class DieStatePrototype(TypedDict):
    Omni: int
    Pyro: int
    Hydro: int
    Anemo: int
    Electro: int
    Dendro: int
    Cryo: int
    Geo: int


def non_negative_setter(func):
    def wrapper(self: "DieState", count: int):
        assert count >= 0, "Invalid die count: count must be non-negative"
        func(self, count)

    return wrapper


class DieState:
    def __init__(self, **kwargs):
        self.die_count = [0 for _ in range(7 + 1)]

        for (k, v) in kwargs.items():
            assert k in element_names, f"Invalid element name: {k}"
            assert isinstance(v, int), f"Invalid die count: {v}"
            setattr(self, k, v)

    def copy(self) -> "DieState":
        kwargs: dict = dict((en, getattr(self, en)) for en in element_names)

        return DieState(**kwargs)

    # region Omni
    @property
    def Omni(self) -> int:
        "万能骰"
        return self.die_count[0]

    @Omni.setter
    def Omni(self, count: int):
        assert count >= 0, "Invalid die count: count must be non-negative"
        self.die_count[0] = count

    # endregion

    # region Pyro
    @property
    def Pyro(self) -> int:
        "火骰"
        return self.die_count[1]

    @Pyro.setter
    def Pyro(self, count: int):
        assert count >= 0, "Invalid die count: count must be non-negative"
        self.die_count[1] = count

    # endregion

    # region Hydro
    @property
    def Hydro(self) -> int:
        "水骰"
        return self.die_count[2]

    @Hydro.setter
    def Hydro(self, count: int):
        assert count >= 0, "Invalid die count: count must be non-negative"
        self.die_count[2] = count

    # endregion

    # region Anemo
    @property
    def Anemo(self) -> int:
        "风骰"
        return self.die_count[3]

    @Anemo.setter
    def Anemo(self, count: int):
        assert count >= 0, "Invalid die count: count must be non-negative"
        self.die_count[3] = count

    # endregion

    # region Electro
    @property
    def Electro(self) -> int:
        "雷骰"
        return self.die_count[4]

    @Electro.setter
    def Electro(self, count: int):
        assert count >= 0, "Invalid die count: count must be non-negative"
        self.die_count[4] = count

    # endregion

    # region Dendro
    @property
    def Dendro(self) -> int:
        "草骰"
        return self.die_count[5]

    @Dendro.setter
    def Dendro(self, count: int):
        assert count >= 0, "Invalid die count: count must be non-negative"
        self.die_count[5] = count

    # endregion

    # region Cryo
    @property
    def Cryo(self) -> int:
        "冰骰"
        return self.die_count[6]

    @Cryo.setter
    def Cryo(self, count: int):
        assert count >= 0, "Invalid die count: count must be non-negative"
        self.die_count[6] = count

    # endregion

    # region Geo
    @property
    def Geo(self) -> int:
        "岩骰"
        return self.die_count[7]

    @Geo.setter
    def Geo(self, count: int):
        assert count >= 0, f"Invalid die count: count ({count}) must be non-negative"
        self.die_count[7] = count

    # endregion

    # region mathop
    def __add__(self, other: "DieState"):
        result = DieState()
        for en in element_names:
            lhs = getattr(self, en)
            rhs = getattr(other, en)
            setattr(result, en, lhs + rhs)
        return result

    def __sub__(self, other: "DieState"):
        result = DieState()
        for en in element_names:
            lhs = getattr(self, en)
            rhs = getattr(other, en)
            setattr(result, en, lhs - rhs)
        return result

    # endregion

    def __ge__(self, other: "DieState") -> bool:
        return all(
            self.die_count[i] >= other.die_count[i] for i in range(len(self.die_count))
        )

    def __gt__(self, other: "DieState") -> bool:
        return all(
            self.die_count[i] > other.die_count[i] for i in range(len(self.die_count))
        )

    def __le__(self, other: "DieState") -> bool:
        return all(
            self.die_count[i] <= other.die_count[i] for i in range(len(self.die_count))
        )

    def __lt__(self, other: "DieState") -> bool:
        return all(
            self.die_count[i] < other.die_count[i] for i in range(len(self.die_count))
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DieState):
            return NotImplemented
        return all(
            self.die_count[i] == other.die_count[i] for i in range(len(self.die_count))
        )


def _create_die_state_by_array(die_counts: List[int]) -> DieState:
    assert element_count == len(die_counts), (
        "Invalid die counts: die_counts must be"
        f"array with {element_count} int elements."
    )
    kwargs = dict(zip(element_names, die_counts))

    return DieState(**kwargs)


def roll_n_dies_raw(die_count: int = 8) -> DieState:
    die_state_array: List[int] = [0 for _ in range(element_count)]

    for i in range(die_count):
        p = random.randint(0, element_count - 1)
        die_state_array[p] = die_state_array[p] + 1

    return _create_die_state_by_array(die_state_array)


def roll_n_dies(die_count: int = 8) -> DieState:
    die_state_array: List[int] = [0 for _ in range(element_count)]
    current_sum = 0

    for i in range(element_count - 1):
        if die_count == current_sum:
            break

        value = random.randint(0, die_count - current_sum)
        die_state_array[i] = value
        current_sum += value

    die_state_array[element_count - 1] = die_count - current_sum
    random.shuffle(die_state_array)

    return _create_die_state_by_array(die_state_array)
