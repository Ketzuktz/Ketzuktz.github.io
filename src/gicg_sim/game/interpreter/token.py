
from gicg_sim.basic.subtypes import CharacterID, PlayerID
from gicg_sim.game.interpreter.utils import lua_vararg_callable
from gicg_sim.game.state import GameState


class TokenSetDelegate():
    def __init__(self, state: GameState, bind_side: PlayerID | None = None, bind_character: CharacterID | None = None) -> None:
        self.__state = state
        self.__bind_side = bind_side
        self.__bind_character = bind_character

    @lua_vararg_callable
    def get(self, name: str, life_cycle: str = "round", default: int = 0):
        token_placeholder = {
            "side": self.__bind_side,
            "character": self.__bind_character,
            "name": name,
            "life_cycle": life_cycle,
            "value": default,
        }
        return token_placeholder
