import typing
from typing import TypedDict

from mihoyo.request import request_wiki


class _ModuleComponentAttribute(TypedDict):
    key: str
    value: typing.List[str]


class _ModuleComponentData(TypedDict):
    moduleName: str
    layout_: str
    name: str
    common_img: str
    gold_img: str
    life: int
    life_bg: int
    energy: int
    energy_bg: int
    attr: typing.List[_ModuleComponentAttribute]
    repeated: bool


class _ModuleComponent(TypedDict):
    component_id: str
    layout: str
    data: str  # MihoyoContentModuleData
    style: str


class _ModuleData(TypedDict):
    name: str
    is_poped: bool
    components: typing.List[_ModuleComponent]
    id: str
    is_customize_name: bool
    is_abstract: bool
    is_show_switch: bool
    switch: bool
    desc: str
    repeated: bool
    is_submodule: bool
    origin_module_id: str


class _PageData(TypedDict, total=False):
    id: str
    name: str
    desc: str
    icon_url: str
    header_img_url: str
    modules: typing.List[_ModuleData]

    filter_values: typing.Set

    menu_id: str
    menu_name: str
    menus: typing.List[typing.Any]

    version: str

    template_layout: typing.Any
    template_id: str

    langs: typing.List[str]
    lang: str

    alias_name: str
    ext: typing.Any


class _InnerPageWrapper(TypedDict):
    page: _PageData


class MihoyoWikiResponse(TypedDict):
    retcode: int
    message: str
    data: _InnerPageWrapper


def get_page(content_id: int) -> _PageData:
    url = "genshin/wapi/entry_page"
    params = {
        "app_sn": "ys_obc",
        "entry_page_id": str(content_id),
        "lang": "zh-cn",
    }

    data: MihoyoWikiResponse = request_wiki(url, params)

    if "page" not in data["data"]:
        raise RuntimeError(
            f"Request to {url} [{content_id}] failed with \
unexpected data: {data['data']}"
        )

    content: _PageData = data["data"]["page"]
    return content
