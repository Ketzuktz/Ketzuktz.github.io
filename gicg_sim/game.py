from .userboard import UserBoard
from .state import State

class GICG_Core:
    def __init__(self) -> None:
        self.state = State()
        
        self.player1 = UserBoard(self.state)
        self.player2 = UserBoard(self.state)
        

    def take_action(self) -> bool:
        '''take a action, return whether to switich player'''
        return True