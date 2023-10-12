from typing import TypedDict


class ColumnDataDict(TypedDict, total=False):
    href: str
    icon_image_key: str
    icon_image_src: str
    name: str
    max_HP: int
    element: str
    weapon: str
    faction: list[str]
    group: str
    cost: dict[str, int]
    effect_comment: str
    usages: int


ColumnDataOrder = [
    "name",
    "group",
    "element",
    "weapon",
    "max_HP",
    "usages",
    "cost",
    "faction",
    "href",
    "icon_image_key",
    "icon_image_src",
    "effect_comment",
]


def sort_column_data_dict(data: ColumnDataDict) -> ColumnDataDict:
    sorted_dict = {
        k: data[k]  # type: ignore
        for k in sorted(data, key=lambda x: ColumnDataOrder.index(x))
    }
    return sorted_dict  # type: ignore
