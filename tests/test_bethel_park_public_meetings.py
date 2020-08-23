from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.utils import file_response
from dateutil import tz
from freezegun import freeze_time

from city_scrapers.spiders.bethel_park_public_meetings import BethelParkSpider

test_response = file_response(
    join(dirname(__file__), "files", "bethel_park_public_meetings.ics"),
    url="http://bethelpark.net/?plugin=all-in-one-event-calendar&controller=ai1ec_exporter_controller&action=export_events&ai1ec_cat_ids=42&no_html=true"
)
spider = BethelParkSpider()

freezer = freeze_time("2020-08-23")
freezer.start()
parsed_items = [item for item in spider.parse(test_response)]
freezer.stop()


def get_test_sample():
    """Return a sample of meetings from the scraped calendar.

    Currently, we return the six latest meetings.
    """
    return sorted(parsed_items, key=lambda e: e["start"], reverse=True)[:6]


def test_event_count():
    assert len(parsed_items) == 28


def test_titles():
    expected_titles = [
        "Council Committee Meeting",
        "Shade Tree Commission Meeting",
        "Shade Tree Commission Meeting",
        "Zoning Hearing Board",
        "Planning & Zoning Commission Workshop Meeting",
        "Municipal Council Committee Meeting July 27th, 2020 7:30 PM – Public Hearings starting at 6:30 PM"
    ]
    for (event, expected_title) in zip(get_test_sample(), expected_titles):
        assert event["title"] == expected_title


def test_start():
    tzinfo = tz.gettz("America/New_York")
    expected_start_dates = [
        datetime(year=2021, month=1, day=27, hour=19, minute=30, tzinfo=tzinfo),
        datetime(year=2020, month=11, day=18, hour=18, minute=30, tzinfo=tzinfo),
        datetime(year=2020, month=9, day=16, hour=18, minute=30, tzinfo=tzinfo),
        datetime(year=2020, month=9, day=8, hour=19, minute=30, tzinfo=tzinfo),
        datetime(year=2020, month=7, day=29, hour=19, minute=00, tzinfo=tzinfo),
        datetime(year=2020, month=7, day=27, hour=18, minute=30, tzinfo=tzinfo)
    ]
    for (event, expected_start) in zip(get_test_sample(), expected_start_dates):
        assert event["start"].year == expected_start.year
        assert event["start"].month == expected_start.month
        assert event["start"].day == expected_start.day
        assert event["start"].hour == expected_start.hour
        assert event["start"].minute == expected_start.minute
        assert event["start"].tzname() == expected_start.tzname()


def test_end():
    # The reason the first five end dates are None: the source returns these events
    # with an end time equal to the start time. In this case, the spider sets "None"
    # for the end time so that the scrapy pipeline can fill it a default. Only the
    # six event has a different end date set, in this specific data set.
    tzinfo = tz.gettz("America/New_York")
    expected_end_dates = [
        None,
        None,
        None,
        None,
        None,
        datetime(year=2020, month=7, day=27, hour=21, minute=00, tzinfo=tzinfo)
    ]
    for (event, expected_end) in zip(get_test_sample(), expected_end_dates):
        if expected_end is None:
            assert event["end"] is None
        else:
            assert event["end"].year == expected_end.year
            assert event["end"].month == expected_end.month
            assert event["end"].day == expected_end.day
            assert event["end"].hour == expected_end.hour
            assert event["end"].minute == expected_end.minute
            assert event["end"].tzname() == expected_end.tzname()

def test_location():
    expected_locations = [
        "Council Caucus Room @ 5100 West Library Ave. Bethel Park, PA 15102",
        "Municipal Building Council Chambers @ 5100 West Library Ave Bethel Park, PA 15102",
        # Note there are slight variations in how the locations are reported, e.g. missing a comma in this case
        "Municipal Building Council Chambers @ 5100 West Library Ave Bethel Park PA 15102",
        "5100 West Library Ave. Bethel Park, PA 15102 @ Council Chambers",
        "5100 West Library Ave. Bethel Park, PA 15102 @ Council Chambers",
        "Municipal Building Council Chambers @ 5100 West Library Road"
    ]
    for (event, expected_location) in zip(get_test_sample(), expected_locations):
        assert event["location"] == expected_location

"""
def test_classification():
    for item in parsed_items:
        assert item["classification"] == BOARD


def test_all_day():
    for item in parsed_items:
        assert item["all_day"] is False


# The 'id' or 'source' fields aren't customized currently, so these are commented out.
# def test_id():
#     assert parsed_items[0]["id"] == "EXPECTED ID"

# def test_source():
#     assert parsed_items[0]["source"] == "EXPECTED URL"
"""
