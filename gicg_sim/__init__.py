import pkgutil
import sys
from importlib.abc import Loader
from typing import Optional

__version__ = "0.0.1"

if sys.version_info < (3, 7):
    raise RuntimeError("gicg_sim requires Python 3.7 or later")

__all__ = []

for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    __all__.append(module_name)
    __loader__: Optional[Loader] = \
        loader.find_module(module_name)  # type: ignore [call-arg]
    if __loader__ is not None:
        _module = __loader__.load_module(module_name)
        globals()[module_name] = _module
