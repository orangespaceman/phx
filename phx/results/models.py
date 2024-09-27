from athletes.models import Athlete
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from fixtures.models import Category


class Result(models.Model):
    title = models.CharField(max_length=200)
    event_date = models.DateField()
    categories = models.ManyToManyField(Category, blank=True)
    event_url = models.URLField(max_length=200, blank=True, null=True)
    results_url = models.URLField(max_length=200, blank=True)
    summary = RichTextField(
        config_name='text',
        blank=True,
        help_text='This is displayed above the results',
    )

    results = RichTextField(
        config_name='table',
        blank=True,
        null=True,
        help_text='Enter results manually if no Events have been linked')

    draft = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User,
        models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return '{0} ({1})'.format(self.title, self.event_date)


class Event(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    power_of_10_meeting_id = models.CharField(max_length=20,
                                              unique=True,
                                              null=True)

    result = models.ForeignKey(Result, models.SET_NULL, blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(
        User,
        models.SET_NULL,
        blank=True,
        null=True,
    )

    @property
    def date(self):
        performances = self.__getattribute__('performance_set')

        if performances.count() == 0:
            return None
        else:
            return performances.order_by('date').first().date

    def __str__(self) -> str:
        return f"{self.name} | {self.location}"


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
    overall_position = models.CharField(max_length=20)
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
        ordering = ['date', 'distance', 'round', 'time']
