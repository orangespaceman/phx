import logging
from datetime import date

from django.contrib.auth.models import User
from django.db import models

logger = logging.getLogger(__name__)


class Athlete(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    date_of_birth = models.DateField()

    active = models.BooleanField(default=True)
    power_of_10_id = models.CharField(max_length=20, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(
        User,
        models.SET_NULL,
        blank=True,
        null=True,
    )

    def age_today(self, today=date.today()) -> int:
        age = today.year - self.date_of_birth.year - (
            0 if self.birthday_has_passed(today, self.date_of_birth) else 1)

        return age

    @staticmethod
    def birthday_has_passed(today: date, dob: date) -> bool:
        return (dob.month, dob.day) <= (today.month, today.day)
