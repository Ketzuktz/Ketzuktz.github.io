from random import randint

from gicg_sim.basic.enums import PhaseStatusEnum, TossType
from gicg_sim.basic.event.base import (EventBase, EventEffectDamage,
                                       EventEffectElementGauge,
                                       EventEffectEnergyGet, EventEnum,
                                       EventRollDice,
                                       EventSelectActiveCharacter,
                                       EventUseSkill, SysEventSwitchPhase)
from gicg_sim.basic.event.operation import PlayerOperationBase
from gicg_sim.basic.subtypes import PlayerID
from gicg_sim.game.condition import CONTROL_CONDITIONS
from gicg_sim.game.operation_helper import OperationHelper
from gicg_sim.game.state.side import GameSideState
from gicg_sim.model.prototype.effect import SideType as EffectSideType


def tossType2playerID(toss: TossType) -> PlayerID:
    if toss == TossType.RANDOM:
        return PlayerID(randint(1, 2))
    elif toss == TossType.CONST_1:
        return PlayerID(1)
    else:
        return PlayerID(2)


class GameState:
    def __init__(self) -> None:
        self.side1 = GameSideState()
        self.side2 = GameSideState()
        self.sides = (self.side1, self.side2)
        self._phase_status = PhaseStatusEnum.Preparation
        self.active_player: PlayerID = PlayerID(-1)

        self.operation_history: list[PlayerOperationBase] = []

        self.event_history: list[EventBase] = []
        self.event_history_phase_begin: int = 0

    def initialize(self, toss: TossType = TossType.CONST_1) -> None:
        self._phase_status = PhaseStatusEnum.Preparation
        self.side1.reset()
        self.side2.reset()
        self.active_player = tossType2playerID(toss)

    def initialize_player(self, player: PlayerID, **kwargs):
        side = self.get_side_absolute(player)
        side.initialize(**kwargs)

    def _update_control_state(self) -> bool:
        for c in CONTROL_CONDITIONS:
            if c.current_phase == self.phase_status:
                if c.validate(self.get_phase_events()):
                    self._phase_status = c.target_phase
                    self.event_history.append(
                        SysEventSwitchPhase(
                            phase=self.phase_status,
                        )
                    )
                    self.event_history_phase_begin = len(self.event_history)
                    return True
        return False

    def get_phase_events(self) -> list[EventBase]:
        return self.event_history[self.event_history_phase_begin :]

    def take_operation(self, operation: PlayerOperationBase):
        self.operation_history.append(operation)
        side = self.get_side_absolute(operation.player_id)
        events = OperationHelper.map_operation_events(operation, side)
        self.apply_events(events)

        while True:
            if not self._update_control_state():
                break

    def get_side_relative(
        self, player: PlayerID, side_type: EffectSideType
    ) -> GameSideState:
        match side_type:
            case EffectSideType.self:
                return self.get_side_absolute(player)
            case EffectSideType.enemy:
                return self.get_side_absolute(PlayerID(3 - int(player)))
            case _:
                raise NotImplementedError()

    def get_side_absolute(self, player: PlayerID) -> GameSideState:
        if player == PlayerID(1):
            return self.side1
        elif player == PlayerID(2):
            return self.side2
        else:
            raise ValueError("Invalid player ID")

    def apply_events(self, events: list[EventBase]):
        for e_raw in events:
            assert e_raw.player_id is not None
            side: GameSideState = self.get_side_absolute(e_raw.player_id)

            self.event_history.append(e_raw)

            match e_raw.event_type:
                case EventEnum.DrawCard:
                    pass
                case EventEnum.RedrawCard:
                    pass
                case EventEnum.SelectActiveCharacter:
                    assert isinstance(e_raw, EventSelectActiveCharacter)
                    e_selectactive: EventSelectActiveCharacter = e_raw
                    assert e_selectactive.active_character_id is not None
                    side._switch_character(e_selectactive.active_character_id)
                case EventEnum.RollDice:
                    assert isinstance(e_raw, EventRollDice)
                    e_rolldice: EventRollDice = e_raw
                    side._roll_dice(e_rolldice.count)
                    pass
                case EventEnum.RerollDice:
                    pass
                case EventEnum.UseSkill:
                    assert isinstance(e_raw, EventUseSkill)
                    e_us: EventUseSkill = e_raw
                    side = self.get_side_absolute(e_us.player_id)
                    side._pay_cost(e_us.skill.cost)
                case EventEnum.EffectDamage:
                    assert isinstance(e_raw, EventEffectDamage)
                    e_ed: EventEffectDamage = e_raw
                    side = self.get_side_relative(
                        e_ed.player_id, e_ed.damage.target.side  # type: ignore
                    )
                    side._damaged(e_ed.damage)
                case EventEnum.EffectEnergyGet:
                    assert isinstance(e_raw, EventEffectEnergyGet)
                    e_eg: EventEffectEnergyGet = e_raw
                    side._get_energy(e_eg.energy)
                    pass
                case EventEnum.EffectElementGauge:
                    assert isinstance(e_raw, EventEffectElementGauge)
                case _:
                    raise ValueError(
                        f"Invalid event type {e_raw.event_type} for {e_raw}"
                    )

    @property
    def phase_status(self) -> PhaseStatusEnum:
        return self._phase_status
