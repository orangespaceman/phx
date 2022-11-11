from django.test import TestCase

from ...templatetags.templatehelpers import url_self_with_params


class TestTemplateTagsTemplateHelpers(TestCase):

    def test_url_no_params(self):
        """
        Return page param
        """
        field_name = 'page'
        value = 3
        current_querystring = ''

        results = url_self_with_params(field_name, value, current_querystring)

        self.assertEqual(results, '?page=3')

    def test_url_replace_params(self):
        """
        Update page param
        """
        field_name = 'page'
        value = 3
        current_querystring = 'page=2'

        results = url_self_with_params(field_name, value, current_querystring)

        self.assertEqual(results, '?page=3')

    def test_url_new_params(self):
        """
        Return params replacing page
        """
        field_name = 'page'
        value = 3
        current_querystring = 'search=foo&page=2'

        results = url_self_with_params(field_name, value, current_querystring)

        self.assertEqual(results, '?page=3&search=foo')
