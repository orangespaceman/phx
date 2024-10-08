from datetime import datetime, timedelta

from athletes.models import Athlete
from django.test import TestCase
from results.models import Event, Performance


class TestEventsModel(TestCase):

    def test_date_returns_date_of_first_performance(self):
        athlete = Athlete()
        athlete.save()

        event = Event(name="parkrun")
        event.save()

        today = datetime.now()
        yesterday = today - timedelta(days=1)
        Performance(event=event,
                    athlete=athlete,
                    time=timedelta(minutes=20),
                    distance="5K",
                    date=today,
                    overall_position=1).save()

        Performance(event=event,
                    athlete=athlete,
                    time=timedelta(minutes=20),
                    distance="5K",
                    date=yesterday,
                    overall_position=1).save()

        self.assertEqual(event.date, yesterday.date())

    def test_date_returns_none_if_no_performances(self):
        event = Event(name="parkrun")
        event.save()

        self.assertEqual(event.date, None)
