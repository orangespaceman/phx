from datetime import datetime, timedelta

from athletes.tests.factories import AthleteFactory
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import make_aware
from fixtures.tests.factories import CategoryFactory
from pages.models import Page

from ...models import Result
from ..factories import EventFactory, PerformanceFactory, ResultFactory


class TestResultsView(TestCase):

    def test_url_resolves(self):
        """"
        URL resolves as expected
        """
        url = reverse('results-index')

        self.assertEqual(url, '/results/')

    def test_get(self):
        """"
        GET request uses template
        """
        url = reverse('results-index')
        Page.objects.create(title='results')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'results/result_list.html')

    def test_result_content(self):
        """"
        GET request retrieves expected result/fixture data in view context
        """
        url = reverse('results-index')
        Page.objects.create(title='results')

        first_result = ResultFactory(title='First result')

        response = self.client.get(url)
        self.assertEqual(len(response.context['results']), 1)

        result = response.context['results'].first()
        self.assertEqual(result, first_result)

    def test_result_content_date(self):
        """"
        GET request retrieves expected past result data in view context
        """
        url = reverse('results-index')
        Page.objects.create(title='results')

        # five results in the future, five in the past
        today = datetime.now().date()
        past = today - timedelta(days=7)
        future = today - timedelta(days=-7)
        ResultFactory.create_batch(5, event_date=past)
        ResultFactory.create_batch(5, event_date=future)

        past_results = Result.objects.filter(
            event_date__lte=timezone.now()).distinct()

        latest_past_result = past_results.last()

        response = self.client.get(url, {'order': 'date-added'})
        self.assertEqual(len(response.context['results']), 5)

        result = response.context['results'].first()
        self.assertEqual(result, latest_past_result)
        self.assertLessEqual(result.event_date, today)

    def test_result_search(self):
        """
        GET request retrieves results filtered by search
        """
        Page.objects.create(title='results')
        url = reverse('results-index')

        first_result = ResultFactory(title='First result')
        ResultFactory(title='Second result')

        response = self.client.get(url, {'search': 'first result'})
        self.assertEqual(len(response.context['results']), 1)

        result = response.context['results'].first()
        self.assertEqual(result, first_result)

    def test_result_search_empty(self):
        """
        GET request retrieves results filtered by search (none found)
        """
        Page.objects.create(title='results')
        url = reverse('results-index')

        ResultFactory(title='First result')
        ResultFactory(title='Second result')

        response = self.client.get(url, {'search': 'third result'})
        self.assertEqual(len(response.context['results']), 0)

    def test_result_category_search(self):
        """
        GET request retrieves results filtered by search
        """
        Page.objects.create(title='results')
        url = reverse('results-index')

        first_category = CategoryFactory(title='Cat 1')
        second_category = CategoryFactory(title='Cat 2')

        first_result = ResultFactory(
            title='First Result', categories=[first_category, second_category])

        ResultFactory(title='Second result')

        response = self.client.get(url, {'search': 'cat 2'})
        self.assertEqual(len(response.context['results']), 1)

        result = response.context['results'].first()
        self.assertEqual(result, first_result)

    def test_result_category_search_empty(self):
        """
        GET request retrieves results filtered by search
        """
        Page.objects.create(title='results')
        url = reverse('results-index')

        first_category = CategoryFactory(title='Cat 1')
        CategoryFactory(title='Cat 2')

        ResultFactory(title='First result', categories=[first_category])
        ResultFactory(title='Second result')

        response = self.client.get(url, {'search': 'cat 3'})
        self.assertEqual(len(response.context['results']), 0)

    def test_result_athlete_search(self):
        """
        GET request retrieves results filtered by search
        """
        Page.objects.create(title='results')
        url = reverse('results-index')

        result = ResultFactory(title='parkrun')
        john = AthleteFactory(first_name='John', last_name='Doe')
        jane = AthleteFactory(first_name='Jane', last_name='Doe')
        event = EventFactory(result=result)
        PerformanceFactory(athlete=john, event=event)
        PerformanceFactory(athlete=jane, event=event)

        response = self.client.get(url, {'search': 'john doe'})
        self.assertEqual(len(response.context['results']), 1)

    def test_result_event_name_search(self):
        """
        GET request retrieves results filtered by search
        """
        Page.objects.create(title='results')
        url = reverse('results-index')

        result = ResultFactory(title='parkrun')
        john = AthleteFactory(first_name='John', last_name='Doe')
        jane = AthleteFactory(first_name='Jane', last_name='Doe')
        first_event = EventFactory(name='Preston Park', result=result)
        second_event = EventFactory(name='Hove Prom', result=result)
        PerformanceFactory(athlete=john, event=first_event)
        PerformanceFactory(athlete=jane, event=second_event)

        response = self.client.get(url, {'search': 'Preston'})
        self.assertEqual(len(response.context['results']), 1)

    def test_get_year(self):
        """"
        GET request uses year, tested against gallery dates
        """
        Page.objects.create(title='results')

        date_2018 = make_aware(datetime(2018, 1, 1))
        date_2016 = make_aware(datetime(2016, 1, 1))

        first_result = ResultFactory(event_date=date_2018)

        second_result = ResultFactory(event_date=date_2016)

        url = reverse('results-index')
        response = self.client.get(url)
        self.assertEqual(len(response.context['result_list']), 2)

        response = self.client.get(url, {'year': '2018'})
        self.assertEqual(len(response.context['result_list']), 1)
        self.assertEqual(response.context['result_list'][0], first_result)

        response = self.client.get(url, {'year': '2016'})
        self.assertEqual(len(response.context['result_list']), 1)
        self.assertEqual(response.context['result_list'][0], second_result)

        # year out of range, not used in query
        response = self.client.get(url, {'year': '1999'})
        self.assertEqual(len(response.context['result_list']), 2)

    def test_get_page_size(self):
        """"
        GET request uses page_size
        """
        Page.objects.create(title='results')

        ResultFactory.create_batch(100)

        url = reverse('results-index')
        response = self.client.get(url)
        self.assertEqual(len(response.context['result_list']), 50)
        self.assertEqual(response.context['paginate_by'], 50)

        response = self.client.get(url, {'pageSize': '10'})
        self.assertEqual(len(response.context['result_list']), 10)
        self.assertEqual(response.context['paginate_by'], 10)

        response = self.client.get(url, {'pageSize': '87'})
        self.assertEqual(len(response.context['result_list']), 50)
        self.assertEqual(response.context['paginate_by'], 50)

    def test_drafts(self):
        """
        GET request ignores drafts
        """

        url = reverse('results-index')
        Page.objects.create(title='results')

        ResultFactory(title='Published')
        ResultFactory(title='Draft 1', draft=True)
        ResultFactory(title='Draft 2', draft=True)

        response = self.client.get(url)
        results = response.context['results'].all()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, 'Published')
