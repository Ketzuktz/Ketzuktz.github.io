from enum import Enum
from functools import wraps
from typing import List

from gicg_sim.card.action import ActionCard
from gicg_sim.card.character import Character
from gicg_sim.die import DieState, create_die_state


class PlayerID(Enum):
    Undefined = 0
    Player_1 = 1
    Player_2 = 2


class PlayerActionState(Enum):
    """
    New Turn -> (Set_Reroll_Dies, Set_Reroll_Dies)
    """

    Undefined = 0
    Wait = 1
    Set_Reroll_Dies = 2
    Select_Active_Character = 3
    Normal_Action = 4


def validate_action_state(required_state: PlayerActionState):
    def decorator(func):
        @wraps(func)
        def wrapper(self: "State", player: PlayerID, *args, **kwargs):
            id = self.player2index(player)
            action_state: PlayerActionState = self.player_action_state[id]
            if action_state != required_state:
                raise ValueError(
                    f"Invalid player action state. Expected {required_state}."
                )

            return func(self, player, *args, **kwargs)

        return wrapper

    return decorator


class State:
    def __init__(self, current_player=PlayerID.Player_1) -> None:
        self.turn_count = 0
        self.player_action_state: List[PlayerActionState] = [
            PlayerActionState.Wait for _ in range(2)
        ]

        self.characters_lists: List[List[Character]] = [[], []]
        self.active_character_index = [-1, -1]

        self.deck_lists: List[List[ActionCard]] = [[], []]
        self.hand_cards_lists: List[List[ActionCard]] = [[], []]
        self.die_states: List[DieState] = [create_die_state() for _ in range(2)]

    def player2index(self, player: PlayerID) -> int:
        if player == PlayerID.Player_1:
            return 0
        elif player == PlayerID.Player_2:
            return 1
        else:
            raise ValueError("player cannot be Undefined.")

    def characters(self, player: PlayerID) -> List[Character]:
        id = self.player2index(player)
        return self.characters_lists[id]

    def character_append(self, player: PlayerID, character_name: str):
        self.characters(player).append(Character.create(character_name))

    def deck(self, player: PlayerID):
        id = self.player2index(player)
        return self.deck_lists[id]

    def deck_set(self, player: PlayerID, deck):
        id = self.player2index(player)
        for card in deck:
            self.deck_lists[id].append(card)

    def hand_cards(self, player: PlayerID):
        id = self.player2index(player)
        return self.hand_cards_lists[id]

    def hand_cards_append(self, player: PlayerID, cards):
        id = self.player2index(player)
        self.hand_cards_lists[id].extend(cards)

    @validate_action_state(PlayerActionState.Set_Reroll_Dies)
    def set_reroll_dies(self, player: PlayerID, keep_dies: DieState):
        self.player2index(player)

        pass
