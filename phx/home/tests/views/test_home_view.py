from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from factory import SubFactory
from fixtures.models import Fixture
from fixtures.tests.factories import FixtureFactory
from gallery.tests.factories import GalleryFactory
from news.models import News
from news.tests.factories import NewsFactory
from pages.models import Page
from pages.tests.factories import (
    ComponentFactory,
    ListItemFactory,
    ListItemsFactory,
)
from results.models import Result
from results.tests.factories import ResultFactory

from ..factories import (
    AnnouncementFactory,
    ContentFactory,
    HeroFactory,
    HeroImageCategoryFactory,
)


class TestHomeView(TestCase):

    def test_url_resolves(self):
        """"
        URL resolves as expected
        """
        url = reverse('home-index')

        self.assertEqual(url, '/')

    def test_get(self):
        """"
        GET request uses template
        """
        url = reverse('home-index')
        Page.objects.create(title='home')
        ContentFactory()
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')

    def test_home_content(self):
        """
        Home model returns content to view as expected
        """
        url = reverse('home-index')
        Page.objects.create(title='home')
        content = ContentFactory()
        response = self.client.get(url)

        self.assertEqual(response.context['title'], content.title)
        self.assertEqual(response.context['join'], content.join)
        self.assertEqual(response.context['about'], content.about)

    def test_home_announcement_none(self):
        """
        Home model returns no announcement content if there aren't any
        """
        url = reverse('home-index')
        Page.objects.create(title='home')
        ContentFactory()
        response = self.client.get(url)

        self.assertEqual(response.context['announcement'], None)

    def test_home_announcement_past(self):
        """
        Home model returns no announcement content if an announcement is
        in the past
        """
        url = reverse('home-index')
        Page.objects.create(title='home')
        ContentFactory()
        AnnouncementFactory()
        response = self.client.get(url)

        self.assertEqual(response.context['announcement'], None)

    def test_home_announcement_future(self):
        """
        Home model returns an announcement if it is in the future
        """
        url = reverse('home-index')
        Page.objects.create(title='home')
        ContentFactory()

        future = timezone.now() + timezone.timedelta(days=+7)
        announcement = AnnouncementFactory(display_until=future)
        response = self.client.get(url)

        self.assertEqual(response.context['announcement'],
                         announcement.announcement)

    def test_home_announcement_future_latest(self):
        """
        Home model returns the last announcement to be created if two future
        announcements exist
        """
        url = reverse('home-index')
        Page.objects.create(title='home')
        ContentFactory()

        future = timezone.now() + timezone.timedelta(days=+7)
        AnnouncementFactory()
        AnnouncementFactory(display_until=future)
        latest_announcement = AnnouncementFactory(display_until=future)
        response = self.client.get(url)

        self.assertEqual(response.context['announcement'],
                         latest_announcement.announcement)

    def test_gallery(self):
        """
        Test gallery is returned
        """
        url = reverse('home-index')
        Page.objects.create(title='home')
        gallery = GalleryFactory()
        ContentFactory(gallery=gallery)

        response = self.client.get(url)

        self.assertEqual(response.context['gallery'], gallery)

    def test_fixtures(self):
        """
        Test latest fixtures are returned
        """
        url = reverse('home-index')
        Page.objects.create(title='home')
        ContentFactory()

        future = timezone.now() + timezone.timedelta(days=+7)
        FixtureFactory.create_batch(5, event_date=future)

        response = self.client.get(url)

        self.assertEqual(len(response.context['fixtures']), 5)
        self.assertEqual(response.context['fixtures'][0],
                         Fixture.objects.first())

    def test_heroes(self):
        """
        Test hero images are returned as expected
        """
        url = reverse('home-index')
        Page.objects.create(title='home')
        ContentFactory()

        first_category = HeroImageCategoryFactory(category='Cat 1', count=1)
        second_category = HeroImageCategoryFactory(category='Cat 2', count=2)

        first_hero = HeroFactory(caption='First Fixture',
                                 image_categories=[first_category])
        HeroFactory.create_batch(5, image_categories=[second_category])

        response = self.client.get(url)

        self.assertEqual(len(response.context['heroes']), 3)
        self.assertIn(first_hero, response.context['heroes'])

    def test_heroes_dedupe(self):
        """
        Test that hero images don't contain duplicates -
        Although hero is in both categories, it should only be retrieved once
        """
        url = reverse('home-index')
        Page.objects.create(title='home')
        ContentFactory()

        first_category = HeroImageCategoryFactory(category='Cat 1', count=1)
        second_category = HeroImageCategoryFactory(category='Cat 2', count=1)

        HeroFactory(caption='First Fixture',
                    image_categories=[first_category, second_category])

        response = self.client.get(url)

        self.assertEqual(len(response.context['heroes']), 1)

    def test_results(self):
        """
        Test latest results are returned
        """
        url = reverse('home-index')
        Page.objects.create(title='home')
        ContentFactory()

        past = timezone.now() - timezone.timedelta(days=7)
        ResultFactory(event_date=past)

        response = self.client.get(url)

        self.assertEqual(len(response.context['results']), 1)
        self.assertEqual(response.context['results'][0],
                         Result.objects.first())

    def test_draft_results(self):
        """
        Test draft results are not returned
        """

        url = reverse('home-index')
        Page.objects.create(title='home')
        ContentFactory()

        ResultFactory(draft=True)

        response = self.client.get(url)

        self.assertEqual(len(response.context['results']), 0)

    def test_news(self):
        """
        Test latest news are returned
        """
        url = reverse('home-index')
        Page.objects.create(title='home')
        ContentFactory()

        NewsFactory.create_batch(3)

        response = self.client.get(url)

        self.assertEqual(len(response.context['news']), 3)
        self.assertEqual(response.context['news'][0], News.objects.first())

    def test_components(self):
        """
        Test home page components are returned
        """
        url = reverse('home-index')
        page = Page.objects.create(title='home')
        ContentFactory()

        list_items = ListItemsFactory(
            component=SubFactory(ComponentFactory, page=page))
        ListItemFactory.create_batch(3, list_items=list_items)

        response = self.client.get(url)

        component = response.context['components'].first()
        first_list_items = component.list_items
        self.assertEqual(first_list_items, list_items)
        self.assertEqual(len(first_list_items.list_items.all()), 3)
