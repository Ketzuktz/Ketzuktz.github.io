
import pytest

from gicg_sim.basic.event.operation import (PlayerOpDrawCard,
                                            PlayerOpRedrawCard,
                                            PlayerOpSelectActiveCharacter)
from gicg_sim.basic.subtypes import CharacterID, PlayerID
from gicg_sim.game.manager import GameManager


class TestSelectActiveCharacter:
    def setup_method(self):
        gm = GameManager()
        gm.initialize()
        gm.initialize_player_card(["Diluc", "Diluc"], PlayerID(1))
        gm.initialize_player_card(["Diluc"], PlayerID(2))

        gm.take_operation(PlayerOpDrawCard(count=5, player_id=PlayerID(1)))
        gm.take_operation(PlayerOpDrawCard(count=5, player_id=PlayerID(2)))

        gm.take_operation(PlayerOpRedrawCard(count=4, player_id=PlayerID(1)))
        gm.take_operation(PlayerOpRedrawCard(count=0, player_id=PlayerID(2)))

        self.gm = gm

    def test_select_character_1(self):
        gm = self.gm

        gm.take_operation(
            PlayerOpSelectActiveCharacter(
                player_id=PlayerID(1), character_id=CharacterID(1)
            )
        )
        gm.take_operation(
            PlayerOpSelectActiveCharacter(
                player_id=PlayerID(2), character_id=CharacterID(1)
            )
        )

        assert gm.game_state.side1.active_id == CharacterID(1)
        assert gm.game_state.side2.active_id == CharacterID(1)

    def test_select_character_2(self):
        gm = self.gm

        gm.take_operation(
            PlayerOpSelectActiveCharacter(
                player_id=PlayerID(1), character_id=CharacterID(2)
            )
        )

        assert gm.game_state.side1.active_id == CharacterID(2)

    def test_error_out_of_range_1(self):
        gm = self.gm

        with pytest.raises(ValueError):
            gm.take_operation(
                PlayerOpSelectActiveCharacter(
                    player_id=PlayerID(1), character_id=CharacterID(0)
                )
            )

    def test_error_out_of_range_2(self):
        gm = self.gm

        with pytest.raises(ValueError):
            gm.take_operation(
                PlayerOpSelectActiveCharacter(
                    player_id=PlayerID(2), character_id=CharacterID(2)
                )
            )
