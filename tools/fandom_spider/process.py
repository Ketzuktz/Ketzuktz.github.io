import typing
from typing import Callable, Optional

import bs4  # type: ignore

from tools.fandom_spider.datatype import ColumnDataDict, sort_column_data_dict


class HierarchicalTableTreeNode:
    def __init__(
        self,
        name: str,
        level: int = -1,
        children: list["HierarchicalTableTreeNode"] = [],
        table: Optional[bs4.Tag] = None,
        parent: Optional["HierarchicalTableTreeNode"] = None,
    ):
        self.name: str = name
        self.level: int = level
        self.children: list["HierarchicalTableTreeNode"] = children
        self.table: Optional[bs4.Tag] = table
        self.parent: Optional["HierarchicalTableTreeNode"] = parent


ENUM_SETS: dict[str, set[str]] = {
    "Element": set(),
    "Weapon": set(),
    "Faction": set(),
    "Group": set(),
    "Cost": set(),
}


def extract_a_titles_texts(cell: bs4.Tag) -> tuple[list[str], list[str]]:
    a_tags = cell.find_all("a")
    values, texts = [], []

    for a in a_tags:
        title_value: str = a.get("title")
        value = title_value.removesuffix("Card").strip()
        text = a.get_text()
        if value not in values:
            values.append(value)
            texts.append(text)

    return values, texts


def extract_span_titles_texts(cell: bs4.Tag) -> tuple[list[str], list[str]]:
    span_tags = cell.select("span.tcg-cost")
    values, texts = [], []

    for s in span_tags:
        title_value: str = s.get("title")
        value = title_value.removesuffix("Card").strip()
        text = s.get_text()
        if value not in values:
            values.append(value)
            texts.append(text)

    return values, texts


def process_general_column(cell: bs4.Tag, header: str) -> ColumnDataDict:
    """Process a column tag into a string"""
    match header:
        case "Icon":
            a_tag = cell.find("a")
            href_value: str = a_tag.get("href")
            data_image_key_value: str = a_tag.find("img").get("data-image-key")
            data_src_value: str = a_tag.find("img").get("data-src")

            return {
                "href": href_value,
                "icon_image_key": data_image_key_value,
                "icon_image_src": data_src_value,
            }
        case "Name":
            a_tag = cell.find("a")
            href_value = a_tag.get("href")
            name = a_tag.get_text(strip=True)
            return {
                "href": href_value,
                "name": name,
            }
        case "Health":
            value = int(cell.get_text(strip=True))
            return {
                "max_HP": value,
            }
        case "Element":
            values, *_ = extract_a_titles_texts(cell)
            assert len(values) == 1

            ENUM_SETS["Element"].add(values[0])

            return {
                "element": values[0],
            }
        case "Weapon":
            values, *_ = extract_a_titles_texts(cell)
            assert len(values) == 1

            ENUM_SETS["Weapon"].add(values[0])

            return {
                "weapon": values[0],
            }
        case "Faction":
            values, *_ = extract_a_titles_texts(cell)
            # assert len(values) == 1

            if len(values) == 0:
                values.append("Undefined")

            for v in values:
                ENUM_SETS["Faction"].add(v)

            return {
                "faction": values,
            }
        case "Group":
            values, *_ = extract_a_titles_texts(cell)
            # assert len(values) >= 1

            group_value = " ".join(values) if len(values) >= 1 else "Undefined"
            ENUM_SETS["Group"].add(group_value)

            return {
                "group": group_value,
            }
        case "Cost":
            cost_types, values = extract_span_titles_texts(cell)
            assert len(values) >= 1

            for ct in cost_types:
                ENUM_SETS["Cost"].add(ct)

            costs = dict(zip(cost_types, [int(v) for v in values]))

            return {
                "cost": costs,
            }
        case "Effect":
            return {"effect_comment": cell.get_text(strip=True)}
        case "Usage(s)":
            usage = cell.get_text(strip=True)
            if len(usage) > 0:
                return {"usages": int(usage)}
            else:
                return {}
        case _:
            print(header)
            print(cell)
            exit(0)


def process_general_table(table: bs4.Tag) -> list[ColumnDataDict]:
    """Process a table tag into a list of dict"""
    headers = [header.text.strip() for header in table.find_all("th")]
    result: list[ColumnDataDict] = []

    for row in table.find("tbody").find_all("tr"):
        cells = row.find_all("td")
        if len(cells) == 0:
            continue

        data_dict: ColumnDataDict = {}
        for i, header in enumerate(headers):
            try:
                new_data = process_general_column(cells[i], header)
            except Exception as e:
                print(header, cells[i])
                raise e

            for k, v in new_data.items():
                if k in data_dict:
                    assert data_dict[k] == v, f"key {k} not match, "  # type: ignore
                    f"prev: {data_dict[k]}, current: {v}"  # type: ignore
                # else:
                # data_dict[k] = v
            data_dict.update(new_data)

        sorted_dict = sort_column_data_dict(data_dict)
        result.append(sorted_dict)  # type: ignore

    return result


def HierarchicalTableTreeNode_to_dict(
    node: HierarchicalTableTreeNode,
) -> dict[str, typing.Any]:
    node_content: typing.Any = (
        process_general_table(node.table)
        if node.table is not None
        else [HierarchicalTableTreeNode_to_dict(child)  # type: ignore
              for child in node.children]
    )

    return {node.name: node_content}


def extract_hierarchical_tables_tree(
    root: bs4.Tag, pred: Callable[[bs4.Tag], bool] = lambda _: True
) -> HierarchicalTableTreeNode:
    def get_h_id(x):
        return next(x.children)["id"]

    def name_str_guard(x: bs4.Tag) -> str:
        return x.name if x.name is not None else ""

    root_node = HierarchicalTableTreeNode("root", level=0, children=[], table=None)
    current_node = root_node

    for i in root.children:
        if name_str_guard(i).startswith("h") and pred(i):
            h_level = int(i.name[1:])
            h_id = get_h_id(i)
            print(f"Found h{h_level} {h_id}")

            while h_level <= current_node.level:
                assert current_node.parent is not None
                current_node = current_node.parent

            new_node = HierarchicalTableTreeNode(
                h_id, level=h_level, children=[], parent=current_node
            )
            current_node.children.append(new_node)
            current_node = new_node
        elif i.name == "table":
            current_node.table = i
        else:
            continue

    return root_node
