# import pytest

import os

from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse

TEST_SITE_ROOT = os.path.join(settings.SITE_ROOT, 'components/tests')


# @pytest.mark.current
class TestComponentListView(TestCase):

    def test_url_resolves(self):
        """"
        URL resolves as expected
        """
        url = reverse('components-list')

        self.assertEqual(url, '/components/')

    @override_settings(SITE_ROOT=TEST_SITE_ROOT)
    def test_get(self):
        """"
        GET request uses template
        """
        url = reverse('components-list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'components/components_list.html')
        self.assertIn('components', response.context)
        components = response.context['components']
        self.assertEqual(len(components), 1)
        self.assertEqual(components[0]['dir'], 'foo')
        self.assertIn('Bar', components[0]['components'])
