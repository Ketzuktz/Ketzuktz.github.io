import json
import os

import yaml
from mihoyo.channel import get_channel
from mihoyo.wiki.card import get_card
from mihoyo.wiki.smarter import (CardInfoType, DictContext,
                                 card_info_extract_data)

yaml.SafeDumper.org_represent_str = yaml.SafeDumper.represent_str


def repr_str(dumper, data):
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.org_represent_str(data)


yaml.add_representer(str, repr_str, Dumper=yaml.SafeDumper)

if not os.path.exists("output.d"):
    os.mkdir("output.d")

if not os.path.exists("output_data.d"):
    os.mkdir("output_data.d")

CARD_LISTS_CHANNEL_ID = 231

if __name__ == "__main__":
    if not os.path.exists("output.d/card_lists.json"):
        card_lists = get_channel(CARD_LISTS_CHANNEL_ID)

        with open("output.d/card_lists.json", "w", encoding="utf-8") as f:
            json.dump(card_lists, f, ensure_ascii=False, indent=4)

    with open("output.d/card_lists.json", "r", encoding="utf-8") as f:
        card_lists = json.load(f)

    context: DictContext = DictContext()

    for card_list in card_lists["children"]:
        card_type = card_list["name"]
        subpath_raw = os.path.join("output.d", card_type)
        subpath_data = os.path.join("output_data.d", card_type)

        if not os.path.exists(subpath_raw):
            os.mkdir(subpath_raw)
        if not os.path.exists(subpath_data):
            os.mkdir(subpath_data)

        for card in card_list["list"]:
            card_name = card["title"]
            card_id = card["content_id"]
            card_path = os.path.join(subpath_raw, f"{card_name}.json")
            card_data_path = os.path.join(subpath_data, f"{card_name}.yml")

            if not os.path.exists(card_path):
                card_data = get_card(card_id)

                with open(card_path, "w", encoding="utf-8") as f:
                    json.dump(card_data, f, ensure_ascii=False, indent=4)

            # if not os.path.exists(card_data_path):
            with open(card_path, "r", encoding="utf-8") as f:
                card_data = json.load(f)

            data = card_info_extract_data(card_data, CardInfoType(card_type), context)

            with open(card_data_path, "w", encoding="utf-8") as f:
                yaml.dump(data, f, allow_unicode=True, sort_keys=False)

    with open("output_data.d/dictionary.yml", "w", encoding="utf-8") as f:
        yaml.safe_dump(context.data, f, allow_unicode=True)
