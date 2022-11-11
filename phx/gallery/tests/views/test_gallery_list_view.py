from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import make_aware

from ..factories import GalleryFactory


class TestGalleryListView(TestCase):

    def test_url_resolves(self):
        """"
        URL resolves as expected
        """
        url = reverse('gallery-list')

        self.assertEqual(url, '/gallery/')

    def test_get(self):
        """"
        GET request uses template
        """
        url = reverse('gallery-list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gallery/gallery_list.html')

    def test_get_search(self):
        """"
        GET request uses search string, tested against gallery title/summary
        """
        GalleryFactory(title='The big w race')
        GalleryFactory(summary='The blackcap race')
        GalleryFactory.create_batch(8)

        url = reverse('gallery-list')
        response = self.client.get(url)
        self.assertEqual(len(response.context['gallery_list']), 10)

        response = self.client.get(url, {'search': 'big w race'})
        self.assertEqual(len(response.context['gallery_list']), 1)

        response = self.client.get(url, {'search': 'blackcap'})
        self.assertEqual(len(response.context['gallery_list']), 1)

    def test_get_search_empty(self):
        """"
        GET request uses search string, no results
        """
        GalleryFactory.create_batch(10)

        url = reverse('gallery-list')
        response = self.client.get(url)
        self.assertEqual(len(response.context['gallery_list']), 10)

        response = self.client.get(url, {'search': 'Bleurgh'})
        self.assertEqual(len(response.context['gallery_list']), 0)

    def test_get_year(self):
        """"
        GET request uses year, tested against gallery dates
        """
        date_2018 = make_aware(datetime(2018, 1, 1))
        date_2016 = make_aware(datetime(2016, 1, 1))

        gallery_2018 = GalleryFactory()
        gallery_2018.created_date = date_2018
        gallery_2018.save()

        gallery_2016 = GalleryFactory()
        gallery_2016.created_date = date_2016
        gallery_2016.save()

        GalleryFactory.create_batch(8)

        url = reverse('gallery-list')
        response = self.client.get(url)
        self.assertEqual(len(response.context['gallery_list']), 10)

        response = self.client.get(url, {'year': '2018'})
        self.assertEqual(len(response.context['gallery_list']), 1)
        self.assertEqual(response.context['gallery_list'][0], gallery_2018)

        response = self.client.get(url, {'year': '2016'})
        self.assertEqual(len(response.context['gallery_list']), 1)
        self.assertEqual(response.context['gallery_list'][0], gallery_2016)

    def test_get_year_out_of_range(self):
        """"
        GET request uses year out of range, not used in query
        """
        GalleryFactory.create_batch(10)

        url = reverse('gallery-list')
        response = self.client.get(url)
        self.assertEqual(len(response.context['gallery_list']), 10)

        response = self.client.get(url, {'year': '2018'})
        self.assertEqual(len(response.context['gallery_list']), 0)
        self.assertEqual(response.context['year'], 2018)

        response = self.client.get(url, {'year': '1999'})
        self.assertEqual(len(response.context['gallery_list']), 10)

    def test_get_page_size(self):
        """"
        GET request uses page_size
        """
        GalleryFactory.create_batch(100)

        url = reverse('gallery-list')
        response = self.client.get(url)
        self.assertEqual(len(response.context['gallery_list']), 10)
        self.assertEqual(response.context['paginate_by'], 10)

        response = self.client.get(url, {'pageSize': '50'})
        self.assertEqual(len(response.context['gallery_list']), 50)
        self.assertEqual(response.context['paginate_by'], 50)

        response = self.client.get(url, {'pageSize': '87'})
        self.assertEqual(len(response.context['gallery_list']), 10)
        self.assertEqual(response.context['paginate_by'], 10)
