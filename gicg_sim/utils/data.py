import yaml
from importlib_resources import files

raw_basepath = files("gicg_sim.data")
cards_basepath = files("gicg_sim.data.cards")


def read_cards(card_type: str) -> dict:
    text = cards_basepath.joinpath(f"{card_type}.yaml").read_text()
    data = yaml.load(text, Loader=yaml.SafeLoader)
    return data


def read_raw(data_name: str) -> dict:
    text = raw_basepath.joinpath(f"{data_name}.yaml").read_text()
    data = yaml.load(text, Loader=yaml.SafeLoader)
    return data


""" cards """
card_types = ["character"]

cards_data = dict([(ctype, read_cards(ctype)) for ctype in card_types])

""" raw """

effect_data = read_raw("effect")

dietype_data = read_raw("die_type")
