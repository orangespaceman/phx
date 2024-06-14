from datetime import datetime

from factory import post_generation
from factory.fuzzy import FuzzyDate, FuzzyText
from factory_djoy import CleanModelFactory

from ..models import Category, Fixture


class CategoryFactory(CleanModelFactory):
    title = FuzzyText()
    abbreviation = FuzzyText()

    class Meta:
        model = Category


class FixtureFactory(CleanModelFactory):
    title = FuzzyText()
    event_date = FuzzyDate(datetime.now().date())
    location = FuzzyText()
    link_url = 'http://example.com'

    @post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for category in extracted:
                self.categories.add(category)

    class Meta:
        model = Fixture
        skip_postgeneration_save = True
