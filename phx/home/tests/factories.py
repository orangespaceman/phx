from django.utils import timezone
from factory import post_generation
from factory.django import ImageField
from factory.fuzzy import FuzzyDateTime, FuzzyInteger, FuzzyText
from factory_djoy import CleanModelFactory

from ..models import Announcement, Content, Hero, HeroImageCategory


class ContentFactory(CleanModelFactory):
    title = FuzzyText()
    join = FuzzyText()
    about = FuzzyText()

    class Meta:
        model = Content


class AnnouncementFactory(CleanModelFactory):
    announcement = FuzzyText()
    display_until = FuzzyDateTime(timezone.now())

    class Meta:
        model = Announcement


class HeroFactory(CleanModelFactory):
    image = ImageField()
    caption = FuzzyText()

    @post_generation
    def image_categories(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for category in extracted:
                self.image_categories.add(category)

    class Meta:
        model = Hero
        skip_postgeneration_save = True


class HeroImageCategoryFactory(CleanModelFactory):
    category = FuzzyText
    count = FuzzyInteger(0, 10)

    class Meta:
        model = HeroImageCategory
