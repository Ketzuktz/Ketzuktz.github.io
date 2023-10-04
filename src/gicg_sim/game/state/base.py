import typing
from random import randint

from gicg_sim.action import Action
from gicg_sim.basic.die import DieState
from gicg_sim.basic.enums import PhaseStatusEnum, TossType
from gicg_sim.basic.event.base import EventBase
from gicg_sim.basic.event.operation import PlayerOperationBase
from gicg_sim.basic.subtypes import CharacterID, PlayerID
from gicg_sim.character import Character
from gicg_sim.game.condition import CONTROL_CONDITIONS
from gicg_sim.game.operation_helper import OperationHelper
from gicg_sim.game.state.control import GameControlState
from gicg_sim.placement import Placement


class GameStateSide:
    def __init__(self) -> None:
        self.die_state: DieState = DieState()
        self.deck: list[Character] = []
        self.hand: list[Action] = []
        self.placement: list[Placement] = []
        self.summon: list = []
        self.draw_pile: list[Action] = []

        self.active_id: CharacterID = CharacterID(0)

        self.todo_set: typing.Set[EventBase] = set()

    def reset(self) -> None:
        self.deck.clear()
        self.hand.clear()
        self.placement.clear()
        self.summon.clear()
        self.draw_pile.clear()
        self.die_state = DieState()


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
        self.control_state = GameControlState(phase_status=PhaseStatusEnum.Preparation)
        self.active_player: PlayerID = PlayerID(-1)

        self.operation_history: list[PlayerOperationBase] = []

        self.event_history: list[EventBase] = []

    def initialize(self, toss: TossType = TossType.CONST_1) -> None:
        self.control_state.reset()
        self.side1.reset()
        self.side2.reset()
        self.active_player = tossType2playerID(toss)

    def _update_control_state(self) -> None:
        for c in CONTROL_CONDITIONS:
            if c.state == self.control_state:
                if c.validate(self.get_phase_events()):
                    self.control_state.update(c.target)
                    break

    def take_operation(self, operation: PlayerOperationBase):
        self.operation_history.append(operation)
        events = OperationHelper.map_operation_events(operation)
        self.apply_events(events)

        self._update_control_state()

    def apply_events(self, events: list[EventBase]):
        for e in events:
            self.event_history.append(e)
        pass

    def get_phase_events(self) -> list[EventBase]:
        return self.event_history
