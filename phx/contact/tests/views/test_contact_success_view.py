from django.test import TestCase
from django.urls import reverse


class TestContactSuccessView(TestCase):

    def test_url_resolves(self):
        """"
        URL resolves as expected
        """
        url = reverse('contact-success')

        self.assertEqual(url, '/contact/success/')

    def test_get(self):
        """"
        GET request uses template
        """
        url = reverse('contact-success')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact-success.html')
