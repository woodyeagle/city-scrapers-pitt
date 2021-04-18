from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import BOARD
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.pitt_sports import PittSportsSpider

test_response = file_response(
    join(dirname(__file__), "files", "pitt_sports.html"),
    url="http://www.pgh-sea.com/index.php?path=info-meet-sea",
)
spider = PittSportsSpider()

freezer = freeze_time("2020-12-11")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_title():
    assert parsed_items[0]["title"] == "SEA Board Meeting"


def test_description():
    assert parsed_items[0]["description"] == "Cancelled"


def test_start():
    assert parsed_items[0]["start"] == datetime(2020, 1, 9, 10, 30)


def test_status():
    assert parsed_items[0]["status"] == "cancelled"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "DLCC222",
        "address": "1000 Fort Duquesne Blvd, Pittsburgh, PA 15222",
    }


def test_source():
    assert (
        parsed_items[0]["source"]
        == "http://www.pgh-sea.com/index.php?path=info-meet-sea"
    )


def test_links():
    assert parsed_items[0]["links"] == [{"href": "", "title": ""}]


def test_classification():
    assert parsed_items[0]["classification"] == BOARD


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
