from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import make_aware

from ..factories import NewsFactory


class TestNewsListView(TestCase):

    def test_url_resolves(self):
        """"
        URL resolves as expected
        """
        url = reverse('news-list')

        self.assertEqual(url, '/news/')

    def test_get(self):
        """"
        GET request uses template
        """
        url = reverse('news-list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/news_list.html')

    def test_get_search(self):
        """"
        GET request uses search string, tested against news title/summary
        """
        NewsFactory(title='The big w race')
        NewsFactory(summary='The blackcap race')
        NewsFactory.create_batch(8)

        url = reverse('news-list')
        response = self.client.get(url)
        self.assertEqual(len(response.context['news']), 10)

        response = self.client.get(url, {'search': 'big w race'})
        self.assertEqual(len(response.context['news']), 1)

        response = self.client.get(url, {'search': 'blackcap'})
        self.assertEqual(len(response.context['news']), 1)

    def test_get_search_empty(self):
        """"
        GET request uses search string, no results
        """
        NewsFactory.create_batch(10)

        url = reverse('news-list')
        response = self.client.get(url)
        self.assertEqual(len(response.context['news']), 10)

        response = self.client.get(url, {'search': 'Bleurgh'})
        self.assertEqual(len(response.context['news']), 0)

    def test_get_year(self):
        """"
        GET request uses year, tested against news dates
        """
        date_2018 = make_aware(datetime(2018, 1, 1))
        date_2016 = make_aware(datetime(2016, 1, 1))

        news_2018 = NewsFactory()
        news_2018.created_date = date_2018
        news_2018.save()

        news_2016 = NewsFactory()
        news_2016.created_date = date_2016
        news_2016.save()

        NewsFactory.create_batch(8)

        url = reverse('news-list')
        response = self.client.get(url)
        self.assertEqual(len(response.context['news_list']), 10)

        response = self.client.get(url, {'year': '2018'})
        self.assertEqual(len(response.context['news_list']), 1)
        self.assertEqual(response.context['news_list'][0], news_2018)

        response = self.client.get(url, {'year': '2016'})
        self.assertEqual(len(response.context['news_list']), 1)
        self.assertEqual(response.context['news_list'][0], news_2016)

    def test_get_year_out_of_range(self):
        """"
        GET request uses year out of range, not used in query
        """
        NewsFactory.create_batch(10)

        url = reverse('news-list')
        response = self.client.get(url)
        self.assertEqual(len(response.context['news_list']), 10)

        response = self.client.get(url, {'year': '2018'})
        self.assertEqual(len(response.context['news_list']), 0)
        self.assertEqual(response.context['year'], 2018)

        response = self.client.get(url, {'year': '1999'})
        self.assertEqual(len(response.context['news_list']), 10)

    def test_get_page_size(self):
        """"
        GET request uses page_size
        """
        NewsFactory.create_batch(100)

        url = reverse('news-list')
        response = self.client.get(url)
        self.assertEqual(len(response.context['news_list']), 10)
        self.assertEqual(response.context['paginate_by'], 10)

        response = self.client.get(url, {'pageSize': '50'})
        self.assertEqual(len(response.context['news_list']), 50)
        self.assertEqual(response.context['paginate_by'], 50)

        response = self.client.get(url, {'pageSize': '87'})
        self.assertEqual(len(response.context['news_list']), 10)
        self.assertEqual(response.context['paginate_by'], 10)
