from athletes.athlete_scraper import AtheleteScraper
from django_extensions.management.jobs import WeeklyJob


class Job(WeeklyJob):
    help = "Scrape Power Of 10 to find new Phoenix athletes"

    def execute(self):

        scraper = AtheleteScraper()
        total_atheletes = scraper.find_athletes()

        if (total_atheletes > 0):
            scraper.save()
