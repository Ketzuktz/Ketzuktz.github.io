from gicg_sim.basic.subtypes import CharacterID
from gicg_sim.game.interpreter.token import TokenSetDelegate
from gicg_sim.game.state import GameState


class CharacterDelegate():
    def __init__(self, state: GameState, character_id: CharacterID) -> None:
        self.__state = state
        self.__character_id = character_id


    @property
    def tokens(self) -> TokenSetDelegate:
        return TokenSetDelegate(self.__state, bind_character=self.__character_id)
