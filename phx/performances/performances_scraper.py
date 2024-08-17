import logging
import re
from datetime import date, datetime, timedelta

import requests
from athletes.models import Athlete
from bs4 import BeautifulSoup
from events.models import Event
from performances.models import Performance

logger = logging.getLogger(__name__)


class PerformancesScraper:

    ATHLETE_PROFILE_URL = "https://www.thepowerof10.info/athletes/" \
                          "profile.aspx?athleteid={athlete_id}&viewby=date"

    def __init__(self):
        self.events = {}
        self.performances = []
        self.inactive_athletes = set[str]()

    def find_performances(self, athlete: Athlete, since: date):
        """
        Search Power of 10 for all performances by the given athlete since the
        given date

        Returns the total number of performances found
        """

        if not athlete.power_of_10_id:
            logger.warning(f"No Power of 10 ID for {athlete}")
            return 0

        (performances, events, active) = self._scrape_profile(athlete, since)

        if not active:
            self.inactive_athletes.add(athlete.power_of_10_id)
            return 0
        else:
            self.events.update(events)
            self.performances.extend(performances)
            return len(performances)

    def _scrape_profile(self, athlete: Athlete, since: date):
        url = PerformancesScraper.ATHLETE_PROFILE_URL.format(
            athlete_id=athlete.power_of_10_id)
        logger.info("Scraping {url}".format(url=url))

        page = requests.get(url)

        athlete_created_date = athlete.created_date.date()
        since = since if athlete_created_date < since else athlete_created_date
        (performances, events, active) = self._parse_page(page, athlete, since)

        return (performances, events, active)

    def _parse_page(self, page, athlete: Athlete, since: date):
        soup = BeautifulSoup(page.content, "html.parser")

        div = soup.select('div[id$=pnlPerformances]')
        tables = div[0].find_all('table')

        rows = self._parse_results_table(tables)
        (performances, events, active) = self._parse_rows(rows, athlete, since)

        return (performances, events, active)

    def _parse_results_table(self, tables):
        if (len(tables) == 4):
            return tables[1].find_all('tr')

        logger.error(f"Expected to find 4 tables, found {len(tables)}")

        return []

    def _parse_rows(self, rows, athlete: Athlete, since: date):
        year = datetime.now().year
        performances = []
        events = {}

        if "Brighton Phoenix" not in rows[0].text:
            logger.warning(f"{athlete} is no longer a Phoenix athlete")
            return (performances, events, False)

        if str(year) not in rows[0].text and str(year - 1) not in rows[0].text:
            logger.warning(f"{athlete} has no recent performances")
            return (performances, events, False)

        for row in rows[1:]:
            (performance, event) = self._parse_row(row, athlete)

            # Irrelevant row
            if not performance or not event:
                continue

            # Performance is too old
            if performance.date < since:
                logger.info(f"Performance too old, stopping search {since}")
                return (performances, events, True)

            performances.append(performance)
            events[event.power_of_10_meeting_id] = event

        return (performances, events, True)

    def _parse_meeting_id(self, cell):
        match = re.search(r'results\.aspx\?meetingid=(\d+)', str(cell))
        return match.group(1) if match else None

    def _parse_time(self, cell):
        parts = cell.text.strip().split(':')

        if (len(parts) == 3):
            return timedelta(hours=int(parts[0]),
                             minutes=int(parts[1]),
                             seconds=float(parts[2]))
        elif (len(parts) == 2):
            return timedelta(minutes=int(parts[0]), seconds=float(parts[1]))
        else:
            return timedelta(seconds=float(parts[0]))

    def _parse_row(self, row, athlete: Athlete):
        # Skip intermediate header rows
        if "Grey" in row.get('style'):
            return (None, None)

        cells = row.find_all('td')

        if len(cells) == 12:
            po10_id = self._parse_meeting_id(cells[9])
            perf_date = datetime.strptime(cells[11].text.strip(), "%d %b %y")

            event = Event(name=cells[10].text.strip(),
                          location=cells[9].text.strip(),
                          power_of_10_meeting_id=po10_id)

            performance = Performance(
                athlete=athlete,
                # Placeholder Event, will be replaced before save
                event=Event(power_of_10_meeting_id=po10_id),
                distance=cells[0].text.strip(),
                time=self._parse_time(cells[1]),
                category=f"{athlete.gender}{athlete.age_category}",
                round=cells[6].text.strip(),
                date=perf_date.date(),
                overall_position=int(cells[5].text.strip()))

            return (performance, event)

        return (None, None)

    def save(self):
        events = Event.objects.bulk_create(
            self.events.values(),
            update_conflicts=True,
            unique_fields=["power_of_10_meeting_id"],
            update_fields=["name", "location"])

        events = {event.power_of_10_meeting_id: event for event in events}

        for p in self.performances:
            p.event = events[p.event.power_of_10_meeting_id]

        performances = Performance.objects.bulk_create(
            self.performances,
            update_conflicts=True,
            unique_fields=["athlete", "event", "distance", "round"],
            update_fields=[
                "distance", "time", "round", "overall_position", "date"
            ])

        inactive_athletes = Athlete.objects.filter(
            power_of_10_id__in=self.inactive_athletes).update(active=False)

        return len(performances), len(events), inactive_athletes
