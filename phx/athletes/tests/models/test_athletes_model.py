from datetime import date

from athletes.models import Athlete
from django.test import TestCase


class TestAthletesModel(TestCase):

    def test_age_today_when_birthday_has_passed(self, ):
        athlete = Athlete(date_of_birth=date(1987, 6, 1))

        self.assertEqual(37, athlete.age_today(today=date(2024, 12, 1)))

    def test_age_today_when_test_birthday_has_not_passed(self):
        athlete = Athlete(date_of_birth=date(1987, 6, 1))

        self.assertEqual(36, athlete.age_today(today=date(2024, 1, 1)))

    def test_age_today_when_test_birthday_is_today(self):
        athlete = Athlete(date_of_birth=date(1987, 6, 1))

        self.assertEqual(37, athlete.age_today(today=date(2024, 6, 1)))
