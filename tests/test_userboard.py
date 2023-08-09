from gicg_sim.state import PlayerID, State
from gicg_sim.userboard import UserBoard


class TestUserBoard:
    def setup_method(self):
        self.state = State()
        self.player = PlayerID.Player_1
        self.userboard = UserBoard(self.state, self.player)

    def test_add_character(self):
        self.userboard.add_character("Diluc")
        assert len(self.userboard.characters) == 1
        assert self.userboard.characters[0].name == "Diluc"
