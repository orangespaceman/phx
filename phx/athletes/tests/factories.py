from datetime import datetime, timezone

from factory.fuzzy import FuzzyDateTime, FuzzyText
from factory_djoy import CleanModelFactory

from ..models import Athlete


class AthleteFactory(CleanModelFactory):
    first_name = FuzzyText()
    last_name = FuzzyText()
    age_category = FuzzyText(length=3)
    gender = FuzzyText(length=1)
    power_of_10_id = FuzzyText()
    last_checked = FuzzyDateTime(datetime.now(timezone.utc))

    class Meta:
        model = Athlete
        skip_postgeneration_save = True
