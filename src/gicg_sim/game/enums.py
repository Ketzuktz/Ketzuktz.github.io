from enum import Enum


class ElementType(Enum):
    Pyro = "Pyro"  # 火
    Hydro = "Hydro"  # 水
    Anemo = "Anemo"  # 风
    Electro = "Electro"  # 雷
    Dendro = "Dendro"  # 草
    Cryo = "Cryo"  # 冰
    Geo = "Geo"  # 岩


class DieType(Enum):
    Pyro = "Pyro"  # 火
    Hydro = "Hydro"  # 水
    Anemo = "Anemo"  # 风
    Electro = "Electro"  # 雷
    Dendro = "Dendro"  # 草
    Cryo = "Cryo"  # 冰
    Geo = "Geo"  # 岩
    Omni = "Omni"  # 万能


class CostType(Enum):
    Pyro = "Pyro"  # 火
    Hydro = "Hydro"  # 水
    Anemo = "Anemo"  # 风
    Electro = "Electro"  # 雷
    Dendro = "Dendro"  # 草
    Cryo = "Cryo"  # 冰
    Geo = "Geo"  # 岩
    Matching = "Matching"  # 同色
    Unaligned = "Unaligned"  # 不同色


class WeaponType(Enum):
    Sword = "Sword"  # 单手剑
    Bow = "Bow"  # 弓
    Claymore = "Claymore"  # 双手剑
    Polearm = "Polearm"  # 长柄武器
    Catalyst = "Catalyst"  # 法器


class SkillType(Enum):
    NormalAttack = "Normal Attack"
    ElementalSkill = "Elemental Skill"
    ElementalBurst = "Elemental Burst"
