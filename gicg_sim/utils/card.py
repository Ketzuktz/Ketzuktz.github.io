from .data import cards_data


class Card:
    character_card_dict = None

    def build_character_dict():
        assert "character" in cards_data, "No character data"
        Card.character_card_dict = dict(
            [(character["name"], character) for character in cards_data["character"]]
        )

    def create_character(name: str) -> dict:
        if Card.character_card_dict is None:
            Card.build_character_dict()
        assert name in Card.character_card_dict, f"No such character: {name}"
        return Card.character_card_dict[name]
