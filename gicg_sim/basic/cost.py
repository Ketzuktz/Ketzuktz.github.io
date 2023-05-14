from typing import Optional

from typing_extensions import TypedDict


class DieCost(TypedDict):
    Same: Optional[int]
    Pyro: Optional[int]
    Hydro: Optional[int]
    Anemo: Optional[int]
    Electro: Optional[int]
    Dendro: Optional[int]
    Cryo: Optional[int]
    Geo: Optional[int]
    Any: Optional[int]
