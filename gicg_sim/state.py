from enum import Enum
from functools import wraps
from typing import List

from gicg_sim.card.action import ActionCard
from gicg_sim.card.character import Character
from gicg_sim.die import DieState, roll_n_dies


class PlayerID(Enum):
    Undefined = 0
    Player_1 = 1
    Player_2 = 2


class DuelPhase(Enum):
    PREPARATION = 1
    ROUNDS = 2
    VICTORY_EVALUATION = 3


class RoundPhase(Enum):
    ROLL = 1
    ACTION = 2
    END = 3


def validate_round_phase(required_state: RoundPhase):
    def decorator(func):
        @wraps(func)
        def wrapper(self: "State", *args, **kwargs):
            if self.duel_phase != DuelPhase.ROUNDS:
                raise ValueError("Invalid duel phase. Expected ROUNDS.")
            if self.round_phase != required_state:
                raise ValueError(f"Invalid round phase. Expected {required_state}.")

            return func(self, *args, **kwargs)

        return wrapper

    return decorator


class RoundState(Enum):
    Roll_Phase = 0
    Start_Phase = 1
    Action_Phase = 2
    End_Phase = 3


class State:
    def __init__(self, first_action_player: PlayerID = PlayerID.Player_1) -> None:
        # self.duel_phase: DuelPhase = DuelPhase.PREPARATION
        self.duel_phase: DuelPhase = DuelPhase.ROUNDS  # 先 ROUNDS，之后再加选牌流程
        self.round_phase: RoundPhase = RoundPhase.END
        self.turn_count = 0
        self.players = [PlayerID.Player_1, PlayerID.Player_2]
        self.player_max_roll_times = [1, 1]
        self.player_roll_times = [1, 1]
        self.first_action_player = first_action_player

        self.characters_lists: List[List[Character]] = [[], []]
        self.active_character_index = [-1, -1]

        self.deck_lists: List[List[ActionCard]] = [[], []]
        self.hand_cards_lists: List[List[ActionCard]] = [[], []]
        self._die_states: List[DieState] = [DieState() for _ in range(2)]

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

    def die_state(self, player: PlayerID) -> DieState:
        id = self.player2index(player)
        return self._die_states[id]

    @validate_round_phase(RoundPhase.ROLL)
    def reroll_dies(self, player: PlayerID, keep_dies: DieState) -> DieState:
        id = self.player2index(player)
        assert self.player_roll_times[id] > 0, "player has no roll times."

        reroll_dies = self._die_states[id] - keep_dies
        reroll_dies = roll_n_dies(reroll_dies.die_count)
        self._die_states[id] = keep_dies + reroll_dies

        self.reroll_dies_end(player)
        return self._die_states[id]

    @validate_round_phase(RoundPhase.ROLL)
    def reroll_dies_end(self, player: PlayerID) -> None:
        id = self.player2index(player)
        assert self.player_roll_times[id] > 0, "player has no roll times."
        self.player_roll_times[id] -= 1

        if self.player_roll_times[id] == 0:
            if sum(self.player_roll_times) == 0:
                self.round_phase = RoundPhase.ACTION

    def newturn(self) -> None:
        assert self.round_phase == RoundPhase.END, "round phase is not END."

        for pid in self.players:
            i = self.player2index(pid)
            self._die_states[i] = roll_n_dies(8)
            self.player_roll_times[i] = self.player_max_roll_times[i]

        self.round_phase = RoundPhase.ROLL
