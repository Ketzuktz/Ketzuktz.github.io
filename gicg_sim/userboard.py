from typing import List

from .card.character import Character
from .state import PlayerID, State


class UserBoard:
    def __init__(self, state: State, player: PlayerID) -> None:
        self.state = state
        self.player = player

    def add_character(self, name: str):
        self.characters.append(Character.create(name))

    def draw_cards(self):
        pass

    def set_dies(self):
        pass

    @property
    def characters(self) -> List[Character]:
        return self.state.characters(self.player)
