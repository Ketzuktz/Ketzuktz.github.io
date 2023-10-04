from copy import deepcopy

from gicg_sim.basic.event.base import (EventBase, EventDrawCard,
                                       EventRedrawCard,
                                       EventSelectActiveCharacter)
from gicg_sim.basic.event.operation import (PlayerOpDrawCard,
                                            PlayerOperationBase,
                                            PlayerOperationEnum,
                                            PlayerOpRedrawCard,
                                            PlayerOpSelectActiveCharacter)
from gicg_sim.basic.subtypes import OperationID


class OperationHelper:
    OPERATION_GLOBAL_ID = 0

    @staticmethod
    def decorate_operation(operation: PlayerOperationBase) -> PlayerOperationBase:
        op = deepcopy(operation)
        op.operation_id = OperationID(OperationHelper.OPERATION_GLOBAL_ID)
        OperationHelper.OPERATION_GLOBAL_ID += 1
        return op

    @staticmethod
    def map_operation_events(operation: PlayerOperationBase) -> list[EventBase]:
        events: list[EventBase] = []
        match operation.op_type:
            case PlayerOperationEnum.DrawCard:
                assert isinstance(
                    operation, PlayerOpDrawCard
                )
                events.append(
                    EventDrawCard(count=operation.count,
                                  player_id=operation.player_id)
                )
            case PlayerOperationEnum.RedrawCard:
                assert isinstance(
                    operation, PlayerOpRedrawCard
                )
                events.append(
                    EventRedrawCard(
                        count=operation.count, player_id=operation.player_id
                    )
                )
            case PlayerOperationEnum.SelectActiveCharacter:
                assert isinstance(
                    operation, PlayerOpSelectActiveCharacter
                )
                events.append(
                    EventSelectActiveCharacter(
                        selected_id=operation.character_id,
                        player_id=operation.player_id,
                    )
                )
            case _:
                raise ValueError(
                    f"Unknown operation type ({operation.op_type}).")
        return events
