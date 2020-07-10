from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
import re


class PittPublicAlgorithmsTaskForceSpider(CityScrapersSpider):
    name = "pitt_public_algorithms_task_force"
    agency = "Pittsburgh Task Force on Public Algorithms"
    timezone = "America/New_York"
    start_urls = ["https://www.cyber.pitt.edu/community-meetings"]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        meetings_one_line = re.sub('\n', "", response.css("article.field-body"))
        for item in re.findall('<h3>.+<//p>.+<//p>',meetings_one_line):
            meeting = Meeting(
                title=self._parse_title(item),
                description=self._parse_description(item),
                classification=NOT_CLASSIFIED,
                start=self._parse_start(item),
                end=self._parse_end(item),
                all_day=False,
                time_notes=self._parse_time_notes(item),
                location=self._parse_location(item),
                links=self._parse_links(item),
                source=self._parse_source(response),
            )

            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)

            yield meeting

    def _parse_title(self, item):
        """Parse or generate meeting title."""
        return item.css('h3').get()

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        return ""

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        return None

    def _parse_end(self, item):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        return None

    def _parse_time_notes(self, item):
        """Parse any additional notes on the timing of the meeting"""
        return ""

    def _parse_location(self, item):
        """Parse or generate location."""
        return {
            "address": "",
            "name": "",
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        return [{"href": "", "title": ""}]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
