from datetime import datetime

from factory import post_generation
from factory.fuzzy import FuzzyDate, FuzzyText
from factory_djoy import CleanModelFactory

from ..models import Result


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
