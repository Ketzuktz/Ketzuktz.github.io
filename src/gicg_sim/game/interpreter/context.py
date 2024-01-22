from gicg_sim.game.interpreter.character import CharacterDelegate
from gicg_sim.game.state import GameState


class InterpreterContext():
    def __init__(self, state: GameState) -> None:
        self.__state = state

    @property
    def current_character(self) -> CharacterDelegate:
        current_event = self.__state.current_event
        current_character_id = current_event.character_id
        assert current_character_id is not None, "current_character_id is None"
        return CharacterDelegate(self.__state, current_character_id)
