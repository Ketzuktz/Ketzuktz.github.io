from gicg_sim.basic.enums import PhaseStatusEnum
from gicg_sim.basic.event.operation import (PlayerOpDrawCard,
                                            PlayerOpRedrawCard,
                                            PlayerOpRerollDice,
                                            PlayerOpRollDice,
                                            PlayerOpSelectActiveCharacter)
from gicg_sim.basic.subtypes import CharacterID, PlayerID
from gicg_sim.game.manager import GameManager
from gicg_sim.game.state.base import GameState


def test_init():
    gs = GameState()
    gs.initialize()
    assert gs.control_state.phase_status == PhaseStatusEnum.Preparation


def test_preparation():
    gm = GameManager()
    gm.initialize()

    gm.take_operation(PlayerOpDrawCard(count=5, player_id=PlayerID(1)))
    gm.take_operation(PlayerOpDrawCard(count=5, player_id=PlayerID(2)))

    gm.take_operation(PlayerOpRedrawCard(count=4, player_id=PlayerID(1)))
    gm.take_operation(PlayerOpRedrawCard(count=0, player_id=PlayerID(2)))

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

    assert gm.game_state.control_state.phase_status == PhaseStatusEnum.Roll
    assert len(gm.game_state.get_phase_events()) == 0


def get_gm_to_roll() -> GameManager:
    gm = GameManager()
    gm.initialize()

    for pid in [1, 2]:
        p = PlayerID(pid)
        gm.take_operation(PlayerOpDrawCard(count=5, player_id=p))
        gm.take_operation(PlayerOpRedrawCard(count=4, player_id=p))
        gm.take_operation(
            PlayerOpSelectActiveCharacter(character_id=CharacterID(1), player_id=p)
        )

    return gm


def _test_roll():
    gm = get_gm_to_roll()

    for pid in [1, 2]:
        p = PlayerID(pid)
        gm.take_operation(PlayerOpRollDice(count=8, player_id=p))
        gm.take_operation(PlayerOpRerollDice(count=4, player_id=p))

    assert gm.game_state.control_state.phase_status == PhaseStatusEnum.RA_start
    assert len(gm.game_state.get_phase_events()) == 0
