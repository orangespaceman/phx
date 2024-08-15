from django_extensions.management.jobs import DailyJob


class Job(DailyJob):
    help = "Scape the Power of 10 profiles of all Phoenix" \
           "athletes to find new performances"

    def execute(self):

        # 1. Get all athletes
        # 2. Split athletes into chunks (one for each day of the week)
        # 3. Find performances for all the athletes in today's chunk

        pass
