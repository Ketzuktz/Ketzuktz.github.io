from gicg_sim.game.state import GameState
from gicg_sim.types.operation import PlayerOperationBase
from gicg_sim.types.event import EventBase


class GameManager:
    def __init__(self):
        self.game_state: GameState = GameState()
        self.operation_history: list[PlayerOperationBase] = []
        self.event_history: list[EventBase] = []

    def initialize(self):
        self.game_state.initialize()

    def take_operation(self, operation: PlayerOperationBase):
        self.operation_history.append(operation)

    # def get_valid_operations(self) -> list[PlayerOperationBase]:
    #     return self.game_state.get_phase_events()
