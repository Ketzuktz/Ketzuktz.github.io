from gicg_sim.types.event import EventBase, EventEnum
from gicg_sim.types.event import EventDrawCard
from gicg_sim.types.operation import PlayerOperationBase, PlayerOperationEnum
from gicg_sim.types.operation import PlayerOpDrawCard
from gicg_sim.types.subtypes import OperationID
from copy import deepcopy

class OperationHelper:
    OPERATION_GLOBAL_ID = 0
    
    @staticmethod
    def decorate_operation(operation: PlayerOperationBase) -> PlayerOperationBase:
        op = deepcopy(operation)
        op.operation_id = OperationID(OperationHelper.OPERATION_GLOBAL_ID)
        OperationHelper.OPERATION_GLOBAL_ID += 1
        return op
    
    @staticmethod
    def map_operation_event(operation: PlayerOperationBase) -> list[EventBase]:
        events = []
        match operation.op_type:
            case PlayerOperationEnum.DrawCard:
                assert isinstance(operation, PlayerOpDrawCard), f"operation with type {operation.op_type} must be PlayerOpDrawCard."
                events.append(EventDrawCard(count = operation.count, player_id = operation.player_id))
            case _:
                raise ValueError('Unknown operation type.')
        return events