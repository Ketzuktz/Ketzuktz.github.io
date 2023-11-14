from game_init import prepare_game

from gicg_sim.basic.die import DieTypeEnum
from gicg_sim.basic.event.operation import DEBUG_GetDie, PlayerOpUseSkill
from gicg_sim.basic.subtypes import CharacterID, PlayerID, SkillID
from gicg_sim.game.manager import GameManager


def test_Diluc_normal_attack() -> None:
    game: GameManager = prepare_game()

    game.take_operation(DEBUG_GetDie({DieTypeEnum.omni: 1}, PlayerID(1)))

    game.take_operation(
        PlayerOpUseSkill(
            skill_id=SkillID("Tempered Sword"),
            player_id=PlayerID(1),
            character_id=CharacterID(1),
        )
    )

    assert game.game_state.side2.characters[0].hp == 8
    assert game.game_state.side1.characters[0].energy == 1


def test_Diluc_elemental_skill() -> None:
    game: GameManager = prepare_game()

    game.take_operation(DEBUG_GetDie({DieTypeEnum.omni: 3}, PlayerID(1)))

    game.take_operation(
        PlayerOpUseSkill(
            skill_id=SkillID("Searing Onslaught"),
            player_id=PlayerID(1),
            character_id=CharacterID(1),
        )
    )

    assert game.game_state.side2.characters[0].hp == 7
