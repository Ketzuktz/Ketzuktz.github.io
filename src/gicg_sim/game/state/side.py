import typing

from gicg_sim.basic.die import DieState, get_empty_die_state, roll_n_dies
from gicg_sim.basic.event.base import EventBase
from gicg_sim.basic.subtypes import CharacterID
from gicg_sim.model.character import Character
from gicg_sim.model.placement import Placement
from gicg_sim.model.prototype.action_card import ActionCardPrototype
from gicg_sim.model.prototype.effect import (DamagePrototype, DamageType,
                                             SideTargetType)


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

    def get_skill_by_id(self, skill_id: str):
        for c in self.characters:
            for s in c.skills:
                if s.name == skill_id:
                    return s
        else:
            raise ValueError(f"Cannot find skill {skill_id}.")

    @property
    def active_character(self) -> Character:
        return self.characters[self.active_id - 1]
