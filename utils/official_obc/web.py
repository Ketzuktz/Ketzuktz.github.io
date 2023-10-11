from urllib.parse import urljoin

import requests
from fake_useragent import UserAgent  # type: ignore

MIHOYO_OBC_BASEURL = "https://api-static.mihoyo.com/common/blackboard/ys_obc/"
MIHOYO_WIKI_BASEURL = "https://api-takumi-static.mihoyo.com/hoyowiki/"

session = requests.session()

ua = UserAgent()
session.headers["User-Agent"] = ua.random


def request_obc_response(url: str, params: dict) -> requests.Response:
    full_url = urljoin(MIHOYO_OBC_BASEURL, url)
    response = session.get(full_url, params=params)
    if response.status_code != 200:
        raise RuntimeError(
            f"Request to {full_url} failed with status code {response.status_code}"
        )
    print(f"Request to {url} success")

    return response


def request_hoyowiki_response(url: str, params: dict) -> requests.Response:
    full_url = urljoin(MIHOYO_WIKI_BASEURL, url)
    response = session.get(full_url, params=params)
    if response.status_code != 200:
        raise RuntimeError(
            f"Request to {full_url} failed with status code {response.status_code}"
        )
    print(f"Request to {url} success")

    return response
