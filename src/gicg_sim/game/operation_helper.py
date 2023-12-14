from copy import deepcopy

from gicg_sim.basic.die import DieState
from gicg_sim.basic.event.base import (EventBase, EventDrawCard,
                                       EventEffectDamage,
                                       EventEffectElementGauge,
                                       EventEffectEnergyGet, EventRedrawCard,
                                       EventRerollDice, EventRollDice,
                                       EventSelectActiveCharacter,
                                       EventUseSkill)
from gicg_sim.basic.event.operation import (DEBUG_GetDie, DEBUG_GetEnergy,
                                            PlayerOpDrawCard,
                                            PlayerOperationBase,
                                            PlayerOperationEnum,
                                            PlayerOpRedrawCard,
                                            PlayerOpRerollDice,
                                            PlayerOpRollDice,
                                            PlayerOpSelectActiveCharacter,
                                            PlayerOpUseSkill)
from gicg_sim.basic.subtypes import OperationID
from gicg_sim.game.state.side import GameSideState
from gicg_sim.model.prototype.cost import CostType
from gicg_sim.model.prototype.die import DieCostPrototype
from gicg_sim.model.prototype.effect import DamageType


class OperationHelper:
    OPERATION_GLOBAL_ID = 0

    @staticmethod
    def decorate_operation(operation: PlayerOperationBase) -> PlayerOperationBase:
        op = deepcopy(operation)
        op.operation_id = OperationID(OperationHelper.OPERATION_GLOBAL_ID)
        OperationHelper.OPERATION_GLOBAL_ID += 1
        return op

    @staticmethod
    def map_operation_events(
        operation: PlayerOperationBase, context: GameSideState
    ) -> list[EventBase]:
        events: list[EventBase] = []
        match operation.op_type:
            case PlayerOperationEnum.DrawCard:
                assert isinstance(operation, PlayerOpDrawCard)
                events.append(
                    EventDrawCard(count=operation.count, player_id=operation.player_id)
                )
            case PlayerOperationEnum.RedrawCard:
                assert isinstance(operation, PlayerOpRedrawCard)
                events.append(
                    EventRedrawCard(
                        count=operation.count, player_id=operation.player_id
                    )
                )
            case PlayerOperationEnum.SelectActiveCharacter:
                assert isinstance(operation, PlayerOpSelectActiveCharacter)
                events.append(
                    EventSelectActiveCharacter(
                        selected_id=operation.character_id,
                        player_id=operation.player_id,
                    )
                )
            case PlayerOperationEnum.RollDice:
                assert isinstance(operation, PlayerOpRollDice)
                events.append(
                    EventRollDice(count=operation.count, player_id=operation.player_id)
                )
            case PlayerOperationEnum.RerollDice:
                assert isinstance(operation, PlayerOpRerollDice)
                events.append(
                    EventRerollDice(
                        count=operation.count, player_id=operation.player_id
                    )
                )
            case PlayerOperationEnum.UseSkill:
                assert isinstance(operation, PlayerOpUseSkill)

                mapped_result = OperationHelper.map_operation_useskill(
                    operation, context
                )
                events.extend(mapped_result)
            case PlayerOperationEnum.DEBUG_GetDie:
                # DEBUG, set all omni
                # DEBUG operation should not be recorded
                assert isinstance(operation, DEBUG_GetDie)
                dop_get_die: DEBUG_GetDie = operation
                context.die_state.append(dop_get_die.die_dict)
            case PlayerOperationEnum.DEBUG_GetEnergy:
                assert isinstance(operation, DEBUG_GetEnergy)
                dop_get_energy: DEBUG_GetEnergy = operation
                character = context.get_character_by_id(dop_get_energy.character_id)
                character.energy += dop_get_energy.energy
            case _:
                raise ValueError(f"Unknown operation type ({operation.op_type}).")
        return events

    @staticmethod
    def map_operation_useskill(
        operation: PlayerOpUseSkill, context: GameSideState
    ) -> list[EventBase]:
        output: list[EventBase] = []
        skill = context.get_skill_by_id(operation.skill_id)
        cost = skill.cost

        OperationHelper.check_cost_affordable(cost, context)

        output.append(
            EventUseSkill(skill_prototype=skill, player_id=operation.player_id)
        )

        for effect in skill.effect:
            if effect.damage is not None:
                output.append(
                    EventEffectDamage(
                        damage=effect.damage, player_id=operation.player_id
                    )
                )
                match effect.damage.type:
                    case DamageType.physical:
                        pass
                    case DamageType.piercing:
                        pass
                    case _:
                        output.append(
                            EventEffectElementGauge(
                                effect.damage.target,
                                effect.damage.type,
                                damage=True,
                                player_id=operation.player_id,
                            )
                        )
            elif effect.energy is not None:
                output.append(
                    EventEffectEnergyGet(
                        energy=effect.energy,
                        character_id=context.active_id,
                        player_id=operation.player_id,
                    )
                )
            elif effect.buff_get is not None:
                pass
            elif effect.lua_plugin is not None:
                pass
            else:
                raise ValueError(f"Unknown effect type {effect}.")

        return output

    @staticmethod
    def check_cost_affordable(cost: CostType, context: GameSideState) -> None:
        if cost.energy is not None and cost.energy > 0:
            if not cost.energy <= context.active_character.energy:
                raise ValueError("Not enough energy.")

        if not OperationHelper.check_die_affordable(cost.die, context.die_state):
            raise ValueError(
                f"Not enough die, need {cost.die}, but current is {context.die_state}."
            )

    @staticmethod
    def check_die_affordable(cost: DieCostPrototype, current_: DieState) -> bool:
        current = deepcopy(current_)
        basic_elements = ["pyro", "hydro", "cryo", "electro", "anemo", "geo", "dendro"]
        for die_type in basic_elements:
            if not hasattr(cost, die_type) or getattr(cost, die_type) is None:
                continue
            count = getattr(cost, die_type)
            if count > 0 and current[die_type] > 0:
                use_count = min(count, current[die_type])  # type: ignore
                current[die_type] -= use_count  # type: ignore
                count -= use_count
            if count > 0 and current["omni"] > 0:
                use_count = min(count, current["omni"])
                current["omni"] -= use_count
                count -= use_count

            if count > 0:
                return False

        if cost.matching is not None and cost.matching > 0:
            for die_type in basic_elements:
                if current[die_type] < cost.matching:
                    return False
        return True
