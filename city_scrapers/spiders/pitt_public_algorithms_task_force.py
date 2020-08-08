import re
from datetime import datetime

from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider


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
        for item in re.findall(
            "<h3>.+?</p>.+?</p>",
            response.css("article.field-body").get(),
            flags=re.DOTALL,
        ):
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
        return re.search(r"<h3>(.*)</h3>", item).group(1)

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        meeting_info = re.search(r"<p>(.*?)</p>", item, flags=re.DOTALL)
        meeting_lines = meeting_info.group(1).split("<br>")
        description = meeting_lines[1]
        if "collaboration" in description:
            description = re.sub("\n", "", description)
            return description
        return ""

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        dtline = re.search(r"<p>(.*?\s*\|\s*.*?)(?:\-.*?)?<br>", item)
        return datetime.strptime(dtline.group(1), "%B %d, %Y | %I:%M%p")

    def _parse_end(self, item):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        dtline = re.search(r"<p>(.*?)\|(.*?)\-(.*?)(?: \(.*?\))?<br>", item)
        if dtline is None:
            return None
        dtend = dtline.group(1) + dtline.group(3)
        return datetime.strptime(dtend, "%B %d, %Y %I:%M%p")

    def _parse_time_notes(self, item):
        """Parse any additional notes on the timing of the meeting"""
        dtline = re.search(r"<p>(.*)\|(.*)\-(.*) \((.*?)\)<br>", item)
        if dtline is None:
            return ""
        return dtline.group(4)

    def _parse_location(self, item):
        """Parse or generate location."""
        meeting_info = re.search(r"<p>(.*?)</p>", item, flags=re.DOTALL).group(1)
        address = ""
        name = ""
        if "PA" in meeting_info:
            meeting_info = re.sub("\n", "", meeting_info)
            meeting_lines = meeting_info.split("<br>")
            address = (
                meeting_lines[len(meeting_lines) - 2]
                + "\n"
                + meeting_lines[len(meeting_lines) - 1]
            )
            for linenum in range(1, len(meeting_lines) - 2):
                if len(meeting_lines[linenum]) < 50:
                    if len(name):
                        name = name + "\n" + meeting_lines[linenum]
                    else:
                        name = meeting_lines[linenum]
        return {
            "address": address,
            "name": name,
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        link_info = re.search(r"<a href=\"(.*?)\".*?>(.*?)</a>", item)
        href = link_info.group(1)
        title = link_info.group(2)
        return [{"href": href, "title": title}]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
