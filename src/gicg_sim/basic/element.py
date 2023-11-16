from enum import Enum


class ElementType(Enum):
    Pyro = "pyro"  # 火
    Hydro = "hydro"  # 水
    Anemo = "anemo"  # 风
    Electro = "electro"  # 雷
    Dendro = "dendro"  # 草
    Cryo = "cryo"  # 冰
    Geo = "geo"  # 岩


class DieTypeEnum(Enum):
    pyro = "pyro"
    hydro = "hydro"
    anemo = "anemo"
    electro = "electro"
    dendro = "dendro"
    cryo = "cryo"
    geo = "geo"
    omni = "omni"
