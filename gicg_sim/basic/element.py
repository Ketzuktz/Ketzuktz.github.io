from typing_extensions import Literal

element_names = ["Pyro", "Hydro", "Anemo", "Electro", "Dendro", "Cryo", "Geo"]
element_count = len(element_names)

ElementType = Literal["Pyro", "Hydro", "Anemo", "Electro", "Dendro", "Cryo", "Geo"]

# class ElementType(TypedDict):
#     Pyro: int
#     Hydro: int
#     Anemo: int
#     Electro: int
#     Dendro: int
#     Cryo: int
#     Geo: int


die_element_names = [
    "Omni",
    "Pyro",
    "Hydro",
    "Anemo",
    "Electro",
    "Dendro",
    "Cryo",
    "Geo",
]
die_element_count = len(die_element_names)
