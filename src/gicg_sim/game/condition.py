from copy import deepcopy

from gicg_sim.basic.enums import PhaseStatusEnum
from gicg_sim.basic.event.base import (EventBase, EventDrawCard,
                                       EventRedrawCard, EventRerollDice,
                                       EventRollDice,
                                       EventSelectActiveCharacter)
from gicg_sim.basic.event.logic import (CtrlCondition, EventLogic,
                                        EventLogicAnd, EventLogicSequence,
                                        EventLogicSingle, EventLogicTrue,
                                        EventsLogicOr)
from gicg_sim.basic.subtypes import PlayerID
from gicg_sim.game.state.control import GameControlState as CtrlState


def el_and(*events: EventBase) -> EventLogic:
    return EventLogicAnd(*[el_single(e) for e in events])


def el_or(*events: EventBase) -> EventLogic:
    return EventsLogicOr(*[el_single(e) for e in events])


def el_sequence(*events: EventBase) -> EventLogic:
    return EventLogicSequence(*[el_single(e) for e in events])


def el_single(event: EventBase) -> EventLogic:
    return EventLogicSingle(event)


def _le_once(
    logic_event: EventLogic,
    phase_status: PhaseStatusEnum,
    target: CtrlState,
) -> CtrlCondition:
    return CtrlCondition(
        state=CtrlState(
            phase_status=phase_status,
        ),
        logic_event=deepcopy(logic_event),
        target=target,
    )


def _auto_switch(
    phase_status: PhaseStatusEnum,
    target: CtrlState,
) -> CtrlCondition:
    return CtrlCondition(
        state=CtrlState(
            phase_status=phase_status,
        ),
        logic_event=EventLogicTrue(),
        target=target,
    )


def _normal_condition(
    phase_status: PhaseStatusEnum,
    logic_event: EventLogic,
    target: CtrlState,
) -> CtrlCondition:
    return CtrlCondition(
        state=CtrlState(phase_status=phase_status),
        logic_event=deepcopy(logic_event),
        target=target,
    )


CONTROL_CONDITIONS: list[CtrlCondition] = [
    # phase-preparation
    _normal_condition(
        phase_status=PhaseStatusEnum.Preparation,
        logic_event=EventLogicAnd(
            el_sequence(
                EventDrawCard(count=5, player_id=PlayerID(1)),
                EventRedrawCard(count=5, player_id=PlayerID(1)),
                EventSelectActiveCharacter(player_id=PlayerID(1)),
            ),
            el_sequence(
                EventDrawCard(count=5, player_id=PlayerID(2)),
                EventRedrawCard(count=5, player_id=PlayerID(2)),
                EventSelectActiveCharacter(player_id=PlayerID(2)),
            ),
        ),
        target=CtrlState(phase_status=PhaseStatusEnum.Roll),
    ),
    # phase-round round-roll
    _normal_condition(
        phase_status=PhaseStatusEnum.Roll,
        logic_event=EventLogicAnd(
            el_sequence(
                EventRollDice(count=8, player_id=PlayerID(1)),
                EventRerollDice(count=8, player_id=PlayerID(1)),
            ),
            el_sequence(
                EventRollDice(count=8, player_id=PlayerID(2)),
                EventRerollDice(count=8, player_id=PlayerID(2)),
            ),
        ),
        target=CtrlState(phase_status=PhaseStatusEnum.RA_start),
    ),
    _auto_switch(
        phase_status=PhaseStatusEnum.RA_start,
        target=CtrlState(phase_status=PhaseStatusEnum.RA_all_continue_1),
    ),
    # _must_be_once(
    #     phase_status=PhaseStatusEnum.Roll,
    #     event=EventRedrawCard(
    #         min_count=0,
    #         max_count=8,
    #         pre_event=EventEnum.RollDice,
    #     ),
    #     # custom switch state
    # ),
    # # phase-round round-action combat
    # _must_be_once(
    #     phase_status=PhaseStatusEnum.RA_all_continue_1,
    #     event=EventCombatAction(player_id=PlayerID(1)),
    #     target=CtrlState(
    #         phase_status=PhaseStatusEnum.RA_all_continue_2
    #     ),
    # ),
    # _must_be_once(
    #     phase_status=PhaseStatusEnum.RA_all_continue_2,
    #     event=EventCombatAction(player_id=PlayerID(2)),
    #     target=CtrlState(
    #         phase_status=PhaseStatusEnum.RA_all_continue_1
    #     ),
    # ),
    # # phase-round round-action declare end
    # _must_be_once(
    #     phase_status=PhaseStatusEnum.RA_all_continue_1,
    #     event=EventDeclareRoundEnd(player_id=PlayerID(1)),
    #     target=CtrlState(
    #         phase_status=PhaseStatusEnum.RA_only_continue_2
    #     ),
    # ),
    # _must_be_once(
    #     phase_status=PhaseStatusEnum.RA_all_continue_2,
    #     event=EventDeclareRoundEnd(player_id=PlayerID(2)),
    #     target=CtrlState(
    #         phase_status=PhaseStatusEnum.RA_only_continue_1
    #     ),
    # ),
    # _must_be_once(
    #     phase_status=PhaseStatusEnum.RA_only_continue_1,
    #     event=EventDeclareRoundEnd(player_id=PlayerID(1)),
    #     target=CtrlState(
    #         phase_status=PhaseStatusEnum.RA_all_end
    #     ),
    # ),
    # _must_be_once(
    #     phase_status=PhaseStatusEnum.RA_only_continue_2,
    #     event=EventDeclareRoundEnd(player_id=PlayerID(2)),
    #     target=CtrlState(
    #         phase_status=PhaseStatusEnum.RA_all_end
    #     ),
    # ),
    # # phase-round round-action auto end
    # _auto_switch(
    #     phase_status=PhaseStatusEnum.RA_all_end,
    #     target=CtrlState(phase_status=PhaseStatusEnum.End),
    # ),
    # # phase-round round-end
    # # check VE or continue
    # _auto_switch(
    #     phase_status=PhaseStatusEnum.End,
    #     target=CtrlState(phase_status=PhaseStatusEnum.Roll),
    # ),
]


# def validate_op(state: GameState, sys_event: SystemEventBase) -> bool:
#     if state.control_state.phase_status == PhaseStatusEnum.Preparation:
#         pass
#     return False
