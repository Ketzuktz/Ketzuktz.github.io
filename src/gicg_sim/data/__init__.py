from gicg_sim.data.loader import read_data

""" data """
character_data: list = read_data("character")
effect_data: dict = read_data("effect")

""" map name to data """
character_mapping: dict[str, dict] = {
    c["name"]: c for c in character_data
}
effect_mapping: dict[str, dict] = {
    e["name"]: e for e in effect_data
}

__all__ = [
    'character_data',
    'effect_data',
    'character_mapping',
    'effect_mapping',
    # common
    'read_data',
]
