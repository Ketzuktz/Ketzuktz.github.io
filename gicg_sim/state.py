from typing import Enum, List
from typing_extensions import TypedDict
from .card.character import Character
from .die import DieState, create_die_state
import functools


class PlayerID(Enum):
    Undefined = 0
    Player_1 = 1
    Player_2 = 2
    
def validate_player(func):
    """Validate player argument isn't undefined

    Raises:
        ValueError: player cannot be Undefined.
    """    
    @functools.wraps(func)
    def wrapper_require_player(self, player: PlayerID, *args, **kwargs):
        if player == PlayerID.Undefined:
            raise ValueError("player cannot be Undefined.")
        return func(self, player, *args, **kwargs)
    return wrapper_require_player


class State:
    def __init__(self, current_player = PlayerID.Player_1) -> None:
        self.turn_count = 0
        self.current_player = current_player
        
        self.characters_lists = [[], []]
        self.active_character_index = [-1, -1]
        
        self.deck_lists = [[], []]
        self.hand_cards_lists = [[], []]
        self.die_states = [create_die_state() for _ in range(2)]
        
    @validate_player
    def player2index(self, player: PlayerID) -> int:
        if player == PlayerID.Player_1:
            return 0
        elif player == PlayerID.Player_2:
            return 1
        
    def characters(self, player: PlayerID) -> List[Character]:
        id = self.player2index(self, player)
        return self.characters_lists[id]
    
    def append_character(self, player: PlayerID, character_name: str):
        self.characters(player).append(Character.create(character_name))
    
    def deck(self, player: PlayerID):
        id = self.player2index(self, player)
        return self.deck_lists[id]
    
    def deck_set(self, player: PlayerID, deck):
        id = self.player2index(self, player)
        for card in deck:
            self.deck_lists[id].append(card)
        
    def hand_cards(self, player: PlayerID):
        id = self.player2index(self, player)
        return self.hand_cards_lists[id]
    
    def hand_cards_extend(self, player: PlayerID, cards):
        id = self.player2index(self, player)
        self.hand_cards_lists[id].extend(cards)