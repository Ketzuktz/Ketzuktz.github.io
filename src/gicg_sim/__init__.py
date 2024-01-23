import sys

__version__ = "0.0.1"

if sys.version_info < (3, 7):
    raise RuntimeError("gicg_sim requires Python 3.7 or later")

from gicg_sim.data import character_data, read_data
from gicg_sim.game import enums, game

__all__ = [
    'read_data',
    'character_data',
    'enums',
    'game',
]
