import typing
from typing import TypedDict

from web import request_hoyowiki_response, request_obc_response


class MihoyoChannelData(TypedDict):
    id: int
    name: str
    parent_id: int
    depth: int
    ch_ext: str
    children: typing.List["MihoyoChannelData"]  # type: ignore
    list: typing.List[typing.Any]
    layout: str
    entry_limit: int
    hidden: bool


class MihoyoPageModuleAttribute(TypedDict):
    key: str
    value: typing.List[str]


class MihoyoPageModuleData(TypedDict):
    moduleName: str
    layout_: str
    name: str
    common_img: str
    gold_img: str
    life: int
    life_bg: int
    energy: int
    energy_bg: int
    attr: typing.List[MihoyoPageModuleAttribute]
    repeated: bool


class MihoyoPageComponent(TypedDict):
    component_id: str
    layout: str
    data: str   # MihoyoContentModuleData
    style: str


class MihoyoPageData(TypedDict):
    name: str
    is_poped: bool
    components: typing.List[MihoyoPageComponent]
    id: str
    is_customize_name: bool
    is_abstract: bool
    is_show_switch: bool
    switch: bool
    desc: str
    repeated: bool
    is_submodule: bool
    origin_module_id: str


class MihoyoGeneralInnerWrapper(TypedDict, total=False):
    list: typing.List[typing.Any]
    page: MihoyoPageData


class MihoyoGeneralData(TypedDict):
    retcode: int
    message: str
    data: MihoyoGeneralInnerWrapper


def get_mihoyo_channel_list_data(channel_id: int) -> MihoyoChannelData:
    list_url = "v1/home/content/list"

    list_params = {
        "app_sn": "ys_obc",
        "channel_id": str(channel_id),
    }

    response = request_obc_response(list_url, list_params)

    data: MihoyoGeneralData = response.json()

    if data["retcode"] != 0:
        raise RuntimeError(
            f"Request to {list_url} [{channel_id}] failed with \
retcode {data['retcode']}: {data['message']}"
        )

    if len(data["data"]["list"]) != 1:
        raise RuntimeError(
            f"Request to {list_url} [{channel_id}] failed with \
unexpected data: {data['data']}"
        )

    channel_data: MihoyoChannelData = data["data"]["list"][0]

    if channel_data["id"] != channel_id:
        raise RuntimeError(
            f"Request to {list_url} [{channel_id}] failed with \
unexpected channel_id: {channel_data['id']}"
        )

    return channel_data


def get_mihoyo_content_data(content_id: int) -> MihoyoPageData:
    url = "genshin/wapi/entry_page"
    params = {
        "app_sn": "ys_obc",
        "entry_page_id": str(content_id),
        "lang": "zh-cn",
    }

    response = request_hoyowiki_response(url, params)

    data: MihoyoGeneralData = response.json()

    if data["retcode"] != 0:
        raise RuntimeError(
            f"Request to {url} [{content_id}] failed with \
retcode {data['retcode']}: {data['message']}"
        )

    if 'page' not in data['data']:
        raise RuntimeError(
            f"Request to {url} [{content_id}] failed with \
unexpected data: {data['data']}"
        )

    content: MihoyoPageData = data["data"]["page"]
    return content
