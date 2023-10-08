from gicg_sim.basic.event.operation import PlayerOperationBase


class Mutation:
    def __init__(self, src_operation: PlayerOperationBase):
        self.src_operation = src_operation
