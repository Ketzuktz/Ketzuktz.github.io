from enum import Enum

from gicg_sim.basic.enums import PhaseStatusEnum
from gicg_sim.basic.subtypes import CharacterID, EventID, PlayerID, SkillID


class EventEnum(Enum):
    DrawCard = 1
    RedrawCard = 2
    SelectActiveCharacter = 3
    RollDice = 4
    RerollDice = 5
    CombatAction = 6
    DeclareRoundEnd = 7
    UseSkill = 8

    SYS_SwitchPhaseRound = 100


class EventBase:
    def __init__(
        self,
        event_type: EventEnum,
        player_id: PlayerID | None = None,
        event_id: EventID | None = None,
        skill_id: SkillID | None = None,
        system_flag: bool = False,
    ) -> None:
        self.event_type = event_type
        self.player_id = player_id
        self.event_id = event_id
        self.skill_id = skill_id
        self.is_system = system_flag

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, EventBase):
            return False
        if self.event_type != __value.event_type:
            return False
        if self.player_id != __value.player_id:
            return False
        if self.event_id != __value.event_id:
            return False
        if self.is_system != __value.is_system:
            return False
        return True


class EventDrawCard(EventBase):
    def __init__(self, count: int = 1, **kwargs) -> None:
        super().__init__(EventEnum.DrawCard, **kwargs)
        self.count: int = count


class EventRedrawCard(EventBase):
    def __init__(self, count: int = 1, **kwargs) -> None:
        super().__init__(EventEnum.RedrawCard, **kwargs)
        self.count: int = count


class EventSelectActiveCharacter(EventBase):
    def __init__(self, selected_id: CharacterID | None = None, **kwargs) -> None:
        super().__init__(EventEnum.SelectActiveCharacter, **kwargs)
        self.active_character_id: CharacterID | None = selected_id


class EventRollDice(EventBase):
    def __init__(self, count: int = 8, **kwargs) -> None:
        super().__init__(EventEnum.RollDice, **kwargs)
        self.count: int = count


class EventRerollDice(EventBase):
    def __init__(self, *, count: int = 8, **kwargs) -> None:
        super().__init__(EventEnum.RerollDice, **kwargs)
        self.count: int = count


class EventCombatAction(EventBase):
    def __init__(self, **kwargs) -> None:
        super().__init__(EventEnum.CombatAction, **kwargs)


class EventDeclareRoundEnd(EventBase):
    def __init__(self, player_id: PlayerID, **kwargs) -> None:
        super().__init__(EventEnum.DeclareRoundEnd, player_id=player_id, **kwargs)


class SystemEventBase(EventBase):
    def __init__(
        self,
        event_type: EventEnum,
        player_id: PlayerID | None = None,
        event_id: EventID | None = None,
    ) -> None:
        super().__init__(event_type, player_id, event_id, system_flag=True)

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, SystemEventBase):
            return False
        return super().__eq__(__value)


class SysEventSwitchPhase(SystemEventBase):
    def __init__(self, phase: PhaseStatusEnum, **kwargs) -> None:
        super().__init__(EventEnum.SYS_SwitchPhaseRound, **kwargs)
        self.phase: PhaseStatusEnum = phase
