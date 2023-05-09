from .card.character import Character
from .state import State, PlayerID
from typing import List

class UserBoard:
    def __init__(self, state: State, player: PlayerID) -> None:
        self.state = state
        self.player = player
        self.hand = []
        self.deck = []
        self.dies = {}
        self.effects = []

    def add_character(self, name: str):
        self.charaters.append(Character.create(name))
        
    def draw_cards(self):
        pass
    
    def set_dies(self):
        pass
    
    @property
    def characters(self) -> List[Character]:
        return self.state.characters