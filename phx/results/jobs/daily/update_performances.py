import logging
import math
import random
from datetime import datetime, timedelta

from athletes.models import Athlete
from django.db.models import Q
from django_extensions.management.jobs import DailyJob
from performances.performances_scraper import PerformancesScraper

logger = logging.getLogger(__name__)


class Job(DailyJob):
    help = "Scape the Power of 10 profiles of all Phoenix" \
           "athletes to find new performances"

    MAX_ATHLETES_PER_DAY = 100

    def execute(self):
        now = datetime.now()
        weekday = now.weekday()
        fraction_to_check = 1 / (7 - weekday)

        last_month = now - timedelta(days=30)
        last_week = now - timedelta(days=weekday + 1)
        last_week = last_week.replace(hour=23,
                                      minute=59,
                                      second=59,
                                      microsecond=0)

        athletes = Athlete.objects.filter(Q(last_checked__lt=last_week)
                                          | Q(last_checked__isnull=True),
                                          active=True)
        num_to_check = math.ceil(
            min(self.MAX_ATHLETES_PER_DAY,
                len(athletes) * fraction_to_check))

        athletes_to_check = random.sample(list(athletes), num_to_check)

        logger.info(f"{len(athletes)} athletes left to check this week")
        logger.info(f"Checking {len(athletes_to_check)} athletes today")

        scraper = PerformancesScraper(include_parkrun=False)

        for athlete in athletes_to_check:
            scraper.find_performances(athlete, since=last_month.date())

        performances, events, inactives = scraper.save()

        logger.info(f"{inactives} inactive athletes found")
        logger.info(f"{performances} performances updated")
        logger.info(f"{events} events updated")
        logger.info("Job complete")
