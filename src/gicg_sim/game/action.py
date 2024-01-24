from enum import Enum

class ActionType(Enum):
    SelectActiveCharacter = "SelectActiveCharacter"
    RedrawCard = "DrawCard"
    RollDice = "RollDice"


ACTION_RESOURCES = {
    ActionType.SelectActiveCharacter: "active_character_not_selected",
    ActionType.RedrawCard: "redraw_card_not_selected",
}