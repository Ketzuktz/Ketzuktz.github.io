from .character import Character


class UserBoard:
    def __init__(self) -> None:
        self.charaters = []
        self.hand = []
        self.dies = {}
        self.effects = []

    def add_character(self, name: str):
        self.charaters.append(Character.create(name))
