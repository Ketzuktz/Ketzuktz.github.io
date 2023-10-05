
import typing

from gicg_sim.basic.event.base import EventBase
from gicg_sim.basic.subtypes import CharacterID
from gicg_sim.model.character import Character
from gicg_sim.model.placement import Placement
from gicg_sim.model.prototype.action_card import Action
from gicg_sim.model.prototype.die import DieState


class GameSideState:
    def __init__(self) -> None:
        self.die_state: DieState = DieState()
        self.characters: list[Character] = []
        self.hand: list[Action] = []
        self.placement: list[Placement] = []
        self.summon: list = []
        self.draw_pile: list[Action] = []

        self.active_id: CharacterID = CharacterID(0)

        self.todo_set: typing.Set[EventBase] = set()

    def reset(self) -> None:
        self.characters.clear()
        self.hand.clear()
        self.placement.clear()
        self.summon.clear()
        self.draw_pile.clear()
        self.die_state = DieState()

    def initialize(self, character_names: list[str] = [], draw_pile: list[Action] = []):
        for cname in character_names:
            self.characters.append(Character.load(cname))
        pass

    def _switch_character(self, character_id: CharacterID) -> CharacterID:
        if character_id <= 0 or character_id > len(self.characters):
            raise ValueError(f"Invalid character ID {character_id}")

        self.active_id = character_id
        return self.active_id
