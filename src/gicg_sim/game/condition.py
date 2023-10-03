from copy import deepcopy

from gicg_sim.game.state import GameControlState
from gicg_sim.game.state import GameControlState as CtrlState
from gicg_sim.game.state import GameState
from gicg_sim.types.condition import CtrlCondition
from gicg_sim.types.enums import PhaseType, RoundType
from gicg_sim.types.subtypes import PlayerID
from gicg_sim.types.sysEvent import (SysEventCombatAction,
                                     SysEventDeclareRoundEnd, SysEventDrawCard,
                                     SysEventEnum, SysEventRedrawCard,
                                     SysEventRollDice,
                                     SysEventSelectActiveCharacter,
                                     SystemEventBase)


def _le_once(
    event: SystemEventBase,
    phase_status: PhaseType,
    round_status: RoundType | None = None,
    target: CtrlState | None = None,
) -> CtrlCondition:
    return CtrlCondition(
        state=GameControlState(
            phase_status=phase_status,
            round_status=round_status,
        ),
        sys_event=deepcopy(event),
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
        sys_event=None,
        min_count=0,
        max_count=0,
        target=target,
    )


def _must_be_once(
    event: SystemEventBase,
    phase_status: PhaseType,
    round_status: RoundType | None = None,
    target: CtrlState | None = None,
) -> CtrlCondition:
    return CtrlCondition(
        state=GameControlState(
            phase_status=phase_status,
            round_status=round_status,
        ),
        sys_event=deepcopy(event),
        min_count=1,
        max_count=1,
        target=target,
    )


CONTROL_CONDITIONS = [
    # phase-preparation
    _must_be_once(phase_status=PhaseType.Preparation, event=SysEventDrawCard(5)),
    _must_be_once(
        phase_status=PhaseType.Preparation,
        event=SysEventRedrawCard(
            min_count=0, max_count=5, pre_event=SysEventEnum.DrawCard
        ),
    ),
    _must_be_once(
        phase_status=PhaseType.Preparation,
        event=SysEventSelectActiveCharacter(pre_event=SysEventEnum.RedrawCard),
        target=CtrlState(phase_status=PhaseType.Round, round_status=RoundType.Roll),
    ),
    # phase-round round-roll
    _must_be_once(
        phase_status=PhaseType.Round,
        round_status=RoundType.Roll,
        event=SysEventRollDice(8),
    ),
    _must_be_once(
        phase_status=PhaseType.Round,
        round_status=RoundType.Roll,
        event=SysEventRedrawCard(
            min_count=0,
            max_count=8,
            pre_event=SysEventEnum.RollDice,
        ),
        # custom switch state
    ),
    # phase-round round-action combat
    _must_be_once(
        phase_status=PhaseType.Round,
        round_status=RoundType.RA_all_continue_1,
        event=SysEventCombatAction(player_id=PlayerID(1)),
        target=CtrlState(
            phase_status=PhaseType.Round, round_status=RoundType.RA_all_continue_2
        ),
    ),
    _must_be_once(
        phase_status=PhaseType.Round,
        round_status=RoundType.RA_all_continue_2,
        event=SysEventCombatAction(player_id=PlayerID(2)),
        target=CtrlState(
            phase_status=PhaseType.Round, round_status=RoundType.RA_all_continue_1
        ),
    ),
    # phase-round round-action declare end
    _must_be_once(
        phase_status=PhaseType.Round,
        round_status=RoundType.RA_all_continue_1,
        event=SysEventDeclareRoundEnd(player_id=PlayerID(1)),
        target=CtrlState(
            phase_status=PhaseType.Round, round_status=RoundType.RA_only_continue_2
        ),
    ),
    _must_be_once(
        phase_status=PhaseType.Round,
        round_status=RoundType.RA_all_continue_2,
        event=SysEventDeclareRoundEnd(player_id=PlayerID(2)),
        target=CtrlState(
            phase_status=PhaseType.Round, round_status=RoundType.RA_only_continue_1
        ),
    ),
    _must_be_once(
        phase_status=PhaseType.Round,
        round_status=RoundType.RA_only_continue_1,
        event=SysEventDeclareRoundEnd(player_id=PlayerID(1)),
        target=CtrlState(
            phase_status=PhaseType.Round, round_status=RoundType.RA_all_end
        ),
    ),
    _must_be_once(
        phase_status=PhaseType.Round,
        round_status=RoundType.RA_only_continue_2,
        event=SysEventDeclareRoundEnd(player_id=PlayerID(2)),
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
