from copy import deepcopy

from gicg_sim.game.state import GameControlState as CtrlState
from gicg_sim.game.state import GameState
from gicg_sim.types.event import EventBase


class EventLogic:
    def __init__(self) -> None:
        pass


class EventLogicSingle(EventLogic):
    def __init__(self, event: EventBase, min_count: int = 0, max_count: int = 1) -> None:
        self.event: EventBase = event
        self.min_count: int = min_count
        self.max_count: int  = max_count


class EventsLogicOr(EventLogic):
    def __init__(self, *events: EventLogicSingle) -> None:
        self.events = events


class EventLogicAnd(EventLogic):
    def __init__(self, *events: EventLogicSingle) -> None:
        self.events = events


class CtrlCondition:
    def __init__(
        self,
        state: CtrlState,
        logic_event: EventLogic,
        min_count: int = 0,
        max_count: int = 1,
        target: CtrlState | None = None,
    ) -> None:
        self.state = deepcopy(state)
        self.event = deepcopy(logic_event)
        self.min_count = min_count
        self.max_count = max_count
        self.target = deepcopy(target)

    def validate(self, game_state: GameState, event: list[EventBase]) -> bool:
        raise NotImplementedError
        if self.state != game_state.control_state:
            return False
        if self.event != event:
            return False
        return True
