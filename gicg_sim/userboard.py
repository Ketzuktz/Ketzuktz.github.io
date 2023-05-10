from typing import List

from gicg_sim.card.character import Character
from gicg_sim.die import DieState
from gicg_sim.state import PlayerID, State


class UserBoard:
    def __init__(self, state: State, player: PlayerID) -> None:
        self._state = state
        self._player = player

    def add_character(self, name: str):
        self.characters.append(Character.create(name))

    def draw_cards(self):
        pass

    def reroll_dies(self, keep_dies: DieState) -> DieState:
        return self._state.reroll_dies(self._player, keep_dies)

    @property
    def die_state(self) -> DieState:
        return self._state.die_state(self._player)

    @property
    def characters(self) -> List[Character]:
        return self._state.characters(self._player)
