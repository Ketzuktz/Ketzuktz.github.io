import bs4  # type: ignore
from datatype import ColumnDataDict
from web import request_soup


def validate_character_data(data: ColumnDataDict) -> bool:
    assert data["name"] is not None
    assert data["element"] is not None
    assert data["weapon"] is not None
    assert data["max_HP"] is not None
    assert data["faction"] is not None
    assert data["href"] is not None

    assert data["icon_image_key"] is not None
    assert data["icon_image_src"] is not None

    return True


def get_character_data_online():
    return


if __name__ == "__main__":
    href = "/wiki/Abyss_Lector:_Fathomless_Flames_(Character_Card)"
    soup = request_soup(href)

    content_wrapper = soup.find(id="mw-content-text")
    content: bs4.Tag = content_wrapper.find_all("div", class_="mw-parser-output")[0]

    h2_element = soup.select_one('h2:has(.mw-headline#Skills)')

    skill_table = h2_element.find_next_sibling('table')

    print(skill_table)
