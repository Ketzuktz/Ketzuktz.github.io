from enum import Enum

from gicg_sim.types.subtypes import CharacterID, PlayerID


class SysEventEnum(Enum):
    DrawCard = 1
    RedrawCard = 2
    SelectActiveCharacter = 3
    RollDice = 4
    RerollDice = 5
    CombatAction = 6
    DeclareRoundEnd = 7
    UseSkill = 8


class SystemEventBase:
    def __init__(
        self,
        event_type: SysEventEnum,
        player_id: PlayerID,
        pre_sys_event: SysEventEnum | None = None,
    ) -> None:
        self.event_type = event_type
        self.player_id = player_id
        self.pre_event = pre_sys_event

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, SystemEventBase):
            return False
        if self.event_type != __value.event_type:
            return False
        if self.player_id != __value.player_id:
            return False
        if (
            self.pre_event is not None
            and __value.pre_event is not None
            and self.pre_event != __value.pre_event
        ):
            return False
        return True


class SysEventDrawCard(SystemEventBase):
    def __init__(self, count: int = 1, **kwargs) -> None:
        super().__init__(SysEventEnum.DrawCard, **kwargs)
        self.count: int = count


class SysEventRedrawCard(SystemEventBase):
    def __init__(self, *, min_count: int = 0, max_count: int = 1, **kwargs) -> None:
        super().__init__(SysEventEnum.RedrawCard, **kwargs)
        self.min_count: int = min_count
        self.max_count: int = max_count


class SysEventSelectActiveCharacter(SystemEventBase):
    def __init__(self, selected_id: CharacterID, **kwargs) -> None:
        super().__init__(SysEventEnum.SelectActiveCharacter, **kwargs)
        self.active_character_id: CharacterID = selected_id


class SysEventRollDice(SystemEventBase):
    def __init__(self, count: int = 8, **kwargs) -> None:
        super().__init__(SysEventEnum.RollDice, **kwargs)
        self.count: int = count


class SysEventRerollDice(SystemEventBase):
    def __init__(self, *, min_count: int = 0, max_count: int = 8, **kwargs) -> None:
        super().__init__(SysEventEnum.RerollDice, **kwargs)
        self.min_count: int = min_count
        self.max_count: int = max_count


class SysEventCombatAction(SystemEventBase):
    def __init__(self, **kwargs) -> None:
        super().__init__(SysEventEnum.CombatAction, **kwargs)


class SysEventDeclareRoundEnd(SystemEventBase):
    def __init__(self, player_id: PlayerID, **kwargs) -> None:
        super().__init__(SysEventEnum.DeclareRoundEnd, player_id=player_id, **kwargs)
