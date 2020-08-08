from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.pitt_public_algorithms_task_force import (
    PittPublicAlgorithmsTaskForceSpider,
)

test_response = file_response(
    join(dirname(__file__), "files", "pitt_public_algorithms_task_force.html"),
    url="https://www.cyber.pitt.edu/community-meetings",
)
spider = PittPublicAlgorithmsTaskForceSpider()

freezer = freeze_time("2020-06-12")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()

# def test_tests():
#    print("Please write some tests for this spider or at least disable this one.")
#    assert False
"""
Uncomment below
"""


def test_title():
    assert parsed_items[0]["title"] == "Public Meeting"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2020, 3, 10, 17, 30)


def test_end():
    assert parsed_items[0]["end"] == datetime(2020, 3, 10, 19, 30)


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Homewood-Brushton Branch YMCA\n2nd Floor Conference Room",
        "address": "7140 Bennett Street\nPittsburgh, PA 15208",
    }


def test_source():
    assert parsed_items[0]["source"] == "https://www.cyber.pitt.edu/community-meetings"


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "href": "https://pitt.co1.qualtrics.com/jfe/form/SV_6fiAWakicanFJ9r",
            "title": "Please RSVP",
        }
    ]


def test_classification():
    assert parsed_items[0]["classification"] == NOT_CLASSIFIED


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
