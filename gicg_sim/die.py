from typing_extensions import TypedDict

element_names = ["Omni", "Pyro", "Hydro", "Anemo", "Electro", "Dendro", "Cryo", "Geo"]


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
        assert count >= 0, "Invalid die count: count must be non-negative"
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


def create_die_state(
    omni: int = 0,
    pyro: int = 0,
    hydro: int = 0,
    anemo: int = 0,
    electro: int = 0,
    dendro: int = 0,
    cryo: int = 0,
    geo: int = 0,
):
    kwargs = {
        "Omni": omni,
        "Pyro": pyro,
        "Hydro": hydro,
        "Anemo": anemo,
        "Electro": electro,
        "Dendro": dendro,
        "Cryo": cryo,
        "Geo": geo,
    }

    return DieState(**kwargs)
