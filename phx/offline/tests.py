from django.test import TestCase
from django.urls import reverse


class TestOfflineView(TestCase):

    def test_url_resolves(self):
        """"
        URL resolves as expected
        """
        url = reverse('offline-index')

        self.assertEqual(url, '/offline/')

    def test_get(self):
        """"
        GET request uses template
        """
        url = reverse('offline-index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offline/offline.html')
