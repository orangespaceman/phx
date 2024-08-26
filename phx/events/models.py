import logging
from datetime import datetime, timedelta, timezone

from django.contrib.auth.models import User
from django.db import models

logger = logging.getLogger(__name__)


class Event(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    power_of_10_meeting_id = models.CharField(max_length=20,
                                              unique=True,
                                              null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(
        User,
        models.SET_NULL,
        blank=True,
        null=True,
    )

    @property
    def new(self):
        """
        Created in the last 14 days and not associated with a Result
        """
        since = datetime.now(tz=timezone.utc) - timedelta(days=14)
        recent = self.created_date > since
        return recent and self.__getattribute__('result_set').count() == 0

    @property
    def date(self):
        performances = self.__getattribute__('performance_set')

        if performances.count() == 0:
            return None
        else:
            return performances.order_by('date').first().date

    def __str__(self) -> str:
        return f"{self.name} | {self.location}"
