from gicg_sim.game.state.data import GameState


class EventDelegate():
    def __init__(self, state: GameState) -> None:
        self.__state = state

