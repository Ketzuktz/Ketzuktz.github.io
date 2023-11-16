import typing

from gicg_sim.basic.die import DieState, get_empty_die_state, roll_n_dies
from gicg_sim.basic.element import DieTypeEnum, ElementType
from gicg_sim.basic.event.base import EventBase
from gicg_sim.basic.subtypes import CharacterID
from gicg_sim.model.character import Character
from gicg_sim.model.placement import Placement
from gicg_sim.model.prototype.action_card import ActionCardPrototype
from gicg_sim.model.prototype.cost import CostType
from gicg_sim.model.prototype.die import DieCostPrototype
from gicg_sim.model.prototype.effect import (DamagePrototype, DamageType,
                                             SideTargetType)


def pay_die(die_state: DieState, die_cost: DieCostPrototype) -> DieState:
    """
    1. 对于基本元素，逐个检查
        1. 如果对应骰子能满足，则直接消耗
        2. 如果对应骰子不能满足，则检查万能骰子
            1. 如果万能骰子能满足，则消耗万能骰子
            2. 如果万能骰子不能满足，则报错
    2. 对于匹配元素，逐个检查
        1. 如果基础骰子能满足，则直接消耗
        2. 如果基础骰子不能满足，则检查万能骰子
            1. 如果万能骰子加特定基础骰子能满足，则消耗
            2. 如果都不能满足，则报错
    3. 对于不匹配元素，计算总数，然后直接消耗（后续考虑优先消耗异色）
    """
    for e_ in ElementType:
        e = e_.value
        count = getattr(die_cost, e)
        if die_state[e] >= count:
            die_state[e] -= count
        elif die_state[DieTypeEnum.omni] + die_state[e] >= count:
            die_state[DieTypeEnum.omni] -= count - die_state[e]
            die_state[e] = 0
        else:
            raise ValueError(f"Cannot pay die cost {die_cost}.")

    if die_cost.matching is not None:
        count = die_cost.matching
        for e_ in ElementType:
            e = e_.value
            if die_state[e] >= count:
                die_state[e] -= count
                count = 0
            elif die_state[DieTypeEnum.omni] + die_state[e] >= count:
                count -= die_state[e]
                die_state[e] = 0
            else:
                raise ValueError(f"Cannot pay die cost {die_cost}.")

    if die_cost.unaligned is not None:
        count = die_cost.unaligned
        for dt_ in DieTypeEnum:
            e = dt_.value
            if die_state[e] < count:
                count -= die_state[e]
                die_state[e] = 0
            elif die_state[e] >= count:
                die_state[e] -= count
                count = 0
                break
        else:
            raise ValueError(f"Cannot pay die cost {die_cost}.")

    return die_state


class GameSideState:
    def __init__(self) -> None:
        self.die_state: DieState = get_empty_die_state()
        self.characters: list[Character] = []
        self.hand: list[ActionCardPrototype] = []
        self.placement: list[Placement] = []
        self.summon: list = []
        self.draw_pile: list[ActionCardPrototype] = []

        self.active_id: CharacterID = CharacterID(0)

        self.todo_set: typing.Set[EventBase] = set()

    def reset(self) -> None:
        self.characters.clear()
        self.hand.clear()
        self.placement.clear()
        self.summon.clear()
        self.draw_pile.clear()
        self.die_state = get_empty_die_state()

    def initialize(
        self, character_names: list[str] = [], draw_pile_names: list[str] = []
    ):
        for cname in character_names:
            self.characters.append(Character.load(cname))
        pass

    def _roll_dice(self, dice_count: int) -> DieState:
        self.die_state = roll_n_dies(dice_count)

        return self.die_state

    def _switch_character(self, character_id: CharacterID) -> CharacterID:
        if character_id <= 0 or character_id > len(self.characters):
            raise ValueError(f"Invalid character ID {character_id}")

        self.active_id = character_id
        return self.active_id

    def _damaged(self, damage: DamagePrototype):
        if damage.target.target != SideTargetType.active:
            raise NotImplementedError()

        ch = self.active_character
        ch.hp = max(0, ch.hp - damage.value)

        match damage.type:
            case DamageType.physical:
                "do nothing"
                pass
            case DamageType.piercing:
                "skip shield"
                pass
            case _:
                pass

    def _get_energy(self, value: int):
        ch = self.active_character
        ch.energy += value

    def _pay_cost(self, cost: CostType):
        ch = self.active_character
        if cost.energy is not None:
            ch.energy -= cost.energy

        self.die_state = pay_die(self.die_state, cost.die)

    def get_skill_by_id(self, skill_id: str):
        for c in self.characters:
            for s in c.skills:
                if s.name == skill_id:
                    return s
        else:
            raise ValueError(f"Cannot find skill {skill_id}.")

    def get_character_by_id(self, character_id: CharacterID):
        if character_id <= 0 or character_id > len(self.characters):
            raise ValueError(f"Invalid character ID {character_id}")

        return self.characters[character_id - 1]

    @property
    def active_character(self) -> Character:
        return self.characters[self.active_id - 1]
