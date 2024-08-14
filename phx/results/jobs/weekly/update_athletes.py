import logging

from athletes.athlete_scraper import AtheleteScraper
from django_extensions.management.jobs import WeeklyJob

logger = logging.getLogger(__name__)


class Job(WeeklyJob):
    help = "Scrape Power Of 10 to find new Phoenix athletes"

    def execute(self):

        scraper = AtheleteScraper()
        total_atheletes = scraper.find_athletes()

        logger.info(f"Found {total_atheletes} athletes")

        if (total_atheletes > 0):
            saved_athletes = scraper.save()
            logger.info(f"Inserted or updated {saved_athletes} athletes")
