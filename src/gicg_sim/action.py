from enum import Enum
from typing import Optional

from gicg_sim.card import CardBase


class ActionType(Enum):
    USE_SKILL = 1
    SWITCH_CHARACTERS = 2
    PLAY_CARD = 3
    ELEMENTAL_TUNING = 4
    DECLARE_ROUND_END = 5


class Action:
    def __init__(self, type: ActionType) -> None:
        self.type: ActionType = type
        self.card: Optional[CardBase] = None

    def set_card(self, card: CardBase) -> None:
        self.card = card

    def __str__(self) -> str:
        return f"Action(type={self.type}, card={self.card})"
