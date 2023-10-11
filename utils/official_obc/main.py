import json
import os

import mihoyo
from mihoyo import get_mihoyo_channel_list_data

if not os.path.exists('output.d'):
    os.mkdir('output.d')

CARD_LISTS_CHANNEL_ID = 231

if __name__ == '__main__':
    if not os.path.exists('output.d/card_lists.json'):
        card_lists = get_mihoyo_channel_list_data(CARD_LISTS_CHANNEL_ID)

        with open('output.d/card_lists.json', 'w', encoding='utf-8') as f:
            json.dump(card_lists, f, ensure_ascii=False, indent=4)

    with open('output.d/card_lists.json', 'r', encoding='utf-8') as f:
        card_lists = json.load(f)

    for card_list in card_lists['children']:
        subpath = f'output.d/{card_list["name"]}'
        if not os.path.exists(subpath):
            os.mkdir(subpath)

        for card in card_list['list']:
            card_name = card['title']
            card_id = card['content_id']

            card_data = mihoyo.get_mihoyo_content_data(card_id)

            card_path = f'{subpath}/{card_name}.json'
            with open(card_path, 'w', encoding='utf-8') as f:
                json.dump(card_data, f, ensure_ascii=False, indent=4)

            break
