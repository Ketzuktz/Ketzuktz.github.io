from gicg_sim.game.action import ActionType
from gicg_sim.game.config import UserDeckConfig
from gicg_sim.game.deck import Deck
from gicg_sim.game.event import Event, EventType
from gicg_sim.game.token import Token


class Game:
    def __init__(self, user_configs: list[UserDeckConfig]) -> None:
        assert len(user_configs) == 2
        self.user_configs = user_configs
        self.decks = [Deck(config) for config in user_configs]
        self.event_history: list[Event] = []
        

    def start(self) -> None:
        self.event_history.clear()
        self.event_history.append(Event(EventType.GAME_START))
        self.event_tokens
        return

    def event_tokens(self, event_type: EventType) -> list[Token]:
        match event_type:
            case EventType.GAME_START:
                return [Token("active_character_not_selected"), Token("card_not_drawn")]
            case EventType.ROUND_START:
                return []
            case _:
                return []

    def step(self) -> None:
        return 
