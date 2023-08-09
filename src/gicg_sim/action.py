from __future__ import annotations

from enum import Enum

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

    def __repr__(self) -> str:
        return f"Action(type={self.type})"


class ActionSkill(Action):
    def __init__(self, skillID: int, skillName: str = "<Undefined Skill>") -> None:
        super().__init__(ActionType.USE_SKILL)
        self.skillID: int = skillID
        self.skillName: str = skillName

    def __repr__(self) -> str:
        return f"ActionSkill(skillID={self.skillID}, skillName={self.skillName})"


class ActionSwitch(Action):
    def __init__(
        self, characterID: int, characterName: str = "<Undefined Character>"
    ) -> None:
        super().__init__(ActionType.SWITCH_CHARACTERS)
        self.characterID: int = characterID
        self.characterName: str = characterName

    def __repr__(self) -> str:
        output_str = f"ActionSwitch(characterID={self.characterID},"\
                     f" characterName={self.characterName})"
        return output_str


class ActionPlayCard(Action):
    def __init__(self, card: CardBase) -> None:
        super().__init__(ActionType.PLAY_CARD)
        self.card: CardBase = card

    def __repr__(self) -> str:
        return f"ActionPlayCard(card={self.card})"


class ActionElementalTuning(Action):
    def __init__(self, card: CardBase) -> None:
        super().__init__(ActionType.ELEMENTAL_TUNING)
        self.card: CardBase = card

    def __repr__(self) -> str:
        return f"ActionElementalTuning(card={self.card})"


class ActionDeclareRoundEnd(Action):
    def __init__(self) -> None:
        super().__init__(ActionType.DECLARE_ROUND_END)

    def __repr__(self) -> str:
        return "ActionDeclareRoundEnd()"
