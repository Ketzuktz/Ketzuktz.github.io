from gicg_sim.basic.event.operation import PlayerOperationBase
from gicg_sim.game.state.base import GameState


class GameManager:
    def __init__(self):
        self.game_state: GameState = GameState()
        self.operation_history: list[PlayerOperationBase] = []

    def initialize(self):
        self.game_state.initialize()

    def initialize_player_card(self):
        pass

    def take_operation(self, operation: PlayerOperationBase):
        self.game_state.take_operation(operation)

    # def get_valid_operations(self) -> list[PlayerOperationBase]:
    #     return self.game_state.get_phase_events()
