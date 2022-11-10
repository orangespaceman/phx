import os

from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse

TEST_SITE_ROOT = os.path.join(settings.SITE_ROOT, 'components/tests')
TEST_TEMPLATE_DIR = os.path.join(TEST_SITE_ROOT, 'templates')
TEST_TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEST_TEMPLATE_DIR],
    },
]


@override_settings(SITE_ROOT=TEST_SITE_ROOT, TEMPLATES=TEST_TEMPLATES)
class TestComponentDetailView(TestCase):

    def test_url_resolves(self):
        """"
        URL resolves as expected
        """
        url = reverse('components-detail',
                      kwargs={
                          'group': 'foo',
                          'component': 'Bar'
                      })

        self.assertEqual(url, '/components/foo/Bar/')

    def test_get(self):
        """"
        GET request uses template
        """
        url = reverse('components-detail',
                      kwargs={
                          'group': 'foo',
                          'component': 'Bar'
                      })

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'components/foo/Bar/demo/demo.html')

        self.assertEqual(response.context['data'], {'foo': 'bar'})
