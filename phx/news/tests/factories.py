from components.models import (
    ALIGNMENT_CHOICES,
    BACKGROUND_CHOICES,
    TEXT_SIZE_CHOICES,
)
from factory import RelatedFactory, Sequence, SubFactory
from factory.django import ImageField
from factory.fuzzy import FuzzyChoice, FuzzyText
from factory_djoy import CleanModelFactory
from gallery.tests.factories import GalleryFactory as GalleryModelFactory
from results.tests.factories import ResultFactory as ResultModelFactory

from ..models import (
    Component,
    Editorial,
    Embed,
    Feature,
    Gallery,
    Image,
    ListItem,
    ListItems,
    News,
    Profile,
    ProfileMember,
    Quote,
    Result,
    Table,
    Thumbnail,
)


class ThumbnailFactory(CleanModelFactory):
    image = ImageField()

    class Meta:
        model = Thumbnail


class NewsFactory(CleanModelFactory):
    title = FuzzyText()
    summary = FuzzyText()

    RelatedFactory(ThumbnailFactory, 'news')

    class Meta:
        model = News


class ComponentFactory(CleanModelFactory):
    order = Sequence(lambda n: n)

    class Meta:
        model = Component


class EditorialFactory(CleanModelFactory):
    title = FuzzyText()
    content = FuzzyText()

    class Meta:
        model = Editorial


class EmbedFactory(CleanModelFactory):
    title = FuzzyText()
    content = FuzzyText()

    class Meta:
        model = Embed


class FeatureFactory(CleanModelFactory):
    title = FuzzyText()
    content = FuzzyText()
    align = FuzzyChoice([i[0] for i in ALIGNMENT_CHOICES])
    background = FuzzyChoice([i[0] for i in BACKGROUND_CHOICES])
    text_size = FuzzyChoice([i[0] for i in TEXT_SIZE_CHOICES])
    image = ImageField()

    class Meta:
        model = Feature


class ImageFactory(CleanModelFactory):
    caption = FuzzyText()
    image = ImageField()

    class Meta:
        model = Image


class ListItemsFactory(CleanModelFactory):

    class Meta:
        model = ListItems


class ListItemFactory(CleanModelFactory):
    title = FuzzyText()
    image = ImageField()

    class Meta:
        model = ListItem


class ProfileFactory(CleanModelFactory):
    title = FuzzyText()

    class Meta:
        model = Profile


class ProfileMemberFactory(CleanModelFactory):
    name = FuzzyText()
    role = FuzzyText()
    image = ImageField()

    class Meta:
        model = ProfileMember


class QuoteFactory(CleanModelFactory):
    quote = FuzzyText()
    author = FuzzyText()
    align = FuzzyChoice([i[0] for i in ALIGNMENT_CHOICES])
    background = FuzzyChoice([i[0] for i in BACKGROUND_CHOICES])
    text_size = FuzzyChoice([i[0] for i in TEXT_SIZE_CHOICES])
    image = ImageField()

    class Meta:
        model = Quote


class TableFactory(CleanModelFactory):
    title = FuzzyText()
    content = FuzzyText()

    class Meta:
        model = Table


class ResultFactory(CleanModelFactory):
    result = SubFactory(ResultModelFactory)

    class Meta:
        model = Result


class GalleryFactory(CleanModelFactory):
    gallery = SubFactory(GalleryModelFactory)

    class Meta:
        model = Gallery
