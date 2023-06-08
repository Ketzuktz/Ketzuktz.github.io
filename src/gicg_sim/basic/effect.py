from enum import Enum


class SkillEffectType(Enum):
    DAMAGE = 1
    DAMAGE_ADD = 2
    # local counter
    COUNTER_ADD = 21
    COUNTER_CLEAR = 22
    COUNTER_CHECK = 23


class Effect:
    pass


class SkillEffect(Effect):
    pass
