from gicg_sim.action import Action
from gicg_sim.state import PlayerID, State
from gicg_sim.userboard import UserBoard


class GICG_Core:
    def __init__(self) -> None:
        self.state = State()

        self.player1 = UserBoard(self.state, PlayerID.Player_1)
        self.player2 = UserBoard(self.state, PlayerID.Player_2)

    def take_action(self, action: Action) -> bool:
        """take a action, return whether to switich player"""
        return True
