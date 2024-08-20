from datetime import datetime, timedelta

from athletes.models import Athlete
from django.test import TestCase
from events.models import Event
from performances.models import Performance
from results.models import Result


class TestEventsModel(TestCase):

    def test_new_returns_true_if_not_associated_with_a_result(self):
        event = Event(name="parkrun")
        event.save()

        self.assertEqual(event.new, True)

    def test_new_returns_false_if_associated_with_a_result(self):
        event = Event(name="parkrun")
        event.save()

        Result(event=event, event_date=datetime.now()).save()

        self.assertEqual(event.new, False)

    def test_new_returns_false_if_not_recently_created(self):
        event = Event(name="parkrun")
        event.save()
        event.created_date = event.created_date - timedelta(days=15)

        self.assertEqual(event.new, False)

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
