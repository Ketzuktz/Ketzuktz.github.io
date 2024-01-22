from functools import singledispatchmethod
from typing import Any

from gicg_sim.game.interpreter.utils import lua_vararg_callable
from gicg_sim.game.state.data import GameState


class SubEventItemDelegate:
    def __init__(self, state: GameState, attr_name: str) -> None:
        self.__state = state
        self.__attr_name = attr_name

    @singledispatchmethod
    def increment(self, *args) -> Any:
        return NotImplementedError(
            f"increment is not implemented for this input type: {type(args[0])}"
        )

    @increment.register
    def _increment_named(self, name: str, value: int | float) -> Any:
        pass

    @increment.register
    def _increment_unnamed(self, value: int | float) -> Any:
        pass

    @singledispatchmethod
    def set(self, *args) -> Any:
        return NotImplementedError(
            f"set is not implemented for this input type: {type(args[0])}"
        )

    @set.register
    def _set_named(self, name: str, value: int | float) -> Any:
        pass

    @set.register
    def _set_unnamed(self, value: int | float) -> Any:
        pass


class SubEventDelegate:
    __valid_sub_event_item_names: set[str] = {"token", "damage", "heal"}

    def __init__(self, state: GameState, name: str | None = None) -> None:
        self.__state = state
        self.__item_name = name

    def __getattribute__(self, attr_name: str) -> Any:
        if attr_name in SubEventDelegate.__valid_sub_event_item_names:
            return SubEventItemDelegate(self.__state, attr_name)
        else:
            return super().__getattribute__(attr_name)


class SubEventSetDelegate:
    def __init__(self, state: GameState) -> None:
        self.__state = state

    @lua_vararg_callable
    def create(self, name: str | None = None) -> SubEventDelegate:
        sub_event = SubEventDelegate(self.__state, name=name)
        return sub_event
