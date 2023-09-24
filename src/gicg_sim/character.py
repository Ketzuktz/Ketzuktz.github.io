from gicg_sim.decorator import PrototypeBase, prototype_loadable


@prototype_loadable
class Character(PrototypeBase):
    def __init__(self) -> None:
        self.status = {...}
