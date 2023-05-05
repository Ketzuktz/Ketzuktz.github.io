from .userboard import UserBoard


class GICG_Core:
    def __init__(self) -> None:
        self.player1 = UserBoard()
        self.player2 = UserBoard()
