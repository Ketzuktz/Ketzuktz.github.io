from gicg_sim.basic.enums import PhaseStatusEnum


class GameControlState:
    def __init__(
        self, *, phase_status: PhaseStatusEnum
    ) -> None:
        self.phase_status: PhaseStatusEnum = phase_status

    def reset(self) -> None:
        self.phase_status = PhaseStatusEnum.Preparation

    def update(self, new_state: 'GameControlState') -> None:
        self.phase_status = new_state.phase_status

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, GameControlState):
            return False
        if (self.phase_status != __value.phase_status):
            return False
        return True
