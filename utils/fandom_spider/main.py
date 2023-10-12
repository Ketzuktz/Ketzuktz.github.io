import yaml
from process import (HierarchicalTableTreeNode_to_dict,
                     extract_hierarchical_tables_tree)
from web import extract_content, request_soup  # type: ignore

DATASRC_BASEURL = "https://genshin-impact.fandom.com"
DATASRC_CARDLIST_PATH = "/wiki/Genius_Invokation_TCG/Card_List"

EXPECTED_TYPES = [
    "Character_Cards",
    "Equipment_Cards",
    "Support_Cards",
    "Event_Cards",
    "Summons",
]


if __name__ == "__main__":
    soup = request_soup(DATASRC_CARDLIST_PATH)

    content = extract_content(soup)

    assert content is not None

    def h2_check(x):
        return not (x.name == "h2" and next(x.children)["id"] not in EXPECTED_TYPES)

    root_node = extract_hierarchical_tables_tree(content, h2_check)

    generated = HierarchicalTableTreeNode_to_dict(root_node)

    with open("fetched_data.yml", mode="w", encoding="utf-8") as f:
        yaml.dump(generated["root"], f, sort_keys=False)

    # with open("enums.yml", mode="w", encoding="utf-8") as f:
    #     enums = dict([(k, sorted(list(s))) for k, s in ENUM_SETS.items()])
    #     yaml.dump(enums, f, sort_keys=False)
