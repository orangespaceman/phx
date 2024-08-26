import logging

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
