from gicg_sim.action import Action
from gicg_sim.character import Character
from gicg_sim.placement import Placement


class GameStateSide:
    def __init__(self) -> None:
        self.deck: list[Character] = []
        self.hand: list[Action] = []
        self.placement: list[Placement] = []
        self.summon: list = []


class GameStateControl:
    def __init__(self) -> None:
        self.round_status = ...


class GameState:
    def __init__(self) -> None:
        self.side1 = GameStateSide()
        self.side2 = GameStateSide()
        self.sides = (self.side1, self.side2)
        self.control_state = GameStateControl()
