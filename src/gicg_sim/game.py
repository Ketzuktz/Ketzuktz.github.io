from gicg_sim.action import Action, ActionType
from gicg_sim.state import PlayerID, State
from gicg_sim.userboard import UserBoard


class GICG_Core:
    def __init__(self) -> None:
        self.state = State()

        self.player1 = UserBoard(self.state, PlayerID.Player_1)
        self.player2 = UserBoard(self.state, PlayerID.Player_2)

    def take_action(self, action: Action) -> bool:
        """take a action, return whether to switch player"""
        if action.type == ActionType.USE_SKILL:
            return True
        elif action.type == ActionType.SWITCH_CHARACTERS:
            return True
        elif action.type == ActionType.PLAY_CARD:
            return False
        elif action.type == ActionType.ELEMENTAL_TUNING:
            return False
        elif action.type == ActionType.DECLARE_ROUND_END:
            return True
        else:
            raise ValueError(f"Unknown action type: {action.type}")
