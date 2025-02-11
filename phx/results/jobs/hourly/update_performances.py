import logging
import math
import random
from datetime import datetime, timedelta

from athletes.models import Athlete
from django.db.models import Q
from django_extensions.management.jobs import HourlyJob
from results.performances_scraper import PerformancesScraper

logger = logging.getLogger(__name__)


class Job(HourlyJob):
    help = "Scape the Power of 10 profiles of all Phoenix athletes to " \
           "find new performances. Runs each hour between 6am and 10pm" \
           "every Monday and Friday"

    MAX_ATHLETES_PER_HOUR = 100

    def execute(self):
        now = datetime.now()

        # Only scrape on Mondays and Fridays
        if now.weekday() not in [0, 4]:
            logger.info("Not today, sorry!")
            return

        fraction_to_check = fraction_to_check = self.fraction_to_check(now)

        last_month = now - timedelta(days=30)
        six_months_ago = now - timedelta(days=180)
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)

        athletes = Athlete.objects.filter(
            self.athletes_query(six_months_ago, midnight))

        num_to_check = math.ceil(
            min(self.MAX_ATHLETES_PER_HOUR,
                len(athletes) * fraction_to_check))

        athletes_to_check = random.sample(list(athletes), num_to_check)

        logger.info(f"{len(athletes)} athletes left to check this week")
        logger.info(f"Checking {len(athletes_to_check)} athletes today")

        scraper = PerformancesScraper(include_parkrun=True)

        for athlete in athletes_to_check:
            scraper.find_performances(athlete, since=last_month.date())

        performances, events, inactives = scraper.save()

        remaining = Athlete.objects.filter(
            self.athletes_query(six_months_ago, midnight)).count()

        if remaining == 0:
            logger.info("All athletes checked for today, publishing results")
            scraper.publish_results()

        logger.info(f"{inactives} inactive athletes found")
        logger.info(f"{performances} performances updated")
        logger.info(f"{events} events updated")
        logger.info("Job complete")

    @staticmethod
    def athletes_query(six_months_ago: datetime, midnight: datetime) -> Q:
        return Q(last_checked__lt=six_months_ago, active=False) | \
               Q(last_checked__lt=midnight, active=True) | \
               Q(last_checked__isnull=True)

    @staticmethod
    def fraction_to_check(time: datetime) -> float:
        if time.hour < 6 or time.hour >= 22:
            return 0

        return 1 / (22 - time.hour)
