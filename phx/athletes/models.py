import logging

from django.contrib.auth.models import User
from django.db import models

logger = logging.getLogger(__name__)


class Athlete(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age_category = models.CharField(max_length=3)
    gender = models.CharField(max_length=1)

    active = models.BooleanField(default=True)
    power_of_10_id = models.CharField(max_length=20, unique=True, null=True)
    last_checked = models.DateTimeField(null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(
        User,
        models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.age_category})"
