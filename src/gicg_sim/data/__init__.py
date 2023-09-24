from gicg_sim.data.loader import read_data

""" data """
character_data: list = read_data("character")
effect_data: dict = read_data("effect")

__all__ = [
    'character_data',
    'effect_data',
    'read_data',
]
