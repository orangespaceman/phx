import logging
import re
from string import ascii_lowercase

import requests
from athletes.models import Athlete
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class AtheleteScraper:

    ATHLETE_LOOKUP_URL = "https://www.thepowerof10.info/athletes/" \
                         "athleteslookup.aspx?surname={surname}" \
                         "&firstname=&club=Brighton+Phoenix"

    def __init__(self):
        self.athletes = []

    def find_athletes(self):
        """
        Seatch Power of 10 for all Brighton Phoenix athletes.

        Returns the total number of athletes found
        """

        self.athletes = []

        for c in ascii_lowercase:
            athletes = self.find_by_surname(c)
            self.athletes.extend(athletes)

        return len(self.athletes)

    def find_by_surname(self, surname):
        url = AtheleteScraper.ATHLETE_LOOKUP_URL.format(surname=surname)
        logger.info("Scraping {url}".format(url=url))

        page = requests.get(url)

        return self._parse_page(page)

    def _parse_page(self, page):
        soup = BeautifulSoup(page.content, "html.parser")

        table = soup.select('div[id$=Results]')
        rows = self._parse_results_table(table)
        athletes = self._parse_rows(rows)

        return athletes

    def _parse_results_table(self, table):
        if len(table) == 1:
            return table[0].find_all('tr')

        print(f"Expected a single results table, found {len(table)}")

        return []

    def _parse_rows(self, rows):
        athletes = []

        # Parse each row, ignoring the header
        for row in rows[1:]:
            athlete = self._parse_row(row)
            if athlete:
                athletes.append(athlete)

        return athletes

    def _parse_row(self, row):
        cells = row.find_all('td')

        if (len(cells) == 9):
            return Athlete(first_name=cells[0].text.strip(),
                           last_name=cells[1].text.strip(),
                           age_category=cells[3].text.strip(),
                           gender=cells[5].text.strip(),
                           power_of_10_id=self._parse_power_of_10_id(cells[7]))

        return None

    def _parse_power_of_10_id(self, cell):
        match = re.search(r'profile\.aspx\?athleteid=(\d+)', str(cell))
        return match.group(1) if match else None

    def save(self):
        created = Athlete.objects.bulk_create(self.athletes,
                                              update_conflicts=True,
                                              update_fields=[
                                                  "first_name", "last_name",
                                                  "age_category", "gender"
                                              ],
                                              unique_fields=["power_of_10_id"])
        return len(created)
