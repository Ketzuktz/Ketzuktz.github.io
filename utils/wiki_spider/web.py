from urllib.parse import urljoin

import bs4  # type: ignore
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent  # type: ignore

DATASRC_BASEURL = "https://genshin-impact.fandom.com"

session = requests.session()

ua = UserAgent()
session.headers["User-Agent"] = ua.random


def request_soup(url: str) -> bs4.BeautifulSoup:
    response = session.get(urljoin(DATASRC_BASEURL, url))
    if response.status_code != 200:
        raise RuntimeError(
            f"Request to {url} failed with status code {response.status_code}"
        )
    print(f"Request to {url} success")

    return BeautifulSoup(response.text, "html.parser")


def extract_content(soup: bs4.BeautifulSoup) -> bs4.Tag:
    content_wrapper = soup.find(id="mw-content-text")
    contents: list[bs4.Tag] = content_wrapper.find_all("div", class_="mw-parser-output")
    assert len(contents) == 1
    return contents[0]
