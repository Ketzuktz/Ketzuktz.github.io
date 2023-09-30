from copy import deepcopy

from gicg_sim.game.state import GameControlState as CtrlState
from gicg_sim.game.state import GameState
from gicg_sim.types.operation import Operation


class CtrlCondition:
    def __init__(
        self,
        state: CtrlState,
        op: Operation | None,
        min_count: int = 0,
        max_count: int = 1,
        target: CtrlState | None = None,
    ) -> None:
        self.state = deepcopy(state)
        self.op = deepcopy(op)
        self.min_count = min_count
        self.max_count = max_count
        self.target = deepcopy(target)

    def validate(self, game_state: GameState, op: Operation) -> bool:
        if self.state != game_state.control_state:
            return False
        if self.op != op:
            return False
        return True
