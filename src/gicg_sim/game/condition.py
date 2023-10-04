from copy import deepcopy

from gicg_sim.game.state import GameControlState
from gicg_sim.game.state import GameControlState as CtrlState
from gicg_sim.game.state import GameState
from gicg_sim.types.condition import (CtrlCondition, EventLogic, EventLogicAnd,
                                      EventLogicSingle, EventsLogicOr)
from gicg_sim.types.enums import PhaseType, RoundType
from gicg_sim.types.event import (EventBase, EventCombatAction,
                                  EventDeclareRoundEnd, EventDrawCard,
                                  EventEnum, EventRedrawCard, EventRollDice,
                                  EventSelectActiveCharacter)
from gicg_sim.types.subtypes import PlayerID


def el_and(*events: EventBase) -> EventLogic:
    return EventLogicAnd(*[el_single(e) for e in events])

def el_or(*events: EventBase) -> EventLogic:
    return EventsLogicOr(*[el_single(e) for e in events])

def el_single(event: EventBase) -> EventLogic:
    return EventLogicSingle(event)

def _le_once(
    logic_event: EventLogic,
    phase_status: PhaseType,
    round_status: RoundType | None = None,
    target: CtrlState | None = None,
) -> CtrlCondition:
    return CtrlCondition(
        state=GameControlState(
            phase_status=phase_status,
            round_status=round_status,
        ),
        logic_event=deepcopy(logic_event),
        min_count=0,
        max_count=1,
        target=target,
    )


def _auto_switch(
    phase_status: PhaseType,
    round_status: RoundType | None = None,
    target: CtrlState | None = None,
) -> CtrlCondition:
    return CtrlCondition(
        state=GameControlState(
            phase_status=phase_status,
            round_status=round_status,
        ),
        logic_event=None,
        min_count=0,
        max_count=0,
        target=target,
    )


def _must_be_once(
    logic_event: EventLogic,
    phase_status: PhaseType,
    round_status: RoundType | None = None,
    target: CtrlState | None = None,
) -> CtrlCondition:
    return CtrlCondition(
        state=GameControlState(
            phase_status=phase_status,
            round_status=round_status,
        ),
        logic_event=deepcopy(logic_event),
        min_count=1,
        max_count=1,
        target=target,
    )


CONTROL_CONDITIONS = [
    # phase-preparation
    _must_be_once(phase_status=PhaseType.Preparation, event=EventDrawCard(5)),
    _must_be_once(
        phase_status=PhaseType.Preparation,
        event=EventRedrawCard(
            min_count=0, max_count=5, pre_event=EventEnum.DrawCard
        ),
    ),
    _must_be_once(
        phase_status=PhaseType.Preparation,
        event=EventSelectActiveCharacter(pre_event=EventEnum.RedrawCard),
        target=CtrlState(phase_status=PhaseType.Round, round_status=RoundType.Roll),
    ),
    # phase-round round-roll
    _must_be_once(
        phase_status=PhaseType.Round,
        round_status=RoundType.Roll,
        event=EventRollDice(8),
    ),
    _must_be_once(
        phase_status=PhaseType.Round,
        round_status=RoundType.Roll,
        event=EventRedrawCard(
            min_count=0,
            max_count=8,
            pre_event=EventEnum.RollDice,
        ),
        # custom switch state
    ),
    # phase-round round-action combat
    _must_be_once(
        phase_status=PhaseType.Round,
        round_status=RoundType.RA_all_continue_1,
        event=EventCombatAction(player_id=PlayerID(1)),
        target=CtrlState(
            phase_status=PhaseType.Round, round_status=RoundType.RA_all_continue_2
        ),
    ),
    _must_be_once(
        phase_status=PhaseType.Round,
        round_status=RoundType.RA_all_continue_2,
        event=EventCombatAction(player_id=PlayerID(2)),
        target=CtrlState(
            phase_status=PhaseType.Round, round_status=RoundType.RA_all_continue_1
        ),
    ),
    # phase-round round-action declare end
    _must_be_once(
        phase_status=PhaseType.Round,
        round_status=RoundType.RA_all_continue_1,
        event=EventDeclareRoundEnd(player_id=PlayerID(1)),
        target=CtrlState(
            phase_status=PhaseType.Round, round_status=RoundType.RA_only_continue_2
        ),
    ),
    _must_be_once(
        phase_status=PhaseType.Round,
        round_status=RoundType.RA_all_continue_2,
        event=EventDeclareRoundEnd(player_id=PlayerID(2)),
        target=CtrlState(
            phase_status=PhaseType.Round, round_status=RoundType.RA_only_continue_1
        ),
    ),
    _must_be_once(
        phase_status=PhaseType.Round,
        round_status=RoundType.RA_only_continue_1,
        event=EventDeclareRoundEnd(player_id=PlayerID(1)),
        target=CtrlState(
            phase_status=PhaseType.Round, round_status=RoundType.RA_all_end
        ),
    ),
    _must_be_once(
        phase_status=PhaseType.Round,
        round_status=RoundType.RA_only_continue_2,
        event=EventDeclareRoundEnd(player_id=PlayerID(2)),
        target=CtrlState(
            phase_status=PhaseType.Round, round_status=RoundType.RA_all_end
        ),
    ),
    # phase-round round-action auto end
    _auto_switch(
        phase_status=PhaseType.Round,
        round_status=RoundType.RA_all_end,
        target=CtrlState(phase_status=PhaseType.Round, round_status=RoundType.End),
    ),
    # phase-round round-end
    # check VE or continue
    _auto_switch(
        phase_status=PhaseType.Round,
        round_status=RoundType.End,
        target=CtrlState(phase_status=PhaseType.Round, round_status=RoundType.Roll),
    ),
]


def validate_op(state: GameState, sys_event: SystemEventBase) -> bool:
    if state.control_state.phase_status == PhaseType.Preparation:
        pass
    return False
