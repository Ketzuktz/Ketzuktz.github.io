from typing import Any, TypedDict
from urllib.parse import urljoin

import requests
from fake_useragent import UserAgent  # type: ignore


class MihoyoResponse(TypedDict):
    retcode: int
    message: str
    data: Any


MIHOYO_OBC_BASEURL = "https://api-static.mihoyo.com/common/blackboard/ys_obc/"
MIHOYO_WIKI_BASEURL = "https://api-takumi-static.mihoyo.com/hoyowiki/"

session = requests.session()

ua = UserAgent()
session.headers["User-Agent"] = ua.random


def request(
    url: str, params: dict, baseurl: str = MIHOYO_OBC_BASEURL
) -> MihoyoResponse:
    full_url = urljoin(baseurl, url)
    response = session.get(full_url, params=params)
    if response.status_code != 200:
        raise RuntimeError(
            f"Request to {full_url} failed with status code {response.status_code}"
        )
    print(f"Request to {url} success")

    data: MihoyoResponse = response.json()

    if data["retcode"] != 0:
        raise RuntimeError(
            f"Request to {full_url} failed with \
retcode {data['retcode']}: {data['message']}"
        )

    return data


def request_obc(url: str, params: dict) -> MihoyoResponse:
    return request(url, params, MIHOYO_OBC_BASEURL)


def request_wiki(url: str, params: dict) -> MihoyoResponse:
    return request(url, params, MIHOYO_WIKI_BASEURL)
