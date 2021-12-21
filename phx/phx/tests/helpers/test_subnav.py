from django.test import TestCase
from pages.models import Page

from ...helpers.subnav import generate_subnav


class TestHelperSubnav(TestCase):
    def setUp(self):
        top = Page.objects.create(title='lorem')

        child_one = Page.objects.create(title='ipsum', parent=top)
        Page.objects.create(title='sit', parent=child_one)
        Page.objects.create(title='amet', parent=child_one)

        child_two = Page.objects.create(title='dolor', parent=top)
        Page.objects.create(title='foo', parent=child_two)
        Page.objects.create(title='bar', parent=child_two)

    def test_first_level(self):
        """
        Test that top level links are displayed, child links aren't
        """
        page = Page.objects.get(title='lorem')

        results = generate_subnav('/lorem/', page)

        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]['title'], 'lorem')
        self.assertIs(results[0]['active'], True)
        self.assertIs(results[1]['active'], False)
        self.assertEqual(len(results[1]['children']), 0)
        self.assertEqual(len(results[2]['children']), 0)

    def test_second_level(self):
        """
        Test that second level links are displayed for selected page
        """
        page = Page.objects.get(title='lorem')

        results = generate_subnav('/lorem/ipsum/', page)

        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]['title'], 'lorem')
        self.assertEqual(results[1]['title'], 'ipsum')
        self.assertIs(results[0]['active'], False)
        self.assertIs(results[1]['active'], True)
        self.assertEqual(len(results[1]['children']), 2)
        self.assertEqual(len(results[2]['children']), 0)

    def test_third_level(self):
        """
        Test that third level link is displayed and selected
        """
        page = Page.objects.get(title='lorem')

        results = generate_subnav('/lorem/ipsum/sit/', page)

        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]['title'], 'lorem')
        self.assertEqual(results[2]['title'], 'dolor')
        self.assertIs(results[0]['active'], False)
        self.assertIs(results[1]['active'], False)
        self.assertEqual(len(results[1]['children']), 2)
        self.assertEqual(len(results[2]['children']), 0)
        self.assertIs(results[1]['children'][0]['active'], True)
        self.assertIs(results[1]['children'][1]['active'], False)
