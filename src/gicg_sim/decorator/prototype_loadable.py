from abc import ABCMeta, abstractmethod


def prototype_loadable(cls):
    def __init__(self, data: dict, *args, **kwargs):
        self._prototype = data
        super(cls, self).__init__(*args, **kwargs)

    cls.__init__ = __init__
    return cls


class PrototypeBase(metaclass=ABCMeta):
    @property
    @abstractmethod
    def _prototype(self) -> dict:
        ...
