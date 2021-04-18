import re
from datetime import datetime

from city_scrapers_core.constants import BOARD
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider


class PittSportsSpider(CityScrapersSpider):
    name = "pitt_sports"
    agency = "Pittsburgh Sports & Exhibition Authority"
    timezone = "America/New_York"
    start_urls = ["http://www.pgh-sea.com/index.php?path=info-meet-sea"]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        for item in response.css("tr:not([bgcolor])"):
            meeting = Meeting(
                title="SEA Board Meeting",
                description=self._parse_description(item),
                classification=BOARD,
                start=self._parse_start(item),
                end=self._parse_end(item),
                all_day=self._parse_all_day(item),
                time_notes=self._parse_time_notes(item),
                location=self._parse_location(item),
                links=self._parse_links(item),
                source=self._parse_source(response),
            )
            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)

            yield meeting

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        description = item.css("strong::text").get()
        if description:
            return description
        return ""

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        meeting_info = item.css("td::text").getall()
        schedule_date_time_pre = meeting_info[0]
        if meeting_info[1] == "Rescheduled":
            schedule_date_time_pre = meeting_info[2]
        if not ":" in schedule_date_time_pre:
            schedule_date_time_pre += " -- 10:30AM"
        schedule_date_time = re.sub(
            r"\s?([ap]m)",
            lambda match: r"{}".format(match.group(1).upper()),
            schedule_date_time_pre,
        )
        return datetime.strptime(schedule_date_time, "%a, %b %d, %Y -- %I:%M%p")

    def _parse_end(self, item):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        return None

    def _parse_time_notes(self, item):
        """Parse any additional notes on the timing of the meeting"""
        return ""

    def _parse_all_day(self, item):
        """Parse or generate all-day status. Defaults to False."""
        return False

    def _parse_location(self, item):
        """Parse or generate location."""
        meeting_info = item.css("td::text").getall()
        meeting_location = meeting_info[-1]
        if "DLCC" in meeting_location:
            return {
                "address": "1000 Fort Duquesne Blvd, Pittsburgh, PA 15222",
                "name": meeting_location,
            }
        return {
            "address": "",
            "name": meeting_location,
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        agenda_link = item.css("a::attr(href)").get()
        if agenda_link and ("http" in agenda_link):
            return [{"href": agenda_link, "title": "agenda"}]
        return [{"href": "", "title": ""}]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
