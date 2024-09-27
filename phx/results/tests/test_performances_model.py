from datetime import datetime, timedelta

from athletes.models import Athlete
from django.test import TestCase
from results.models import Event, Performance


class TestPerformancesModel(TestCase):

    def test_orders_by_date_distance_round_time(self):
        athlete = Athlete()
        athlete.save()

        event = Event(name="Open Meet")
        event.save()

        today = datetime.now()
        yesterday = today - timedelta(days=1)

        performances = [
            Performance(event=event,
                        athlete=athlete,
                        time=timedelta(minutes=20),
                        distance="5000",
                        round="1",
                        date=today,
                        overall_position=1),
            Performance(event=event,
                        athlete=athlete,
                        time=timedelta(minutes=18),
                        distance="5000",
                        round="2",
                        date=today,
                        overall_position=1),
            Performance(event=event,
                        athlete=athlete,
                        time=timedelta(minutes=1),
                        distance="400",
                        date=today,
                        overall_position=1),
            Performance(event=event,
                        athlete=athlete,
                        time=timedelta(minutes=2),
                        distance="400",
                        date=today,
                        overall_position=1),
            Performance(event=event,
                        athlete=athlete,
                        time=timedelta(minutes=3),
                        distance="400",
                        date=yesterday,
                        overall_position=1),
        ]

        Performance.objects.bulk_create(performances)
        saved = Performance.objects.all()
        times = [performance.time for performance in saved]

        self.assertEqual(
            [
                # A 400 meters yesterday
                timedelta(minutes=3),
                # A 400 meters today - faster than yesterday but a day later
                timedelta(minutes=1),
                # A 400 meters today - slower than the other 400 meters today
                timedelta(minutes=2),
                # A round 1 5000 meters - distance is 'greater' than 400
                timedelta(minutes=20),
                # A round 2 5000 meters - faster 5000 but 'greater' round
                timedelta(minutes=18),
            ],
            times)
