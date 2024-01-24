from gicg_sim.game.config import UserDeckConfig
from gicg_sim.model.character import Character


def instantiate_characters(character: str) -> Character:
    return Character.load(character)

class Deck:
    def __init__(self, config: UserDeckConfig) -> None:
        self.config = config
        self.stack_cards = []
        self.hand_cards = []
        self.characters = [instantiate_characters(character) for character in config.characters]
        self.active_character_id = -1
        self.assistances = []
        self.summons = []

