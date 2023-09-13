import sys

__version__ = "0.0.1"

if sys.version_info < (3, 7):
    raise RuntimeError("gicg_sim requires Python 3.7 or later")
