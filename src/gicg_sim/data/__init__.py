from gicg_sim.data.loader import read_data

""" data """
character_data: list = read_data("character")
effect_data: list = read_data("effect")
action_card_data: list = read_data("action_card")


""" map name to data """
character_mapping: dict[str, dict] = {
    c["name"]: c for c in character_data
}
effect_mapping: dict[str, dict] = {
    e["name"]: e for e in effect_data
}
action_card_mapping: dict[str, dict] = {
    a["name"]: a for a in action_card_data
}

__all__ = [
    # datas
    'character_data',
    'effect_data',
    'action_card_data',
    # mapping
    'character_mapping',
    'effect_mapping',
    'action_card_mapping',
    # common
    'read_data',
]
