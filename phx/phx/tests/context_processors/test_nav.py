from unittest.mock import Mock

from django.test import TestCase

from ...context_processors.nav import nav


class TestContextProcessorNav(TestCase):

    def test_nav(self):
        """
        Test nav returns expected number of results
        """
        request = Mock()
        request.get_full_path = lambda: '/lorem/ipsum/'

        results = nav(request)
        self.assertEqual(len(results['nav']), 10)
        self.assertEqual(results['nav'][0]['active'], False)

    def test_nav_active(self):
        """
        Test nav returns correct active state when on a sub-page
        """
        request = Mock()
        request.get_full_path = lambda: '/about/sub-page/'

        results = nav(request)
        self.assertEqual(results['nav'][0]['active'], True)

    def test_nav_contact(self):
        """
        Test nav correctly identifies contact page
        """
        request = Mock()
        request.get_full_path = lambda: '/lorem/ipsum/'

        results = nav(request)
        self.assertEqual(results['nav'][0]['contact'], False)
        self.assertEqual(results['nav'][9]['contact'], True)
