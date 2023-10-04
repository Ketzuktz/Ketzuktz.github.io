from gicg_sim.basic.enums import PhaseStatusEnum
from gicg_sim.basic.event.operation import (PlayerOpDrawCard,
                                            PlayerOpRedrawCard,
                                            PlayerOpSelectActiveCharacter)
from gicg_sim.basic.subtypes import PlayerID
from gicg_sim.game.manager import GameManager
from gicg_sim.game.state.base import GameState


def test_init():
    gs = GameState()
    gs.initialize()


def test_preparation():
    gm = GameManager()
    gm.initialize()

    gm.take_operation(PlayerOpDrawCard(count=5, player_id=PlayerID(1)))
    gm.take_operation(PlayerOpDrawCard(count=5, player_id=PlayerID(2)))

    gm.take_operation(PlayerOpRedrawCard(count=4, player_id=PlayerID(1)))
    gm.take_operation(PlayerOpRedrawCard(count=0, player_id=PlayerID(2)))

    gm.take_operation(
        PlayerOpSelectActiveCharacter(player_id=PlayerID(1), character_id=1)
    )
    gm.take_operation(
        PlayerOpSelectActiveCharacter(player_id=PlayerID(2), character_id=1)
    )

    assert gm.game_state.control_state.phase_status == PhaseStatusEnum.Roll
