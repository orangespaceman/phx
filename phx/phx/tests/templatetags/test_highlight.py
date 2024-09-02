from django.test import TestCase

from ...templatetags.highlight import highlight


class TestTemplateTagsHighlight(TestCase):

    def test_highlight_no_params(self):
        """
        No search, return original string
        """
        full_text = 'Lorem ipsum dolor sit amet'
        search_term = ''
        expected = 'Lorem ipsum dolor sit amet'

        results = highlight(full_text, search_term)

        self.assertEqual(results, expected)

    def test_highlight_replace_text(self):
        """
        Matching search, replace
        """
        full_text = 'Lorem ipsum dolor sit amet'
        search_term = 'ipsum'
        expected = ('Lorem <span class="u-highlight">ipsum</span> '
                    'dolor sit amet')

        results = highlight(full_text, search_term)

        self.assertEqual(results, expected)

    def test_highlight_dont_replace_text(self):
        """
        No matching search, don't replace
        """
        full_text = 'Lorem ipsum dolor sit amet'
        search_term = 'foo bar'
        expected = 'Lorem ipsum dolor sit amet'

        results = highlight(full_text, search_term)

        self.assertEqual(results, expected)

    def test_None_text_dont_replace_text(self):
        """
        Text is missing, don't attempt replace.
        """

        results = highlight(None, 'foo bar')

        self.assertEqual(results, None)
