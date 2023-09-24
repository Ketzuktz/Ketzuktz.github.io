import typing
from pathlib import Path

import yaml
from importlib_resources import files  # type: ignore [import]

_data_basepath: Path = files("gicg_sim.data")


def read_data(data_name: str) -> typing.Any:
    text = _data_basepath.joinpath(f"{data_name}.yaml").read_text()
    data = yaml.load(text, Loader=yaml.SafeLoader)
    return data
