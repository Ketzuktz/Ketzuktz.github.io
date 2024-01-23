from gicg_sim.game.config import UserDeckConfig
from gicg_sim.game.deck import Deck
from gicg_sim.game.enums import GameState

class Game:
    def __init__(self, user_configs: list[UserDeckConfig]) -> None:
        assert len(user_configs) == 2
        self.user_configs = user_configs
        self.decks = [Deck(config) for config in user_configs]
        self.event_history = []
    
    @staticmethod
    def start() -> 'Game':
        return Game([])
    
    