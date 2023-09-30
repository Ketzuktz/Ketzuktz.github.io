from copy import deepcopy

from gicg_sim.game.state import GameControlState
from gicg_sim.game.state import GameControlState as CtrlState
from gicg_sim.game.state import GameState
from gicg_sim.types.condition import CtrlCondition
from gicg_sim.types.enums import PhaseType, RoundType
from gicg_sim.types.operation import (OpCombatAction, OpDeclareRoundEnd,
                                      OpDrawCard, OpEnum, Operation,
                                      OpRedrawCard, OpRollDice,
                                      OpSelectActiveCharacter)
from gicg_sim.types.subtypes import PlayerID


def _le_once(
    op: Operation,
    phase_status: PhaseType,
    round_status: RoundType | None = None,
    target: CtrlState | None = None,
) -> CtrlCondition:
    return CtrlCondition(
        state=GameControlState(
            phase_status=phase_status,
            round_status=round_status,
        ),
        op=deepcopy(op),
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
        op=None,
        min_count=0,
        max_count=0,
        target=target,
    )


def _must_be_once(
    op: Operation,
    phase_status: PhaseType,
    round_status: RoundType | None = None,
    target: CtrlState | None = None,
) -> CtrlCondition:
    return CtrlCondition(
        state=GameControlState(
            phase_status=phase_status,
            round_status=round_status,
        ),
        op=deepcopy(op),
        min_count=1,
        max_count=1,
        target=target,
    )


CONTROL_CONDITIONS = [
    # phase-preparation
    _must_be_once(phase_status=PhaseType.Preparation, op=OpDrawCard(5)),
    _must_be_once(
        phase_status=PhaseType.Preparation,
        op=OpRedrawCard(min_count=0, max_count=5, pre_op=OpEnum.DrawCard),
    ),
    _must_be_once(
        phase_status=PhaseType.Preparation,
        op=OpSelectActiveCharacter(pre_op=OpEnum.RedrawCard),
        target=CtrlState(phase_status=PhaseType.Round, round_status=RoundType.Roll),
    ),
    # phase-round round-roll
    _must_be_once(
        phase_status=PhaseType.Round, round_status=RoundType.Roll, op=OpRollDice(8)
    ),
    _must_be_once(
        phase_status=PhaseType.Round,
        round_status=RoundType.Roll,
        op=OpRedrawCard(
            min_count=0,
            max_count=8,
            pre_op=OpEnum.RollDice,
        ),
        # custom switch state
    ),
    # phase-round round-action combat
    _must_be_once(
        phase_status=PhaseType.Round,
        round_status=RoundType.RA_all_continue_1,
        op=OpCombatAction(player_id=PlayerID(1)),
        target=CtrlState(
            phase_status=PhaseType.Round, round_status=RoundType.RA_all_continue_2
        ),
    ),
    _must_be_once(
        phase_status=PhaseType.Round,
        round_status=RoundType.RA_all_continue_2,
        op=OpCombatAction(player_id=PlayerID(2)),
        target=CtrlState(
            phase_status=PhaseType.Round, round_status=RoundType.RA_all_continue_1
        ),
    ),
    # phase-round round-action declare end
    _must_be_once(
        phase_status=PhaseType.Round,
        round_status=RoundType.RA_all_continue_1,
        op=OpDeclareRoundEnd(player_id=PlayerID(1)),
        target=CtrlState(
            phase_status=PhaseType.Round, round_status=RoundType.RA_only_continue_2
        ),
    ),
    _must_be_once(
        phase_status=PhaseType.Round,
        round_status=RoundType.RA_all_continue_2,
        op=OpDeclareRoundEnd(player_id=PlayerID(2)),
        target=CtrlState(
            phase_status=PhaseType.Round, round_status=RoundType.RA_only_continue_1
        ),
    ),
    _must_be_once(
        phase_status=PhaseType.Round,
        round_status=RoundType.RA_only_continue_1,
        op=OpDeclareRoundEnd(player_id=PlayerID(1)),
        target=CtrlState(
            phase_status=PhaseType.Round, round_status=RoundType.RA_all_end
        ),
    ),
    _must_be_once(
        phase_status=PhaseType.Round,
        round_status=RoundType.RA_only_continue_2,
        op=OpDeclareRoundEnd(player_id=PlayerID(2)),
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


def validate_op(state: GameState, operation: Operation) -> bool:
    if state.control_state.phase_status == PhaseType.Preparation:
        pass
    return False
