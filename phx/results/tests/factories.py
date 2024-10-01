from datetime import datetime, timezone

from factory import post_generation
from factory.fuzzy import FuzzyDate, FuzzyDateTime, FuzzyInteger, FuzzyText
from factory_djoy import CleanModelFactory

from ..models import Event, Performance, Result


class ResultFactory(CleanModelFactory):
    title = FuzzyText()
    event_date = FuzzyDate(datetime.now().date())
    summary = FuzzyText()
    results = FuzzyText()
    results_url = 'http://example.com'
    draft = False

    @post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for category in extracted:
                self.categories.add(category)

    class Meta:
        model = Result
        skip_postgeneration_save = True


class EventFactory(CleanModelFactory):
    name = FuzzyText()
    location = FuzzyText()
    power_of_10_meeting_id = FuzzyText()

    class Meta:
        model = Event
        skip_postgeneration_save = True


class FuzzyTime(FuzzyDateTime):

    def fuzz(self):
        return super().fuzz().time()


class PerformanceFactory(CleanModelFactory):
    date = FuzzyDate(datetime.now().date())
    distance = FuzzyText()
    category = FuzzyText(length=4)
    overall_position = FuzzyText(length=2)
    time = FuzzyDateTime(datetime.now(
        timezone.utc)).fuzz().strftime('%H:%M:%S')
    round = FuzzyText(length=1)
    gender_position = FuzzyInteger(1)
    age_position = FuzzyInteger(1)

    class Meta:
        model = Performance
        skip_postgeneration_save = True
