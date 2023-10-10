from mihoyo import get_mihoyo_channel_list_data

CARD_LISTS_CHANNEL_ID = 231

if __name__ == '__main__':
    card_lists = get_mihoyo_channel_list_data(CARD_LISTS_CHANNEL_ID)

    for card_list_info in card_lists['children']:
        print(f'{card_list_info["name"]} ({card_list_info["id"]}) \
has {len(card_list_info["list"])} items.')
