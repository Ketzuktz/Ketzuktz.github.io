from gicg_sim.basic.enums import PhaseStatusEnum
from gicg_sim.basic.event.operation import (PlayerOpDrawCard,
                                            PlayerOpRedrawCard,
                                            PlayerOpRerollDice,
                                            PlayerOpRollDice,
                                            PlayerOpSelectActiveCharacter)
from gicg_sim.basic.subtypes import CharacterID, PlayerID
from gicg_sim.game.manager import GameManager


def prepare_game() -> GameManager:
    pile_names = ['Sweet Madame' for _ in range(30)]

    gm = GameManager()
    gm.initialize()
    gm.initialize_player_card(["Diluc"], PlayerID(1), draw_pile_names=pile_names)
    gm.initialize_player_card(["Diluc"], PlayerID(2), draw_pile_names=pile_names)

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

    assert gm.game_state.phase_status == PhaseStatusEnum.Roll
    assert len(gm.game_state.get_phase_events()) == 0

    for pid in [1, 2]:
        p = PlayerID(pid)
        gm.take_operation(PlayerOpRollDice(count=8, player_id=p))
        gm.take_operation(PlayerOpRerollDice(count=4, player_id=p))

    return gm
