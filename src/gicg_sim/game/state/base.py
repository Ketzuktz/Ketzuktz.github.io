import typing
from random import randint

from gicg_sim.model.action import Action
from gicg_sim.basic.die import DieState
from gicg_sim.basic.enums import PhaseStatusEnum, TossType
from gicg_sim.basic.event.base import EventBase, SysEventSwitchPhase
from gicg_sim.basic.event.operation import PlayerOperationBase
from gicg_sim.basic.subtypes import CharacterID, PlayerID
from gicg_sim.model.character import Character
from gicg_sim.game.condition import CONTROL_CONDITIONS
from gicg_sim.game.operation_helper import OperationHelper
from gicg_sim.game.state.control import GameControlState
from gicg_sim.model.placement import Placement


class GameStateSide:
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
        
    def initialize(self, characters: list[Character], draw_pile: list[Action]):
        pass


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
        self.event_history_phase_begin: int = 0

    def initialize(self, toss: TossType = TossType.CONST_1) -> None:
        self.control_state.reset()
        self.side1.reset()
        self.side2.reset()
        self.active_player = tossType2playerID(toss)

    def initialize_player(self, player: PlayerID, *args, **kwargs):
        if player == PlayerID(1):
            self.side1.initialize(*args, **kwargs)
        elif player == PlayerID(2):
            self.side2.initialize(*args, **kwargs)
        else:
            raise ValueError("Invalid player ID")

    def _update_control_state(self) -> bool:
        for c in CONTROL_CONDITIONS:
            if c.state == self.control_state:
                if c.validate(self.get_phase_events()):
                    self.control_state.update(c.target)
                    self.event_history.append(
                        SysEventSwitchPhase(
                            phase=self.control_state.phase_status,
                        )
                    )
                    self.event_history_phase_begin = len(self.event_history)
                    return True
        return False

    def take_operation(self, operation: PlayerOperationBase):
        self.operation_history.append(operation)
        events = OperationHelper.map_operation_events(operation)
        self.apply_events(events)

        while True:
            if not self._update_control_state():
                break

    def apply_events(self, events: list[EventBase]):
        for e in events:
            self.event_history.append(e)
        pass

    def get_phase_events(self) -> list[EventBase]:
        return self.event_history[self.event_history_phase_begin:]
