import logging

from athletes.models import Athlete
from django.contrib.auth.models import User
from django.db import models
from events.models import Event

logger = logging.getLogger(__name__)


class Performance(models.Model):

    athlete = models.ForeignKey(
        Athlete,
        models.CASCADE,
    )

    event = models.ForeignKey(
        Event,
        models.CASCADE,
    )

    date = models.DateField()
    distance = models.CharField(max_length=100)
    time = models.DurationField()
    category = models.CharField(max_length=20)
    round = models.CharField(max_length=20, null=True)
    overall_position = models.PositiveIntegerField()
    age_position = models.PositiveIntegerField(null=True)
    gender_position = models.PositiveIntegerField(null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(
        User,
        models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['athlete', 'event', 'distance', 'round'],
                name='unique_performance')
        ]
