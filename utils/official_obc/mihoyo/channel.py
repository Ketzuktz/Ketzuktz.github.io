import typing
from typing import TypedDict

from mihoyo.request import request_obc


class MihoyoChannelItem(TypedDict):
    id: int
    name: str
    parent_id: int
    depth: int
    ch_ext: str
    children: typing.List["MihoyoChannelItem"]  # type: ignore
    list: typing.List[typing.Any]
    layout: str
    entry_limit: int
    hidden: bool


class _InnerListWrapper(TypedDict):
    list: typing.List[MihoyoChannelItem]


class MihoyoChannelResponse(TypedDict):
    retcode: int
    message: str
    data: _InnerListWrapper


def get_channel(channel_id: int) -> MihoyoChannelItem:
    list_url = "v1/home/content/list"

    list_params = {
        "app_sn": "ys_obc",
        "channel_id": str(channel_id),
    }

    response: MihoyoChannelResponse = request_obc(list_url, list_params)

    if len(response["data"]["list"]) != 1:
        raise RuntimeError(
            f"Request to {list_url} [{channel_id}] failed with \
unexpected data: {response['data']}"
        )

    channel_data: MihoyoChannelItem = response["data"]["list"][0]

    if channel_data["id"] != channel_id:
        raise RuntimeError(
            f"Request to {list_url} [{channel_id}] failed with \
unexpected channel_id: {channel_data['id']}"
        )

    return channel_data
