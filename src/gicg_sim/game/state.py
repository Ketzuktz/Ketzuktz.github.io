import typing
from random import randint

from gicg_sim.action import Action
from gicg_sim.character import Character
from gicg_sim.placement import Placement
from gicg_sim.types.die import DieState
from gicg_sim.types.enums import PhaseType, RoundType, TossType
from gicg_sim.types.operation import PlayerOperationBase
from gicg_sim.types.subtypes import CharacterID, PlayerID
from gicg_sim.types.sysEvent import SystemEventBase


class GameStateSide:
    def __init__(self) -> None:
        self.die_state: DieState = DieState()
        self.deck: list[Character] = []
        self.hand: list[Action] = []
        self.placement: list[Placement] = []
        self.summon: list = []
        self.draw_pile: list[Action] = []

        self.active_id: CharacterID = CharacterID(0)

        self.todo_set: typing.Set[SystemEventBase] = set()

    def reset(self) -> None:
        self.deck.clear()
        self.hand.clear()
        self.placement.clear()
        self.summon.clear()
        self.draw_pile.clear()
        self.die_state = DieState()


class GameControlState:
    def __init__(
        self, *, phase_status: PhaseType, round_status: RoundType | None = None
    ) -> None:
        self.phase_status: PhaseType = phase_status
        self.round_status: RoundType = round_status

    def reset(self) -> None:
        self.phase_status = PhaseType.Preparation
        self.round_status = RoundType.Roll

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, GameControlState):
            return False
        if (
            self.phase_status != ...
            and __value.phase_status != ...
            and self.phase_status != __value.phase_status
        ):
            return False
        if (
            self.round_status is not None
            and __value.round_status is not None
            and self.round_status != __value.round_status
        ):
            return False
        return True


def tossType2playerID(toss: TossType) -> PlayerID:
    if toss == TossType.RANDOM:
        return PlayerID(randint(1, 2))
    elif toss == TossType.CONST_1:
        return PlayerID(1)
    else:
        return PlayerID(2)


class GameState:
    def __init__(self) -> None:
        self.side1 = GameStateSide()
        self.side2 = GameStateSide()
        self.sides = (self.side1, self.side2)
        self.control_state = GameControlState(phase_status=PhaseType.Preparation)
        self.active_player: PlayerID = PlayerID(0)

        self.operation_history: list[PlayerOperationBase] = []
        self.operation_history_1: list[SystemEventBase] = []
        self.operation_history_2: list[SystemEventBase] = []

        self.event_history: list[SystemEventBase] = []

    def initialize(self, toss: TossType = TossType.CONST_1) -> None:
        self.control_state.reset()
        self.side1.reset()
        self.side2.reset()
        self.active_player = tossType2playerID(toss)

    def take_operation(self, operation: PlayerOperationBase):
        self.operation_history.append(operation)
        if operation.player_id == PlayerID(1):
            self.operation_history_1.append(operation)
        elif operation.player_id == PlayerID(2):
            self.operation_history_2.append(operation)
        else:
            raise ValueError(f"Invalid player id ({operation.player_id}) in operation.")

    def get_phase_events(self) -> list[SystemEventBase]:
        return self.event_history
