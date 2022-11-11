from django.test import TestCase
from django.urls import reverse

from ..factories import NewsFactory


class TestNewsModel(TestCase):

    def test_get_absolute_url(self):
        """
        Get the URL for the News instance - the sluggified title
        """
        news = NewsFactory(title='this? is& a! (test*)')
        expected_url = reverse('news-detail',
                               kwargs={
                                   'pk': news.id,
                                   'slug': news.slug
                               })

        url = news.get_absolute_url()

        self.assertEqual(url, expected_url)
        self.assertEqual(news.slug, 'this-is-a-test')
