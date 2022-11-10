from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import reverse
from pages.models import Page

from ..factories import FixtureFactory


class TestFixturesView(TestCase):

    def test_url_resolves(self):
        """"
        URL resolves as expected
        """
        url = reverse('fixtures-index')

        self.assertEqual(url, '/fixtures/')

    def test_get(self):
        """"
        GET request uses template
        """
        url = reverse('fixtures-index')
        Page.objects.create(title='fixtures')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fixtures/fixture_list.html')

    def test_fixture_content(self):
        """"
        GET request retrieves expected fixture data in view context
        """
        url = reverse('fixtures-index')
        Page.objects.create(title='fixtures')

        first_fixture = FixtureFactory(title='First Fixture', )
        FixtureFactory.create_batch(9)

        response = self.client.get(url)
        self.assertEqual(len(response.context['fixtures']), 10)

        fixture = response.context['fixtures'].first()
        self.assertEqual(fixture, first_fixture)

    def test_fixture_content_date(self):
        """"
        GET request retrieves expected future fixture data in view context
        """
        url = reverse('fixtures-index')
        Page.objects.create(title='fixtures')

        # five fixtures in the future to show, five in the past not shown
        today = datetime.now().date()
        past = today - timedelta(days=7)
        future = today - timedelta(days=-7)
        FixtureFactory.create_batch(5, event_date=past)
        FixtureFactory.create_batch(5, event_date=future)

        response = self.client.get(url)
        self.assertEqual(len(response.context['fixtures']), 5)

        fixture = response.context['fixtures'].first()
        self.assertGreaterEqual(fixture.event_date, today)
