import unicodedata
from urllib.parse import urlencode

import ics
from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider


class BethelParkSpider(CityScrapersSpider):
    name = "bethel_park_public_meetings"
    agency = "Municipality of Bethel Park"
    timezone = "America/New_York"

    # The Bethel Park webpage using a WordPress plugin called
    # "All-in-one Event Calendar". This plugin exposes an endpoint
    # through which you can downloading different views of a calendar,
    # via a GET request. The below configuration of request parameters
    # fetches all public meeting events on the Bethel Park calendar
    # (events in category "42")
    params = {
        "plugin": "all-in-one-event-calendar",
        "controller": "ai1ec_exporter_controller",
        "action": "export_events",
        "ai1ec_cat_ids": "42",
        "no_html": "true"
    }
    start_urls = ["http://bethelpark.net/?" + urlencode(params)]

    def normalize(self, s):
        if not s:
            return None
        return unicodedata.normalize("NFKD", s).strip()

    def parse(self, response):
        raw_calendar = response.body.decode("utf-8")
        ics_calendar = ics.Calendar(raw_calendar)

        for event in ics_calendar.events:
            yield Meeting(
                title=self.normalize(event.name),
                description=self.normalize(event.description),
                classification=NOT_CLASSIFIED,
                start=self._parse_start(event),
                end=self._parse_end(event),
                all_day=False,
                time_notes=None,
                location=self.normalize(event.location),
                links=[],
                source=event.url,
            )

    def _parse_start(self, event):
        if event.begin:
            return event.begin.datetime
        else:
            return None

    def _parse_end(self, event):
        if event.end:
            # Some of the events have a start time which equals the end time.
            # In this case, just set end to "None", and use whatever default
            # is set by the parent spider
            if event.begin == event.end:
                return None
            else:
                return event.end.datetime
        else:
            return None
