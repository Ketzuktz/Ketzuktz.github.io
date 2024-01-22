import lupa


def lua_vararg_callable(func):
    def wrapper(self=None, lua_table={}, *args, **kwargs):
        if isinstance(lua_table, lupa.LuaTable):
            if self is None:
                return func(**lua_table)
            else:
                return func(self, *lua_table)
        else:
            return func(self, lua_table, *args, **kwargs)
    return wrapper
