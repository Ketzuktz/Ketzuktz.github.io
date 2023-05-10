from pathlib import Path
from typing import Dict

import yaml
from importlib_resources import files  # type: ignore [import]

raw_basepath: Path = files("gicg_sim.data")
cards_basepath: Path = files("gicg_sim.data.cards")


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

cards_data: Dict[str, dict] = dict([(ctype, read_cards(ctype)) for ctype in card_types])

""" raw """

effect_data: dict = read_raw("effect")
