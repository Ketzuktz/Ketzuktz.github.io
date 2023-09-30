from enum import Enum

from gicg_sim.types.subtypes import CharacterID, OperationID, PlayerID


class OpEnum(Enum):
    DrawCard = 1
    RedrawCard = 2
    SelectActiveCharacter = 3
    RollDice = 4
    RerollDice = 5
    CombatAction = 6
    DeclareRoundEnd = 7
    UseSkill = 8


class Operation:
    def __init__(
        self,
        op_type: OpEnum,
        player_id: PlayerID,
        operation_id: OperationID | None = None,
        pre_op: OpEnum | None = None,
    ) -> None:
        self.op_type = op_type
        self.player_id = player_id
        self.operation_id = operation_id
        self.pre_op = pre_op

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Operation):
            return False
        if self.op_type != __value.op_type:
            return False
        if self.player_id != __value.player_id:
            return False
        if (
            self.operation_id is not None
            and __value.operation_id is not None
            and self.operation_id != __value.operation_id
        ):
            return False
        if (
            self.pre_op is not None
            and __value.pre_op is not None
            and self.pre_op != __value.pre_op
        ):
            return False
        return True


class OpDrawCard(Operation):
    def __init__(self, count: int = 1, **kwargs) -> None:
        super().__init__(OpEnum.DrawCard, **kwargs)
        self.count: int = count


class OpRedrawCard(Operation):
    def __init__(self, *, min_count: int = 0, max_count: int = 1, **kwargs) -> None:
        super().__init__(OpEnum.RedrawCard, **kwargs)
        self.min_count: int = min_count
        self.max_count: int = max_count


class OpSelectActiveCharacter(Operation):
    def __init__(self, selected_id: CharacterID, **kwargs) -> None:
        super().__init__(OpEnum.SelectActiveCharacter, **kwargs)
        self.active_character_id: CharacterID = selected_id


class OpRollDice(Operation):
    def __init__(self, count: int = 8, **kwargs) -> None:
        super().__init__(OpEnum.RollDice, **kwargs)
        self.count: int = count


class OpRerollDice(Operation):
    def __init__(self, *, min_count: int = 0, max_count: int = 8, **kwargs) -> None:
        super().__init__(OpEnum.RerollDice, **kwargs)
        self.min_count: int = min_count
        self.max_count: int = max_count


class OpCombatAction(Operation):
    def __init__(self, **kwargs) -> None:
        super().__init__(OpEnum.CombatAction, **kwargs)


class OpDeclareRoundEnd(Operation):
    def __init__(self, player_id: PlayerID, **kwargs) -> None:
        super().__init__(OpEnum.DeclareRoundEnd, player_id=player_id, **kwargs)
