from gicg_sim.game.manager import GameManager
from gicg_sim.game.state import GameState
from gicg_sim.types.enums import PhaseType, RoundType
from gicg_sim.types.operation import (OpDrawCard, OpRedrawCard,
                                      OpSelectActiveCharacter)
from gicg_sim.types.subtypes import PlayerID


def test_init():
    gs = GameState()
    gs.initialize()


def test_preparation():
    gm = GameManager()
    gm.initialize()

    gm.take_operation(OpDrawCard(count=5, player_id=PlayerID(1)))
    gm.take_operation(OpDrawCard(count=5, player_id=PlayerID(2)))

    gm.take_operation(OpRedrawCard(count=4, player_id=PlayerID(1)))
    gm.take_operation(OpRedrawCard(count=0, player_id=PlayerID(1)))

    gm.take_operation(OpSelectActiveCharacter(player_id=PlayerID(1), character_id=1))
    gm.take_operation(OpSelectActiveCharacter(player_id=PlayerID(2), character_id=1))

    assert gm.game_state.control_state.phase_status == PhaseType.Round
    assert gm.game_state.control_state.round_status == RoundType.Roll
