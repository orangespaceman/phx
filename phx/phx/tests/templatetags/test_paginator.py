from unittest.mock import Mock

from django.test import TestCase

from ...templatetags.paginator import paginator


class TestTemplateTagsPaginator(TestCase):

    def test_paginator_simple(self):
        """
        Return paginator params for three pages
        """
        page_obj = Mock()
        page_obj.number = 1
        page_obj.next_page_number = 2
        # page_obj.previous_page_number
        page_obj.has_next = True
        page_obj.has_previous = False
        page_obj.paginator = Mock()
        page_obj.paginator.num_pages = 3
        page_obj.paginator.per_page = 10

        context = {
            'page_obj': page_obj,
            'request': None,
        }
        adjacent_pages = 3

        results = paginator(context, adjacent_pages)

        self.assertEqual(results['page_numbers'], [1, 2, 3])
        self.assertEqual(results['show_first'], False)
        self.assertEqual(results['show_last'], False)

    def test_paginator_complex(self):
        """
        Return paginator params for n pages
        """
        page_obj = Mock()
        page_obj.number = 12
        page_obj.next_page_number = 13
        page_obj.previous_page_number = 11
        page_obj.has_next = True
        page_obj.has_previous = True
        page_obj.paginator = Mock()
        page_obj.paginator.num_pages = 50
        page_obj.paginator.per_page = 10

        context = {
            'page_obj': page_obj,
            'request': None,
        }
        adjacent_pages = 3

        results = paginator(context, adjacent_pages)

        self.assertEqual(results['page_numbers'], [9, 10, 11, 12, 13, 14, 15])
        self.assertEqual(results['show_first'], True)
        self.assertEqual(results['show_last'], True)
