import typing


def prototype_loadable(cls):
    def __init__(self, data: dict, *args, **kwargs):
        self._prototype = data
        super(cls, self).__init__(*args, **kwargs)

    cls.__init__ = __init__
    return cls


class PrototypeBase:
    def __init__(self) -> None:
        self._prototype: dict = {}
        self._state: typing.Any = None
