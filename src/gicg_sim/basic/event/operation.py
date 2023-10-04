from enum import Enum

from gicg_sim.basic.subtypes import (CardID, CharacterID, OperationID,
                                     PlayerID, SkillID)


class PlayerOperationEnum(Enum):
    DrawCard = 1
    RedrawCard = 2
    SelectActiveCharacter = 3
    RollDice = 4
    RerollDice = 5
    UseSkill = 6
    PlayCard = 7
    ElementalTuning = 8
    SwitchCharacter = 9
    DeclareRoundEnd = 10


class PlayerOperationBase:
    def __init__(
        self,
        op_type: PlayerOperationEnum,
        player_id: PlayerID,
        operation_id: OperationID | None = None,
    ) -> None:
        self.op_type: PlayerOperationEnum = op_type
        self.player_id: PlayerID = player_id
        self.operation_id: OperationID | None = operation_id

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, PlayerOperationBase):
            return False
        if self.op_type != __value.op_type:
            return False
        if self.player_id != __value.player_id:
            return False
        if self.operation_id != __value.operation_id:
            return False
        return True


class PlayerOpDrawCard(PlayerOperationBase):
    def __init__(
        self, *args, count: int, player_id: PlayerID, op_id: OperationID | None = None
    ) -> None:
        self.count: int = count
        super().__init__(PlayerOperationEnum.DrawCard, player_id, op_id, *args)


class PlayerOpRedrawCard(PlayerOperationBase):
    def __init__(
        self, *args, count: int, player_id: PlayerID, op_id: OperationID | None = None
    ) -> None:
        self.count: int = count
        super().__init__(PlayerOperationEnum.RedrawCard, player_id, op_id, *args)


class PlayerOpSelectActiveCharacter(PlayerOperationBase):
    def __init__(
        self,
        *args,
        character_id: CharacterID,
        player_id: PlayerID,
        op_id: OperationID | None = None,
    ) -> None:
        self.character_id: CharacterID = character_id
        super().__init__(
            PlayerOperationEnum.SelectActiveCharacter, player_id, op_id, *args
        )


class PlayerOpRollDice(PlayerOperationBase):
    def __init__(
        self, *args, count: int, player_id: PlayerID, op_id: OperationID | None = None
    ) -> None:
        self.count: int = count
        super().__init__(PlayerOperationEnum.RollDice, player_id, op_id, *args)


class PlayerOpRerollDice(PlayerOperationBase):
    def __init__(
        self, *args, count: int, player_id: PlayerID, op_id: OperationID | None = None
    ) -> None:
        self.count: int = count
        super().__init__(PlayerOperationEnum.RerollDice, player_id, op_id, *args)


class PlayerOpUseSkill(PlayerOperationBase):
    def __init__(
        self,
        *args,
        skill_id: SkillID,
        player_id: PlayerID,
        op_id: OperationID | None = None,
    ) -> None:
        self.skill_id: SkillID = skill_id
        super().__init__(PlayerOperationEnum.UseSkill, player_id, op_id, *args)


class PlayerOpPlayCard(PlayerOperationBase):
    def __init__(
        self,
        *args,
        card_id: CardID,
        player_id: PlayerID,
        op_id: OperationID | None = None,
    ) -> None:
        self.card_id: CardID = card_id
        super().__init__(PlayerOperationEnum.PlayCard, player_id, op_id, *args)


class PlayerOpElementalTuning(PlayerOperationBase):
    def __init__(
        self,
        *args,
        card_id: CardID,
        player_id: PlayerID,
        op_id: OperationID | None = None,
    ) -> None:
        self.card_id: CardID = card_id
        super().__init__(PlayerOperationEnum.ElementalTuning, player_id, op_id, *args)


class PlayerOpSwitchCharacter(PlayerOperationBase):
    def __init__(
        self,
        *args,
        character_id: int,
        player_id: PlayerID,
        op_id: OperationID | None = None,
    ) -> None:
        self.character_id: int = character_id
        super().__init__(PlayerOperationEnum.SwitchCharacter, player_id, op_id, *args)


class PlayerOpDeclareRoundEnd(PlayerOperationBase):
    def __init__(
        self, *args, player_id: PlayerID, op_id: OperationID | None = None
    ) -> None:
        super().__init__(PlayerOperationEnum.DeclareRoundEnd, player_id, op_id, *args)
