import json
import typing
from typing import TypedDict

from mihoyo.wiki.base import get_page


class CardInfo(TypedDict):
    id: str
    name: str
    desc: str
    icon_url: str

    infos: typing.Dict[str, typing.Any]


def get_card(card_id: int) -> CardInfo:
    card_page = get_page(card_id)

    infos: typing.Dict[str, typing.Any] = {}

    for module in card_page['modules']:
        if len(module['components']) != 1:
            raise RuntimeError(
                f"Incorrect module components length: {len(module['components'])}"
            )

        module_name = module['name']

        component = module['components'][0]
        module_id = component['component_id']

        module_data = json.loads(component['data'])

        info_item = {
            'name': module_name,
            'id': module_id,
            'data': module_data,
        }

        infos[module_name] = infos.get(module_name, []) + [info_item]

    output: CardInfo = {
        'id': card_page['id'],
        'name': card_page['name'],
        'desc': card_page['desc'],
        'icon_url': card_page['icon_url'],
        'infos': infos,
    }

    return output
