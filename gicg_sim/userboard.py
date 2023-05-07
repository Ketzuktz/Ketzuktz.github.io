from .utils.card import Card


class UserBoard:
    def __init__(self) -> None:
        self.charaters = []
        self.hand = []
        self.dies = {}
        self.effects = []

    def add_character(self, name: str):
        self.charaters.append(Card.create_character(name))
