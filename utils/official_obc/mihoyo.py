import typing
from typing import TypedDict

from web import request_obc_response


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


class _ListWrapperDict(TypedDict):
    list: typing.List[typing.Any]


class MihoyoGeneralData(TypedDict):
    retcode: int
    message: str
    data: _ListWrapperDict


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
