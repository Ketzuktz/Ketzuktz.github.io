from copy import deepcopy

from gicg_sim.basic.event.base import EventBase
from gicg_sim.game.state.control import GameControlState as CtrlState


class EventLogic:
    def __init__(self) -> None:
        pass

    def _match(self, events: list[EventBase]) -> tuple[bool, int]:
        raise NotImplementedError

    def match(self, events: list[EventBase]) -> bool:
        raise NotImplementedError


class EventLogicSingle(EventLogic):
    def __init__(
        self, event: EventBase, min_count: int = 1, max_count: int = 1
    ) -> None:
        self.event: EventBase = event
        self.min_count: int = min_count
        self.max_count: int = max_count

    def _match(self, events: list[EventBase]) -> tuple[bool, int]:
        for i, e in enumerate(events):
            if self.event == e:
                return True, i
        return False, -1

    def match(self, events: list[EventBase]) -> bool:
        return self._match(events)[0]


class EventsLogicOr(EventLogic):
    def __init__(self, *events: EventLogic) -> None:
        self.events = events

    def _match(self, events: list[EventBase]) -> tuple[bool, int]:
        for event_logic in self.events:
            matched, index = event_logic._match(events)
            if matched:
                return True, index
        return False, -1

    def match(self, events: list[EventBase]) -> bool:
        return self._match(events)[0]


class EventLogicAnd(EventLogic):
    def __init__(self, *events: EventLogic) -> None:
        self.events = events

    def _match(self, events: list[EventBase]) -> tuple[bool, int]:
        max_index = 0
        for event_logic in self.events:
            matched, index = event_logic._match(events)
            if not matched:
                return False, -1
            max_index = max(max_index, index)
        return True, max_index

    def match(self, events: list[EventBase]) -> bool:
        return self._match(events)[0]


class EventLogicSequence(EventLogic):
    def __init__(self, *events: EventLogic) -> None:
        self.events = events

    def _match(self, events: list[EventBase]) -> tuple[bool, int]:
        index = 0
        for event_logic in self.events:
            matched, span = event_logic._match(events[index:])
            if not matched:
                return False, -1
            index += span
        return True, index

    def match(self, events: list[EventBase]) -> bool:
        return self._match(events)[0]


class EventLogicTrue(EventLogic):
    def __init__(self) -> None:
        pass

    def _match(self, events: list[EventBase]) -> tuple[bool, int]:
        return True, 0

    def match(self, events: list[EventBase]) -> bool:
        return True


class CtrlCondition:
    def __init__(
        self,
        state: CtrlState,
        logic_event: EventLogic,
        target: CtrlState | None = None,
    ) -> None:
        self.state = deepcopy(state)
        self.logic_event = deepcopy(logic_event)
        self.target = deepcopy(target)

    def validate(self, events: list[EventBase]) -> bool:
        if not self.logic_event.match(events):
            return False
        return True
