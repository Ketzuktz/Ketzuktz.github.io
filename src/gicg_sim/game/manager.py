from gicg_sim.game.state import GameState
from gicg_sim.types.operation import Operation


class GameManager:
    def __init__(self):
        self.game_state: GameState = GameState()
        self.operation_history: list[Operation] = []

    def initialize(self):
        self.game_state.initialize()

    def take_operation(self, operation: Operation):
        self.operation_history.append(operation)

    def get_valid_operations(self) -> list[Operation]:
        return self.game_state.get_valid_operations()
