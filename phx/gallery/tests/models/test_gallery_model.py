from django.test import TestCase
from django.urls import reverse

from ..factories import GalleryFactory


class TestGalleryModel(TestCase):

    def test_get_absolute_url(self):
        """
        Get the URL for the Gallery instance - the sluggified title
        """
        gallery = GalleryFactory(title='this? is& a! (test*)')
        expected_url = reverse('gallery-detail',
                               kwargs={
                                   'pk': gallery.id,
                                   'slug': gallery.slug
                               })

        url = gallery.get_absolute_url()

        self.assertEqual(url, expected_url)
        self.assertEqual(gallery.slug, 'this-is-a-test')
